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
    # Clean stale plan files (> 2 hours old)
    try:
        for pf in glob.glob(os.path.join(PLAN_DIR, "*.md")):
            if time.time() - os.path.getmtime(pf) > 7200:
                os.remove(pf)
    except Exception:
        pass

    # Fast exit: no guard active
    if not os.path.exists(GUARD_ACTIVE):
        sys.exit(0)

    # Check if guard belongs to current project
    try:
        with open(GUARD_ACTIVE, "r") as f:
            guard_project = f.read().strip()
        if guard_project and guard_project != "active" and guard_project != os.getcwd():
            # Guard is for a different project — clean up and allow
            os.remove(GUARD_ACTIVE)
            sys.exit(0)
    except Exception:
        pass

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

    # Check if user already switched to Sonnet (e.g. via Desktop dropdown)
    settings_path = os.path.expanduser("~/.claude/settings.json")
    try:
        with open(settings_path, "r") as f:
            settings = json.load(f)
        model = settings.get("model", "").lower()
        if model and "opus" not in model:
            # Already on Sonnet — remove guard and allow through
            try:
                os.remove(GUARD_ACTIVE)
            except Exception:
                pass
            sys.exit(0)
        # Still on Opus — switch to Sonnet in settings.json
        if "opus" in model:
            settings["model"] = "claude-sonnet-4-6"
            with open(settings_path, "w") as f:
                json.dump(settings, f, indent=2)
                f.write("\n")
    except Exception:
        pass

    # DO NOT remove guard here — it must persist until the GO signal in
    # plan-mode-enforcer.py properly removes it after model switch.
    # Removing on first block was a bug: Opus would get blocked once,
    # then proceed freely on the next Edit/Write attempt.

    result = {
        "decision": "block",
        "reason": (
            f"PLAN EXECUTION BLOCKED — You are still in Opus mode.\n"
            f"Plan: {plan_path} | {complexity} | {step_count} steps | {file_count} files\n\n"
            "settings.json updated to claude-sonnet-4-6.\n\n"
            "Tell the user EXACTLY:\n"
            "'Switch to Sonnet before executing:\n"
            "  - Desktop app: Click the model selector dropdown → pick Sonnet\n"
            "  - CLI: Run /model sonnet\n"
            "Then type: go'\n\n"
            "Do NOT attempt to execute the plan. Do NOT call Edit or Write. "
            "Output ONLY the switch instructions above and stop."
        ),
    }
    print(json.dumps(result))
    sys.exit(2)


if __name__ == "__main__":
    main()
