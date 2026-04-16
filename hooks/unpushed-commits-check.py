#!/usr/bin/env python3
"""Stop hook: Warn if there are unpushed commits.

GitHub is the source of truth. iCloud corrupts git repos. Every commit
must be pushed before a session ends. This hook checks for unpushed
commits and warns the agent to push them.

Exit code 0 always.
"""
import json
import sys
import os
import subprocess

try:
    hook_input = json.load(sys.stdin)
except (json.JSONDecodeError, EOFError):
    sys.exit(0)

if hook_input.get("hook_event_name") != "Stop":
    sys.exit(0)
if hook_input.get("stop_hook_active"):
    sys.exit(0)

cwd = os.getcwd()

try:
    # Check if we're in a git repo
    result = subprocess.run(
        ["git", "rev-parse", "--is-inside-work-tree"],
        capture_output=True, text=True, timeout=3, cwd=cwd
    )
    if result.returncode != 0:
        sys.exit(0)

    # Fetch to compare (quick, quiet)
    subprocess.run(
        ["git", "fetch", "origin", "--quiet"],
        capture_output=True, text=True, timeout=10, cwd=cwd
    )

    # Get current branch
    branch_result = subprocess.run(
        ["git", "branch", "--show-current"],
        capture_output=True, text=True, timeout=3, cwd=cwd
    )
    current_branch = branch_result.stdout.strip()

    # Get upstream tracking ref
    upstream_result = subprocess.run(
        ["git", "rev-parse", "--abbrev-ref", "@{u}"],
        capture_output=True, text=True, timeout=3, cwd=cwd
    )
    upstream = upstream_result.stdout.strip()  # e.g. "origin/main" or "origin/claude/bold-spence"

    # If upstream is origin/main but we're not on main, the worktree branch
    # has no dedicated tracking ref — check against the branch's own remote ref instead.
    if upstream in ("origin/main", "origin/master") and current_branch not in ("main", "master"):
        remote_branch_ref = f"origin/{current_branch}"
        check_ref = subprocess.run(
            ["git", "rev-parse", "--verify", remote_branch_ref],
            capture_output=True, text=True, timeout=3, cwd=cwd
        )
        if check_ref.returncode == 0:
            upstream = remote_branch_ref
        else:
            # Branch not pushed at all — fall back to main comparison
            pass

    # Check for unpushed commits vs the resolved upstream
    result = subprocess.run(
        ["git", "log", "--oneline", f"{upstream}..HEAD"],
        capture_output=True, text=True, timeout=5, cwd=cwd
    )

    unpushed = result.stdout.strip()
    if unpushed and result.returncode == 0:
        count = len(unpushed.splitlines())
        print(json.dumps({
            "decision": "block",
            "reason": (
                f"UNPUSHED COMMITS ({count}): GitHub is the source of truth. "
                f"iCloud corrupts git repos. Push before ending this session.\n"
                f"Unpushed:\n{unpushed}\n\n"
                f"Run: git push origin $(git branch --show-current)"
            )
        }))
    else:
        # Also check for uncommitted changes
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True, text=True, timeout=5, cwd=cwd
        )
        changes = result.stdout.strip()
        if changes:
            file_count = len(changes.splitlines())
            print(json.dumps({
                "systemMessage": (
                    f"Note: {file_count} uncommitted changes in working directory. "
                    f"Consider committing and pushing before ending session."
                )
            }))

except Exception:
    pass

sys.exit(0)
