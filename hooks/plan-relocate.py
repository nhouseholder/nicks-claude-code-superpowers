#!/usr/bin/env python3
"""
Plan Relocate — Move harness-written plan files into the owning project.

Fires on PostToolUse:Write|Edit. When Claude writes to ~/.claude/plans/<slug>.md
(the harness-mandated path), this hook:

  1. Computes the owning project root (git toplevel containing cwd, else cwd).
  2. Moves the real file to <project-root>/.plans/<YYYY-MM-DD>_<slug>.md.
  3. Replaces the original path with a symlink pointing to the real file so
     the harness's "plan file exists at ~/.claude/plans/<slug>.md" path still
     resolves for subsequent Edit/Read operations.

Idempotent: if the path is already a symlink or already lives under a project
.plans/ dir, the hook is a no-op. Safe to run on Edit events (second write
just updates the real file through the symlink).

Why: plans used to pile up in the global ~/.claude/plans/ directory. Multiple
parallel projects produced latest-mtime collisions where the execution guard
pointed at the wrong project's plan. Keeping the real file inside the project
tree binds the plan to its owning project and makes `find-project-plans`
authoritative.

Exit code 0 always (PostToolUse can't block).
"""
from __future__ import annotations

import datetime
import json
import os
import shutil
import sys

# Make sibling _plan_utils importable
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
try:
    import _plan_utils as plan_utils  # noqa: E402
except Exception:
    sys.exit(0)

PLAN_DIR_ABS = os.path.abspath(plan_utils.PLAN_DIR)


def relocate(abs_path: str) -> None:
    """Move abs_path into <project-root>/.plans/ and replace with symlink."""
    # Already a symlink? Nothing to do — the underlying real file was written
    # through the link. Idempotent re-entry on second Edit.
    if os.path.islink(abs_path):
        return

    # File must exist as a real regular file to relocate it
    if not os.path.isfile(abs_path):
        return

    root = plan_utils.project_root()
    scoped_dir = plan_utils.ensure_project_plans_dir(root)

    # If we're already inside a project tree (shouldn't be the case for
    # ~/.claude/plans/ writes, but be defensive), skip.
    if os.path.realpath(abs_path).startswith(os.path.realpath(scoped_dir) + os.sep):
        return

    slug = os.path.basename(abs_path)
    date_prefix = datetime.date.today().isoformat()  # YYYY-MM-DD
    dest_name = f"{date_prefix}_{slug}"
    dest = os.path.join(scoped_dir, dest_name)

    # Collision — append a numeric suffix. Preserves any concurrent plan.
    suffix = 1
    while os.path.exists(dest):
        dest = os.path.join(scoped_dir, f"{date_prefix}_{suffix}_{slug}")
        suffix += 1

    try:
        shutil.move(abs_path, dest)
    except Exception:
        return

    try:
        os.symlink(dest, abs_path)
    except Exception:
        # Symlink failed — move the file back so harness can still find it
        try:
            shutil.move(dest, abs_path)
        except Exception:
            pass


def main() -> None:
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

    try:
        abs_path = os.path.abspath(os.path.expanduser(file_path))
    except Exception:
        sys.exit(0)

    # Only act on writes inside ~/.claude/plans/
    if not abs_path.startswith(PLAN_DIR_ABS + os.sep):
        sys.exit(0)

    # Only act on plan-looking filenames (*.md). Skip hidden sidecars etc.
    if not abs_path.endswith(".md"):
        sys.exit(0)

    try:
        relocate(abs_path)
    except Exception:
        pass

    sys.exit(0)


if __name__ == "__main__":
    main()
