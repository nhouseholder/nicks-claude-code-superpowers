#!/usr/bin/env python3
"""
Session Bridge — Ensures GLM-5 picks up from the VERY LAST message when switching models.
Prevents re-processing older messages in the same session.
"""
import json
import sys
import os
import urllib.request
from pathlib import Path


def detect_model():
    """Detect current model from CLAUDE_MODEL env var or proxy's /last-route."""
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

    if event != "UserPromptSubmit":
        sys.exit(0)

    model_lower = detect_model()
    if "haiku" not in model_lower:
        sys.exit(0)

    prompt = hook_input.get("prompt", "")
    transcript_path = hook_input.get("transcript_path", "")

    # Extract the VERY LAST exchange from the transcript
    last_user_msg = ""
    last_assistant_msg = ""

    if transcript_path and Path(transcript_path).exists():
        try:
            with open(transcript_path) as f:
                lines = f.readlines()

            # Scan from END to find the last user message and last assistant response
            for line in reversed(lines):
                try:
                    entry = json.loads(line)
                    role = entry.get("role", "")
                    content = entry.get("content", "")

                    if role == "assistant" and not last_assistant_msg:
                        # Get first 500 chars of last assistant response
                        if isinstance(content, str):
                            last_assistant_msg = content[:500]
                        elif isinstance(content, list):
                            # Extract text from content blocks
                            texts = []
                            for block in content:
                                if isinstance(block, dict) and block.get("type") == "text":
                                    texts.append(block.get("text", ""))
                            last_assistant_msg = " ".join(texts)[:500]

                    elif role == "user" and not last_user_msg:
                        # Get first 300 chars of last user message
                        if isinstance(content, str):
                            last_user_msg = content[:300]
                        elif isinstance(content, list):
                            texts = []
                            for block in content:
                                if isinstance(block, dict) and block.get("type") == "text":
                                    texts.append(block.get("text", ""))
                            last_user_msg = " ".join(texts)[:300]

                except:
                    pass

                if last_user_msg and last_assistant_msg:
                    break

        except Exception:
            pass

    # Build the continuation instruction
    if last_user_msg or last_assistant_msg:
        bridge_context = f"""
[CONTINUATION INSTRUCTION — READ THIS FIRST]

You are continuing a session that was interrupted. The previous model (Opus) was working on:

LAST USER REQUEST: {last_user_msg}

LAST ASSISTANT RESPONSE (what Opus was doing): {last_assistant_msg}...

YOUR TASK: Continue EXACTLY where Opus left off. Do NOT re-process earlier messages in this session. Do NOT go back to older topics. Pick up from the last message and continue forward.

User's current request: {prompt}
"""
        output = {
            "hookSpecificOutput": {
                "hookEventName": "UserPromptSubmit",
                "additionalContext": bridge_context
            }
        }
        print(json.dumps(output))
    else:
        # No transcript context available — pass through
        sys.exit(0)

except Exception:
    sys.exit(0)
