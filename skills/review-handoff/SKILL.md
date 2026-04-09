---
name: review-handoff
description: Read the most recent handoff for this project and orient yourself. The FIRST thing you do when starting a new session.
---

Read the latest handoff and orient. FIRST thing at session start.

Triggers: "review handoff", "pick up where we left off", "read handoff", "session start", "continue from last session"

**READ-ONLY. Do NOT write a new handoff. Do NOT invoke /full-handoff.**

---

## STEP 1: Find Latest Handoff

```bash
PROJECT_PATH=$(pwd)
PROJECT_NAME=$(basename "$PROJECT_PATH")
GITHUB_REPO=$(git remote get-url origin 2>/dev/null | sed 's|.*/||;s|\.git$||')
[ -z "$GITHUB_REPO" ] && GITHUB_REPO="$PROJECT_NAME"

# Primary: project's own handoffs/ directory
LATEST=$(ls -t "$PROJECT_PATH/handoffs"/handoff_*.md 2>/dev/null | head -1)

# Fallback: superpowers repo (transition period — old handoffs stored there)
if [ -z "$LATEST" ]; then
  LATEST=$(ls -t ~/ProjectsHQ/superpowers/handoffs/handoff_${GITHUB_REPO}_*.md 2>/dev/null | head -1)
fi

echo "Project: $PROJECT_NAME | Repo: $GITHUB_REPO"
echo "Latest handoff: ${LATEST:-NONE FOUND}"
```

If no handoff found: "No previous handoff. First session for this project." Then skip to Step 3.

## STEP 2: Read It Fully

Read the ENTIRE handoff. Pay special attention to:
- **In Progress / Blocked** — where to pick up
- **Next Steps** — priority list
- **Warnings** — do not repeat these mistakes

## STEP 3: Gate Check

### GATE 1: Local Matches Remote
```bash
git fetch origin --quiet 2>/dev/null
LOCAL_SHA=$(git rev-parse HEAD 2>/dev/null)
REMOTE_SHA=$(git rev-parse origin/main 2>/dev/null || git rev-parse origin/master 2>/dev/null)
echo "Local:  $LOCAL_SHA"
echo "Remote: $REMOTE_SHA"
if [ "$LOCAL_SHA" != "$REMOTE_SHA" ]; then
  echo "STALE — pulling..."
  git pull
fi
echo "Last commit: $(git log -1 --format='%ci %s' 2>/dev/null)"
```

### GATE 2: Read Context
Read (if they exist): project CLAUDE.md, ~/.claude/anti-patterns.md

## STEP 4: Present Summary

```
SESSION ORIENTED
================
Project: [name] ([repo])
Path: [canonical local path]
Branch: [branch] | Last commit: [date] [message]
Local = Remote: [yes/no]

PREVIOUS SESSION ([date]):
  [1-2 sentence summary from handoff]

PICKUP: [In Progress content, or "All tasks completed"]
BLOCKED: [Blocked content, or "Nothing blocked"]

NEXT STEPS:
  1. [from handoff]
  2. [from handoff]
  3. [from handoff]

WARNINGS: [from handoff, or "None"]

Ready to work. What would you like to tackle?
```

---

## Rules
1. READ-ONLY — never write a handoff.
2. Read the WHOLE handoff. Do not skim.
3. If Gate 1 fails (stale), pull before presenting summary.
4. If unfinished work exists (In Progress), offer to continue it.
