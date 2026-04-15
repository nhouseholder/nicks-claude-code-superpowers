#!/usr/bin/env python3
"""SessionStart hook: surface a pending ACTIVE_PLAN if present.

If the current project has an unexecuted approved plan (ACTIVE_PLAN pointer
exists and the plan file is < 30 min old), inject context into the new
session telling Claude exactly what's pending and what the user must do next.

Prevents pipeline drift across session compactions / restarts. If a session
ends mid-pipeline (plan approved, never executed), the next session sees the
state immediately and reminds the user.

Exit code 0 always — context injection only.
"""
from __future__ import annotations

import json
import os
import sys
import time

# Import shared plan utilities
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    import _plan_utils as plan_utils
except Exception:
    print(json.dumps({"decision": "allow"}))
    sys.exit(0)


def main() -> None:
    try:
        active = plan_utils.get_active_plan()
        if not active or not os.path.isfile(active):
            print(json.dumps({"decision": "allow"}))
            sys.exit(0)

        age_min = (time.time() - os.path.getmtime(active)) / 60.0
        if age_min > 30:
            # Stale — clear it and stay silent
            plan_utils.clear_active_plan()
            print(json.dumps({"decision": "allow"}))
            sys.exit(0)

        context = (
            "PENDING PLAN DETECTED — DO NOT START A NEW TASK YET.\n"
            f"An approved plan is waiting for execution:\n"
            f"  {active}\n"
            f"  (approved {age_min:.0f} min ago)\n\n"
            "Tell the user EXACTLY (one line, verbatim):\n"
            "  Plan ready. Switch to Sonnet, then type: go\n\n"
            "Do NOT execute the plan yourself. Do NOT call Edit or Write. "
            "Output ONLY the message above and stop, then wait for the user."
        )
        print(json.dumps({"decision": "allow", "context": context}))
    except Exception:
        print(json.dumps({"decision": "allow"}))
    sys.exit(0)


if __name__ == "__main__":
    main()
