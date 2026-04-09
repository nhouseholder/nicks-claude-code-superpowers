#!/usr/bin/env python3
"""
Plan Mode Enforcer — Two responsibilities:

1. On plan intent: injects "Sonnet-proof plan" format requirements, cleans old
   plan files, activates the execution guard.

2. On "go" after plan: writes claude-sonnet-4-6 to settings.json BEFORE the
   model processes the turn. If Claude Code hot-reloads settings between the
   hook and model invocation, the switch is automatic. Injects instructions
   to execute the plan from the file.

Fires on UserPromptSubmit. Exit code 0 always.
"""
import json
import glob
import os
import re
import sys
import time

PLAN_DIR = os.path.expanduser("~/.claude/plans")
GUARD_ACTIVE = os.path.expanduser("~/.claude/.plan-guard-active")
SETTINGS_PATH = os.path.expanduser("~/.claude/settings.json")

# Clean stale plan files (> 2 hours old)
try:
    for old in glob.glob(os.path.join(PLAN_DIR, "*.md")):
        if time.time() - os.path.getmtime(old) > 7200:
            os.remove(old)
except Exception:
    pass

try:
    input_data = json.load(sys.stdin)
except (json.JSONDecodeError, Exception):
    sys.exit(0)

# === ExitPlanMode PreToolUse — switch model BEFORE user triggers implementation ===
# When Claude calls ExitPlanMode (end of planning turn), switch settings.json to
# Sonnet immediately so the NEXT turn (however triggered — button or text) uses Sonnet.
tool_name = input_data.get("tool_name", "")
if tool_name == "ExitPlanMode":
    try:
        with open(SETTINGS_PATH, "r") as f:
            settings = json.load(f)
        if "opus" in settings.get("model", "").lower():
            settings["model"] = "claude-sonnet-4-6"
            with open(SETTINGS_PATH, "w") as f:
                json.dump(settings, f, indent=2)
                f.write("\n")
    except Exception:
        pass
    # Clean old plans — prevent Sonnet from executing stale plans.
    # This is critical when user enters plan mode via Desktop UI toggle
    # (detect_plan_intent() never fires, so its cleanup doesn't run).
    try:
        for old_plan in glob.glob(os.path.join(PLAN_DIR, "*.md")):
            os.remove(old_plan)
    except Exception:
        pass

    # ENSURE guard exists — CREATE it if plan mode was toggled via UI (not text).
    if not os.path.exists(GUARD_ACTIVE):
        try:
            with open(GUARD_ACTIVE, "w") as f:
                f.write(os.getcwd())
        except Exception:
            pass
    sys.exit(0)

prompt = input_data.get("prompt", "").strip()
prompt_lower = prompt.lower()

# Skip empty or slash-command prompts
if not prompt or prompt.startswith("/"):
    sys.exit(0)

# === "GO" DETECTION — Execute plan with Sonnet ===
# Two tiers: exact match for short signals, substring for longer button text.
# Desktop app button: "Approve plan and start coding"
# CLI plan mode button: "Implement Plan" or similar
EXACT_GO = [
    "go", "go!", "lets go", "let's go", "start", "begin", "execute",
    "run it", "do it", "proceed", "continue", "go ahead",
    "implement", "implement it",
]
SUBSTRING_GO = [
    "approve plan", "approve the plan", "start coding",
    "execute the plan", "execute plan", "run the plan",
    "implement plan", "implement the plan",
    "do the plan", "apply the plan", "start execution",
]

cleaned = prompt_lower.strip().rstrip("!.")
is_go = cleaned in EXACT_GO or any(sg in prompt_lower for sg in SUBSTRING_GO)

if is_go:
    # Check if there's a recent plan file (written within last 30 min)
    recent_plan = None
    try:
        plan_files = sorted(
            glob.glob(os.path.join(PLAN_DIR, "*.md")),
            key=os.path.getmtime,
            reverse=True,
        )
        if plan_files:
            age = time.time() - os.path.getmtime(plan_files[0])
            if age < 1800:  # 30 minutes
                recent_plan = plan_files[0]
    except Exception:
        pass

    if recent_plan:
        # Switch model to Sonnet in settings.json BEFORE model processes
        try:
            with open(SETTINGS_PATH, "r") as f:
                settings = json.load(f)
            if "opus" in settings.get("model", "").lower():
                settings["model"] = "claude-sonnet-4-6"
                with open(SETTINGS_PATH, "w") as f:
                    json.dump(settings, f, indent=2)
                    f.write("\n")
        except Exception:
            pass

        # Remove guard if it exists
        try:
            os.remove(GUARD_ACTIVE)
        except Exception:
            pass

        output = {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": (
                    f"PLAN EXECUTION MODE — settings.json switched to claude-sonnet-4-6.\n\n"
                    f"Plan file: {recent_plan}\n\n"
                    "INSTRUCTIONS:\n"
                    f"1. Read the plan at {recent_plan}\n"
                    "2. Execute it step by step — every step exactly as written\n"
                    "3. Do NOT rewrite, overwrite, or re-plan. Just execute.\n"
                    "4. Mark tasks as you complete them\n"
                    "5. If you are still running as Opus (check your model ID), tell the user:\n"
                    "   'Switch to Sonnet first — Desktop app: model dropdown → Sonnet. CLI: /model sonnet. Then type go.'"
                )
            }
        }
        print(json.dumps(output))
        sys.exit(0)

# === GUARD ACTIVE — non-GO prompt ===
# Guard is active but prompt wasn't a GO signal (e.g. "Implement Plan" button sends
# different text, or user typed something unrecognized). Inject context so Claude
# immediately tells the user to switch to Sonnet — before executing anything.
if os.path.exists(GUARD_ACTIVE):
    try:
        age = time.time() - os.path.getmtime(GUARD_ACTIVE)
        if age < 1800:  # guard is recent (< 30 min)
            # Check if user already switched to Sonnet (e.g. via Desktop dropdown)
            already_sonnet = False
            try:
                with open(SETTINGS_PATH, "r") as f:
                    settings = json.load(f)
                model = settings.get("model", "").lower()
                if model and "opus" not in model:
                    already_sonnet = True
            except Exception:
                pass

            if already_sonnet:
                # Already on Sonnet — remove guard silently, let through
                try:
                    os.remove(GUARD_ACTIVE)
                except Exception:
                    pass
                sys.exit(0)

            output = {
                "hookSpecificOutput": {
                    "hookEventName": "UserPromptSubmit",
                    "additionalContext": (
                        "PLAN GUARD ACTIVE — MANDATORY, output this FIRST before anything else:\n\n"
                        "Tell the user VERBATIM:\n"
                        "\"⚠️ You're in Opus mode. Switch to Sonnet before executing (~50% cheaper):\n"
                        "   - Desktop app: Click the model selector dropdown → pick Sonnet\n"
                        "   - CLI: Run /model sonnet\n"
                        "   Then type: go\n"
                        "Waiting for you to switch...\"\n\n"
                        "Do NOT read files, run commands, or execute any plan steps. "
                        "Output ONLY the message above and stop."
                    )
                }
            }
            print(json.dumps(output))
            sys.exit(0)
    except Exception:
        pass

# === PLAN DETECTION SIGNALS ===
PLAN_SIGNALS = [
    r"\bwrite\s+(a\s+|the\s+|me\s+a\s+)?plan\b",
    r"\bmake\s+(a\s+|the\s+|me\s+a\s+)?plan\b",
    r"\bplan\s+(for|this|out|the|how|to)\b",
    r"\bplan\s+mode\b",
    r"\bplanning\s+mode\b",
    r"\bsonnet.proof\b",
    r"\bbreak\s+(this\s+|it\s+)?down\b",
    r"\bdesign\s+(the\s+)?(approach|architecture|system|implementation)\b",
    r"\barchitect\s+(this|the|a|an)\b",
    r"\broadmap\b",
    r"\bimplementation\s+(plan|strategy)\b",
    r"\bstep.by.step\b",
    r"\bopus.plan\b",
    r"\bsonnet.execute\b",
    r"\bdetailed\s+plan\b",
    r"\bplan\s+first\b",
]


def detect_plan_intent(text):
    """Return True if the prompt indicates the user wants a plan."""
    text_lower = text.lower()
    for pattern in PLAN_SIGNALS:
        if re.search(pattern, text_lower):
            return True
    return False


if detect_plan_intent(prompt):
    # Clean up old plan files so Sonnet doesn't confuse them with the current plan
    try:
        for old_plan in glob.glob(os.path.join(PLAN_DIR, "*.md")):
            os.remove(old_plan)
    except Exception:
        pass

    # Activate the guard — blocks Edit/Write until "go" triggers model switch
    try:
        with open(GUARD_ACTIVE, "w") as f:
            f.write(os.getcwd())
    except Exception:
        pass

    output = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": (
                "MANDATORY PLAN FORMAT — This overrides default plan mode behavior.\n\n"
                "STEP 0 — SAVE THE PLAN TO DISK (CRITICAL, DO THIS FIRST):\n"
                "Before writing inline, use the Write tool to save the COMPLETE plan to:\n"
                f"  {PLAN_DIR}/plan-<YYYY-MM-DD-HHMM>.md\n"
                "Use today's date and current time. The file MUST exist on disk — "
                "Sonnet reads it from there during execution. If you skip this, "
                "the entire pipeline breaks.\n\n"
                "You MUST write a 'Sonnet-proof' plan: ultra-specific, zero ambiguity, "
                "mechanically executable. Sonnet will execute this plan with NO judgment calls.\n\n"
                "EVERY step MUST include ALL of these:\n"
                "1. EXACT file path (absolute, not relative)\n"
                "2. EXACT code — the literal old_string → new_string for Edit, or full content for Write. "
                "Copy-paste ready. Never pseudocode. Never 'similar to above.' Never '...' ellipsis.\n"
                "3. EXACT shell commands with expected output where relevant\n"
                "4. A verification command after each logical group\n\n"
                "BANNED in plans:\n"
                "- 'Update the component to...' (vague — SHOW the exact code)\n"
                "- 'Add appropriate error handling' (ambiguous — WRITE the handler)\n"
                "- 'Similar changes in other files' (lazy — LIST every file)\n"
                "- 'Modify as needed' / 'adjust accordingly' (decision point — DECIDE now)\n"
                "- Pseudocode, placeholder comments, or partial snippets\n\n"
                "If a step requires choosing between approaches, make the choice NOW "
                "and document WHY in the plan. Zero decision points for the executor.\n\n"
                "AFTER writing the plan file and calling ExitPlanMode:\n"
                "Do NOT start executing the plan yourself. Tell the user to type 'go' "
                "to begin execution with Sonnet. You are the PLANNER, not the executor."
            )
        }
    }
    print(json.dumps(output))

sys.exit(0)
