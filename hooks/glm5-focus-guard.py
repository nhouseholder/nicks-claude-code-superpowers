#!/usr/bin/env python3
"""
GLM-5 Focus Guard — Injects a focus reminder after tool calls.
Fires on PostToolUse ONLY when Haiku/GLM-5 is active.
Prevents the model from dumping large amounts of text after reading files.
"""
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from detect_model import is_glm5


try:
    hook_input = json.load(sys.stdin)
    event = hook_input.get("hook_event_name", "")

    if event != "PostToolUse":
        sys.exit(0)

    if not is_glm5():
        sys.exit(0)

    tool_name = hook_input.get("tool_name", "")

    # After file reads and searches — highest hallucination risk
    high_risk_tools = {"Read", "Grep", "Glob", "WebFetch", "WebSearch"}

    if tool_name in high_risk_tools:
        reminder = "REMINDER: You just read data. Report only what's relevant to the user's question. Do NOT summarize the entire file or generate code from memory. Keep text output under 20 lines."
    else:
        # Light reminder for other tools
        reminder = "Stay focused on the user's request. Brief output only."

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": reminder
        }
    }))

except Exception:
    sys.exit(0)
