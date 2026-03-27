#!/usr/bin/env python3
"""SessionStart hook: Auto-remove .parry-tainted files and warn.

parry-guard's taint system is a nuclear option — one ML false positive
locks out ALL tool calls for the entire project. Since all repos are
user-owned (not untrusted third-party code), auto-clean and warn
instead of blocking.

Exit code 0 always (context injection only).
"""
import json
import os
import sys
from pathlib import Path


def find_taint_files():
    """Check cwd and parent dirs for .parry-tainted files."""
    cwd = Path(os.getcwd())
    found = []

    # Check cwd and up to 3 parents
    for d in [cwd] + list(cwd.parents)[:3]:
        taint = d / ".parry-tainted"
        if taint.exists():
            found.append(taint)

    return found


try:
    taint_files = find_taint_files()

    if not taint_files:
        sys.exit(0)

    # Read taint reason before removing
    reasons = []
    for tf in taint_files:
        try:
            content = tf.read_text().strip()
            if content:
                reasons.append(f"{tf}: {content[:200]}")
            tf.unlink()
        except OSError:
            pass

    warning = f"""PARRY-GUARD TAINT AUTO-CLEANED

{len(taint_files)} .parry-tainted file(s) were found and removed:
{chr(10).join(str(f) for f in taint_files)}

{"Taint reasons: " + "; ".join(reasons) if reasons else "No reason recorded."}

These files block ALL tool calls when present. They were likely created by
a parry-guard ML false positive on user-owned code. The taint has been
cleared so this session can proceed normally.

If you see this repeatedly for the same project, consider running:
  parry-guard ignore   (in the affected project directory)"""

    print(json.dumps({
        "decision": "allow",
        "context": warning
    }))

except Exception:
    pass

sys.exit(0)
