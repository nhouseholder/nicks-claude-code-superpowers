---
name: full-handoff
description: Generate a lean handoff document and store it in this project's repo. The LAST thing you do before ending a session.
---

Generate a lean handoff, commit it to this project's repo, and push. The LAST thing you do before ending a session.

Triggers: "full handoff", "prepare handoff", "session handoff", "wrap up", "end session"

---

## STEP 1: Detect Project

```bash
PROJECT_PATH=$(pwd)
PROJECT_NAME=$(basename "$PROJECT_PATH")
GITHUB_REPO=$(git remote get-url origin 2>/dev/null | sed 's|.*/||;s|\.git$||')
[ -z "$GITHUB_REPO" ] && GITHUB_REPO="$PROJECT_NAME"
HANDOFF_FILE="handoff_$(date +%Y-%m-%d_%H%M).md"
HANDOFF_DIR="$PROJECT_PATH/handoffs"
echo "Project: $PROJECT_NAME | Repo: $GITHUB_REPO | File: $HANDOFF_FILE"
echo "Directory: $(pwd) | Remote: $(git remote get-url origin 2>/dev/null || echo 'none')"
```

**CRITICAL: The handoff header MUST match the directory you are in. If pwd is `mmalogic/`, the handoff says mmalogic, not whatever you were discussing.**

## STEP 2: Gather Git Facts

```bash
echo "=== BRANCH ===" && git branch --show-current
echo "=== RECENT COMMITS ===" && git log --oneline --since="12 hours ago" 2>/dev/null
echo "=== DIFF STAT ===" && git diff --stat HEAD~10 2>/dev/null || echo "fewer than 10 commits"
echo "=== STATUS ===" && git status --short
echo "=== LAST COMMIT ===" && git log -1 --format="%H %s (%ci)"
git fetch origin --quiet 2>/dev/null
LOCAL_SHA=$(git rev-parse HEAD)
REMOTE_SHA=$(git rev-parse origin/main 2>/dev/null || git rev-parse origin/master 2>/dev/null)
echo "Local SHA:  $LOCAL_SHA"
echo "Remote SHA: $REMOTE_SHA"
```

## STEP 3: Push Unpushed Work

```bash
if [ "$LOCAL_SHA" != "$REMOTE_SHA" ]; then
  echo "UNPUSHED WORK — pushing now..."
  git push origin $(git branch --show-current)
fi
```

## STEP 4: Write the Handoff

Create `$HANDOFF_DIR/$HANDOFF_FILE` using the Write tool. Every section must have real content — no brackets, no placeholders, no "N/A" unless truly not applicable.

```markdown
# Handoff — [PROJECT_NAME] — [YYYY-MM-DD HH:MM]
**Repo:** nhouseholder/[REPO] | **Branch:** [branch] | **Last commit:** [SHA] [date]
**Local = Remote:** [yes/no]

---

## 1. Session Summary
[2-4 sentences. What the user wanted, what was accomplished, current state.]

## 2. What Changed
[Every completed task. Format: "- **Task**: files changed — outcome"]
[Include git diff --stat output from Step 2]

## 3. In Progress / Blocked
**In progress:** [Exactly where to pick up — files, line numbers, what remains. Or: "All tasks completed."]
**Blocked:** [External dependencies waiting on. Or: "Nothing blocked."]

## 4. Next Steps (Prioritized)
1. [Most important] — [why]
2. [Second] — [why]
3. [Third] — [why]

## 5. Warnings
[Failures from this session and their root causes — reference anti-pattern IDs if logged]
[Miscommunications or wrong assumptions]
[Data contradictions detected]
[If nothing: "Clean session — no warnings."]

## 6. For The Next Agent
Read first: (1) This handoff, (2) [project CLAUDE.md if exists], (3) ~/.claude/anti-patterns.md
**Canonical path:** [full local path]
```

**Verify before saving:** (1) project name in header matches pwd, (2) all 6 sections have real content, (3) git data is filled in.

## STEP 5: Store, Commit, Push

```bash
mkdir -p "$HANDOFF_DIR"
# Write the handoff file (done in Step 4)

# Archive: keep last 5, move older to _archived/
mkdir -p "$HANDOFF_DIR/_archived"
ls -t "$HANDOFF_DIR"/handoff_*.md 2>/dev/null | tail -n +6 | while read f; do
  mv "$f" "$HANDOFF_DIR/_archived/"
done

# Commit and push
git add "$HANDOFF_DIR/"
git commit -m "handoff: $(date +%Y-%m-%d) session — [1-line summary]

Co-Authored-By: Claude <noreply@anthropic.com>"
git push origin $(git branch --show-current)
```

## STEP 6: Output Summary

```
HANDOFF COMPLETE
================
File: handoffs/$HANDOFF_FILE
Project: $PROJECT_NAME ($GITHUB_REPO)
Last commit: [SHA] [date]
Local = Remote: [yes/no — verify AFTER push]
Pushed: [yes/FAILED]
Archived: [N] old handoffs moved to _archived/
```

---

## Rules

| Rule | Why |
|------|-----|
| Header must match pwd | Prevents cross-project contamination |
| Push unpushed work BEFORE handoff | Ensures nothing is lost |
| Store in project repo only | Each project owns its handoffs |
| Keep last 5, archive older | Prevents directory bloat |
| Commit + push the handoff | Next session finds it via git pull |
