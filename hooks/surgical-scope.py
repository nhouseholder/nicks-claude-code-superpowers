#!/usr/bin/env python3
"""PostToolUse hook: Warn when edits happen outside expected project scope.

Rule #27: Surgical scope — only touch what you were asked to touch.
This is a WARNING, not a block — too many legitimate cross-file edits
to block safely. But the warning makes the agent aware.

Exit code 0 always (informational only).
"""
import json
import os
import sys

# Files that should almost never be edited during routine work
SENSITIVE_PATTERNS = [
    "/admin",
    "/AdminPanel",
    "/AdminDashboard",
    "firebase.json",
    "firebaseConfig",
    ".github/workflows/",
    "wrangler.toml",
    "wrangler.json",
    ".env",
    "credentials",
    "serviceAccount",
]


def main():
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        sys.exit(0)

    tool_input = hook_input.get("tool_input", {})
    file_path = tool_input.get("file_path", "") or tool_input.get("path", "")

    if not file_path:
        sys.exit(0)

    for pattern in SENSITIVE_PATTERNS:
        if pattern.lower() in file_path.lower():
            print(json.dumps({
                "decision": "allow",
                "context": (
                    f"SCOPE WARNING: Editing sensitive file matching '{pattern}': {os.path.basename(file_path)}. "
                    f"Rule #27: Only touch files directly related to your task. "
                    f"If this edit wasn't explicitly requested, STOP and ask the user."
                )
            }))
            sys.exit(0)

    sys.exit(0)


if __name__ == "__main__":
    main()
