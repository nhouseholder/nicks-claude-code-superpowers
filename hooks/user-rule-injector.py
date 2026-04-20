#!/usr/bin/env python3
"""UserPromptSubmit hook: Inject user rules into context before every turn.

Reads ~/.claude/user-rules.md and project-scoped user_rules.md, then
injects them as context so the orchestrator ALWAYS has rules available —
even after compaction, context switches, or long sessions.

This is the mechanical enforcement layer that prevents rules from being
forgotten when context pressure builds up.

Exit code 0 always (informational context injection).
"""
import json
import os
import sys
from pathlib import Path

GLOBAL_RULES = os.path.expanduser("~/.claude/user-rules.md")


def read_rules(path):
    """Read rules file, return content or None."""
    try:
        with open(path, "r") as f:
            content = f.read().strip()
        return content if content else None
    except (FileNotFoundError, PermissionError):
        return None


def find_project_rules(cwd):
    """Walk up from cwd to find project-scoped user_rules.md."""
    # Check standard project memory paths
    candidates = [
        os.path.join(cwd, ".claude", "memory", "user_rules.md"),
        os.path.join(cwd, ".claude", "projects", "memory", "user_rules.md"),
    ]
    for c in candidates:
        content = read_rules(c)
        if content:
            return c, content

    # Walk up to find project root with .claude/memory/user_rules.md
    current = cwd
    for _ in range(10):  # max 10 levels up
        parent = os.path.dirname(current)
        if parent == current:
            break
        candidate = os.path.join(parent, ".claude", "memory", "user_rules.md")
        content = read_rules(candidate)
        if content:
            return candidate, content
        current = parent

    return None, None


def main():
    try:
        hook_input = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        sys.exit(0)

    user_message = hook_input.get("user_message", "") or hook_input.get("prompt", "")
    if not user_message:
        sys.exit(0)

    rules_parts = []

    # Global rules (always loaded)
    global_content = read_rules(GLOBAL_RULES)
    if global_content:
        rules_parts.append(("Global Rules", global_content))

    # Project-scoped rules
    proj_path, proj_content = find_project_rules(os.getcwd())
    if proj_content:
        rules_parts.append(("Project Rules", proj_content))

    if not rules_parts:
        sys.exit(0)

    # Build context injection
    context_lines = [
        "⚠️ USER RULES — HARD CONSTRAINTS (enforced mechanically, not by memory):",
        "Violating any rule below is a bug. Check these BEFORE acting.",
        ""
    ]

    for label, content in rules_parts:
        context_lines.append(f"## {label}")
        # Extract just the rule lines (skip headers, keep bullets)
        for line in content.splitlines():
            stripped = line.strip()
            if stripped.startswith("- ") or stripped.startswith("* "):
                context_lines.append(stripped)
        context_lines.append("")

    context_lines.append(
        "ENFORCEMENT: Before any action, check if a rule applies. "
        "If an action would violate a rule, STOP and tell the user. "
        "After any change, commit and push to GitHub — no exceptions."
    )

    print(json.dumps({
        "decision": "allow",
        "context": "\n".join(context_lines)
    }))

    sys.exit(0)


if __name__ == "__main__":
    main()
