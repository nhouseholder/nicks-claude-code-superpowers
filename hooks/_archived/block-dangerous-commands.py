#!/usr/bin/env python3
"""PreToolUse hook: Block dangerous shell commands before Claude executes them.

Reads hook input JSON from stdin, checks the Bash command against a blocklist
of dangerous patterns. Exit code 2 = block the command. Exit code 0 = allow.
"""
import json
import re
import sys

# Patterns that should NEVER execute without explicit user request
BLOCKED_PATTERNS = [
    # Filesystem destruction — only block truly destructive root/home targets
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

    # Cloudflare deploy without safety (handled by deploy-guard.py but double-check)
    (r'wrangler\s+deploy\s+--force', "forced wrangler deploy (bypasses safety)"),

    # Directory rename kills active sessions (2026-03-26 incident — 7 sessions lost)
    (r'mv\s+.*(?:Projects|ProjectsHQ|Mobile\s+Documents)', "renaming project directory kills active Claude sessions"),
    (r'mv\s+.*~/Projects\b', "renaming ~/Projects kills active Claude sessions"),
]

def strip_quoted_content(command: str) -> str:
    """Remove content inside heredocs, double quotes, and single quotes.

    This prevents false positives when dangerous patterns appear in
    commit messages, echo strings, or other quoted contexts.
    """
    # Remove heredoc blocks: <<'EOF' ... EOF  or <<EOF ... EOF
    result = re.sub(r"<<'?(\w+)'?.*?\n.*?\1", "", command, flags=re.DOTALL)
    # Remove double-quoted strings (non-greedy, handling escaped quotes)
    result = re.sub(r'"(?:[^"\\]|\\.)*"', '""', result)
    # Remove single-quoted strings (no escaping in single quotes)
    result = re.sub(r"'[^']*'", "''", result)
    return result

def check_command(command: str) -> tuple[bool, str]:
    """Returns (is_blocked, reason)."""
    # Strip quoted content so patterns in commit messages, echo, etc. don't trigger
    stripped = strip_quoted_content(command)
    for pattern, reason in BLOCKED_PATTERNS:
        if re.search(pattern, stripped, re.IGNORECASE):
            return True, reason
    return False, ""

def main():
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        sys.exit(0)  # Can't parse = allow (don't block on hook errors)

    tool_input = hook_input.get("tool_input", {})
    command = tool_input.get("command", "")

    if not command:
        sys.exit(0)

    blocked, reason = check_command(command)
    if blocked:
        # Exit code 2 = block the tool call
        result = {
            "decision": "block",
            "reason": f"BLOCKED: {reason}. Command: {command[:100]}..."
        }
        print(json.dumps(result))
        sys.exit(2)

    sys.exit(0)

if __name__ == "__main__":
    main()
