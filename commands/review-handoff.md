Read the most recent handoff for this project and orient yourself to pick up where the last session left off. This is the FIRST thing you do when starting a new session.

Triggers: "review handoff", "pick up where we left off", "what was the last session", "orient yourself", "read handoff", "session start", "continue from last session"

**This command is READ-ONLY. Do NOT write a new handoff. Do NOT invoke /full-handoff. You are READING, not WRITING.**

---

## STEP 0: Identify This Project

```bash
PROJECT_PATH=$(pwd)
PROJECT_NAME=$(basename "$PROJECT_PATH")
GITHUB_REPO=""
if git remote get-url origin 2>/dev/null; then
  GITHUB_REPO=$(git remote get-url origin 2>/dev/null | sed 's|.*/||;s|\.git$||')
fi
if [ -z "$GITHUB_REPO" ]; then
  GITHUB_REPO="$PROJECT_NAME"
fi
echo "Project: $PROJECT_NAME | Repo: $GITHUB_REPO | Path: $PROJECT_PATH"
```

---

## STEP 1: Find the Most Recent Handoff

Search these locations in priority order. Use the FIRST match found:

### 1a. GitHub superpowers repo (most reliable — always pushed)
```bash
cd /tmp && rm -rf review-handoff-tmp
git clone --depth 5 https://github.com/nhouseholder/nicks-claude-code-superpowers.git review-handoff-tmp 2>&1 | tail -1
ls -t /tmp/review-handoff-tmp/handoffs/handoff_${GITHUB_REPO}_*.md 2>/dev/null | head -1
```

### 1b. Project-specific memory
```bash
MEMORY_PATH="$HOME/.claude/projects/$(echo "$PROJECT_PATH" | sed 's|/|-|g; s|^-||')/memory"
ls -t "$MEMORY_PATH"/handoff_*.md 2>/dev/null | grep -v ARCHIVED | head -1
```

### 1c. Local project directory
```bash
ls "$PROJECT_PATH/HANDOFF.md" 2>/dev/null
```

**If NO handoff is found in any location:** Say "No previous handoff found for this project. This appears to be the first session. Would you like me to explore the codebase and orient myself?" Then run the 3-Gate Verification from ~/.claude/CLAUDE.md and summarize what you find.

---

## STEP 2: Read the Handoff (FULLY)

Read the ENTIRE handoff document. Do not skim. Do not summarize prematurely. Read every section.

Pay special attention to:
- **Section 3 (What Failed)** — every failure includes an anti-pattern ID if logged; grep `~/.claude/anti-patterns.md` for each ID to get full context
- **Section 6 (In Progress)** — this is where you pick up
- **Section 7 (Blocked)** — things that may still be blocked
- **Section 8 (Next Steps)** — your priority list
- **Section 9 (Agent Observations)** — learn from the previous agent's mistakes AND check for data contradictions
- **Section 10 (Miscommunications)** — avoid repeating these
- **Section 15 (Memory Updates)** — check which anti-patterns and memories were added; read the full entries
- **Section 17 (For The Next Agent)** — mandatory reading list

---

## STEP 3: Run 3-Gate Verification

Execute the full 3-Gate Verification from ~/.claude/CLAUDE.md:

### GATE 1: Correct Repo
```bash
echo "Directory: $(pwd)"
echo "Git remote: $(git remote get-url origin 2>/dev/null || echo 'none — iCloud dir, will clone for git ops')"
cat ~/Projects/site-to-repo-map.json 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); [print(f'{k} → {v[\"github_repo\"]} → {v[\"local_path\"]}') for k,v in d.get('sites',{}).items() if '$GITHUB_REPO' in v.get('github_repo','') or '$PROJECT_NAME' in v.get('local_path','')]" 2>/dev/null || echo "No site mapping found"
```

### GATE 2: Local Matches Remote
```bash
git fetch origin --quiet 2>/dev/null
LOCAL_SHA=$(git rev-parse HEAD 2>/dev/null || echo "no-local-git")
REMOTE_SHA=$(git rev-parse origin/main 2>/dev/null || git rev-parse origin/master 2>/dev/null || echo "no-remote")
echo "Local:  $LOCAL_SHA"
echo "Remote: $REMOTE_SHA"
if [ "$LOCAL_SHA" != "$REMOTE_SHA" ] && [ "$LOCAL_SHA" != "no-local-git" ]; then
  echo "⚠️ STALE — pulling..."
  git pull
fi
echo "Last commit: $(git log -1 --format='%ci %s' 2>/dev/null || echo 'N/A')"
```

### GATE 3: Read Context
Read these files (from the handoff's Section 17 list, plus defaults):
1. The handoff itself (already read in Step 2)
2. Project CLAUDE.md (if exists)
3. Project MEMORY.md or memory/ directory
4. ~/.claude/anti-patterns.md
5. ~/.claude/recurring-bugs.md
6. Any other files listed in Section 17

---

## STEP 4: Present Orientation Summary

Print this summary to the user. Be concise but complete:

```
SESSION ORIENTED ✓
==================
Project: [name] ([github repo])
Path: [canonical local path]
Branch: [branch] | Last commit: [date] [message]
Local = Remote: [yes/no]

PREVIOUS SESSION ([date]):
  Model: [model from handoff header]
  Summary: [1-2 sentences from Section 1]

PICKUP POINT:
  [Section 6 content — or "All tasks completed" if clean]

BLOCKED:
  [Section 7 content — or "Nothing blocked"]

PRIORITY QUEUE:
  1. [from Section 8]
  2. [from Section 8]
  3. [from Section 8]

WARNINGS:
  [Any items from Section 9/10 the next agent should know]
  [Any gate failures from Step 3]
  [NEW anti-patterns from Section 15: list IDs + 1-line summary]

Ready to work. What would you like to tackle?
```

---

## STEP 5: Clean Up

```bash
rm -rf /tmp/review-handoff-tmp 2>/dev/null
```

---

## CRITICAL RULES

1. **This command is READ-ONLY.** Never write a handoff. Never invoke /full-handoff. Never create HANDOFF.md.
2. **Read the WHOLE handoff.** Don't skip sections. Section 17 tells you what else to read.
3. **Run 3-Gate Verification.** Even if the handoff looks clean, verify the repo state yourself.
4. **Don't start working until the summary is printed.** The user needs to see the orientation before giving you tasks.
5. **If the handoff mentions unfinished work (Section 6), offer to continue it.** Don't wait to be told.
6. **If gates fail, fix them before presenting the summary.** Pull stale repos. Flag wrong directories. Don't proceed on bad state.

---

## What This Command Prevents

| Problem | How This Fixes It |
|---------|-------------------|
| Agent starts fresh, ignores prior session | Forces reading the handoff before any work |
| Agent writes an empty handoff over a real one | READ-ONLY — no writing allowed |
| Agent doesn't know what was in progress | Section 6 explicitly shown in summary |
| Agent repeats mistakes from prior session | Sections 9/10 surfaced as WARNINGS |
| Agent works in wrong directory or stale repo | 3-Gate Verification catches this |
| Agent asks "what should I work on?" | Priority queue from Section 8 presented automatically |
