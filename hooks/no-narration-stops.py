#!/usr/bin/env python3
"""Stop hook: Block stops when Claude ended with narration or no output.

Three failure modes:
1. Narration-only: "Let me read..." / "Reading the source..." then stop
2. Silent stop: reads files, produces no text, stops ("No response requested")
3. Thin output: very short message after tool calls (not a real response)

Exit code 2 = BLOCK the stop (force continuation).
Exit code 0 = allow the stop.
"""
import json
import os
import sys
import hashlib

NARRATION_SIGNALS = [
    "let me ",
    "i'll start by",
    "i'll begin by",
    "first i need to",
    "first, i'll",
    "let me continue",
    "i'll continue",
    "i need to ",
    "i should ",
    "i want to ",
    "let me explore",
    "let me check",
    "let me read",
    "let me look",
    "i'll now ",
    "next i'll",
    "let me investigate",
    "i'll investigate",
    "reading the ",
    "looking at ",
    "checking the ",
    "examining ",
    "now i'll ",
    "now let me",
    "i'll examine",
    "i'll look at",
    "this is the critical",
    "this is the key",
    "now — this is",
]

COMPLETION_SIGNALS = [
    "done", "fixed", "updated", "created", "archived", "removed",
    "changed", "committed", "pushed", "deployed", "verified",
    "all cases pass", "here's the", "result", "summary",
    "ready to work", "no previous handoff", "session oriented",
]

MAX_BLOCKS = 3


def get_counter_file(session_id):
    """Per-session counter file so sessions don't interfere."""
    sid = session_id or "default"
    short = hashlib.md5(sid.encode()).hexdigest()[:8]
    return f"/tmp/.claude-stop-block-{short}"


def get_block_count(path):
    try:
        if os.path.exists(path):
            return int(open(path).read().strip())
    except Exception:
        pass
    return 0


def block(reason, counter_file):
    """Block the stop if under the limit."""
    count = get_block_count(counter_file) + 1
    try:
        open(counter_file, "w").write(str(count))
    except Exception:
        pass

    if count <= MAX_BLOCKS:
        sys.stderr.write(reason)
        sys.exit(2)

    # Over limit — allow stop, reset
    try:
        os.remove(counter_file)
    except Exception:
        pass
    sys.exit(0)


def main():
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        sys.exit(0)

    last_message = (hook_input.get("last_assistant_message", "") or "").strip()
    session_id = hook_input.get("session_id", "")
    counter_file = get_counter_file(session_id)

    last_lower = last_message.lower()
    is_completion = any(s in last_lower for s in COMPLETION_SIGNALS)

    # --- Check 1: Silent/thin stop (short message, no real content) ---
    if len(last_message) < 80 and not is_completion:
        block(
            "BLOCKED STOP: You stopped without producing meaningful output. "
            "Continue working — analyze what you've read and take action. "
            "Chain multiple tool calls together in one response. "
            "Never stop after reading files without acting on them.",
            counter_file
        )

    # --- Check 2: Narration-only stop ---
    if len(last_message) < 200 and not is_completion:
        for signal in NARRATION_SIGNALS:
            if signal in last_lower:
                block(
                    "BLOCKED STOP: You ended with narration instead of action. "
                    "Rule: NEVER end a turn with only narration. "
                    "Make the tool calls you described. Do not stop.",
                    counter_file
                )
                break

    # Legitimate stop — reset block counter
    try:
        if os.path.exists(counter_file):
            os.remove(counter_file)
    except Exception:
        pass
    sys.exit(0)


if __name__ == "__main__":
    main()
