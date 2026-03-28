#!/usr/bin/env python3
"""
Claude Code Stop Hook — Session-aware notification
Shows macOS notification with session/project name when Claude finishes.
"""
import json
import sys
import subprocess
import os

try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError:
    sys.exit(0)

# Get session info
session_id = input_data.get("session_id", "")
transcript = input_data.get("transcript", [])
stop_reason = input_data.get("stopReason", "end_turn")

# Skip if conversation is trivial (< 4 messages)
if len(transcript) < 4:
    sys.exit(0)

# Determine project/session name from CWD
cwd = os.getcwd()
project_name = os.path.basename(cwd)

# Clean up common directory names
name_map = {
    "superpowers": "Superpowers (Skills)",
    "com~apple~CloudDocs": "iCloud",
    "Mobile Documents": "iCloud",
}
display_name = name_map.get(project_name, project_name)

# If in a /tmp clone, get the real project name
if cwd.startswith("/tmp/"):
    display_name = os.path.basename(cwd).replace("-work", "").replace("-sync", "").replace("-push", "")

# Get short session ID (last 6 chars)
short_session = session_id[-6:] if session_id else ""

# Build notification message
title = f"Claude Code — {display_name}"
message = f"Task complete. Session: {short_session}" if short_session else "Task complete."

# Send macOS notification
subprocess.run([
    "osascript", "-e",
    f'display notification "{message}" with title "{title}" sound name "Glass"'
], capture_output=True)

sys.exit(0)
