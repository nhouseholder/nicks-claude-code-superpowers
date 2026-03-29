Search project memory and observation history for context from previous sessions. Use when you need to find what was done, decided, or encountered before.

Triggers: "recall", "what did we do with", "when did we", "search memory", "find in history", "do you remember"

---

## How to Search

You have three search layers. Use them in order — start cheap, go deeper only if needed.

### Layer 1: Memory Files (fastest, most curated)
```bash
# Search current project memory
MEMORY_PATH="$HOME/.claude/projects/$(pwd | sed 's|/|-|g; s|^-||')/memory"
grep -r -i -l "$SEARCH_TERM" "$MEMORY_PATH"/ 2>/dev/null

# Search global memory
grep -r -i -l "$SEARCH_TERM" "$HOME/.claude/memory/" 2>/dev/null

# Search ALL project memories (cross-project)
grep -r -i -l "$SEARCH_TERM" "$HOME/.claude/projects/"/*/memory/ 2>/dev/null
```
Read any matching files fully — these are curated, high-signal memories.

### Layer 2: Observation History (richer, noisier)
```bash
# Search current project observations
PROJECT_HASH=$(python3 -c "
import json, hashlib, subprocess, os
try:
    r = subprocess.run(['git','remote','get-url','origin'], capture_output=True, text=True, timeout=2)
    if r.returncode == 0:
        print(hashlib.sha256(r.stdout.strip().encode()).hexdigest()[:12])
except: pass
")

if [ -n "$PROJECT_HASH" ]; then
    OBS_FILE="$HOME/.claude/homunculus/projects/$PROJECT_HASH/observations.jsonl"
else
    OBS_FILE="$HOME/.claude/homunculus/observations.jsonl"
fi

# Search observations by keyword
grep -i "$SEARCH_TERM" "$OBS_FILE" 2>/dev/null | python3 -c "
import sys, json
for line in sys.stdin:
    try:
        o = json.loads(line)
        print(f\"[{o['ts'][:10]}] {o.get('summary', 'no summary')}\")
    except: pass
" | tail -30
```

### Layer 3: Cross-Project Observation Search
```bash
# Search ALL project observations
for obs in $HOME/.claude/homunculus/projects/*/observations.jsonl $HOME/.claude/homunculus/observations.jsonl; do
    if [ -f "$obs" ]; then
        MATCHES=$(grep -i -c "$SEARCH_TERM" "$obs" 2>/dev/null)
        if [ "$MATCHES" -gt 0 ]; then
            # Look up project name
            HASH=$(basename $(dirname "$obs"))
            NAME=$(python3 -c "
import json
try:
    r = json.load(open('$HOME/.claude/homunculus/projects.json'))
    print(r.get('$HASH', {}).get('name', '$HASH'))
except: print('$HASH')
")
            echo "=== $NAME ($MATCHES matches) ==="
            grep -i "$SEARCH_TERM" "$obs" | python3 -c "
import sys, json
for line in sys.stdin:
    try:
        o = json.loads(line)
        print(f\"  [{o['ts'][:10]}] {o.get('summary', '')}\")
    except: pass
" | tail -10
        fi
    fi
done
```

### Layer 4: Handoff History
```bash
# Search all handoffs
grep -r -i -l "$SEARCH_TERM" $HOME/.claude/projects/*/memory/handoff_*.md 2>/dev/null
```

## Output Format

Present results as:
```
RECALL: "$SEARCH_TERM"
========================
MEMORY FILES: [N matches]
  - [filename] — [1-line summary of what it says]

OBSERVATIONS: [N matches]
  [date] — [summary]
  [date] — [summary]

HANDOFFS: [N matches]
  - [filename] — [relevant section]

Source: [which layer(s) searched]
```

## Rules
1. Always search Layer 1 first. Only go to Layer 2+ if Layer 1 has no results.
2. Show the user what you found — don't just say "I found it."
3. If nothing found across all layers: say so honestly. Don't fabricate.
4. Cross-project search (Layer 3) only when the user asks about something not in the current project.
