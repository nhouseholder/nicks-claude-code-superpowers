#!/usr/bin/env python3
"""PostToolUse hook: Detect impossible statistics in agent output.

Rule #16: Extreme results = bug in your analysis, not a finding.
Scans agent responses for implausible numbers and warns before
they get presented to the user as fact.

Exit code 0 always (informational warning).
"""
import json
import os
import re
import sys


def detect_impossible_stats(text):
    """Return list of warnings for impossible statistics found in text."""
    warnings = []

    # Profit with 0 wins: "+XX.XXu" near "0W" or "0 wins"
    if re.search(r'\+\d+\.?\d*u.*?0[Ww]|0\s*[Ww].*?\+\d+\.?\d*u', text):
        warnings.append("Profit > 0 with 0 wins — impossible")

    # 0W-0L with non-zero P/L
    if re.search(r'0[Ww]-0[Ll].*?[+-]\d+\.?\d*u|[+-]\d+\.?\d*u.*?0[Ww]-0[Ll]', text):
        warnings.append("0W-0L with non-zero P/L — scoring bug")

    # 100% win rate with large sample (20+)
    match = re.search(r'100(?:\.0)?%.*?(?:(\d+)[Ww]|wins?:?\s*(\d+))', text)
    if match:
        wins = int(match.group(1) or match.group(2) or "0")
        if wins >= 20:
            warnings.append(f"100% win rate over {wins} samples — suspect data leakage")

    # 0% win rate with large sample
    match = re.search(r'(?:0(?:\.0)?%\s*(?:win|rate)).*?(?:(\d+)\s*(?:bets|total|samples))', text, re.IGNORECASE)
    if match:
        total = int(match.group(1))
        if total >= 20:
            warnings.append(f"0% win rate over {total} samples — suspect query bug")

    # Duplicate entries in what looks like a ranked list
    # Look for repeated names in numbered lists
    names_in_list = re.findall(r'^\s*\d+[\.\)]\s*(.+?)(?:\s*[-—|]|\s*$)', text, re.MULTILINE)
    if len(names_in_list) > 3:
        seen = set()
        for name in names_in_list:
            clean = name.strip().lower()[:30]
            if clean in seen and len(clean) > 3:
                warnings.append(f"Duplicate entry in ranked list: '{name.strip()}'")
                break
            seen.add(clean)

    # Percentage over 100% (but not odds like +150)
    for match in re.finditer(r'(\d{3,})%', text):
        val = int(match.group(1))
        if val > 100 and val < 1000:  # Skip odds-like values
            # Check it's not in an odds context
            ctx = text[max(0, match.start()-20):match.end()+10]
            if not re.search(r'odds|line|moneyline|\+', ctx, re.IGNORECASE):
                warnings.append(f"Percentage over 100%: {val}% — check if this should be a raw value")

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

    # Check tool output for impossible stats
    tool_output = hook_input.get("tool_output", "") or hook_input.get("output", "")
    if not tool_output:
        sys.exit(0)

    # Only check substantial output (skip short responses)
    if len(str(tool_output)) < 50:
        sys.exit(0)

    text = str(tool_output)
    warnings = detect_impossible_stats(text)

    if warnings:
        warning_text = " | ".join(warnings)
        print(json.dumps({
            "decision": "allow",
            "context": (
                f"IMPOSSIBLE STATISTICS DETECTED — Rule #16: {warning_text}. "
                f"Verify your query before presenting these as findings. "
                f"Test on 1-2 known events manually to validate."
            )
        }))

    sys.exit(0)


if __name__ == "__main__":
    main()
