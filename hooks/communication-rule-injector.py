#!/usr/bin/env python3
"""SessionStart hook: Inject communication rules at the top of every session.

Fires unconditionally — not directory-scoped. Ensures BLUF/brevity/tables rules
are front-and-center before the first user prompt, every session.

Exit code 0 always (context injection only).
Pattern mirrors ufc-context-loader.py.
"""
import json
import sys

COMMUNICATION_BRIEF = """COMMUNICATION RULES — FRONT AND CENTER (non-negotiable, every session, zero drift):
- 50% WORD TARGET: every response must use ≤50% of the words your instinct says. Your first draft is always too long. Cut ruthlessly before sending.
- END EVERY RESPONSE with a BLUF debrief: DONE: [one tight sentence] | FOUND: [one tight sentence or N/A]. No exceptions.
- BLUF: first sentence = the answer. Not "Let me check", not "I'll now". The answer.
- Tables for 2+ comparisons; bullets for 3+ items; one-liner otherwise.
- Bullets = full-line (~80–120 chars). No 3-word filler bullets.
- No preamble. No post-amble. No filler. Just do the work, report the result.
- Caveman OK: cut "the/a/is/that" when meaning survives.
- Exception: ULTRATHINK only — user must type it explicitly."""


def main():
    print(json.dumps({
        "decision": "allow",
        "context": COMMUNICATION_BRIEF
    }))
    sys.exit(0)


if __name__ == "__main__":
    main()
