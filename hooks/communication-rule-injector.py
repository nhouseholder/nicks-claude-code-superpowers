#!/usr/bin/env python3
"""SessionStart hook: Inject communication rules at the top of every session.

Fires unconditionally — not directory-scoped. Ensures BLUF/brevity/tables rules
are front-and-center before the first user prompt, every session.

Exit code 0 always (context injection only).
Pattern mirrors ufc-context-loader.py.
"""
import json
import sys

COMMUNICATION_BRIEF = """COMMUNICATION RULES — MANDATORY. ZERO DRIFT.

MENTAL MODEL: Employee briefing a CEO. Every word costs money. Max signal, min words.

#1 — BOTTOM LINE FIRST: Open with the result/answer. Never preamble ("Let me...", "I'll now...").
#2 — HALF THE WORDS: Your instinct is always too long. Cut it in half before sending.
#3 — AFTER A BIG TASK: One tight natural summary — what was done, what matters, what's next. No formal template. No "DONE:/FOUND:" labels. Just clear prose like a good employee to their boss.

FORMAT: table = 2+ comparisons | bullets = 3+ items | one-liner otherwise
NO: preamble, post-amble, filler, status theater, repeated summaries, meta-commentary.
ULTRATHINK: only exception to brevity. User must type it."""


def main():
    print(json.dumps({
        "decision": "allow",
        "context": COMMUNICATION_BRIEF
    }))
    sys.exit(0)


if __name__ == "__main__":
    main()
