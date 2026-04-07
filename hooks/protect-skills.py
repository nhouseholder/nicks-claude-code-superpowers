#!/usr/bin/env python3
"""PreToolUse hook: Block modifications to protected aitmpl.com skills.

These 10 skills were installed from AI Templates and are READ-ONLY.
Claude may READ their SKILL.md but must NEVER edit, replace, or overwrite them.

Exit code 2 = block. Exit code 0 = allow.
"""
import json
import sys

PROTECTED_SKILLS = {
    "frontend-design",
    "code-reviewer",
    "senior-frontend",
    "skill-creator",
    "ui-ux-pro-max",
    "webapp-testing",
    "brainstorming",
    "canvas-design",
    "react-best-practices",
    "ui-design-system",
}


def main():
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        sys.exit(0)

    tool_input = hook_input.get("tool_input", {})

    # Check Write tool
    file_path = tool_input.get("file_path", "") or tool_input.get("path", "")
    if not file_path:
        sys.exit(0)

    # Check if the path targets a protected skill
    for skill in PROTECTED_SKILLS:
        if f"/skills/{skill}/" in file_path or f"/skills/{skill}\\" in file_path:
            result = {
                "decision": "block",
                "reason": (
                    f"PROTECTED SKILL: '{skill}' is a read-only aitmpl.com skill. "
                    f"Do NOT modify it. If it needs updating, tell the user to "
                    f"reinstall from https://www.aitmpl.com/my-components"
                ),
            }
            print(json.dumps(result))
            sys.exit(2)

    sys.exit(0)


if __name__ == "__main__":
    main()
