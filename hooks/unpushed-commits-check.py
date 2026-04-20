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

    # Resolve the ref to compare against:
    # Priority 1: origin/<current-branch> if it exists
    # Priority 2: configured @{u} upstream
    # Priority 3: origin/main or origin/master
    compare_ref = None

    if current_branch:
        branch_remote = f"origin/{current_branch}"
        check = subprocess.run(
            ["git", "rev-parse", "--verify", branch_remote],
            capture_output=True, text=True, timeout=3, cwd=cwd
        )
        if check.returncode == 0:
            compare_ref = branch_remote

    if compare_ref is None:
        # Try configured upstream
        upstream_result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "@{u}"],
            capture_output=True, text=True, timeout=3, cwd=cwd
        )
        if upstream_result.returncode == 0 and upstream_result.stdout.strip():
            compare_ref = upstream_result.stdout.strip()

    if compare_ref is None:
        # Fall back to origin/main or origin/master
        for ref in ("origin/main", "origin/master"):
            check = subprocess.run(
                ["git", "rev-parse", "--verify", ref],
                capture_output=True, text=True, timeout=3, cwd=cwd
            )
            if check.returncode == 0:
                compare_ref = ref
                break

    if compare_ref is None:
        sys.exit(0)

    # Check for unpushed commits vs resolved ref
    result = subprocess.run(
        ["git", "log", "--oneline", f"{compare_ref}..HEAD"],
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
        # Also check for uncommitted changes — BLOCK, not just notify
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True, text=True, timeout=5, cwd=cwd
        )
        changes = result.stdout.strip()
        if changes:
            file_count = len(changes.splitlines())
            changed_files = changes.splitlines()
            staged = [l for l in changed_files if not l.startswith("??")]
            unstaged = [l for l in changed_files if l.startswith("??") or l[0] in (" ", "M", "A", "D", "R")]
            print(json.dumps({
                "decision": "block",
                "reason": (
                    f"UNCOMMITTED CHANGES ({file_count} files): GitHub is the source of truth. "
                    f"Commit and push before ending this session.\n"
                    f"Staged: {len(staged)} | Unstaged/untracked: {len(unstaged)}\n\n"
                    f"Run: git add -A && git commit -m 'message' && git push origin $(git branch --show-current)"
                )
            }))

except Exception:
    pass

sys.exit(0)
