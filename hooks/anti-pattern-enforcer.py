#!/usr/bin/env python3
"""
Anti-Pattern Enforcer — SessionStart hook
Injects the most relevant anti-patterns into context based on the current project.

Instead of hoping Claude reads anti-patterns.md, this hook mechanically injects
the relevant entries every session. Can't be forgotten. Can't be skipped.

Strategy:
1. Detect current project from CWD
2. Extract all anti-pattern IDs + "Applies when" + "Flawed assumption" lines
3. Filter to entries relevant to this project
4. Inject a compact summary into the session context
"""
import json
import os
import re
import sys

def get_project_from_cwd(cwd):
    """Map CWD to project keywords for filtering."""
    cwd_lower = cwd.lower()
    project_map = {
        'mmalogic': ['ufc', 'mma', 'backtest', 'registry', 'parlay', 'method', 'round', 'combo', 'picks', 'bout'],
        'ufc-predict': ['ufc', 'mma', 'backtest', 'registry', 'parlay', 'method', 'round', 'combo', 'picks', 'bout'],
        'diamondpredictions': ['diamond', 'mlb', 'nhl', 'nba', 'betting', 'grading'],
        'diamond-predictions': ['diamond', 'mlb', 'nhl', 'nba', 'betting', 'grading'],
        'courtside': ['courtside', 'nba', 'ncaa', 'basketball', 'betting', 'admin'],
        'mystrainai': ['strain', 'cannabis', 'ai'],
        'enhancedhealthai': ['health', 'ai', 'wellness'],
        'enhanced-health-ai': ['health', 'ai', 'wellness'],
        'nestwisehq': ['nestwise', 'financial', 'planning'],
        'dad-financial': ['nestwise', 'financial', 'planning'],
        'researcharia': ['research', 'aria'],
        'aria-research': ['research', 'aria'],
        'superpowers': ['skill', 'hook', 'command', 'settings', 'memory'],
    }

    for key, keywords in project_map.items():
        if key in cwd_lower:
            return keywords

    # Universal keywords that apply everywhere
    return ['deploy', 'cloudflare', 'git', 'icloud', 'directory', 'settings']

def parse_anti_patterns(filepath):
    """Parse anti-patterns.md into structured entries."""
    if not os.path.exists(filepath):
        return []

    with open(filepath, 'r') as f:
        content = f.read()

    entries = []
    # Match entry headers: ### ID — DATE
    pattern = r'### (.+?)\s*—\s*(\d{4}-\d{2}-\d{2})'
    matches = list(re.finditer(pattern, content))

    for i, match in enumerate(matches):
        entry_id = match.group(1).strip()
        date = match.group(2)
        start = match.end()
        end = matches[i+1].start() if i+1 < len(matches) else len(content)
        body = content[start:end].strip()

        # Extract key fields
        applies = ''
        assumption = ''
        fix = ''

        applies_match = re.search(r'\*\*Applies when\*\*:\s*(.+?)(?:\n|$)', body)
        if applies_match:
            applies = applies_match.group(1).strip()

        assumption_match = re.search(r'\*\*Flawed assumption\*\*:\s*(.+?)(?:\n|$)', body)
        if assumption_match:
            assumption = assumption_match.group(1).strip()

        reasoning_match = re.search(r'\*\*Reasoning lesson\*\*:\s*(.+?)(?:\n|$)', body)
        if reasoning_match:
            fix = reasoning_match.group(1).strip()

        # Build searchable text from the full body
        searchable = (entry_id + ' ' + body).lower()

        entries.append({
            'id': entry_id,
            'date': date,
            'applies': applies,
            'assumption': assumption,
            'lesson': fix,
            'searchable': searchable,
        })

    return entries

def filter_entries(entries, project_keywords):
    """Filter entries relevant to current project + universal entries."""
    universal_keywords = ['deploy', 'cloudflare', 'git', 'icloud', 'directory',
                          'settings', 'never', 'always', 'integration', 'overwrite',
                          'destroy', 'session', 'argue']

    all_keywords = set(project_keywords + universal_keywords)

    relevant = []
    for entry in entries:
        score = 0
        for kw in all_keywords:
            if kw in entry['searchable']:
                score += 1
        if score >= 1:
            entry['relevance'] = score
            relevant.append(entry)

    # Sort by relevance (desc) then date (desc)
    relevant.sort(key=lambda e: (-e['relevance'], e['date']), reverse=False)

    return relevant

def format_output(entries, max_entries=25):
    """Format as compact injection for session context."""
    if not entries:
        return ""

    lines = [
        "ANTI-PATTERN ENFORCEMENT — These known failures apply to this project.",
        "Violating any of these is a CRITICAL error. Read before writing code.",
        ""
    ]

    for entry in entries[:max_entries]:
        line = f"  [{entry['id']}]"
        if entry['applies']:
            line += f" WHEN: {entry['applies'][:120]}"
        if entry['assumption']:
            line += f" | TRAP: {entry['assumption'][:100]}"
        elif entry['lesson']:
            line += f" | LESSON: {entry['lesson'][:100]}"
        lines.append(line)

    if len(entries) > max_entries:
        lines.append(f"  ... +{len(entries) - max_entries} more in ~/.claude/anti-patterns.md")

    lines.append("")
    lines.append("Full details: cat ~/.claude/anti-patterns.md | grep -A 10 'PATTERN_ID'")

    return '\n'.join(lines)

def main():
    # Read hook input
    try:
        hook_input = json.loads(sys.stdin.read())
    except:
        hook_input = {}

    cwd = hook_input.get('cwd', os.getcwd())
    ap_file = os.path.expanduser('~/.claude/anti-patterns.md')

    entries = parse_anti_patterns(ap_file)
    if not entries:
        sys.exit(0)

    project_keywords = get_project_from_cwd(cwd)
    relevant = filter_entries(entries, project_keywords)

    if not relevant:
        sys.exit(0)

    output = format_output(relevant)

    if output:
        result = {
            "additionalContext": output
        }
        print(json.dumps(result))

if __name__ == '__main__':
    main()
