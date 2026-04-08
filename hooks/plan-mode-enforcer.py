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
                "PLAN MODE ENFORCEMENT: Write a highly detailed and specific "
                "step-by-step plan that Sonnet can execute with minimal room for error. "
                "Requirements for every plan:\n"
                "- Exact file paths to create or modify\n"
                "- Exact line numbers or unique string matches for edits\n"
                "- Exact code blocks — copy-paste ready, not pseudocode\n"
                "- Exact shell commands to run (with expected output where relevant)\n"
                "- Zero decision points — every step must be unambiguous\n"
                "- Verification steps after each logical group of changes\n\n"
                "The plan must be 'Sonnet-proof' — a mechanical executor should follow it "
                "without needing judgment calls. If a step requires a choice, make the choice "
                "in the plan and document why."
            )
        }
    }
    print(json.dumps(output))

sys.exit(0)
