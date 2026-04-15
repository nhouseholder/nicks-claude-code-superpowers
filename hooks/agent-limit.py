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

    # Haiku nudge — Explore agents and simple lookups must use Haiku (20x cheaper).
    tool_input = hook_input.get("tool_input", {}) or {}
    subagent_type = str(tool_input.get("subagent_type", "")).lower()
    model = str(tool_input.get("model", "")).lower()
    haiku_types = {"explore"}
    needs_haiku_nudge = subagent_type in haiku_types and "haiku" not in model

    context = f"Agent {new_count}/{MAX_AGENTS} spawned."
    if needs_haiku_nudge:
        context += (
            " HAIKU REQUIRED: Explore agents must use model='haiku' — 20x cheaper"
            " than Sonnet/Opus for file reads and searches. Respawn with model='haiku'."
        )

    print(json.dumps({"decision": "allow", "context": context}))
    sys.exit(0)


if __name__ == "__main__":
    main()
