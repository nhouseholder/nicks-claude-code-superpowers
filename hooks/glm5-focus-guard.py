#!/usr/bin/env python3
"""
GLM-5 Focus Guard — Context-aware nudges after tool calls.
Fires on PostToolUse ONLY when Haiku/GLM-5 is active.
Different guidance depending on the tool used.
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

    # Context-aware reminders based on what tool just ran
    reminders = {
        "Read": "You just read a file. Before moving on: note the KEY FACT from this file that's relevant to the task. If debugging across files, write down what you learned before reading the next file.",
        "Grep": "Search results returned. Which results are actually relevant? Pick the specific matches that answer the question — ignore the rest.",
        "Glob": "File list returned. Which file(s) do you actually need to read? Pick the most likely one first.",
        "Edit": "You just edited a file. Does this change break anything else? Consider imports, callers, and tests.",
        "Write": "You just wrote a file. Verify: does it match the existing project patterns? Is anything hardcoded that shouldn't be?",
        "Bash": "Command completed. Did the output match what you expected? If not, diagnose before continuing.",
        "WebFetch": "Web content received. Extract only the specific data point you need — don't summarize the whole page.",
        "WebSearch": "Search results returned. Pick the most authoritative source. Don't try to synthesize all results.",
    }

    default = "Good. Connect this result back to what the user asked."
    reminder = reminders.get(tool_name, default)

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PostToolUse",
            "additionalContext": reminder
        }
    }))

except Exception:
    sys.exit(0)
