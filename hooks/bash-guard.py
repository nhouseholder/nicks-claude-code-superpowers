#!/usr/bin/env python3
"""PreToolUse hook: Unified Bash safety guard.

Combines three former hooks into one subprocess:
  - block-dangerous-commands.py — pattern blocklist for destructive commands
  - deploy-guard.py — block wrangler deploy with uncommitted frontend changes
  - version-bump-check.py — block deploy/push without version bump

Exit code 2 = block. Exit code 0 = allow.
"""
import json
import os
import re
import subprocess
import sys
from datetime import datetime


# === Dangerous command patterns ===

BLOCKED_PATTERNS = [
    # Filesystem destruction
    (r'rm\s+(-[a-zA-Z]*\s+)?/\s*$', "rm on filesystem root"),
    (r'rm\s+(-[a-zA-Z]*\s+)?/\*', "rm on root wildcard"),
    (r'rm\s+-[a-zA-Z]*rf\s+~\s*$', "rm -rf on home directory root"),
    (r'rm\s+-[a-zA-Z]*rf\s+~/\*', "rm -rf home wildcard"),
    (r'rm\s+-[a-zA-Z]*rf\s+\*', "rm -rf with wildcard"),
    (r'rm\s+-[a-zA-Z]*rf\s+\.(?!\.|/)', "rm -rf on current directory"),
    (r'>\s*/dev/sd[a-z]', "writing to raw disk device"),
    (r'mkfs\.', "formatting filesystem"),
    (r'dd\s+.*of=/dev/', "dd to raw device"),
    # Git destruction
    (r'git\s+push\s+.*--force\s+.*(?:main|master)', "force push to main/master"),
    (r'git\s+push\s+-f\s+.*(?:main|master)', "force push to main/master"),
    (r'git\s+reset\s+--hard\s+(?!HEAD\b)', "git reset --hard to non-HEAD ref"),
    (r'git\s+clean\s+-[a-zA-Z]*f[a-zA-Z]*d', "git clean -fd (deletes untracked files and dirs)"),
    (r'git\s+branch\s+-D\s+(?:main|master)', "delete main/master branch"),
    (r'git\s+checkout\s+--\s+\.', "git checkout -- . (discard all changes)"),
    # Remote code execution
    (r'curl\s+.*\|\s*(?:ba)?sh', "piping curl to shell"),
    (r'wget\s+.*\|\s*(?:ba)?sh', "piping wget to shell"),
    (r'curl\s+.*\|\s*python', "piping curl to python"),
    # System destruction
    (r'chmod\s+-R\s+777\s+/', "chmod 777 on root"),
    (r'chown\s+-R\s+.*\s+/', "chown on root"),
    (r'kill\s+-9\s+-1', "kill all user processes"),
    (r'killall\s+-9', "killall -9"),
    # Database destruction
    (r'DROP\s+DATABASE', "DROP DATABASE"),
    (r'DROP\s+TABLE(?!\s+IF\s+EXISTS)', "DROP TABLE without IF EXISTS"),
    (r'TRUNCATE\s+TABLE', "TRUNCATE TABLE"),
    # Credential exposure
    (r'cat\s+.*\.env\b.*\|\s*curl', "exfiltrating .env via curl"),
    (r'cat\s+.*id_rsa', "reading SSH private key"),
    (r'cat\s+.*\.pem\b', "reading PEM certificate/key"),
    # Cloudflare forced deploy
    (r'wrangler\s+deploy\s+--force', "forced wrangler deploy (bypasses safety)"),
    # Directory rename kills sessions
    (r'mv\s+.*(?:Projects|ProjectsHQ|Mobile\s+Documents)', "renaming project directory kills active Claude sessions"),
    (r'mv\s+.*~/Projects\b', "renaming ~/Projects kills active Claude sessions"),
]

VERSION_FILES = [
    "version.js", "src/version.js", "src/lib/version.ts",
    "package.json", "VERSION",
]


def strip_quoted_content(command: str) -> str:
    """Remove content inside heredocs, double quotes, and single quotes."""
    result = re.sub(r"<<'?(\w+)'?.*?\n.*?\1", "", command, flags=re.DOTALL)
    result = re.sub(r'"(?:[^"\\]|\\.)*"', '""', result)
    result = re.sub(r"'[^']*'", "''", result)
    return result


def run(cmd, cwd=None):
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=15, cwd=cwd
        )
        return result.stdout.strip()
    except Exception:
        return ""


def check_dangerous_patterns(command: str):
    """Check for blocked shell patterns. Returns (blocked, reason)."""
    stripped = strip_quoted_content(command)
    for pattern, reason in BLOCKED_PATTERNS:
        if re.search(pattern, stripped, re.IGNORECASE):
            return True, f"BLOCKED: {reason}. Command: {command[:100]}..."
    return False, ""


def check_deploy_guard(command: str, cwd: str):
    """Block wrangler deploy with uncommitted frontend changes."""
    if not re.search(r'wrangler(?:@[\d.]+)?\s+deploy', command):
        return False, ""

    # Check uncommitted frontend changes
    status = run("git status --porcelain public/", cwd=cwd)
    if status.strip():
        return True, (
            "DEPLOY GUARD: UNCOMMITTED FRONTEND CHANGES in public/. "
            "Commit them first or they will be deployed but not saved in git. "
            "To proceed: (1) git add public/ && git commit, (2) then deploy."
        )

    # Age warning (informational, not blocking)
    git_date = run("git log -1 --format='%Y-%m-%dT%H:%M:%S' -- public/", cwd=cwd)
    if git_date:
        try:
            git_dt = datetime.fromisoformat(git_date)
            age_hours = (datetime.now() - git_dt).total_seconds() / 3600
            if age_hours > 24:
                print(json.dumps({
                    "decision": "allow",
                    "context": (
                        f"DEPLOY GUARD WARNING: Last git commit to public/ was {age_hours:.0f}h ago. "
                        "Verify the live site matches your local files before deploying."
                    )
                }))
        except (ValueError, TypeError):
            pass

    return False, ""


def check_version_bump(command: str, cwd: str):
    """Block deploy/push without version bump for website projects."""
    is_deploy = re.search(r'wrangler(?:@[\d.]+)?\s+deploy', command)
    is_push = re.search(r'git\s+push\s+.*(?:main|master)', command)
    if not is_deploy and not is_push:
        return False, ""

    # Block deploys from /tmp/ or worktree dirs — but allow if the command
    # explicitly cd's to a canonical project path first (worktree→canonical push)
    if "/tmp/" in cwd or "/.claude/worktrees/" in cwd:
        # Check if command cd's to a canonical path before push/deploy
        canonical_cd = re.search(r'cd\s+~/(?:Projects|ProjectsHQ)/\w+', command)
        if not canonical_cd:
            return True, (
                f"WRONG DIRECTORY: Deploying from {cwd} which is a temp/worktree directory. "
                f"Deploy from the canonical project directory under ~/Projects/. "
                f"Hint: prefix with 'cd ~/ProjectsHQ/<project> && ' to push from canonical path."
            )

    # Check for suspiciously old version (UFC-specific)
    for vf in VERSION_FILES:
        vpath = os.path.join(cwd, vf)
        if os.path.exists(vpath):
            try:
                with open(vpath, "r") as f:
                    content = f.read()
                ver_match = re.search(r'["\']?v?(\d+)\.\d+', content)
                if ver_match:
                    major = int(ver_match.group(1))
                    if major < 10 and "ufc" in cwd.lower():
                        return True, (
                            f"STALE VERSION: {vf} shows major version {major} which looks old. "
                            f"You may be in the wrong directory."
                        )
            except Exception:
                pass
            break

    # Only enforce version bump for website projects
    is_website = (
        os.path.exists(os.path.join(cwd, "public"))
        or os.path.exists(os.path.join(cwd, "dist"))
        or os.path.exists(os.path.join(cwd, "wrangler.toml"))
        or os.path.exists(os.path.join(cwd, "wrangler.json"))
    )
    if not is_website:
        return False, ""

    # Check if version was bumped
    diff = run("git diff --name-only HEAD", cwd=cwd)
    staged = run("git diff --cached --name-only", cwd=cwd)
    committed = run("git diff --name-only HEAD~1..HEAD", cwd=cwd)
    all_changed = (diff + "\n" + staged + "\n" + committed).strip()

    for vf in VERSION_FILES:
        if vf in all_changed:
            return False, ""

    return True, (
        "VERSION NOT BUMPED: No version file was modified in the current diff. "
        "Update version.js, package.json, or VERSION before deploying."
    )


def check_fast_mode_backtest(command: str):
    """Block backtests running with FAST_MODE=1 — results are useless for evaluation."""
    # Detect backtest-like commands with FAST_MODE
    is_backtest = re.search(r'backtest|sweep|coefficient|param.*test', command, re.IGNORECASE)
    has_fast_mode = re.search(r'FAST_MODE\s*=\s*1', command)
    if is_backtest and has_fast_mode:
        return True, (
            "BLOCKED: FAST_MODE=1 on a backtest/sweep. Fast mode limits to ~21 events — "
            "results are meaningless for evaluation. Remove FAST_MODE=1 to run the full dataset."
        )
    return False, ""


def main():
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        sys.exit(0)

    command = hook_input.get("tool_input", {}).get("command", "")
    if not command:
        sys.exit(0)

    cwd = os.getcwd()

    # Check 1: Dangerous patterns (fastest — pure regex, no subprocess)
    blocked, reason = check_dangerous_patterns(command)
    if blocked:
        print(json.dumps({"decision": "block", "reason": reason}))
        sys.exit(2)

    # Check 2: Deploy guard (only fires on wrangler deploy)
    blocked, reason = check_deploy_guard(command, cwd)
    if blocked:
        print(json.dumps({"decision": "block", "reason": reason}))
        sys.exit(2)

    # Check 3: Version bump (only fires on deploy/push to main)
    blocked, reason = check_version_bump(command, cwd)
    if blocked:
        print(json.dumps({"decision": "block", "reason": reason}))
        sys.exit(2)

    # Check 4: FAST_MODE on backtests (useless results)
    blocked, reason = check_fast_mode_backtest(command)
    if blocked:
        print(json.dumps({"decision": "block", "reason": reason}))
        sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()
