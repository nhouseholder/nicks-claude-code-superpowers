#!/usr/bin/env python3
"""SessionStart guard: Prevents double-initialization after compaction.

Problem: When Claude Code compacts, it fires SessionStart hooks TWICE in
rapid succession (Compacted→init, then another init). This causes all
hooks to run twice and the model to choke on doubled context.

Strategy: This runs FIRST. On first init it writes a lock file. On second
init (within 60s) it outputs a SKIP signal. Other hooks check for the
lock and skip if it exists AND is >2s old (meaning a prior init already ran).

The >2s check is key: hooks in the SAME init batch see a lock that's <2s
old and proceed normally. Only a SECOND init batch (>2s later) gets blocked.

Exit code 0 always.
"""
import json
import os
import sys
import time
from pathlib import Path

LOCK = Path(os.path.expanduser("~/.claude/.session-init-lock"))
COOLDOWN = 60  # seconds — block re-inits within this window

try:
    hook_input = json.load(sys.stdin)
except (json.JSONDecodeError, EOFError):
    hook_input = {}

# Check if we JUST initialized (within cooldown window but >2s ago)
try:
    if LOCK.exists():
        age = time.time() - LOCK.stat().st_mtime
        if 2 < age < COOLDOWN:
            # Second init detected within cooldown — skip everything
            sys.exit(0)
except OSError:
    pass

# First init (or cooldown expired) — write the lock
try:
    LOCK.write_text(str(time.time()))
except OSError:
    pass

sys.exit(0)
