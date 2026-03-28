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
    "src/lib/version.ts",
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
    """Check if any version file was modified in working tree, staged, or latest commit."""
    diff = run("git diff --name-only HEAD", cwd=cwd)
    staged = run("git diff --cached --name-only", cwd=cwd)
    committed = run("git diff --name-only HEAD~1..HEAD", cwd=cwd)
    all_changed = (diff + "\n" + staged + "\n" + committed).strip()

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

    # BLOCK: Deploying from /tmp/ or worktree directories
    if "/tmp/" in cwd or "/.claude/worktrees/" in cwd:
        result = {
            "decision": "block",
            "reason": (
                f"WRONG DIRECTORY: Deploying from {cwd} which is a temp/worktree directory. "
                f"Deploy from the canonical project directory under ~/Projects/. "
                f"Deploying from /tmp/ or worktrees has caused version reversions."
            ),
        }
        print(json.dumps(result))
        sys.exit(2)

    # BLOCK: Version looks suspiciously old
    for vf in VERSION_FILES:
        vpath = os.path.join(cwd, vf)
        if os.path.exists(vpath):
            try:
                with open(vpath, "r") as f:
                    content = f.read()
                # Check for very old version patterns (v10.x when we expect v11+)
                import re as re_mod
                ver_match = re_mod.search(r'["\']?v?(\d+)\.\d+', content)
                if ver_match:
                    major = int(ver_match.group(1))
                    if major < 10 and "ufc" in cwd.lower():
                        result = {
                            "decision": "block",
                            "reason": (
                                f"STALE VERSION: {vf} shows major version {major} which looks old. "
                                f"You may be in the wrong directory. Check version against production."
                            ),
                        }
                        print(json.dumps(result))
                        sys.exit(2)
            except Exception:
                pass
            break

    # Only enforce version bump for website projects
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
