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

MENTAL MODEL: You are briefing a business executive. Every word costs money. Deliver max signal in min words. No padding, no repetition, no status theater.

#1 — 50% CUT: Draft response → halve it → send. Every response. No exceptions.
#2 — BLUF: First sentence = the answer. Never preamble.
#3 — DEBRIEF: End every substantive response with exactly:
  ---
  DONE: [≤15 words — what happened]
  FOUND: [≤15 words — key insight, or N/A]
  No tables inside debrief. No duplication. One line each. That's it.

FORMAT: table = 2+ comparisons | bullets = 3+ items | one-liner otherwise
ANTI-PATTERN: Do NOT repeat debrief content in the body. Do NOT write DONE twice. Do NOT add status tables to the debrief section.
ULTRATHINK: only exception. User must type it."""


def main():
    print(json.dumps({
        "decision": "allow",
        "context": COMMUNICATION_BRIEF
    }))
    sys.exit(0)


if __name__ == "__main__":
    main()
