Generate a comprehensive handoff document, sync to all locations, and archive old ones. This is the LAST thing you do before ending a session.

Triggers: "full handoff", "prepare handoff", "session handoff", "get handoff ready", "wrap up", "end session"

**Every section must contain real content. Empty or placeholder sections = handoff failure.**

---

## STEP 1: Detect Project Identity

```bash
PROJECT_PATH=$(pwd)
PROJECT_NAME=$(basename "$PROJECT_PATH")

# Detect the GitHub repo name (may differ from directory name)
GITHUB_REPO=""
if git remote get-url origin 2>/dev/null; then
  GITHUB_REPO=$(git remote get-url origin 2>/dev/null | sed 's|.*/||;s|\.git$||')
fi

# If no local git, try to infer from directory name or CLAUDE.md
if [ -z "$GITHUB_REPO" ]; then
  GITHUB_REPO="$PROJECT_NAME"
fi

# Handoff filename: project-specific + timestamped
HANDOFF_FILENAME="handoff_${GITHUB_REPO}_$(date +%Y-%m-%d_%H%M).md"
echo "Project: $PROJECT_NAME | Repo: $GITHUB_REPO | Handoff: $HANDOFF_FILENAME"
```

## STEP 2: Gather Machine Facts

Run ALL of these. Paste raw output into sections 11-13. Do NOT reconstruct from memory.

```bash
# Git facts (if available)
echo "=== GIT BRANCH ===" && git branch --show-current 2>/dev/null || echo "No git repo"
echo "=== GIT LOG (last 12h) ===" && git log --oneline --since="12 hours ago" 2>/dev/null || echo "No recent commits"
echo "=== GIT DIFF STAT ===" && git diff --stat HEAD~10 2>/dev/null || echo "No git diff"
echo "=== GIT STATUS ===" && git status --short 2>/dev/null || echo "No git repo"
echo "=== GIT LAST COMMIT ===" && git log -1 --format="%H %s" 2>/dev/null || echo "No commits"

# Environment
echo "=== NODE ===" && node --version 2>/dev/null || echo "N/A"
echo "=== PYTHON ===" && python3 --version 2>/dev/null || echo "N/A"
echo "=== DEV SERVERS ===" && ps aux | grep -E "(next|vite|express|flask|uvicorn|wrangler)" | grep -v grep || echo "None"
```

If the project has NO local git repo but HAS a GitHub remote, clone to `/tmp/` to get git facts:
```bash
cd /tmp && rm -rf "${GITHUB_REPO}-facts" && git clone "https://github.com/nhouseholder/${GITHUB_REPO}.git" "${GITHUB_REPO}-facts" 2>/dev/null
cd "/tmp/${GITHUB_REPO}-facts" && git log --oneline -10
```

## STEP 3: Find Previous Handoff

Check these locations in order. The FIRST match is the previous handoff:
1. Project memory: `~/.claude/projects/$(echo "$PROJECT_PATH" | sed 's|/|-|g; s|^-||')/memory/handoff_*.md` (newest non-ARCHIVED)
2. GitHub superpowers repo: `handoffs/handoff_${GITHUB_REPO}_*.md` (newest)
3. Local project dir: `HANDOFF.md`

Record the filename for the header.

## STEP 4: Write the Handoff Document

Create the file at `$PROJECT_PATH/HANDOFF.md`. Also save a copy as `$HANDOFF_FILENAME` for archival.

**MANDATORY: All 17 sections below. If a section has no content, write "N/A — [reason]". Never leave brackets or placeholders.**

```markdown
# Handoff — [PROJECT_NAME] — [YYYY-MM-DD] [HH:MM]
## Model: [exact model used — e.g., Claude Opus 4.6 (1M context)]
## Previous handoff: [filename from Step 3, or "First session"]
## GitHub repo: [nhouseholder/REPO_NAME or "none"]

---

## 1. Session Summary
[2-4 sentences. What the user wanted → what was accomplished → current state.]

## 2. What Was Done
[Every completed task. Format: "- **Task name**: files changed — outcome"]

## 3. What Failed (And Why)
[Every failure. Format: "- **What failed**: root cause → what was tried → lesson"]
[If nothing failed: "No failures this session."]

## 4. What Worked Well
[Effective approaches, tools, patterns worth reusing.]

## 5. What The User Wants
[Goals, priorities, preferences, frustrations. Include 2-3 verbatim user quotes with context.]

## 6. In Progress (Unfinished)
[Exactly where to pick up. Files, line numbers, what's left.]
[If nothing: "All tasks completed."]

## 7. Blocked / Waiting On
[External dependencies only. User decisions, API keys, third-party responses.]
[If nothing: "Nothing blocked."]

## 8. Next Steps (Prioritized)
1. [Most important] — [why #1]
2. [Second] — [why]
3. [Third] — [why]

## 9. Agent Observations
### Recommendations
[Technical and process recommendations with reasoning.]

### Where I Fell Short
[Honest self-critique. What to do differently.]

## 10. Miscommunications
[Misunderstandings, corrections, wrong assumptions. Or: "None — session aligned."]

## 11. Files Changed
[Paste git diff --stat from Step 2, then add a table with descriptions:]
| File | Action | Why |
|------|--------|-----|

## 12. Current State
- **Branch**: [from Step 2]
- **Last commit**: [from Step 2]
- **Build**: [tested/untested/passing/failing]
- **Deploy**: [deployed/pending/N/A]
- **Uncommitted changes**: [list or "none"]

## 13. Environment
- **Node.js**: [version]
- **Python**: [version]
- **Dev servers**: [running processes or "none"]

## 14. Session Metrics
- **Duration**: ~[N] minutes
- **Tasks**: [completed] / [attempted]
- **User corrections**: [N]
- **Commits**: [N]
- **Skills used**: [list]

## 15. Memory Updates
[What was saved to anti-patterns, recurring-bugs, project memory, topics.]
[If none: "No updates — [reason]."]

## 16. Skills Used
| Skill | Purpose | Helpful? |
|-------|---------|----------|

## 17. For The Next Agent
Read these files first (in order):
1. This handoff
2. [Previous handoff filename]
3. ~/.claude/anti-patterns.md
4. [Project CLAUDE.md path]
5. [Other critical files]
```

## STEP 5: Verify Before Storing

Before proceeding to storage, verify the handoff:
- Count that all 17 sections exist and have real content (not brackets/placeholders)
- Verify section 11 has actual file paths (not "[paste here]")
- Verify section 12 has actual git data (not "[from Step 2]")
- If ANY section is still templated, go back and fill it in NOW

## STEP 6: Store in 3+ Locations

### 6a. Local project directory
`HANDOFF.md` stays in the project directory.

### 6b. Project-specific memory
```bash
PROJECT_PATH=$(pwd)
MEMORY_PATH="$HOME/.claude/projects/$(echo "$PROJECT_PATH" | sed 's|/|-|g; s|^-||')/memory"
mkdir -p "$MEMORY_PATH"
cp HANDOFF.md "$MEMORY_PATH/$HANDOFF_FILENAME"
```

### 6c. GitHub superpowers repo (project-specific subdirectory)
```bash
cd /tmp && rm -rf superpowers-handoff
git clone https://github.com/nhouseholder/nicks-claude-code-superpowers.git superpowers-handoff 2>&1
if [ $? -eq 0 ]; then
  cd /tmp/superpowers-handoff
  mkdir -p handoffs

  # Store with project-specific name — NEVER overwrite other projects' handoffs
  cp "$PROJECT_PATH/HANDOFF.md" "handoffs/$HANDOFF_FILENAME"

  # Also update the root HANDOFF.md as "latest across all projects"
  cp "$PROJECT_PATH/HANDOFF.md" HANDOFF.md

  # Also sync anti-patterns and recurring-bugs if they exist
  [ -f "$HOME/.claude/anti-patterns.md" ] && cp "$HOME/.claude/anti-patterns.md" anti-patterns.md
  [ -f "$HOME/.claude/recurring-bugs.md" ] && cp "$HOME/.claude/recurring-bugs.md" recurring-bugs.md

  git add -A
  git commit -m "Handoff: $GITHUB_REPO — $(date +%Y-%m-%d) — [1-line summary of session]

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"

  if git push origin main; then
    echo "GITHUB: ✓ pushed"
  else
    echo "GITHUB: PUSH FAILED — commit at $(git log -1 --format=%H)"
  fi
  rm -rf /tmp/superpowers-handoff
else
  echo "GITHUB: CLONE FAILED — handoff saved locally only"
fi
```

**CRITICAL: The handoff file in `handoffs/` is named per-project per-timestamp. It NEVER overwrites another project's handoff.**

## STEP 7: Archive Old Handoffs

```bash
# In project memory — keep 3 newest, archive the rest
MEMORY_PATH="$HOME/.claude/projects/$(echo "$PROJECT_PATH" | sed 's|/|-|g; s|^-||')/memory"
cd "$MEMORY_PATH" 2>/dev/null
ls -t handoff_*.md 2>/dev/null | grep -v ARCHIVED | tail -n +4 | while read f; do
  mv "$f" "${f%.md}.ARCHIVED.md"
  echo "Archived: $f"
done
```

## STEP 8: Protect Architecture (MANDATORY — prevents next-session confusion)

Before printing the summary, run these checks to ensure the project infrastructure is clean for the next agent:

### 8a. Verify repo is pushed to GitHub
```bash
git fetch origin --quiet
LOCAL_SHA=$(git rev-parse HEAD)
REMOTE_SHA=$(git rev-parse origin/main 2>/dev/null || git rev-parse origin/master 2>/dev/null)
if [ "$LOCAL_SHA" != "$REMOTE_SHA" ]; then
  echo "⚠️ UNPUSHED WORK — pushing now..."
  git push origin $(git branch --show-current)
fi
```

### 8b. Verify site-to-repo-map.json is current
```bash
cat ~/Projects/site-to-repo-map.json | python3 -c "
import json, sys
data = json.load(sys.stdin)
for site, info in data.get('sites', {}).items():
    print(f'{site} → {info[\"github_repo\"]} → {info[\"local_path\"]}')
"
```
If any mapping is wrong (e.g., you moved a repo or changed which repo deploys to a site), update `site-to-repo-map.json` AND the CLAUDE.md table.

### 8c. Verify project-manifest.json is current
```bash
python3 -c "
import json
with open('$HOME/Projects/project-manifest.json') as f:
    d = json.load(f)
print(f'Active: {len(d[\"canonical\"])} | Archived: {len(d[\"archived\"])}')
for name in d.get('archived', {}):
    print(f'  ARCHIVED: {name} — {d[\"archived\"][name][\"reason\"]}')
"
```
If you archived any repos this session, they must appear here.

### 8d. Verify no stale artifacts
```bash
# Check for /tmp clones from this session
ls /tmp/*${GITHUB_REPO}* 2>/dev/null && echo "CLEANUP: /tmp artifacts found" && rm -rf /tmp/*${GITHUB_REPO}*
# Check for worktrees
ls .claude/worktrees/ 2>/dev/null && echo "CLEANUP: stale worktrees found"
```

### 8e. Write next-agent bootstrap instructions into the handoff
Append this to the bottom of the HANDOFF.md:
```markdown

---
## NEXT AGENT: MANDATORY STARTUP SEQUENCE
Before doing ANY work, run the 3-Gate Verification from ~/.claude/CLAUDE.md:
1. GATE 1: Check ~/Projects/site-to-repo-map.json — verify you're in the correct repo
2. GATE 2: git fetch && compare local SHA to remote — git pull if behind
3. GATE 3: Read this handoff + MEMORY.md + anti-patterns.md + recurring-bugs.md
ALL 3 GATES MUST PASS before touching any code.
```

## STEP 9: Output Verification Summary

Print this EXACTLY, filling in all values:

```
HANDOFF COMPLETE
================
File: $HANDOFF_FILENAME
Project: $PROJECT_NAME ($GITHUB_REPO)
Previous: [filename or "First session"]
Sections: 17/17 filled
Stored:
  - Local project dir: ✓
  - Project memory ($MEMORY_PATH): ✓
  - GitHub (handoffs/$HANDOFF_FILENAME): [✓/FAILED]
Archived: [N] old handoffs
Anti-patterns synced: [yes/no]
Architecture protected:
  - Repo pushed to GitHub: [✓/unpushed]
  - site-to-repo-map.json: [verified/updated]
  - project-manifest.json: [verified/updated]
  - /tmp cleaned: [✓/skipped]
  - Next-agent bootstrap: appended to handoff ✓

Next agent: Run 3-Gate Verification → Read handoffs/$HANDOFF_FILENAME → Start work
```

---

## Failure Modes This Command Prevents

| Old Problem | Fix |
|-------------|-----|
| All projects overwrite one HANDOFF.md on GitHub | Each handoff is `handoffs/handoff_PROJECTNAME_DATE_TIME.md` |
| Non-git directories (iCloud) produce empty sections | Clone from GitHub to /tmp/ to get facts |
| Agents skip sections or leave placeholders | Step 5 verification catches this before storage |
| Cross-project contamination | Project-specific naming in all locations |
| Previous handoff not found | Step 3 checks 3 locations in priority order |
| GitHub push fails silently | Explicit ✓/FAILED in verification output |
| Next agent uses wrong repo | site-to-repo-map.json checked + bootstrap instructions in handoff |
| Next agent edits stale files | 3-Gate Verification required before any work |
| Unpushed work lost between sessions | Step 8a pushes before handoff completes |
| Archived repos confused with active | project-manifest.json checked + ARCHIVED markers verified |
