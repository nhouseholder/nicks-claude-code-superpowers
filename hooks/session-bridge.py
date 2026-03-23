#!/usr/bin/env python3
"""
Session Bridge — Ensures context continuity when switching models mid-session.
Fires on UserPromptSubmit when model is Haiku (GLM-5) to inject recent context
from the current session transcript.
"""
import json
import sys
import os
from pathlib import Path

try:
    hook_input = json.load(sys.stdin)
    event = hook_input.get("hook_event_name", "")

    # Only fire on UserPromptSubmit when Haiku is active
    if event != "UserPromptSubmit":
        sys.exit(0)

    model = os.environ.get("CLAUDE_MODEL", "").lower()
    if "haiku" not in model:
        sys.exit(0)

    prompt = hook_input.get("prompt", "")
    transcript_path = hook_input.get("transcript_path", "")

    # If user says "continue" or similar, try to extract recent context
    continue_signals = ["continue", "go", "keep going", "go on", "proceed", "carry on", "next", "resume"]
    if prompt.lower().strip() not in continue_signals:
        sys.exit(0)

    # Try to read the last few exchanges from the transcript
    recent_context = ""
    if transcript_path and Path(transcript_path).exists():
        try:
            with open(transcript_path) as f:
                lines = f.readlines()

            # Get last 10 exchanges (user + assistant pairs)
            recent = lines[-20:] if len(lines) > 20 else lines

            # Extract the most recent user message and assistant response
            last_user_msg = ""
            last_assistant_summary = ""

            for line in reversed(recent):
                try:
                    entry = json.loads(line)
                    if entry.get("role") == "user" and not last_user_msg:
                        content = entry.get("content", "")
                        if isinstance(content, str):
                            last_user_msg = content[:200]  # First 200 chars
                    elif entry.get("role") == "assistant" and not last_assistant_summary:
                        content = entry.get("content", "")
                        if isinstance(content, str):
                            last_assistant_summary = content[:300]  # First 300 chars
                except:
                    pass

                if last_user_msg and last_assistant_summary:
                    break

            if last_user_msg or last_assistant_summary:
                recent_context = f"""
[SESSION BRIDGE — Recent Context]
Last user message: {last_user_msg}
Last assistant response: {last_assistant_summary[:300]}...
[END BRIDGE]
"""
        except Exception:
            pass

    # Inject the recent context
    if recent_context:
        output = {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": f"{prompt}\n\n{recent_context}\n\nContinue from where we left off."
            }
        }
    else:
        output = {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": f"{prompt}\n\nNote: Could not extract recent context from transcript. Please check conversation history and continue the most recent task."
            }
        }

    print(json.dumps(output))

except Exception:
    sys.exit(0)
