#!/usr/bin/env python3
"""Stop hook: Passive memory consolidation (inspired by dream-skill + claude-mem).

Runs at session end. Two jobs:
1. FLAG: Check if consolidation is overdue (>24h since last run).
   If so, write a flag file that SessionStart will pick up to inject
   a consolidation prompt into the next session.
2. QUICK HYGIENE: Check MEMORY.md line count. If >150, flag for pruning.

Design: ~50ms overhead. No heavy work at Stop time — heavy consolidation
happens at next SessionStart when flagged.

Exit code 0 always (advisory only).
"""
import json
import os
import sys
from pathlib import Path
from datetime import datetime, timedelta

CONSOLIDATE_FLAG = Path(os.path.expanduser("~/.claude/memory-consolidate-needed"))
LAST_CONSOLIDATE = Path(os.path.expanduser("~/.claude/last-memory-consolidate"))
MEMORY_LINE_WARN = 150
CONSOLIDATE_INTERVAL_HOURS = 24

try:
    hook_input = json.load(sys.stdin)

    if hook_input.get("hook_event_name") != "Stop":
        sys.exit(0)
    if hook_input.get("stop_hook_active"):
        sys.exit(0)

    now = datetime.now()

    # Check if consolidation is overdue
    needs_consolidation = False
    if LAST_CONSOLIDATE.exists():
        try:
            last_time = datetime.fromisoformat(LAST_CONSOLIDATE.read_text().strip())
            if now - last_time > timedelta(hours=CONSOLIDATE_INTERVAL_HOURS):
                needs_consolidation = True
        except (ValueError, OSError):
            needs_consolidation = True
    else:
        # Never consolidated before
        needs_consolidation = True

    # Check MEMORY.md sizes across all project memory dirs
    oversized_memories = []
    projects_dir = Path(os.path.expanduser("~/.claude/projects"))
    if projects_dir.exists():
        for memory_md in projects_dir.rglob("memory/MEMORY.md"):
            try:
                line_count = len(memory_md.read_text().splitlines())
                if line_count > MEMORY_LINE_WARN:
                    oversized_memories.append(f"{memory_md}: {line_count} lines")
            except OSError:
                pass

    # Write flag if needed
    if needs_consolidation or oversized_memories:
        reasons = []
        if needs_consolidation:
            reasons.append("overdue (>24h since last consolidation)")
        if oversized_memories:
            reasons.append(f"oversized MEMORY.md: {', '.join(oversized_memories)}")

        CONSOLIDATE_FLAG.write_text(json.dumps({
            "flagged_at": now.isoformat(),
            "reasons": reasons
        }, indent=2))

except Exception:
    pass

sys.exit(0)
