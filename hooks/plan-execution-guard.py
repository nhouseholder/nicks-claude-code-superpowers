#!/usr/bin/env python3
"""
Plan Execution Guard — Blocks plan execution until model switches to Sonnet.

Fires on PreToolUse:Bash|Edit|Write. When a plan-switch-pending marker
exists (set by plan-mode-enforcer.py), this hook:
1. Allows writes to ~/.claude/plans/ (still writing the plan)
2. Blocks all other tool calls with a model-switch instruction
3. Writes claude-sonnet-4-6 to settings.json
4. Deletes the marker file

This ensures no plan execution happens on Opus after plan approval.
The user sends one follow-up message and Sonnet handles execution.

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

    # Allow writes to plan files (still in plan mode)
    if tool_name in ("Write", "Edit"):
        file_path = tool_input.get("file_path", "") or tool_input.get("path", "")
        if file_path and PLAN_DIR in file_path:
            sys.exit(0)

    # Allow TodoWrite — just task tracking, not execution
    if tool_name in ("TodoWrite",):
        sys.exit(0)

    # === BLOCK EXECUTION — Switch model first ===

    # Assess plan complexity
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
            step_count = len(re.findall(r"^###\s+Step", plan_content, re.MULTILINE))
            file_count = len(re.findall(r"\*\*File:\*\*", plan_content))
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

    # Switch model in settings.json
    try:
        with open(SETTINGS_PATH, "r") as f:
            settings = json.load(f)
        old_model = settings.get("model", "unknown")
        settings["model"] = "claude-sonnet-4-6"
        with open(SETTINGS_PATH, "w") as f:
            json.dump(settings, f, indent=2)
            f.write("\n")
    except Exception:
        old_model = "unknown"

    # Delete marker — one-shot guard
    try:
        os.remove(MARKER_FILE)
    except Exception:
        pass

    # Block with instructions
    result = {
        "decision": "block",
        "reason": (
            f"AUTO-MODEL-SWITCH: Opus → Sonnet 4.6 | Complexity: {complexity} | "
            f"Steps: {step_count} | Files: {file_count}\n\n"
            "Plan approved but execution blocked — model must switch to Sonnet first.\n"
            "settings.json has been updated to claude-sonnet-4-6.\n\n"
            "Tell the user: 'Model switched to Sonnet 4.6 for plan execution "
            f"({complexity} reasoning). Send any message to begin.'\n\n"
            "Do NOT attempt to execute the plan in this turn. STOP your response "
            "after informing the user. Sonnet will handle execution on the next turn."
        ),
    }
    print(json.dumps(result))
    sys.exit(2)


if __name__ == "__main__":
    main()
