#!/usr/bin/env python3
"""UserPromptSubmit hook: Detect user corrections and remind about triple-write.

Rule #31: When the user corrects Claude, the lesson MUST be written to
(1) project memory, (2) anti-patterns.md, (3) GitHub superpowers repo.

This hook detects correction signals in the user's message and injects
a reminder into the context so Claude doesn't forget.

Exit code 0 always (informational context injection).
"""
import json
import re
import sys

CORRECTION_SIGNALS = [
    r"\bthat'?s wrong\b",
    r"\bthat'?s not right\b",
    r"\bthat'?s not correct\b",
    r"\bno,?\s+(?:don'?t|stop|that)\b",
    r"\bstop doing\b",
    r"\bI (?:already )?told you\b",
    r"\bI said\b",
    r"\bwhy did you\b",
    r"\bwhy are you\b",
    r"\byou (?:keep|always|still)\b",
    r"\bwhat (?:the )?(?:heck|hell|fuck)\b",
    r"\bthis (?:is|keeps) (?:wrong|broken|breaking)\b",
    r"\bi'?m (?:so )?(?:sick|tired|frustrated)\b",
    r"\bfix this\b",
    r"\bnot what I (?:asked|wanted|meant)\b",
    r"\byou (?:broke|destroyed|removed|deleted)\b",
    r"\bthat was (?:a )?(?:win|loss|correct|wrong)\b",
    r"\bshould (?:have been|be)\b.*\bnot\b",
]


def detect_correction(text):
    text_lower = text.lower()
    for pattern in CORRECTION_SIGNALS:
        if re.search(pattern, text_lower):
            return True
    return False


def main():
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        sys.exit(0)

    user_message = hook_input.get("user_message", "") or hook_input.get("prompt", "")

    if not user_message:
        sys.exit(0)

    if detect_correction(user_message):
        print(json.dumps({
            "decision": "allow",
            "context": (
                "CORRECTION DETECTED — Rule #31 triple-write is MANDATORY. "
                "Before continuing, you MUST record this correction to ALL THREE locations: "
                "(1) Project memory (~/.claude/projects/<project>/memory/), "
                "(2) Anti-patterns (~/.claude/anti-patterns.md), "
                "(3) GitHub superpowers repo (sync via /tmp/ clone). "
                "If site-specific, also update the relevant site command."
            )
        }))

    sys.exit(0)


if __name__ == "__main__":
    main()
