#!/usr/bin/env python3
"""
Plan Exit Model Switch — Auto-switches to Sonnet 4.6 when a plan is approved.

Fires on PostToolUse:ExitPlanMode. When the user approves a plan:
1. Reads the most recent plan file to assess complexity
2. Modifies settings.json to switch model to claude-sonnet-4-6
3. Injects context telling Claude to STOP and let Sonnet handle execution

The model switch takes effect on the NEXT turn (not the current one),
so the hook instructs Claude to pause and let the user trigger execution.

Exit code 0 always. Writes to settings.json.
"""
import json
import glob
import os
import re
import sys

try:
    hook_input = json.load(sys.stdin)
except (json.JSONDecodeError, Exception):
    sys.exit(0)

tool_name = hook_input.get("tool_name", "")

# Only fire on ExitPlanMode
if tool_name != "ExitPlanMode":
    sys.exit(0)

# Check for approval — inspect all text fields for "approved"
tool_result = str(hook_input.get("tool_result", ""))
tool_output = str(hook_input.get("output", ""))
combined = (tool_result + tool_output).lower()

if "approved" not in combined and "start coding" not in combined:
    # Plan was likely rejected or still pending — don't switch
    sys.exit(0)


# === ASSESS PLAN COMPLEXITY ===
plan_dir = os.path.expanduser("~/.claude/plans")
complexity = "MEDIUM"
step_count = 0
file_count = 0

try:
    plan_files = sorted(
        glob.glob(os.path.join(plan_dir, "*.md")),
        key=os.path.getmtime,
        reverse=True,
    )
    if plan_files:
        with open(plan_files[0], "r") as f:
            plan_content = f.read()

        # Count steps (### Step N patterns)
        step_count = len(re.findall(r"^###\s+Step", plan_content, re.MULTILINE))

        # Count files to modify (**File:** patterns)
        file_count = len(re.findall(r"\*\*File:\*\*", plan_content))

        # Complex signals
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


# === SWITCH MODEL IN SETTINGS ===
settings_path = os.path.expanduser("~/.claude/settings.json")
old_model = "unknown"
switch_success = False

try:
    with open(settings_path, "r") as f:
        settings = json.load(f)

    old_model = settings.get("model", "unknown")

    # Only switch if currently on Opus (don't downgrade if already on Sonnet)
    if "opus" in old_model.lower():
        settings["model"] = "claude-sonnet-4-6"
        with open(settings_path, "w") as f:
            json.dump(settings, f, indent=2)
            f.write("\n")
        switch_success = True
    else:
        # Already on Sonnet or other — no switch needed
        switch_success = True
        old_model = settings.get("model", "unknown")
except Exception:
    pass


# === OUTPUT CONTEXT ===
if switch_success and "opus" in old_model.lower():
    context = (
        f"AUTO-MODEL-SWITCH: {old_model} → claude-sonnet-4-6 | "
        f"Complexity: {complexity} | Steps: {step_count} | Files: {file_count}\n\n"
        "MANDATORY: Do NOT execute the plan in this turn. The model switch takes effect "
        "on the next turn. Instead, tell the user:\n"
        f"'Model auto-switched to Sonnet 4.6 ({complexity} reasoning) for plan execution. "
        f"Send any message to begin.'\n\n"
        "When the user sends their next message, execute the plan mechanically — "
        "follow every step exactly as written. No re-interpretation, no shortcuts, "
        "no skipping verification steps."
    )
else:
    context = (
        f"Plan approved. Model is already {old_model}. "
        "Proceed with plan execution — follow every step exactly as written."
    )

print(json.dumps({
    "decision": "allow",
    "context": context,
}))

sys.exit(0)
