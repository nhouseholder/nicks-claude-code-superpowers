#!/usr/bin/env python3
"""
Context Saver — Tracks prompt count per session, injects compact reminder
at ~60% estimated context usage.

Fires on UserPromptSubmit. Uses a state file to count prompts.
At threshold (15 prompts), injects a one-time reminder to /compact.
Resets after 2 hours (assumed new session) or when state file is deleted.

Exit code 0 always. Lightweight — one file read/write.
"""
import json
import os
import sys
import time

STATE_FILE = os.path.expanduser("~/.claude/.context-saver-state")
PROMPT_THRESHOLD = 15  # ~60% context usage heuristic
CRITICAL_THRESHOLD = 25  # ~80% context usage — quality degrading
SESSION_TIMEOUT = 7200  # 2 hours = new session

try:
    input_data = json.load(sys.stdin)
except (json.JSONDecodeError, Exception):
    sys.exit(0)

prompt = input_data.get("prompt", "").strip()

# Skip empty or slash commands
if not prompt or prompt.startswith("/"):
    sys.exit(0)

# Read or initialize state
state = {"count": 0, "reminded": False, "started": time.time()}
try:
    with open(STATE_FILE, "r") as f:
        state = json.load(f)
    # Reset if session timed out
    if time.time() - state.get("started", 0) > SESSION_TIMEOUT:
        state = {"count": 0, "reminded": False, "started": time.time()}
except (FileNotFoundError, json.JSONDecodeError):
    state = {"count": 0, "reminded": False, "started": time.time()}

# Increment
state["count"] = state.get("count", 0) + 1

# Check thresholds
should_remind = state["count"] >= PROMPT_THRESHOLD and not state.get("reminded", False)
should_critical = state["count"] >= CRITICAL_THRESHOLD and not state.get("critical_reminded", False)

if should_remind:
    state["reminded"] = True
if should_critical:
    state["critical_reminded"] = True

# Write state
try:
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)
except Exception:
    pass

if should_critical:
    output = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": (
                "CONTEXT SAVER (CRITICAL): ~80%+ context estimated "
                f"({state['count']} prompts this session). "
                "Context quality is degrading. "
                "Run /full-handoff NOW, then /compact or start a new session."
            )
        }
    }
    print(json.dumps(output))
elif should_remind:
    output = {
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": (
                "CONTEXT SAVER: ~60% context estimated "
                f"({state['count']} prompts this session). "
                "Before quality degrades:\n"
                "1. Commit and push any uncommitted work\n"
                "2. Suggest /full-handoff to preserve decisions\n"
                "3. Suggest /compact to free context space\n"
                "Deliver this as a brief aside, not a blocker."
            )
        }
    }
    print(json.dumps(output))

sys.exit(0)
