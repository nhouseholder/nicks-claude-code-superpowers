#!/usr/bin/env python3
"""SessionStart hook: Inject memory consolidation prompt if flagged.

Checks for ~/.claude/memory-consolidate-needed (written by memory-consolidate.py
Stop hook). If present, injects context telling the agent to consolidate
memory as a background task early in the session.

After injecting, updates the last-consolidate timestamp and removes the flag.

Exit code 0 always (context injection only).
"""
import json
import os
import sys
from pathlib import Path
from datetime import datetime

FLAG = Path(os.path.expanduser("~/.claude/memory-consolidate-needed"))
LAST_CONSOLIDATE = Path(os.path.expanduser("~/.claude/last-memory-consolidate"))

CONSOLIDATION_PROMPT = """MEMORY CONSOLIDATION NEEDED (auto-flagged by memory-consolidate hook)

Your memory files need maintenance. At a natural pause in this session (not immediately — finish the user's first request first), run a background agent to:

1. **Prune MEMORY.md indexes** — Remove entries pointing to files that no longer exist. Keep under 150 lines.
2. **Deduplicate** — If two memory files say the same thing, merge into one and update the index.
3. **Resolve contradictions** — If two memories conflict, keep the newer one (check file dates).
4. **Convert relative dates** — Any memory with "yesterday", "last week", "Thursday" → convert to absolute dates.
5. **Remove stale project memories** — If a project memory references work that's been completed and merged, it's no longer useful.

Scope: Current project's memory directory only. Do NOT touch other projects' memories.
After consolidation, update ~/.claude/last-memory-consolidate with current ISO timestamp.

This is LOW PRIORITY — do the user's work first. Run consolidation in background only."""

try:
    if not FLAG.exists():
        sys.exit(0)

    try:
        flag_data = json.loads(FLAG.read_text())
        reasons = flag_data.get("reasons", ["unknown"])
    except (json.JSONDecodeError, OSError):
        reasons = ["flag file unreadable"]

    context = f"{CONSOLIDATION_PROMPT}\n\nReasons: {', '.join(reasons)}"

    print(json.dumps({
        "decision": "allow",
        "context": context
    }))

    # Update timestamp and remove flag
    LAST_CONSOLIDATE.write_text(datetime.now().isoformat())
    FLAG.unlink(missing_ok=True)

except Exception:
    pass

sys.exit(0)
