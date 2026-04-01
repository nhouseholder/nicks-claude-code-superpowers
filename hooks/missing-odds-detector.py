#!/usr/bin/env python3
"""PostToolUse hook: Detect missing odds in UFC data output.

Rule: NEVER accept missing prop odds. If ANY fight has null odds,
run the scraper FIRST. "—" in a payout cell is NEVER acceptable.

Exit code 0 always (informational warning).
"""
import json
import os
import re
import sys


def detect_missing_odds(text):
    """Check for missing odds indicators in output text."""
    warnings = []

    # __NO_PROPS__ in data
    if "__NO_PROPS__" in text:
        count = text.count("__NO_PROPS__")
        warnings.append(f"__NO_PROPS__ found {count} time(s) — run odds scraper to backfill")

    # "—" or "–" in what looks like a payout/odds context
    # Match patterns like: "Method: —" or "| — |" in table rows near bet terms
    if re.search(r'(?:method|round|combo|parlay|prop|odds|pnl|payout)\s*[:=|]\s*[—–]', text, re.IGNORECASE):
        warnings.append("Missing odds displayed as '—' — run scraper before accepting as final")

    # null odds in JSON-like output
    null_odds = re.findall(r'(?:method_odds|round_odds|combo_odds|ml_odds)\s*[:=]\s*(?:null|None|undefined)', text)
    if null_odds:
        warnings.append(f"Null odds found ({len(null_odds)} fields) — scrape before displaying")

    return warnings


def is_sports_project():
    """Only run in sports/betting projects — skip all others."""
    cwd = os.getcwd().lower()
    sports_markers = ["mmalogic", "ufc", "diamond", "courtside", "nfl-draft", "loss-analyst"]
    return any(m in cwd for m in sports_markers)


def main():
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        sys.exit(0)

    # Skip non-sports projects entirely
    if not is_sports_project():
        sys.exit(0)

    tool_output = hook_input.get("tool_output", "") or hook_input.get("output", "")
    if not tool_output or len(str(tool_output)) < 30:
        sys.exit(0)

    text = str(tool_output)
    warnings = detect_missing_odds(text)

    if warnings:
        warning_text = " | ".join(warnings)
        print(json.dumps({
            "decision": "allow",
            "context": (
                f"MISSING ODDS DETECTED: {warning_text}. "
                f"PERMANENT RULE: When ANY fight has null prop odds, "
                f"IMMEDIATELY run the prop odds scraper. "
                f"NEVER display '—' for prop bets and call it correct."
            )
        }))

    sys.exit(0)


if __name__ == "__main__":
    main()
