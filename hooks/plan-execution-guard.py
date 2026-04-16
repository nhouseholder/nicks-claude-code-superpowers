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

# Shared plan-utils
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    import _plan_utils as plan_utils
except Exception:
    plan_utils = None

PLAN_DIR = os.path.expanduser("~/.claude/plans")
GUARD_ACTIVE = os.path.expanduser("~/.claude/.plan-guard-active")




def main():
    # Clean stale plan files — SCOPED TO CURRENT PROJECT ONLY.
    # Global cleanup is the #1 source of cross-project data loss.
    if plan_utils is not None:
        try:
            plan_utils.clean_stale_project_plans()
        except Exception:
            pass

    # Fast exit: no guard active.
    # Two activation paths:
    #   1. GUARD_ACTIVE file (set by ExitPlanMode handler — the normal path)
    #   2. Fresh ACTIVE_PLAN pointer (set by plan-relocate.py on any plan write,
    #      even when ExitPlanMode is never called because the session isn't in
    #      plan mode). Without this fallback, Claude can write a plan and
    #      immediately execute in the same turn — bypassing the Sonnet handoff.
    _guard_from_active_plan = False
    if not os.path.exists(GUARD_ACTIVE):
        if plan_utils is not None:
            try:
                _ptr = plan_utils.active_plan_pointer_path()
                if os.path.isfile(_ptr) and (time.time() - os.path.getmtime(_ptr)) <= 1800:
                    _guard_from_active_plan = plan_utils.get_active_plan() != ""
            except Exception:
                pass
        if not _guard_from_active_plan:
            sys.exit(0)

    # Check if guard belongs to current project (GUARD_ACTIVE path only —
    # ACTIVE_PLAN is already project-scoped via git_toplevel).
    if not _guard_from_active_plan:
        try:
            guard_cwd, _guard_real = (
                plan_utils.read_guard() if plan_utils is not None else ("", "")
            )
            if guard_cwd and guard_cwd != "active" and guard_cwd != os.getcwd():
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
    # Skip for ACTIVE_PLAN path (age already verified above).
    if not _guard_from_active_plan:
        try:
            age = time.time() - os.path.getmtime(GUARD_ACTIVE)
            if age > 1800:  # 30 minutes
                os.remove(GUARD_ACTIVE)
                sys.exit(0)
        except Exception:
            sys.exit(0)

    # === Find the plan file for the block message ===
    # PROJECT-SCOPED discovery — see _plan_utils.find_project_plans.
    # Falls back to raw PLAN_DIR glob only if the helper import failed.
    plan_path = "unknown"
    complexity = "MEDIUM"
    step_count = 0
    file_count = 0
    try:
        if plan_utils is not None:
            plan_files = plan_utils.find_project_plans()
        else:
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

    # Guard is active. Block unconditionally.
    # DO NOT check model here — settings.json may not reflect the actual
    # running model (Desktop app can override Sonnet → Opus silently).
    # The guard is ONLY removed by:
    #   1. The explicit GO handler in plan-mode-enforcer.py (correct pathway)
    #   2. 30-minute expiry (checked above)
    # Checking model and removing the guard on "Sonnet" was the bug:
    # settings.json permanently says sonnet, so the guard was instantly
    # removed on the first Edit/Write, letting Opus execute freely.

    result = {
        "decision": "block",
        "reason": (
            f"PLAN EXECUTION BLOCKED — plan pending approval.\n"
            f"Plan: {plan_path} | {complexity} | {step_count} steps | {file_count} files\n\n"
            "Tell the user EXACTLY:\n"
            "'A plan is ready and waiting for your approval.\n"
            "  1. Switch to Sonnet if not already (Desktop: model dropdown; CLI: /model sonnet)\n"
            "  2. Type: go\n"
            "Do NOT attempt to execute the plan. Do NOT call Edit or Write. "
            "Output ONLY the instructions above and stop.'",
        ),
    }
    print(json.dumps(result))
    sys.exit(2)


if __name__ == "__main__":
    main()
