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
    """Move abs_path into <project-root>/.plans/ with topic-based name + symlink.

    Naming format: <YYYY-MM-DD>_<HHMM>_<topic-slug>.md
      - topic-slug extracted from plan's first H1 heading
      - falls back to harness slug (filename) if no heading found
      - HHMM disambiguates same-day plans without numeric suffixes

    Also writes <project-root>/.plans/ACTIVE_PLAN pointer to this real path
    so downstream hooks can resolve THE plan deterministically (not by mtime).
    """
    # Already a symlink? Nothing to do — second Edit writes through the link.
    if os.path.islink(abs_path):
        return

    if not os.path.isfile(abs_path):
        return

    root = plan_utils.project_root()
    scoped_dir = plan_utils.ensure_project_plans_dir(root)

    # Defensive: skip if already inside the project's .plans/
    if os.path.realpath(abs_path).startswith(os.path.realpath(scoped_dir) + os.sep):
        return

    # Read plan content to derive topic slug
    try:
        with open(abs_path, "r") as handle:
            plan_content = handle.read()
    except Exception:
        plan_content = ""

    harness_slug = os.path.basename(abs_path).replace(".md", "")
    topic = plan_utils.extract_topic_slug(plan_content, fallback=harness_slug)

    now = datetime.datetime.now()
    date_prefix = now.strftime("%Y-%m-%d")
    time_prefix = now.strftime("%H%M")
    dest_name = f"{date_prefix}_{time_prefix}_{topic}.md"
    dest = os.path.join(scoped_dir, dest_name)

    # Collision (same minute, same topic) — append numeric suffix
    suffix = 1
    while os.path.exists(dest):
        dest = os.path.join(scoped_dir, f"{date_prefix}_{time_prefix}_{topic}_{suffix}.md")
        suffix += 1

    try:
        shutil.move(abs_path, dest)
    except Exception:
        return

    try:
        os.symlink(dest, abs_path)
    except Exception:
        # Symlink failed — move file back so harness can still find it
        try:
            shutil.move(dest, abs_path)
        except Exception:
            pass
        return

    # Mark as ACTIVE_PLAN — single source of truth for `go` resolution
    try:
        plan_utils.set_active_plan(dest)
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
