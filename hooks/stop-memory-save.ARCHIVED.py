# ============================================================
# ARCHIVED — 2026-03-24
# Reason: Removed from settings.json during token audit (saved ~8K tokens/session)
# Do NOT run this file. Do NOT import from this file.
# Kept for historical reference only.
# ============================================================

#!/usr/bin/env python3
"""
Claude Code Stop Hook — Memory Save Reminder
Runs after every Claude response. Injects a reminder for Claude to save
important learnings to memory before the conversation moves on.
"""
import json
import sys

try:
    input_data = json.load(sys.stdin)
except json.JSONDecodeError:
    sys.exit(0)

# Get the stop reason and transcript info
stop_reason = input_data.get("stopReason", "")
transcript = input_data.get("transcript", [])

# Only trigger on substantive interactions (not empty or error stops)
# Skip if conversation is very short (< 4 messages = greeting/trivial)
if len(transcript) < 4:
    sys.exit(0)

# Build the memory reminder
reminder = """MEMORY CHECK — Before proceeding, briefly consider:

1. Did I learn something new about the user's preferences, workflow, or goals?
2. Did I solve a non-trivial problem or discover something project-specific?
3. Did the user correct me or give feedback on my approach?
4. Did I discover a pattern, gotcha, or important context?

If YES to any: save to memory using the appropriate system:
- Project memory: write to ~/.claude/projects/*/memory/ (project-scoped)
- Global memory: write to ~/.claude/memory/topics/<topic>.md (cross-project)
- Update core.md or MEMORY.md index if significant

If NO: proceed normally. Do NOT force-save trivial interactions."""

output = {
    "hookSpecificOutput": {
        "hookEventName": "Stop",
        "additionalContext": reminder
    }
}
print(json.dumps(output))
sys.exit(0)
