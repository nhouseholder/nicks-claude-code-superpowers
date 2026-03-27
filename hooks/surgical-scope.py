#!/usr/bin/env python3
"""PostToolUse hook: Warn when edits happen outside expected project scope.

Rule #27: Surgical scope — only touch what you were asked to touch.
- WARNING on sensitive file edits (admin, firebase, workflows)
- BLOCK on stub file creation (empty components replacing real ones)

Exit code 0 = allow with warning. Exit code 2 = block.
"""
import json
import os
import sys

# Files that should almost never be edited during routine work
SENSITIVE_PATTERNS = [
    "/admin",
    "/AdminPanel",
    "/AdminDashboard",
    "/AdminBacktest",
    "/AdminAlgorithm",
    "firebase.json",
    "firebaseConfig",
    ".github/workflows/",
    "wrangler.toml",
    "wrangler.json",
    ".env",
    "credentials",
    "serviceAccount",
]

# Stub patterns — empty components that replace real ones
STUB_SIGNALS = [
    "placeholder",
    "TODO: implement",
    "coming soon",
    "stub",
    "export default function",  # only if file is very short
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

    # Check for sensitive file edits
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

    # Check for stub file creation — Write tool with very short content
    # replacing an existing file (tool_name would be Write)
    tool_name = hook_input.get("tool_name", "")
    content = tool_input.get("content", "")

    if tool_name == "Write" and content:
        lines = content.strip().split("\n")
        is_jsx_or_tsx = file_path.endswith((".jsx", ".tsx", ".vue", ".svelte"))

        # Short component file replacing what was likely a real component
        if is_jsx_or_tsx and len(lines) < 15:
            content_lower = content.lower()
            for signal in STUB_SIGNALS:
                if signal in content_lower:
                    result = {
                        "decision": "block",
                        "reason": (
                            f"STUB COMPONENT BLOCKED: Writing a {len(lines)}-line file to "
                            f"{os.path.basename(file_path)} with '{signal}'. "
                            f"This looks like a stub replacing a real component. "
                            f"Rule #27: Never create empty stubs during focused backend tasks. "
                            f"If this component needs rebuilding, do it properly — not a placeholder."
                        ),
                    }
                    print(json.dumps(result))
                    sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()
