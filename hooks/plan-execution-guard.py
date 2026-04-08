#!/usr/bin/env python3
"""
Plan Execution Guard — Blocks code edits until user switches to Sonnet.

Fires on PreToolUse:Edit|Write (NOT Bash — Bash is used for read-only
exploration during plan mode and must not be blocked).

When a .plan-switch-pending marker exists (set by plan-mode-enforcer.py):
1. Allows writes to ~/.claude/plans/ (still writing the plan)
2. Blocks Edit/Write to any other file with a model-switch instruction
3. Deletes the marker (one-shot — only blocks once)

The block tells Claude to instruct the user to run /model sonnet.
settings.json is also updated for new sessions, but the running session
requires /model to actually change.

Exit code 0 = allow, exit code 2 = block.
"""
import json
import glob
import os
import re
import sys

MARKER_FILE = os.path.expanduser("~/.claude/.plan-switch-pending")
SETTINGS_PATH = os.path.expanduser("~/.claude/settings.json")
PLAN_DIR = os.path.expanduser("~/.claude/plans")


def main():
    # Fast exit if no marker — this is the common path
    if not os.path.exists(MARKER_FILE):
        sys.exit(0)

    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        sys.exit(0)

    tool_name = hook_input.get("tool_name", "")
    tool_input = hook_input.get("tool_input", {})

    # Only act on Edit/Write
    if tool_name not in ("Write", "Edit"):
        sys.exit(0)

    # Allow writes to plan files (still in plan mode)
    file_path = tool_input.get("file_path", "") or tool_input.get("path", "")
    if file_path and PLAN_DIR in file_path:
        sys.exit(0)

    # === BLOCK EXECUTION — User must switch to Sonnet first ===

    # Assess plan complexity from most recent plan file
    complexity = "MEDIUM"
    step_count = 0
    file_count = 0
    try:
        plan_files = sorted(
            glob.glob(os.path.join(PLAN_DIR, "*.md")),
            key=os.path.getmtime,
            reverse=True,
        )
        if plan_files:
            with open(plan_files[0], "r") as f:
                plan_content = f.read()
            step_count = len(re.findall(r"^###?\s+Step", plan_content, re.MULTILINE))
            file_count = len(re.findall(r"\*\*File[s]?:\*\*", plan_content))
            complex_keywords = [
                "architecture", "refactor", "migrate", "multi-file",
                "database", "schema", "security", "performance",
                "integration", "concurrent", "parallel",
            ]
            complex_hits = sum(
                1 for kw in complex_keywords if kw in plan_content.lower()
            )
            if step_count >= 8 or file_count >= 5 or complex_hits >= 3:
                complexity = "HIGH"
    except Exception:
        pass

    # Update settings.json for NEW sessions (doesn't affect running session)
    try:
        with open(SETTINGS_PATH, "r") as f:
            settings = json.load(f)
        if "opus" in settings.get("model", "").lower():
            settings["model"] = "claude-sonnet-4-6"
            with open(SETTINGS_PATH, "w") as f:
                json.dump(settings, f, indent=2)
                f.write("\n")
    except Exception:
        pass

    # Delete marker — one-shot guard
    try:
        os.remove(MARKER_FILE)
    except Exception:
        pass

    # Find the plan file path to include in instructions
    plan_path = "the plan file"
    try:
        found = sorted(
            glob.glob(os.path.join(PLAN_DIR, "*.md")),
            key=os.path.getmtime,
            reverse=True,
        )
        if found:
            plan_path = found[0]
    except Exception:
        pass

    # Block with instructions
    result = {
        "decision": "block",
        "reason": (
            f"PLAN EXECUTION BLOCKED — Switch to Sonnet first.\n"
            f"Plan: {plan_path}\n"
            f"Complexity: {complexity} | Steps: {step_count} | Files: {file_count}\n\n"
            "MANDATORY — tell the user EXACTLY this:\n"
            "'Plan approved. Run /model sonnet (or click the model selector) "
            "to switch to Sonnet 4.6 for execution, then send \"go\" to begin.'\n\n"
            "CRITICAL FOR NEXT AGENT (Sonnet): The plan file above is the CURRENT plan. "
            "READ it and EXECUTE it step by step. Do NOT overwrite it. Do NOT write a new plan. "
            "It was written by Opus specifically for you to execute mechanically.\n\n"
            "Do NOT attempt ANY code changes this turn. STOP after delivering the message above."
        ),
    }
    print(json.dumps(result))
    sys.exit(2)


if __name__ == "__main__":
    main()
