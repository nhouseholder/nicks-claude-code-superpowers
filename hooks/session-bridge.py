#!/usr/bin/env python3
"""
Session Bridge — Anchors GLM-5 to the most recent conversation context.
Fires on EVERY UserPromptSubmit when Haiku/GLM-5 is active.
Extracts the last user+assistant exchange and injects it as priority context.
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


def extract_text(content):
    """Extract plain text from a message content field (str or list of blocks)."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        texts = []
        for block in content:
            if isinstance(block, dict):
                if block.get("type") == "text":
                    texts.append(block.get("text", ""))
                elif block.get("type") == "tool_result":
                    # Skip tool results — too noisy
                    pass
        return " ".join(texts)
    return ""


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

    if not transcript_path or not Path(transcript_path).exists():
        sys.exit(0)

    # Read transcript and extract last user + assistant exchange
    last_user_msg = ""
    last_assistant_msg = ""

    try:
        with open(transcript_path) as f:
            lines = f.readlines()

        # Scan from END — find last assistant response, then last user message before it
        found_assistant = False
        for line in reversed(lines):
            try:
                entry = json.loads(line)
                role = entry.get("role", "")
                content = entry.get("content", "")
                text = extract_text(content)

                if not text or len(text.strip()) < 5:
                    continue

                if role == "assistant" and not found_assistant:
                    # Last meaningful assistant response (first 600 chars)
                    last_assistant_msg = text.strip()[:600]
                    found_assistant = True
                elif role == "user" and found_assistant and not last_user_msg:
                    # Last user message before that assistant response
                    last_user_msg = text.strip()[:400]
                    break
            except Exception:
                pass

    except Exception:
        sys.exit(0)

    # Only inject if we found meaningful context
    if not last_assistant_msg:
        sys.exit(0)

    bridge = f"""[SESSION CONTEXT — Most recent exchange before your current message]
USER ASKED: {last_user_msg[:400] if last_user_msg else '(see conversation history)'}
ASSISTANT WAS DOING: {last_assistant_msg[:600]}
[END CONTEXT]
INSTRUCTION: Address the user's CURRENT message below. Use the above only for continuity — do not re-explain or re-summarize it."""

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": bridge
        }
    }))

except Exception:
    sys.exit(0)
