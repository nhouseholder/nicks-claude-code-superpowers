#!/usr/bin/env python3
"""
Plan Write Guard Activator — Creates the cwd-scoped plan guard file when
Opus writes a plan file to ~/.claude/plans/ via the Write/Edit tool.

Fires on PostToolUse:Write|Edit. If the tool's file_path is inside PLAN_DIR,
writes ~/.claude/.plan-guard-active with the current cwd as content. The
existing plan-execution-guard.py (PreToolUse:Edit|Write) then blocks
subsequent non-plan-file Edit/Write calls until:
  - the user types "go" (plan-mode-enforcer.py removes the guard), OR
  - 30 minutes elapse (auto-expiry in plan-execution-guard.py).

Complements plan-mode-enforcer.py's PreToolUse:ExitPlanMode branch:
  - Formal plan mode (Shift+Tab → ExitPlanMode tool call): guard created
    by plan-mode-enforcer.py (existing).
  - Informal "make a plan" prose (no plan mode): guard created HERE after
    the plan file is actually written.

Both paths produce identical guard files. Only "go" or 30-min expiry removes.

Design constraints (from anti-patterns.md → PLAN_AUTO_SWITCH_IMPOSSIBLE):
  - Must store cwd in guard content (project-scoped, no cross-project bleed).
  - Must never read settings.json or attempt to detect the running model.
  - Must never block (PostToolUse can't block anyway — exit 0 always).
  - Must fire only for writes INSIDE PLAN_DIR to avoid false-activating
    on unrelated writes to ~/.claude/memory/, anti-patterns.md, etc.

Exit code 0 always.
"""
import json
import os
import sys

PLAN_DIR = os.path.expanduser("~/.claude/plans")
GUARD_ACTIVE = os.path.expanduser("~/.claude/.plan-guard-active")

try:
    data = json.load(sys.stdin)
except Exception:
    sys.exit(0)

tool_name = data.get("tool_name", "")
if tool_name not in ("Write", "Edit"):
    sys.exit(0)

tool_input = data.get("tool_input", {}) or {}
file_path = tool_input.get("file_path", "") or tool_input.get("path", "")

if not file_path:
    sys.exit(0)

# Normalize to absolute path
try:
    abs_path = os.path.abspath(os.path.expanduser(file_path))
except Exception:
    sys.exit(0)

# Only act on writes INSIDE PLAN_DIR
plan_dir_abs = os.path.abspath(PLAN_DIR)
if not abs_path.startswith(plan_dir_abs + os.sep):
    sys.exit(0)

# Write the cwd-scoped guard. Overwrites any existing guard safely.
# Two-line format (line 1 = cwd, line 2 = real plan path). The real path
# resolves symlinks created by plan-relocate.py so downstream hooks can
# verify the exact plan file being guarded, independent of the harness
# symlink in ~/.claude/plans/.
try:
    real_path = os.path.realpath(abs_path)
    with open(GUARD_ACTIVE, "w") as f:
        f.write(os.getcwd())
        f.write("\n")
        f.write(real_path)
except Exception:
    pass

sys.exit(0)
