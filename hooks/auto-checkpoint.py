#!/usr/bin/env python3
"""
Auto-Checkpoint — Saves a lightweight handoff file after every Stop event.
This runs WHILE Opus is active, creating breadcrumbs that GLM-5 can read later.

On every Stop (Opus finishes responding), writes ~/.claude/last-checkpoint.json with:
- Last user message
- Last assistant response summary
- Timestamp
- Which project directory

When GLM-5 takes over, session-bridge can read this file as a backup
if transcript parsing fails or context is too sparse.
"""
import json
import sys
import os
import subprocess
from pathlib import Path
from datetime import datetime


try:
    hook_input = json.load(sys.stdin)
    event = hook_input.get("hook_event_name", "")

    if event != "Stop":
        sys.exit(0)

    # Don't recurse — if we're already in a Stop hook, skip
    if hook_input.get("stop_hook_active"):
        sys.exit(0)

    transcript_path = hook_input.get("transcript_path", "")
    if not transcript_path or not Path(transcript_path).exists():
        sys.exit(0)

    # Read last few lines of transcript
    try:
        result = subprocess.run(
            ["tail", "-30", transcript_path],
            capture_output=True, text=True, timeout=2
        )
        lines = result.stdout.strip().split("\n") if result.stdout else []
    except Exception:
        sys.exit(0)

    last_user = ""
    last_assistant = ""

    for line in reversed(lines):
        try:
            entry = json.loads(line)
            role = entry.get("role", "")
            content = entry.get("content", "")

            # Extract text
            if isinstance(content, str):
                text = content
            elif isinstance(content, list):
                text = " ".join(
                    b.get("text", "") for b in content
                    if isinstance(b, dict) and b.get("type") == "text"
                )
            else:
                continue

            text = text.strip()
            if len(text) < 5:
                continue

            if role == "assistant" and not last_assistant:
                last_assistant = text[:1000]
            elif role == "user" and not last_user:
                last_user = text[:500]

            if last_user and last_assistant:
                break
        except Exception:
            pass

    if not last_assistant:
        sys.exit(0)

    # Write checkpoint
    checkpoint = {
        "timestamp": datetime.now().isoformat(),
        "project_dir": os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd()),
        "model": os.environ.get("CLAUDE_MODEL", "unknown"),
        "last_user_message": last_user,
        "last_assistant_response": last_assistant,
        "transcript_path": transcript_path,
    }

    checkpoint_path = Path.home() / ".claude" / "last-checkpoint.json"
    checkpoint_path.write_text(json.dumps(checkpoint, indent=2))

except Exception:
    pass  # Never block the Stop event
