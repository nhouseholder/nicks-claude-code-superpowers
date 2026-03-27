#!/usr/bin/env python3
"""Stop hook: Detect when Claude ended with narration instead of action.

Rule #19: Never end a turn with only narration. If the response contains
"Let me...", "I'll start by...", "First I need to..." it should have been
followed by tool calls. If we're at the Stop event, Claude ended its turn
without making those calls — inject a reminder.

Exit code 0 always (context injection).
"""
import json
import sys

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
]


def main():
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        sys.exit(0)

    # Get the stop reason and last message
    stop_reason = hook_input.get("stop_reason", "")
    last_message = hook_input.get("last_assistant_message", "") or ""

    if not last_message:
        sys.exit(0)

    last_lower = last_message.lower().strip()

    # Check if the last message was narration without action
    for signal in NARRATION_SIGNALS:
        if signal in last_lower:
            # Check if it's short (likely just narration, no real content)
            if len(last_message.strip()) < 500:
                print(json.dumps({
                    "decision": "allow",
                    "context": (
                        "NARRATION STOP DETECTED: You ended your turn with narration "
                        "instead of tool calls. Rule #19: NEVER end a turn with only "
                        "narration. Make tool calls alongside narration, or skip the "
                        "narration and just make the tool calls. The user should not "
                        "have to say 'continue'."
                    )
                }))
                break

    sys.exit(0)


if __name__ == "__main__":
    main()
