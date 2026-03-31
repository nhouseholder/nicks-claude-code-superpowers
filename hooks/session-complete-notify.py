#!/usr/bin/env python3
"""Stop hook: Send macOS notification identifying WHICH session completed.

Three notification methods (all fire simultaneously):
1. macOS native notification (banner + sound) with project name in title
2. macOS Say (text-to-speech) announcing the project name
3. Terminal badge update (dock bounce)

The notification includes the project name derived from cwd, so when
running multiple Claude Code sessions, you know which one needs attention.
"""
import json
import sys
import os
import subprocess

try:
    hook_input = json.load(sys.stdin)
except (json.JSONDecodeError, EOFError):
    sys.exit(0)

# Only fire on actual stops, not recursive stop hooks
if hook_input.get("stop_hook_active"):
    sys.exit(0)

# Derive project identity from working directory
cwd = os.getcwd()
project_name = os.path.basename(cwd)

# Clean up common iCloud path noise
project_name = project_name.replace("com~apple~CloudDocs", "iCloud")
if not project_name or project_name == "/":
    project_name = "Unknown Project"

# Get stop reason for context
stop_reason = hook_input.get("stop_reason", "unknown")

# Determine notification body based on stop reason
if stop_reason == "end_turn":
    body = f"Claude is waiting for input in: {project_name}"
elif stop_reason == "max_tokens":
    body = f"Claude hit token limit in: {project_name}"
else:
    body = f"Claude stopped ({stop_reason}) in: {project_name}"

# === METHOD 1: macOS Native Notification ===
# Shows as a banner with project name in title + sound
notification_script = f'''
display notification "{body}" with title "Claude Code — {project_name}" sound name "Glass"
'''
subprocess.Popen(
    ["osascript", "-e", notification_script.strip()],
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
)

# === METHOD 2: Text-to-Speech (short, non-blocking) ===
# Speaks the project name so you know which session without looking
say_text = f"{project_name} needs attention"
subprocess.Popen(
    ["say", "-v", "Samantha", "-r", "200", say_text],
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
)

# === METHOD 3: Dock badge bounce (without stealing focus) ===
# Uses a brief activation trick to trigger dock bounce, then returns focus
bounce_script = '''
tell application "System Events"
    set frontApp to name of first application process whose frontmost is true
    if frontApp is not "Claude" then
        tell application "Claude" to activate
        delay 0.1
        tell application frontApp to activate
    end if
end tell
'''
subprocess.Popen(
    ["osascript", "-e", bounce_script.strip()],
    stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL
)

sys.exit(0)
