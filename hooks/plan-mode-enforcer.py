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

# Shared plan-utils
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    import _plan_utils as plan_utils
except Exception:
    plan_utils = None

PLAN_DIR = os.path.expanduser("~/.claude/plans")
GUARD_ACTIVE = os.path.expanduser("~/.claude/.plan-guard-active")

# Clean stale plan files — SCOPED TO CURRENT PROJECT ONLY.
# Previously this ran a global glob across ~/.claude/plans/ which silently
# deleted approved plans from other concurrent sessions. See anti-patterns.md
# → PLAN_FILE_CROSS_PROJECT_CONFUSION.
if plan_utils is not None:
    try:
        plan_utils.clean_stale_project_plans()
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
    # ENSURE guard exists — blocks Edit/Write until user types "go".
    # Store cwd + newest project-scoped plan real path (two-line format).
    # Also pin ACTIVE_PLAN pointer so `go` resolves deterministically.
    try:
        recent_real = ""
        if plan_utils is not None:
            # Prefer ACTIVE_PLAN if already set by plan-relocate.py
            recent_real = plan_utils.get_active_plan()
            if not recent_real:
                plans = plan_utils.find_project_plans()
                if plans:
                    recent_real = plans[0]
                    plan_utils.set_active_plan(recent_real)
        with open(GUARD_ACTIVE, "w") as f:
            f.write(os.getcwd())
            if recent_real:
                f.write("\n")
                f.write(recent_real)
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
    # Resolve THE plan. Priority:
    #   1. ACTIVE_PLAN pointer (single source of truth, set by ExitPlanMode/relocate)
    #   2. Newest project-scoped plan by mtime (fallback for legacy/edge cases)
    # Either way, age must be < 30 min — old approvals don't auto-execute.
    recent_plan = None
    try:
        if plan_utils is not None:
            active = plan_utils.get_active_plan()
            if active and (time.time() - os.path.getmtime(active)) < 1800:
                recent_plan = active
            else:
                plan_files = plan_utils.find_project_plans()
                if plan_files and (time.time() - os.path.getmtime(plan_files[0])) < 1800:
                    recent_plan = plan_files[0]
        else:
            plan_files = sorted(
                glob.glob(os.path.join(PLAN_DIR, "*.md")),
                key=os.path.getmtime,
                reverse=True,
            )
            if plan_files:
                age = time.time() - os.path.getmtime(plan_files[0])
                if age < 1800:
                    recent_plan = plan_files[0]
    except Exception:
        pass

    if recent_plan:
        # Remove guard — user typed "go", trust them to have switched.
        try:
            os.remove(GUARD_ACTIVE)
        except Exception:
            pass

        # Clear ACTIVE_PLAN pointer — user approved execution, so the
        # sonnet-switch-gate Stop hook no longer needs to block. Without
        # this, the pointer would stay fresh and the gate would block
        # every subsequent assistant turn during execution.
        try:
            if plan_utils is not None:
                plan_utils.clear_active_plan()
        except Exception:
            pass

        # Clean up older plan files so execution targets the right one —
        # PROJECT-SCOPED. Never deletes plans belonging to other projects.
        try:
            project_plans = (
                plan_utils.find_project_plans() if plan_utils is not None
                else [recent_plan]
            )
            for old_plan in project_plans:
                if os.path.realpath(old_plan) != os.path.realpath(recent_plan):
                    try:
                        os.remove(old_plan)
                    except Exception:
                        pass
                    # Remove dangling symlink in ~/.claude/plans/
                    if plan_utils is not None:
                        try:
                            plan_utils._remove_dangling_symlinks_to(old_plan)
                        except Exception:
                            pass
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
                    "4. Mark tasks as you complete them.\n\n"
                    "CRITICAL — DO NOT output any of these:\n"
                    "- 'Switch to Sonnet' or any model recommendation\n"
                    "- A summary of the plan steps\n"
                    "- 'If you'd rather I execute on Opus...' or any alternative offer\n"
                    "- Any preamble, narration, or confirmation request\n"
                    "The user typed 'go'. That IS the approval. Start executing step 1 immediately."
                )
            }
        }
        print(json.dumps(output))
        sys.exit(0)

# === GUARD ACTIVE — non-GO prompt ===
# Only fire the "type go" nudge when ALL of these are true:
#   (a) guard file exists and is recent (< 30 min)
#   (b) guard was created for THIS project (cwd match — no cross-project bleed)
#   (c) a recent plan file actually exists in PLAN_DIR (not orphaned)
#   (d) the user's prompt is SHORT (< 80 chars) — long prose is never a GO
# Otherwise: silently clean up stale guards or skip the injection.
if os.path.exists(GUARD_ACTIVE):
    try:
        age = time.time() - os.path.getmtime(GUARD_ACTIVE)

        # (a) Expire old guards
        if age >= 1800:
            try:
                os.remove(GUARD_ACTIVE)
            except Exception:
                pass
            raise StopIteration  # break out to fall-through

        # (b) Project-scope check — cross-project bleed is the #1 source of
        # false fires. If cwd doesn't match the guard's stored cwd, the guard
        # belongs to a different session in a different project. Clean up.
        try:
            with open(GUARD_ACTIVE, "r") as f:
                guard_project = f.read().strip()
        except Exception:
            guard_project = ""
        if guard_project and guard_project != "active" and guard_project != os.getcwd():
            try:
                os.remove(GUARD_ACTIVE)
            except Exception:
                pass
            raise StopIteration

        # (c) Orphaned guard check — if there's no recent plan file, the guard
        # is leftover from plan-intent detection that never produced a plan.
        # Remove it so future turns are silent. PROJECT-SCOPED discovery.
        has_recent_plan = False
        try:
            if plan_utils is not None:
                plan_files = plan_utils.find_project_plans()
            else:
                plan_files = sorted(
                    glob.glob(os.path.join(PLAN_DIR, "*.md")),
                    key=os.path.getmtime,
                    reverse=True,
                )
            if plan_files and (time.time() - os.path.getmtime(plan_files[0])) < 1800:
                has_recent_plan = True
        except Exception:
            pass
        if not has_recent_plan:
            try:
                os.remove(GUARD_ACTIVE)
            except Exception:
                pass
            raise StopIteration

        # (d) Length filter — real GO signals are short. Long prompts are
        # feature descriptions, clarifications, or continued planning
        # discussion. Silently skip the injection (keep the guard — a later
        # short "go" should still fire).
        if len(prompt) >= 80:
            raise StopIteration

        # All gates passed. This is plausibly a GO signal on the correct
        # project with a real pending plan. Show the nudge.
        output = {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": (
                    "PLAN GUARD ACTIVE — output this FIRST, verbatim:\n"
                    "\"Plan ready. Switch to Sonnet, then type: go\"\n"
                    "Do NOT execute any plan steps. Output only the message and stop."
                )
            }
        }
        print(json.dumps(output))
        sys.exit(0)
    except StopIteration:
        pass  # fall through to plan-intent detection below
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
    # Clean up old plan files so Sonnet doesn't confuse them with the current
    # plan — PROJECT-SCOPED. A "write a plan" prompt in project A must never
    # wipe project B's approved plan.
    try:
        if plan_utils is not None:
            for old_plan in plan_utils.find_project_plans():
                try:
                    os.remove(old_plan)
                except Exception:
                    pass
                try:
                    plan_utils._remove_dangling_symlinks_to(old_plan)
                except Exception:
                    pass
        else:
            for old_plan in glob.glob(os.path.join(PLAN_DIR, "*.md")):
                try:
                    os.remove(old_plan)
                except Exception:
                    pass
    except Exception:
        pass

    # DO NOT activate the guard here. Conversational plan-intent phrases like
    # "make a plan" are too loose to justify locking Edit/Write. The guard is
    # only created by the PreToolUse:ExitPlanMode branch above, which fires
    # when the user actually exits plan mode via the real tool. Creating a
    # guard on prose signals produced orphaned guards that leaked into other
    # sessions/projects and false-fired "A plan is ready for execution".

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
                "AFTER writing the plan file, STOP. Call ExitPlanMode if in plan mode.\n"
                "Then tell the user VERBATIM, as your final output:\n"
                "\"Plan saved. Switch to Sonnet, then type: go\"\n"
                "Do NOT execute plan steps yourself."
            )
        }
    }
    print(json.dumps(output))

sys.exit(0)
