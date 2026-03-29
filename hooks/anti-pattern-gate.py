#!/usr/bin/env python3
"""
Anti-Pattern Gate — PreToolUse hook for Edit/Write
Checks if the content being written contains patterns that match known anti-patterns.

Fires on Edit and Write tool calls. Scans the new content for red-flag patterns
extracted from anti-patterns.md. If a match is found, blocks the edit with a warning.

This is the mechanical enforcement layer — Claude can't "forget" to check.
"""
import json
import os
import re
import sys

# Red-flag patterns extracted from anti-patterns.md
# These are specific code patterns or practices that have caused bugs
# Format: (pattern_regex, anti_pattern_id, message)
STATIC_GATES = [
    # Nullish coalescing on odds — FREE_PICK_NULL_ML_BYPASS
    (r'(?:pick_ml|odds|_ml)\s*\?\?\s*0', 'FREE_PICK_NULL_ML_BYPASS',
     'NEVER use ?? 0 for odds comparison. Null odds ≠ 0. Use explicit null check.'),

    # SUB without DEC fallback — SUB_DEC_NOT_IN_PICKS_ARRAY
    (r'method_pred.*==.*["\']SUB["\'](?!.*DEC)', 'SUB_DEC_NOT_IN_PICKS_ARRAY',
     'SUB method prediction detected — ensure SUB→DEC fallback is applied in ALL output paths.'),

    # parlay.legs with .fighter — PARLAY_LEGS_STRING_VS_OBJECT
    (r'\.legs\.map\(.*\.fighter', 'PARLAY_LEGS_STRING_VS_OBJECT',
     'Parlay legs can be strings OR objects. Handle both: typeof l === "string" ? l : l.fighter'),

    # Overwriting ANTHROPIC_BASE_URL — NEVER modify ANTHROPIC_BASE_URL
    (r'ANTHROPIC_BASE_URL', 'NEVER_MODIFY_ANTHROPIC_BASE_URL',
     'NEVER modify ANTHROPIC_BASE_URL in settings.json unless explicitly asked.'),

    # setdefault for override — SETDEFAULT_DOESNT_OVERRIDE
    (r'\.setdefault\(', 'SETDEFAULT_DOESNT_OVERRIDE',
     'setdefault() does NOT override existing keys. Use direct assignment if you need to override.'),

    # Deploying from root webapp — UFC_WRONG_DIRECTORY_DEPLOY
    (r'wrangler.*pages.*deploy.*(?:webapp/dist|webapp/build)(?!.*frontend)', 'UFC_WRONG_DIRECTORY_DEPLOY',
     'WRONG DIRECTORY — deploy from ufc-predict/webapp/frontend/, not root webapp/. Check version.js first.'),
]

def check_static_gates(content, file_path):
    """Check content against static red-flag patterns."""
    violations = []
    for pattern, ap_id, message in STATIC_GATES:
        if re.search(pattern, content, re.IGNORECASE):
            violations.append((ap_id, message))
    return violations

def main():
    try:
        hook_input = json.loads(sys.stdin.read())
    except:
        sys.exit(0)

    tool_input = hook_input.get('tool_input', {})

    # Get content being written
    content = ''
    file_path = ''

    if 'content' in tool_input:
        content = tool_input['content']
        file_path = tool_input.get('file_path', '')
    elif 'new_string' in tool_input:
        content = tool_input['new_string']
        file_path = tool_input.get('file_path', '')

    if not content:
        sys.exit(0)

    violations = check_static_gates(content, file_path)

    if violations:
        messages = []
        for ap_id, message in violations:
            messages.append(f"⚠️ [{ap_id}] {message}")

        warning = "ANTI-PATTERN GATE — Known bad pattern detected:\n" + "\n".join(messages)
        warning += "\n\nCheck ~/.claude/anti-patterns.md for full context before proceeding."

        # Output as additionalContext (warning, not blocking)
        result = {"additionalContext": warning}
        print(json.dumps(result))

if __name__ == '__main__':
    main()
