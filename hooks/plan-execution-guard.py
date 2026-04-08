#!/usr/bin/env python3
"""
Plan Execution Guard — Blocks Opus from executing plans meant for Sonnet.

Fires on PreToolUse:Edit|Write. When a recent plan file exists, blocks
ALL Edit/Write to non-plan files until the user manually runs /model sonnet.

IMPORTANT: Mid-session model switching from a hook is NOT possible.
settings.json writes only affect new sessions. The running session's model
is locked once started. So this guard blocks repeatedly until the user
manually switches via /model sonnet, at which point the guard file is
consumed and allows through.

The unlock mechanism: when the user runs /model sonnet, Claude will try
Edit/Write again. This time, the guard checks for .plan-guard-unlocked
(written by the user or by Claude after /model switch). If found, allows.

Simpler approach: plan-mode-enforcer writes .plan-guard-active when plan
intent is detected. This guard blocks while that file exists. The user
(or Claude) deletes it after switching models.

Exit code 0 = allow, exit code 2 = block.
"""
import json
import glob
import os
import re
import sys
import time

PLAN_DIR = os.path.expanduser("~/.claude/plans")
GUARD_ACTIVE = os.path.expanduser("~/.claude/.plan-guard-active")


def main():
    # Fast exit: no guard active
    if not os.path.exists(GUARD_ACTIVE):
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

    # Always allow writes to plan files and guard files
    file_path = tool_input.get("file_path", "") or tool_input.get("path", "")
    if file_path and (PLAN_DIR in file_path or ".claude/." in file_path):
        sys.exit(0)

    # === Check guard age — auto-expire after 30 minutes ===
    try:
        age = time.time() - os.path.getmtime(GUARD_ACTIVE)
        if age > 1800:  # 30 minutes
            os.remove(GUARD_ACTIVE)
            sys.exit(0)
    except Exception:
        sys.exit(0)

    # === Find the plan file for the block message ===
    plan_path = "unknown"
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
            plan_path = plan_files[0]
            with open(plan_path, "r") as f:
                plan_content = f.read()
            step_count = len(re.findall(r"^###?\s+Step", plan_content, re.MULTILINE))
            file_count = len(re.findall(r"\*\*File[s]?:\*\*", plan_content))
            complex_keywords = [
                "architecture", "refactor", "migrate", "multi-file",
                "database", "schema", "security", "performance",
                "integration", "concurrent", "parallel",
            ]
            if sum(1 for kw in complex_keywords if kw in plan_content.lower()) >= 3:
                complexity = "HIGH"
            if step_count >= 8 or file_count >= 5:
                complexity = "HIGH"
    except Exception:
        pass

    # === BLOCK — guard is active ===

    # Write Sonnet to settings.json — takes effect on next turn if Claude Code
    # re-reads between turns, otherwise user needs /model sonnet manually
    settings_path = os.path.expanduser("~/.claude/settings.json")
    try:
        with open(settings_path, "r") as f:
            settings = json.load(f)
        if "opus" in settings.get("model", "").lower():
            settings["model"] = "claude-sonnet-4-6"
            with open(settings_path, "w") as f:
                json.dump(settings, f, indent=2)
                f.write("\n")
    except Exception:
        pass

    # Remove guard — one-shot block. Next turn (hopefully Sonnet) proceeds freely.
    try:
        os.remove(GUARD_ACTIVE)
    except Exception:
        pass

    result = {
        "decision": "block",
        "reason": (
            f"PLAN EXECUTION BLOCKED — switching to Sonnet for execution.\n"
            f"Plan: {plan_path} | {complexity} | {step_count} steps | {file_count} files\n\n"
            "settings.json updated to claude-sonnet-4-6. Guard removed.\n\n"
            "Tell the user EXACTLY: 'Type go to execute the plan with Sonnet.'\n\n"
            "If the model did NOT switch automatically on the next turn, tell the user:\n"
            "'Run /model sonnet first, then type go.'\n\n"
            f"NEXT AGENT: Read and execute {plan_path} step by step. "
            "Do NOT rewrite it. Do NOT overwrite it. Just follow it."
        ),
    }
    print(json.dumps(result))
    sys.exit(2)


if __name__ == "__main__":
    main()
