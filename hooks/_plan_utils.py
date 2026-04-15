"""
Shared utilities for plan-hook pipeline.

Imported by:
  - plan-execution-guard.py
  - plan-mode-enforcer.py
  - plan-relocate.py
  - plan-write-guard-activator.py

Responsibilities:
  - Discover the current project root (git toplevel, else cwd).
  - List plan files scoped to the current project.
  - Resolve harness-visible symlinks in ~/.claude/plans/ to real paths.
  - Clean stale plans within project scope only (never cross-project).

Design rules (non-negotiable):
  - NEVER delete plan files outside the current project's .plans/.
  - NEVER rely on latest-mtime across the global plan dir — it crosses projects.
  - Legacy un-relocated plans in ~/.claude/plans/ are visible ONLY as fallback
    when the current cwd owns the active guard (cwd match).
"""
from __future__ import annotations

import glob
import os
import subprocess
import time

PLAN_DIR = os.path.expanduser("~/.claude/plans")
GUARD_ACTIVE = os.path.expanduser("~/.claude/.plan-guard-active")
STALE_SECONDS = 7200  # 2 hours


def git_toplevel(start: str | None = None) -> str | None:
    """Return the git repo root containing `start` (default cwd), or None."""
    try:
        result = subprocess.run(
            ["git", "rev-parse", "--show-toplevel"],
            cwd=start or os.getcwd(),
            capture_output=True,
            text=True,
            timeout=2,
        )
        if result.returncode == 0:
            top = result.stdout.strip()
            if top:
                return top
    except Exception:
        pass
    return None


def project_root(cwd: str | None = None) -> str:
    """Resolve the active project root — git toplevel, else cwd."""
    cwd = cwd or os.getcwd()
    return git_toplevel(cwd) or cwd


def project_plans_dir(root: str | None = None) -> str:
    """Return <project-root>/.plans/ path (does NOT create)."""
    return os.path.join(root or project_root(), ".plans")


def ensure_project_plans_dir(root: str | None = None) -> str:
    """Create and return <project-root>/.plans/."""
    path = project_plans_dir(root)
    os.makedirs(path, exist_ok=True)
    return path


def read_guard() -> tuple[str, str]:
    """Parse the guard sidecar into (cwd, real_plan_path).

    Guard file format (line-separated, backward compatible):
      line 1: cwd (or literal 'active' for legacy)
      line 2: real plan path (optional, added 2026-04)
    """
    try:
        with open(GUARD_ACTIVE, "r") as handle:
            lines = [ln.strip() for ln in handle.read().splitlines()]
    except Exception:
        return ("", "")
    cwd = lines[0] if lines else ""
    real = lines[1] if len(lines) > 1 else ""
    return (cwd, real)


def guard_matches_cwd(cwd: str | None = None) -> bool:
    """True iff the guard belongs to the current cwd's project."""
    cwd = cwd or os.getcwd()
    guard_cwd, _ = read_guard()
    if not guard_cwd or guard_cwd == "active":
        # Legacy guards (no cwd stored) — treat as matching to avoid breakage.
        return True
    return guard_cwd == cwd


def find_project_plans(cwd: str | None = None) -> list[str]:
    """Return plan files relevant to the current project, mtime-desc sorted.

    Discovery order:
      1. Real files in <project-root>/.plans/*.md
      2. Symlinks in ~/.claude/plans/*.md whose realpath points into project
      3. Legacy un-relocated plans in ~/.claude/plans/*.md — ONLY if the
         active guard's cwd matches current cwd (prevents cross-project bleed)
    """
    cwd = cwd or os.getcwd()
    root = project_root(cwd)
    plans: list[str] = []

    # 1. Project-scoped real files
    scoped_dir = project_plans_dir(root)
    if os.path.isdir(scoped_dir):
        plans.extend(glob.glob(os.path.join(scoped_dir, "*.md")))

    # 2 + 3. Files in ~/.claude/plans/
    seen = {os.path.realpath(p) for p in plans}
    guard_owns_cwd = guard_matches_cwd(cwd)
    for legacy in glob.glob(os.path.join(PLAN_DIR, "*.md")):
        real = os.path.realpath(legacy)
        if real in seen:
            continue
        if real != legacy:
            # Symlink — include only if it resolves inside this project
            if real.startswith(root + os.sep):
                plans.append(real)
                seen.add(real)
            continue
        # Un-relocated legacy plan — fallback only when guard owns this cwd
        if guard_owns_cwd:
            plans.append(legacy)
            seen.add(real)

    # Sort by mtime, newest first
    plans.sort(key=lambda p: os.path.getmtime(p) if os.path.exists(p) else 0, reverse=True)
    return plans


def clean_stale_project_plans(cwd: str | None = None, max_age: int = STALE_SECONDS) -> None:
    """Delete stale plans ONLY within the current project's .plans/.

    Never touches plans belonging to other projects. Legacy un-relocated
    plans in ~/.claude/plans/ are cleaned only when this cwd's guard owns
    them (same ownership rule as discovery).
    """
    now = time.time()
    cwd = cwd or os.getcwd()
    root = project_root(cwd)

    # Scoped .plans/ directory
    scoped_dir = project_plans_dir(root)
    if os.path.isdir(scoped_dir):
        for plan in glob.glob(os.path.join(scoped_dir, "*.md")):
            try:
                if now - os.path.getmtime(plan) > max_age:
                    os.remove(plan)
                    # Also clean dangling symlink in ~/.claude/plans/
                    _remove_dangling_symlinks_to(plan)
            except Exception:
                pass

    # Legacy un-relocated — only if guard owns cwd
    if guard_matches_cwd(cwd):
        for legacy in glob.glob(os.path.join(PLAN_DIR, "*.md")):
            try:
                real = os.path.realpath(legacy)
                if real != legacy:
                    # Symlink into some project. Clean if dangling OR stale + in this project
                    if not os.path.exists(real):
                        os.remove(legacy)
                    continue
                if now - os.path.getmtime(legacy) > max_age:
                    os.remove(legacy)
            except Exception:
                pass


def _remove_dangling_symlinks_to(target: str) -> None:
    """Remove symlinks in ~/.claude/plans/ that point to `target`."""
    try:
        for link in glob.glob(os.path.join(PLAN_DIR, "*.md")):
            if os.path.islink(link) and os.readlink(link) == target:
                try:
                    os.remove(link)
                except Exception:
                    pass
    except Exception:
        pass


def resolve_harness_path(path: str) -> str:
    """Resolve ~/.claude/plans/<slug>.md symlink to real project path.

    Returns the input path unchanged if it's already real or can't be resolved.
    """
    try:
        return os.path.realpath(path)
    except Exception:
        return path


# === ACTIVE_PLAN pointer — single source of truth ===

ACTIVE_PLAN_NAME = "ACTIVE_PLAN"


def active_plan_pointer_path(root: str | None = None) -> str:
    """Return absolute path to the project's ACTIVE_PLAN pointer file."""
    return os.path.join(project_plans_dir(root), ACTIVE_PLAN_NAME)


def get_active_plan(cwd: str | None = None) -> str:
    """Read the ACTIVE_PLAN pointer. Returns absolute plan path or '' if none.

    The pointer file contains a single line with the absolute real path of
    the currently-approved plan. If the file is missing, empty, or points to
    a non-existent file, returns ''.
    """
    cwd = cwd or os.getcwd()
    pointer = active_plan_pointer_path(project_root(cwd))
    try:
        if not os.path.isfile(pointer):
            return ""
        with open(pointer, "r") as handle:
            target = handle.read().strip()
        if target and os.path.isfile(target):
            return target
    except Exception:
        pass
    return ""


def set_active_plan(plan_path: str, cwd: str | None = None) -> None:
    """Write the ACTIVE_PLAN pointer to plan_path (absolute real path)."""
    cwd = cwd or os.getcwd()
    try:
        ensure_project_plans_dir(project_root(cwd))
        pointer = active_plan_pointer_path(project_root(cwd))
        with open(pointer, "w") as handle:
            handle.write(os.path.realpath(plan_path))
    except Exception:
        pass


def clear_active_plan(cwd: str | None = None) -> None:
    """Remove the ACTIVE_PLAN pointer (idempotent — no-op if missing)."""
    cwd = cwd or os.getcwd()
    try:
        pointer = active_plan_pointer_path(project_root(cwd))
        if os.path.isfile(pointer):
            os.remove(pointer)
    except Exception:
        pass


# === Topic extraction for human-readable filenames ===

import re as _re  # local import to keep top-of-file imports unchanged


def extract_topic_slug(plan_content: str, fallback: str = "plan") -> str:
    """Extract a kebab-case topic slug from a plan's first H1 heading.

    Examples:
      '# Plan: Project-Scoped Files'  -> 'project-scoped-files'
      '# Bulletproof Pipeline'        -> 'bulletproof-pipeline'
      ''                              -> fallback

    Strips leading 'Plan:' / 'Plan -' prefix. Lowercases. Replaces spaces
    and non-word chars with hyphens. Caps at 50 chars.
    """
    if not plan_content:
        return fallback
    for line in plan_content.splitlines():
        line = line.strip()
        if line.startswith("# ") and not line.startswith("## "):
            heading = line[2:].strip()
            heading = _re.sub(r"^plan\s*[:\-]\s*", "", heading, flags=_re.IGNORECASE)
            heading = heading.lower()
            heading = _re.sub(r"[^a-z0-9]+", "-", heading).strip("-")
            heading = heading[:50].strip("-")
            if heading:
                return heading
            break
    return fallback
