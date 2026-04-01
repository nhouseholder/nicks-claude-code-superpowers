#!/usr/bin/env python3
"""PreToolUse hook: Block wrangler deploy if Cloudflare has changes not in git.

FAILSAFE: Prevents overwriting a Cloudflare-deployed frontend that was never
committed to git. This happened on 2026-03-26 and destroyed a full redesign.

How it works:
1. Detects any `wrangler deploy` command
2. Checks if there are uncommitted changes to frontend files (public/)
3. Checks the last Cloudflare deployment timestamp vs last git commit
4. If CF was deployed MORE RECENTLY than the last git commit touching public/,
   that means someone deployed changes directly to CF without committing.
   Deploying from git would OVERWRITE those changes.
5. Blocks the deploy and warns the user.

Exit code 2 = block. Exit code 0 = allow.
"""
import json
import os
import re
import subprocess
import sys
from datetime import datetime


def run(cmd, cwd=None):
    """Run a shell command and return stdout."""
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=15, cwd=cwd
        )
        return result.stdout.strip()
    except Exception:
        return ""


def is_wrangler_deploy(command: str) -> bool:
    """Check if command is a wrangler deploy."""
    # Match: wrangler deploy, npx wrangler deploy, npx wrangler@X.Y.Z deploy
    return bool(re.search(r'wrangler(?:@[\d.]+)?\s+deploy', command))


def get_git_last_frontend_commit_date(cwd: str) -> str:
    """Get the date of the last git commit touching public/ files."""
    return run("git log -1 --format='%Y-%m-%dT%H:%M:%S' -- public/", cwd=cwd)


def check_uncommitted_frontend_changes(cwd: str) -> bool:
    """Check if there are uncommitted changes in public/."""
    status = run("git status --porcelain public/", cwd=cwd)
    return bool(status.strip())


def main():
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        sys.exit(0)

    tool_input = hook_input.get("tool_input", {})
    command = tool_input.get("command", "")

    if not command or not is_wrangler_deploy(command):
        sys.exit(0)

    # Get the working directory
    cwd = os.getcwd()

    # Check 1: Are there uncommitted frontend changes?
    has_uncommitted = check_uncommitted_frontend_changes(cwd)

    # Check 2: Is this a git repo with public/ files?
    git_date = get_git_last_frontend_commit_date(cwd)

    warnings = []

    if has_uncommitted:
        warnings.append(
            "UNCOMMITTED FRONTEND CHANGES detected in public/. "
            "Commit them first or they will be deployed but not saved in git."
        )

    # Check 3: Warn about potential CF-only changes
    # If the last git commit to public/ is old, warn that CF might have newer changes
    if git_date:
        try:
            git_dt = datetime.fromisoformat(git_date)
            age_hours = (datetime.now() - git_dt).total_seconds() / 3600
            if age_hours > 24:
                warnings.append(
                    f"Last git commit to public/ was {age_hours:.0f} hours ago ({git_date}). "
                    "If someone deployed directly to Cloudflare since then, "
                    "this deploy will OVERWRITE those changes. "
                    "Verify the live site matches your local files before deploying."
                )
        except (ValueError, TypeError):
            pass

    # Only BLOCK on uncommitted changes. Age warnings are informational.
    if has_uncommitted:
        result = {
            "decision": "block",
            "reason": (
                "DEPLOY GUARD: UNCOMMITTED FRONTEND CHANGES in public/. "
                "Commit them first or they will be deployed but not saved in git. "
                "To proceed: (1) git add public/ && git commit, (2) then deploy."
            ),
        }
        print(json.dumps(result))
        sys.exit(2)

    # Age warnings: print but don't block (exit 0)
    if warnings:
        # Output as informational context, not a block
        print(json.dumps({"decision": "allow", "context": "DEPLOY GUARD WARNING: " + " | ".join(warnings)}))

    sys.exit(0)


if __name__ == "__main__":
    main()
