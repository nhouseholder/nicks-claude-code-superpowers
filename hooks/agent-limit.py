#!/usr/bin/env python3
"""PreToolUse hook: Enforce max 2 subagents per session.

Rule #32: Max 2 subagents. NEVER spawn more than 2.
Uses a temp file counter to track agent spawns in this session.

Exit code 2 = block. Exit code 0 = allow.
"""
import json
import os
import sys

COUNTER_FILE = f"/tmp/claude-agent-count-{os.getppid()}"
MAX_AGENTS = 2


def get_count():
    try:
        with open(COUNTER_FILE, "r") as f:
            return int(f.read().strip())
    except (FileNotFoundError, ValueError):
        return 0


def increment():
    count = get_count() + 1
    with open(COUNTER_FILE, "w") as f:
        f.write(str(count))
    return count


def main():
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        sys.exit(0)

    current = get_count()

    if current >= MAX_AGENTS:
        result = {
            "decision": "block",
            "reason": (
                f"AGENT LIMIT: Already spawned {current} subagents (max {MAX_AGENTS}). "
                f"Do this task yourself — do not spawn another agent. "
                f"Rule #32: Max 2 subagents per session."
            ),
        }
        print(json.dumps(result))
        sys.exit(2)

    # Allow and increment
    new_count = increment()
    print(json.dumps({
        "decision": "allow",
        "context": f"Agent {new_count}/{MAX_AGENTS} spawned."
    }))
    sys.exit(0)


if __name__ == "__main__":
    main()
