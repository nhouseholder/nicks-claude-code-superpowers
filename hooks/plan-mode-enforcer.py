#!/usr/bin/env python3
"""
Plan Mode Enforcer — Injects "Sonnet-proof plan" instructions when planning is detected.

Fires on UserPromptSubmit. Detects plan-related intent in the user's prompt
and injects detailed plan requirements so Claude writes plans that Sonnet
can execute with zero ambiguity.

Also writes a marker file (~/.claude/.plan-switch-pending) so the
plan-execution-guard PreToolUse hook can block execution until the model
switches to Sonnet.

Exit code 0 always.
"""
import json
import os
import re
import sys

MARKER_FILE = os.path.expanduser("~/.claude/.plan-switch-pending")

try:
    input_data = json.load(sys.stdin)
except (json.JSONDecodeError, Exception):
    sys.exit(0)

prompt = input_data.get("prompt", "").strip()
prompt_lower = prompt.lower()

# Skip empty, very short, or slash-command prompts
if not prompt or len(prompt) < 3 or prompt.startswith("/"):
    sys.exit(0)

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
    plan_dir = os.path.expanduser("~/.claude/plans")
    try:
        import glob
        for old_plan in glob.glob(os.path.join(plan_dir, "*.md")):
            os.remove(old_plan)
    except Exception:
        pass

    # Write marker file for plan-execution-guard.py
    try:
        with open(MARKER_FILE, "w") as f:
            f.write("pending")
    except Exception:
        pass

    output = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": (
                "MANDATORY PLAN FORMAT — This overrides default plan mode behavior.\n\n"
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
                "and document WHY in the plan. Zero decision points for the executor."
            )
        }
    }
    print(json.dumps(output))

sys.exit(0)
