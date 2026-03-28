#!/usr/bin/env python3
"""PreToolUse hook: Block direct edits to mmalogic webapp unless /mmalogic agent is active.

RULE: Only the /mmalogic dedicated agent command may touch the mmalogic.com website.
No ad-hoc frontend edits, no data syncs to webapp/, no version bumps, no deploys
without loading the full /mmalogic knowledge base first.

This prevents the recurring bugs caused by editing the site without domain context:
- Missing bet types, broken charts, incomplete tables
- Wrong parlay rendering, missing odds, SUB not converted to DEC
- Stale data deployed without validator checks

Exit code 2 = block with message. Exit code 0 = allow.
"""
import json
import os
import sys

# Protected paths (relative patterns within the mmalogic project)
PROTECTED_PATTERNS = [
    "webapp/frontend/src/",
    "webapp/frontend/public/data/",
    "webapp/frontend/src/config/version.js",
]

# Files that are OK to touch without the agent (algorithm, registry, etc.)
ALLOWED_PATTERNS = [
    "UFC_Alg_v4_fast_2026.py",
    "ufc_profit_registry.json",
    "ufc_prop_odds_cache.json",
    "ufc_odds_cache.json",
    "algorithm_stats.json",
    "prediction_output.json",
    "prediction_cache/",
    "prediction_archive/",
    "track_results.py",
    "validate_",
    "constants.json",
    "ufc_expert_consensus/",
    "ufc_systems_registry.json",
    "backtest_summary.json",
    "fight_breakdowns.json",
    "CLAUDE.md",
    "HANDOFF.md",
]

def is_mmalogic_project(tool_input):
    """Check if we're working in the mmalogic project."""
    file_path = tool_input.get("file_path", "") or tool_input.get("command", "")
    return any(p in file_path for p in ["mmalogic", "ufc-predict", "webapp/frontend"])

def is_protected_path(file_path):
    """Check if the file is in a protected webapp path."""
    return any(pattern in file_path for pattern in PROTECTED_PATTERNS)

def is_allowed_path(file_path):
    """Check if the file is in an explicitly allowed path (algorithm, data, etc.)."""
    return any(pattern in file_path for pattern in ALLOWED_PATTERNS)

def check_mmalogic_agent_active():
    """Check if /mmalogic was invoked in this session by looking for its marker."""
    # The /mmalogic skill prints "Loaded: 15-item checklist..." when it runs.
    # We check for a session marker file that /mmalogic sets.
    marker = os.path.expanduser("~/.claude/.mmalogic_agent_active")
    if os.path.exists(marker):
        # Check if marker is from this session (within last 4 hours)
        import time
        age = time.time() - os.path.getmtime(marker)
        return age < 14400  # 4 hours
    return False

def main():
    hook_input = json.loads(sys.stdin.read())
    tool_name = hook_input.get("tool_name", "")
    tool_input = hook_input.get("tool_input", {})

    # Only check Edit and Write tools
    if tool_name not in ("Edit", "Write"):
        return

    file_path = tool_input.get("file_path", "")
    if not file_path:
        return

    # Only guard mmalogic project files
    if not is_mmalogic_project(tool_input):
        return

    # Allow non-webapp files (algorithm, registry, etc.)
    if is_allowed_path(file_path):
        return

    # Check if this is a protected webapp path
    if not is_protected_path(file_path):
        return

    # Protected path detected — check if /mmalogic agent is active
    if check_mmalogic_agent_active():
        return  # Agent is active, allow the edit

    # BLOCK: Direct webapp edit without /mmalogic agent
    filename = os.path.basename(file_path)
    result = {
        "decision": "block",
        "reason": (
            f"🛑 BLOCKED: Direct edit to webapp file '{filename}' without /mmalogic agent.\n\n"
            f"RULE: Only the /mmalogic dedicated agent may touch mmalogic.com website files.\n"
            f"This prevents recurring bugs (missing bet types, broken parlays, wrong odds, etc.).\n\n"
            f"To proceed:\n"
            f"  1. Invoke /mmalogic first (loads knowledge base, runs freshness check, validator)\n"
            f"  2. Then make your edits through the agent's workflow\n\n"
            f"If this is algorithm/data work (not frontend): the file may be in the wrong path.\n"
            f"Protected paths: webapp/frontend/src/, webapp/frontend/public/data/"
        ),
    }
    print(json.dumps(result))
    sys.exit(2)


if __name__ == "__main__":
    main()
