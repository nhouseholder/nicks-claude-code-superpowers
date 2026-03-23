#!/usr/bin/env python3
"""
GLM-5 Focus Guard — Injects a focus reminder after tool calls.
Fires on PostToolUse ONLY when Haiku/GLM-5 is active.
Prevents the model from dumping large amounts of text after reading files.
"""
import json
import sys
import os
import urllib.request


def detect_model():
    model = os.environ.get("CLAUDE_MODEL", "")
    if not model:
        try:
            resp = urllib.request.urlopen("http://127.0.0.1:17532/last-route", timeout=1)
            data = json.loads(resp.read())
            model = data.get("model", "")
        except Exception:
            pass
    return model.lower()


try:
    hook_input = json.load(sys.stdin)
    event = hook_input.get("hook_event_name", "")

    if event != "PostToolUse":
        sys.exit(0)

    model_lower = detect_model()
    if "haiku" not in model_lower:
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
