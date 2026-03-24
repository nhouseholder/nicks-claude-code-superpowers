#!/usr/bin/env python3
"""
Session Bridge — Provides GLM-5 with structured handoff context from the session.
Fires on EVERY UserPromptSubmit when Haiku/GLM-5 is active.
Extracts the last 3 user+assistant exchanges (not just 1) for real continuity.
"""
import json
import sys
import os
import subprocess
from pathlib import Path

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from detect_model import detect_model


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

    # Read last 150 lines to capture more context (3-5 exchanges typically)
    try:
        result = subprocess.run(
            ["tail", "-150", transcript_path],
            capture_output=True, text=True, timeout=3
        )
        lines = result.stdout.strip().split("\n") if result.stdout else []
    except Exception:
        sys.exit(0)

    # Extract up to 3 recent exchanges (user→assistant pairs)
    exchanges = []  # List of (user_msg, assistant_msg) tuples
    current_assistant = ""
    current_user = ""

    for line in reversed(lines):
        try:
            entry = json.loads(line)
            role = entry.get("role", "")
            text = extract_text(entry.get("content", ""))

            if not text or len(text.strip()) < 5:
                continue

            if role == "assistant" and not current_assistant:
                current_assistant = text.strip()[:800]
            elif role == "user" and current_assistant:
                current_user = text.strip()[:300]
                exchanges.append((current_user, current_assistant))
                current_assistant = ""
                current_user = ""
                if len(exchanges) >= 3:
                    break
        except Exception:
            pass

    if not exchanges:
        sys.exit(0)

    # Build structured handoff — most recent first
    exchanges.reverse()  # Chronological order

    bridge_parts = ["[SESSION HANDOFF — You are continuing work from Opus/Sonnet]", ""]

    for i, (user_msg, assistant_msg) in enumerate(exchanges):
        if i == len(exchanges) - 1:
            # Most recent exchange — show more detail
            bridge_parts.append(f"MOST RECENT — User: {user_msg[:300]}")
            bridge_parts.append(f"MOST RECENT — Assistant was: {assistant_msg[:800]}")
        else:
            # Earlier exchanges — just enough for context
            bridge_parts.append(f"Earlier — User: {user_msg[:150]}")
            bridge_parts.append(f"Earlier — Assistant: {assistant_msg[:200]}...")
        bridge_parts.append("")

    bridge_parts.append("YOUR TASK: Pick up EXACTLY where the last assistant response left off.")
    bridge_parts.append("- Do NOT redo work that's already done")
    bridge_parts.append("- Do NOT re-read files that were already read (unless you need specific data)")
    bridge_parts.append("- If the last response was mid-task, continue that task")
    bridge_parts.append("- If the last response completed a task, ask what's next")
    bridge_parts.append("[END HANDOFF]")

    bridge = "\n".join(bridge_parts)

    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": bridge
        }
    }))

except Exception:
    sys.exit(0)
