#!/usr/bin/env python3
"""
GLM-5 Focus Guard — Brief nudge after high-risk tool calls only.
Fires on PostToolUse ONLY when Haiku/GLM-5 is active.
Only fires for Read/Grep/WebFetch — the tools that trigger hallucination.
Skips Edit/Bash/Write/Glob to reduce token noise.
"""
import json
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from detect_model import is_glm5


try:
    hook_input = json.load(sys.stdin)

    if hook_input.get("hook_event_name") != "PostToolUse":
        sys.exit(0)

    if not is_glm5():
        sys.exit(0)

    tool = hook_input.get("tool_name", "")

    # Only fire on high-hallucination-risk tools
    nudge = {
        "Read": "Note the key fact relevant to the task before moving on.",
        "Grep": "Which matches are relevant? Ignore the rest.",
        "WebFetch": "Extract only the data point you need.",
    }.get(tool)

    if nudge:
        print(json.dumps({
            "hookSpecificOutput": {
                "hookEventName": "PostToolUse",
                "additionalContext": nudge
            }
        }))

except Exception:
    sys.exit(0)
