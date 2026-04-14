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
- END EVERY RESPONSE with a BLUF debrief: one clean block at the bottom — DONE: [what was done] | FOUND: [what was found]. No exceptions. Every single response, every chat, forever.
- BLUF: first sentence = the answer. Not "Let me check", not "I'll now". The answer.
- Tables for 2+ comparisons; bullets for 3+ items; one-liner otherwise.
- Bullets = full-line target (~80–120 chars each). No 3-word filler bullets.
- No preamble ("Let me...", "First I need to...", "I'll now..."). Just do the work.
- No post-amble fluff ("In summary", "To summarize", "Let me know if..."). Debrief block IS the summary.
- Caveman OK: cut filler words when meaning survives. Short > verbose, always.
- Exception: ULTRATHINK mode only — user must type it explicitly per request."""


def main():
    print(json.dumps({
        "decision": "allow",
        "context": COMMUNICATION_BRIEF
    }))
    sys.exit(0)


if __name__ == "__main__":
    main()
