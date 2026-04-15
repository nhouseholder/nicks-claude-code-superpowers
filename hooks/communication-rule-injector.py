#!/usr/bin/env python3
"""SessionStart hook: Inject communication rules at the top of every session.

Fires unconditionally — not directory-scoped. Ensures BLUF/brevity/tables rules
are front-and-center before the first user prompt, every session.

Exit code 0 always (context injection only).
Pattern mirrors ufc-context-loader.py.
"""
import json
import sys

COMMUNICATION_BRIEF = """COMMUNICATION RULES — MANDATORY. ZERO EXCEPTIONS. ZERO DRIFT.

#1 RULE — 50% WORD CUT: Your instinct output is always too long. Cut it in half before sending. Every. Single. Response.
- If you wrote 200 words, rewrite to 100. If 100, rewrite to 50. No exceptions.
- Caveman grammar OK: drop "the/a/is/that/which" when meaning survives.
- One sentence beats two. One word beats three.

BLUF: first sentence = the answer. Never "Let me...", "I'll now...", "First,..."
DEBRIEF: end every substantive response with:
  DONE: [one tight sentence]
  FOUND: [one tight sentence or N/A]

FORMAT: tables for 2+ comparisons | bullets for 3+ items | one-liner otherwise
BULLETS: full-line ~80–120 chars. No 3-word bullets. No preamble. No post-amble.
ULTRATHINK: only exception to brevity. User must type it explicitly."""


def main():
    print(json.dumps({
        "decision": "allow",
        "context": COMMUNICATION_BRIEF
    }))
    sys.exit(0)


if __name__ == "__main__":
    main()
