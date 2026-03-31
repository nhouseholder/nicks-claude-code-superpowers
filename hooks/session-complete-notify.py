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

# Derive session name — match what the Claude desktop app shows in the header
cwd = os.getcwd()

# Handle worktree paths: cwd might be something like
# ~/.claude/worktrees/eager-lewin/nfl-draft-predictor or
# ~/Projects/nfl-draft-predictor--claude-worktrees-eager-lewin
# We need to extract the actual project name, not the worktree label
raw_name = os.path.basename(cwd)

# Strip worktree suffixes: "nfl-draft-predictor--claude-worktrees-eager-lewin" → "nfl-draft-predictor"
if "--claude-worktrees" in raw_name:
    raw_name = raw_name.split("--claude-worktrees")[0]

# Handle ~/.claude/worktrees/<label>/<project> paths
if "worktrees" in cwd or "worktree" in cwd:
    # Walk up to find a directory that matches a known project
    parts = cwd.split(os.sep)
    for part in reversed(parts):
        clean = part.split("--claude-worktrees")[0] if "--claude-worktrees" in part else part
        if clean in ("worktrees", "worktree", ".claude", ""):
            continue
        # Skip worktree labels (short random names like "eager-lewin", "50fc")
        if len(clean) <= 12 and "-" in clean and not any(c.isdigit() for c in clean.split("-")[0]):
            continue
        raw_name = clean
        break

# Map known project dirs to their friendly session names (matches app header)
SESSION_NAMES = {
    "superpowers": "Superpowers",
    "mmalogic": "MMALogic",
    "diamondpredictions": "Diamond Predictions",
    "courtside-ai": "Courtside AI",
    "mystrainai": "MyStrainAI",
    "enhancedhealthai": "Enhanced Health AI",
    "nestwisehq": "NestWise HQ",
    "researcharia": "Research Aria",
    "portfolio": "Portfolio",
    "all-things-ai": "All Things AI",
    "nfl-draft-predictor": "NFL Draft Predictor",
    "Residency-app": "Residency App",
    "loss-analyst": "Loss Analyst",
    "Brewmaps": "Brewmaps",
}

project_name = SESSION_NAMES.get(raw_name, raw_name.replace("-", " ").replace("_", " ").title())
if not project_name or project_name == "/":
    project_name = "Unknown Session"

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

# === METHOD 2: Dock badge bounce (without stealing focus) ===
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
