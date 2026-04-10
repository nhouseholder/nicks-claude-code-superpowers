#!/usr/bin/env python3
"""
Plan Mode Enforcer — Two responsibilities:

1. On plan intent: injects "Sonnet-proof plan" format requirements, cleans old
   plan files, activates the execution guard.

2. On "go" after plan: removes the guard and injects execution instructions.
   Does NOT attempt to detect or change the running model — hooks cannot do
   that (see anti-patterns.md → PLAN_AUTO_SWITCH_IMPOSSIBLE). Trusts the user
   to have manually switched to Sonnet before typing "go".

Fires on UserPromptSubmit. Exit code 0 always.

DO NOT re-add:
- Reads of settings.json to infer the running model (settings.json lies — the
  Desktop app locks the model at session startup and the file is stale).
- Substring GO matching (matched "execute plan" inside natural prose like
  "why does execute plans fail"). Start-anchored regex + length guard only.
- Writes to settings.json "model" key from any hook (doesn't propagate to the
  running session, only affects next session).
"""
import json
import glob
import os
import re
import sys
import time

PLAN_DIR = os.path.expanduser("~/.claude/plans")
GUARD_ACTIVE = os.path.expanduser("~/.claude/.plan-guard-active")

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

# === ExitPlanMode PreToolUse ===
# Do NOT change settings.json here — the running session's model is locked.
# Do NOT delete plan files — they're consumed during execution.
tool_name = input_data.get("tool_name", "")
if tool_name == "ExitPlanMode":
    # ENSURE guard exists — blocks Edit/Write until user types "go"
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

# === "GO" DETECTION — Execute plan ===
# ANCHORED REGEX + LENGTH GUARD. Never substring-match on prose.
# Real GO signals are short button text or short user phrases. A diagnostic
# question like "why does execute plan fail?" must NOT match.
GO_PATTERNS = [
    r"^\s*go[!.]?\s*$",
    r"^\s*let'?s\s+go[!.]?\s*$",
    r"^\s*(start|begin|execute|proceed|continue|implement|run\s+it|do\s+it|go\s+ahead)[!.]?\s*$",
    r"^\s*approve\s+(the\s+)?plan\b",
    r"^\s*start\s+coding\b",
    r"^\s*(execute|run|implement|apply|do)\s+(the\s+)?plan\b",
    r"^\s*start\s+execution\b",
]

is_go = len(prompt) < 80 and any(re.search(p, prompt_lower) for p in GO_PATTERNS)

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
        # Remove guard — user typed "go", trust them to have switched.
        try:
            os.remove(GUARD_ACTIVE)
        except Exception:
            pass

        # Clean up older plan files so execution targets the right one.
        try:
            for old_plan in glob.glob(os.path.join(PLAN_DIR, "*.md")):
                if old_plan != recent_plan:
                    os.remove(old_plan)
        except Exception:
            pass

        # Neutral injection — does NOT claim to know which model is running.
        output = {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": (
                    "PLAN EXECUTION MODE.\n\n"
                    f"Plan file: {recent_plan}\n\n"
                    "INSTRUCTIONS:\n"
                    f"1. Read the plan at {recent_plan}\n"
                    "2. Execute it step by step — every step exactly as written\n"
                    "3. Do NOT rewrite, overwrite, or re-plan. Just execute.\n"
                    "4. Mark tasks as you complete them."
                )
            }
        }
        print(json.dumps(output))
        sys.exit(0)

# === GUARD ACTIVE — non-GO prompt ===
# Guard is active but prompt wasn't a GO signal. Inject a reminder telling the
# user to switch to Sonnet and type "go". We do NOT check the current model
# because the hook cannot determine it reliably — trust the user.
if os.path.exists(GUARD_ACTIVE):
    try:
        age = time.time() - os.path.getmtime(GUARD_ACTIVE)
        if age < 1800:  # guard is recent (< 30 min)
            output = {
                "hookSpecificOutput": {
                    "hookEventName": "UserPromptSubmit",
                    "additionalContext": (
                        "PLAN GUARD ACTIVE — MANDATORY, output this FIRST before anything else:\n\n"
                        "Tell the user VERBATIM:\n"
                        "\"A plan is ready for execution. For ~40-60% token savings:\n"
                        "   - Desktop app: Click the model selector dropdown → pick Sonnet\n"
                        "   - CLI: Run /model sonnet\n"
                        "   Then type: go\n"
                        "(If you'd rather execute on the current model, just type: go)\"\n\n"
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

    # Activate the guard — blocks Edit/Write until "go" triggers execution
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
                "to begin execution (manually switching to Sonnet first is recommended for cost)."
            )
        }
    }
    print(json.dumps(output))

sys.exit(0)
