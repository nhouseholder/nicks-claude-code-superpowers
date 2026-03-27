#!/usr/bin/env python3
"""PreToolUse hook: Block deploys if version wasn't bumped.

Checks git diff for changes to version files before allowing
wrangler deploy or git push to main.

Exit code 2 = block. Exit code 0 = allow.
"""
import json
import os
import re
import subprocess
import sys


VERSION_FILES = [
    "version.js",
    "src/version.js",
    "package.json",
    "VERSION",
]


def run(cmd, cwd=None):
    try:
        result = subprocess.run(
            cmd, shell=True, capture_output=True, text=True, timeout=10, cwd=cwd
        )
        return result.stdout.strip()
    except Exception:
        return ""


def is_deploy_or_push(command):
    if re.search(r'wrangler(?:@[\d.]+)?\s+deploy', command):
        return True
    if re.search(r'git\s+push\s+.*(?:main|master)', command):
        return True
    return False


def version_was_bumped(cwd):
    """Check if any version file was modified in the current git diff."""
    diff = run("git diff --name-only HEAD", cwd=cwd)
    staged = run("git diff --cached --name-only", cwd=cwd)
    all_changed = (diff + "\n" + staged).strip()

    for vf in VERSION_FILES:
        if vf in all_changed:
            return True

    return False


def is_website_project(cwd):
    """Check if this looks like a website project (has public/ or dist/)."""
    return (
        os.path.exists(os.path.join(cwd, "public"))
        or os.path.exists(os.path.join(cwd, "dist"))
        or os.path.exists(os.path.join(cwd, "wrangler.toml"))
        or os.path.exists(os.path.join(cwd, "wrangler.json"))
    )


def main():
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        sys.exit(0)

    tool_input = hook_input.get("tool_input", {})
    command = tool_input.get("command", "")

    if not command or not is_deploy_or_push(command):
        sys.exit(0)

    cwd = os.getcwd()

    # Only enforce for website projects
    if not is_website_project(cwd):
        sys.exit(0)

    if not version_was_bumped(cwd):
        result = {
            "decision": "block",
            "reason": (
                "VERSION NOT BUMPED: No version file was modified in the current diff. "
                "Update version.js, package.json, or VERSION before deploying. "
                "Every deploy must have a version bump."
            ),
        }
        print(json.dumps(result))
        sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()
