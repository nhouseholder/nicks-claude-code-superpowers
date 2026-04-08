#!/usr/bin/env python3
"""
Plan Execution Guard — Blocks code edits until user switches to Sonnet.

Fires on PreToolUse:Edit|Write. Uses plan file recency as the signal
(NOT a marker file — plan mode is entered via UI button, not keywords).

Logic:
1. Check if a plan file in ~/.claude/plans/ was modified < 10 minutes ago
2. Check if .plan-guard-consumed references that same plan (already blocked)
3. If recent plan + not consumed → BLOCK once, write consumed marker
4. If consumed or no recent plan → ALLOW (fast path)

Always allows writes to ~/.claude/plans/ (still writing the plan).

Exit code 0 = allow, exit code 2 = block.
"""
import json
import glob
import os
import re
import sys
import time

SETTINGS_PATH = os.path.expanduser("~/.claude/settings.json")
PLAN_DIR = os.path.expanduser("~/.claude/plans")
CONSUMED_FILE = os.path.expanduser("~/.claude/.plan-guard-consumed")


def main():
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        sys.exit(0)

    tool_name = hook_input.get("tool_name", "")
    tool_input = hook_input.get("tool_input", {})

    # Only act on Edit/Write
    if tool_name not in ("Write", "Edit"):
        sys.exit(0)

    # If already on Sonnet — allow immediately. The guard only blocks Opus.
    try:
        with open(SETTINGS_PATH, "r") as f:
            current_model = json.load(f).get("model", "")
        if "sonnet" in current_model.lower():
            sys.exit(0)
    except Exception:
        pass

    # Always allow writes to plan files
    file_path = tool_input.get("file_path", "") or tool_input.get("path", "")
    if file_path and PLAN_DIR in file_path:
        sys.exit(0)

    # === Check for recent plan file ===
    recent_plan = None
    try:
        plan_files = sorted(
            glob.glob(os.path.join(PLAN_DIR, "*.md")),
            key=os.path.getmtime,
            reverse=True,
        )
        if plan_files:
            age = time.time() - os.path.getmtime(plan_files[0])
            if age < 600:  # 10 minutes
                recent_plan = plan_files[0]
    except Exception:
        pass

    # No recent plan — fast exit
    if not recent_plan:
        sys.exit(0)

    # Check if already consumed for this specific plan
    try:
        if os.path.exists(CONSUMED_FILE):
            with open(CONSUMED_FILE, "r") as f:
                consumed_plan = f.read().strip()
            if consumed_plan == recent_plan:
                sys.exit(0)  # Already blocked once, now allow
    except Exception:
        pass

    # === BLOCK — Recent plan exists, not yet consumed ===

    # Mark as consumed (one-shot — won't block again for this plan)
    try:
        with open(CONSUMED_FILE, "w") as f:
            f.write(recent_plan)
    except Exception:
        pass

    # Assess plan complexity
    complexity = "MEDIUM"
    step_count = 0
    file_count = 0
    try:
        with open(recent_plan, "r") as f:
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

    # Update settings.json for new sessions
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

    # Block with instructions
    result = {
        "decision": "block",
        "reason": (
            f"PLAN EXECUTION BLOCKED — Switch to Sonnet first.\n"
            f"Plan file: {recent_plan}\n"
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
