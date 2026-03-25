Generate a comprehensive handoff document, sync across all locations, archive old handoffs, and clean up stale files. This is the LAST thing you do before ending a session. Triggers on: "get handoff document ready", "full handoff", "prepare handoff", "session handoff".

**This is NOT optional. Every section must be filled with real content, not placeholders.**

## Phase 0: Gather Facts (Before Writing Anything)

Run these commands FIRST and save the output — use it to populate sections automatically:

```bash
# Project identity
PROJECT_NAME=$(basename "$(pwd)")
PROJECT_PATH=$(pwd)
MEMORY_PATH="$HOME/.claude/projects/$(echo "$PROJECT_PATH" | sed 's|/|-|g; s|^-||')/memory"

# Git history for this session (last 12 hours)
git log --oneline --since="12 hours ago" 2>/dev/null || echo "No git repo or no recent commits"

# Files changed (machine-generated — DO NOT skip)
git diff --stat HEAD~10 2>/dev/null || echo "No git history available"

# Current state
git branch --show-current 2>/dev/null || echo "No git repo"
git log -1 --format="%H %s" 2>/dev/null || echo "No commits"
git status --short 2>/dev/null || echo "No git repo"

# Environment state
node --version 2>/dev/null || echo "No Node.js"
python3 --version 2>/dev/null || echo "No Python"
ps aux | grep -E "(next|vite|express|flask|uvicorn|wrangler)" | grep -v grep || echo "No dev servers running"

# Session duration estimate
echo "Session start: check first tool call timestamp"
```

Use this output to populate sections 12, 13, and 17 with FACTS, not memory reconstruction.

## Phase 1: Generate HANDOFF.md

Create `HANDOFF.md` in the current project directory. EVERY section below is mandatory.

```markdown
# Handoff — $PROJECT_NAME — [Date] [Time]
## Model: [which model was used this session]
## Previous handoff: [filename of the most recent prior handoff, or "First session"]

---

## 1. Session Summary
[2-4 sentences: what was the user's goal, what was accomplished, what's the current state]

## 2. What Was Done (Completed Tasks)
- [Task]: [files changed] — [outcome]
- [Task]: [files changed] — [outcome]
[List EVERY completed task with specific file paths. Cross-reference with git log output from Phase 0.]

## 3. What Failed (And Why)
- [Task that failed]: [what went wrong] → [root cause] → [what was tried]
- [Approach that didn't work]: [why it failed] → [lesson learned]
[If nothing failed, write "No failures this session"]

## 4. What Worked Well
- [Approach/technique that was effective]: [why it worked]
- [Tool/skill that helped]: [how it helped]
[Highlight successful patterns for the next agent to reuse]

## 5. What The User Wants (Goals & Priorities)
- [User's primary goal]: [current status]
- [User's secondary goals]: [status]
- [Explicit preferences expressed]: [what the user said they want]
- [Frustrations expressed]: [what annoyed the user — the next agent must avoid this]

### User Quotes (Verbatim)
Pull 2-3 key quotes from the conversation that capture the user's priorities, frustrations, or preferences. Exact words > paraphrase.
- "[exact quote]" — context: [when/why they said it]
- "[exact quote]" — context: [when/why they said it]

## 6. What's In Progress (Unfinished Work)
- [Task]: [current state] → [what's left to do] → [files involved]
[Include enough detail that another agent can pick up exactly where this left off]

## 7. Blocked / Waiting On
Items that CANNOT proceed without external input:
- [Blocked item]: waiting on [user decision / API key / deploy approval / third-party response / etc.]
- [Blocked item]: waiting on [what]
[If nothing is blocked, write "Nothing blocked"]
[This is DIFFERENT from "In Progress" — blocked means external dependency, in-progress means just unfinished]

## 8. Next Steps (Prioritized)
1. [Most important next task] — [why it's #1]
2. [Second priority] — [why]
3. [Third priority] — [why]

## 9. Agent Observations
Combine recommendations, insights, and self-critique into one honest section. No filler.

### Recommendations
- [Technical recommendation]: [reasoning]
- [Process recommendation]: [reasoning]

### Patterns & Insights
- [Insight about the codebase]: [evidence]
- [Insight about the user's workflow]: [evidence]
- [Insight about recurring issues]: [evidence]

### Where I Fell Short
- [Where the agent could have done better]: [what should be done differently next time]
- [Where the codebase needs attention]: [technical debt, fragile areas]

## 10. Miscommunications to Address
- [Misunderstanding that occurred]: [what the user meant vs. what the agent did]
- [Correction the user had to make]: [what the next agent should know]
- [Assumption that was wrong]: [the correct understanding]
[If no miscommunications, write "None — session was well-aligned"]

## 11. Files Changed This Session
**Machine-generated from git (paste `git diff --stat` output):**
```
[paste git diff --stat output here]
```

**Human-annotated descriptions:**
| File | Action | Description |
|------|--------|-------------|
| path/to/file | created/modified/deleted | what changed and why |

[The git output ensures nothing is missed. The table adds context.]

## 12. Current State
Populated from Phase 0 commands — do NOT reconstruct from memory.
- **Branch**: [from `git branch --show-current`]
- **Last commit**: [from `git log -1`]
- **Build status**: [run build command if available, or "untested"]
- **Deploy status**: [deployed/not deployed/needs deploy]
- **Uncommitted changes**: [from `git status --short` — list if any]

## 13. Environment State
- **Node.js**: [version or N/A]
- **Python**: [version or N/A]
- **Running dev servers**: [from `ps aux` grep — list PIDs and ports, or "none"]
- **Environment variables set this session**: [list any that were exported, or "none"]
- **Active MCP connections**: [list any relevant ones, or "default"]

## 14. Session Metrics
- **Duration**: [approximate session length]
- **Tasks completed**: [N] / [N attempted]
- **User corrections**: [count of times the user corrected the agent's approach]
- **Tool calls**: [approximate count — check conversation length]
- **Skills/commands invoked**: [list]
- **Commits made**: [count from git log]

## 15. Memory & Anti-Patterns Updated
- [What was saved to ~/.claude/anti-patterns.md]: [entry summary]
- [What was saved to ~/.claude/recurring-bugs.md]: [entry summary]
- [What was saved to project memory]: [entry summary]
- [What was saved to ~/.claude/memory/topics/]: [entry summary]
[If nothing was updated, write "No memory updates this session" and explain why — was nothing learned?]

## 16. Skills & Agents Used
| Skill/Agent | How It Was Used | Was It Helpful? |
|-------------|----------------|-----------------|
| [skill name] | [what it did] | [yes/no/partially — 1 sentence why] |

## 17. For The Next Agent — Read These First
1. This HANDOFF.md
2. Previous handoff: [filename from header]
3. ~/.claude/anti-patterns.md
4. ~/.claude/recurring-bugs.md
5. [Project-specific CLAUDE.md]
6. [Project-specific memory files]
7. [Any other critical files discovered this session]
```

## Phase 2: Store in 3 Locations

### 2a. Current project directory
The HANDOFF.md created in Phase 1 stays here.

### 2b. Project memory
```bash
# Auto-detect project memory path
PROJECT_PATH=$(pwd)
MEMORY_PATH="$HOME/.claude/projects/$(echo "$PROJECT_PATH" | sed 's|/|-|g; s|^-||')/memory"
mkdir -p "$MEMORY_PATH"
cp HANDOFF.md "$MEMORY_PATH/handoff_$(date +%Y%m%d_%H%M).md"
```

### 2c. iCloud superpowers repo
```bash
cp HANDOFF.md ~/Library/Mobile\ Documents/com~apple~CloudDocs/superpowers/HANDOFF.md
```

### 2d. GitHub (with fallback)
```bash
cd /tmp && rm -rf superpowers-handoff
git clone https://github.com/nhouseholder/nicks-claude-code-superpowers.git superpowers-handoff
if [ $? -ne 0 ]; then
  echo "GITHUB CLONE FAILED — handoff saved locally only. Sync manually later."
  echo "GitHub sync pending" >> "$PROJECT_PATH/HANDOFF.md"
else
  cp "$PROJECT_PATH/HANDOFF.md" /tmp/superpowers-handoff/HANDOFF.md
  cd /tmp/superpowers-handoff
  git add -A
  git commit -m "$(cat <<'EOF'
Handoff: $PROJECT_NAME — $(date +%Y-%m-%d) — [1-line summary]

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>
EOF
  )"
  if ! git push origin main; then
    echo "GITHUB PUSH FAILED — commit saved at $(git log -1 --format=%H)"
    echo "GitHub sync pending — commit: $(git log -1 --format=%H)" >> "$PROJECT_PATH/HANDOFF.md"
  fi
  rm -rf /tmp/superpowers-handoff
fi
```

## Phase 3: Archive Old Handoffs

### 3a. In the project directory
```bash
cd "$PROJECT_PATH"
# Find any HANDOFF*.md files that are NOT the one we just created
for f in HANDOFF_*.md; do
  [ -f "$f" ] || continue
  # Skip if already archived
  [[ "$f" == *.ARCHIVED.md ]] && continue
  mv "$f" "${f%.md}.ARCHIVED.md"
  echo "Archived: $f → ${f%.md}.ARCHIVED.md"
done
# If a previous HANDOFF.md existed (now overwritten), it's already replaced
```

### 3b. In project memory
```bash
cd "$MEMORY_PATH"
# List all handoff files sorted by date (newest first), skip first 3
ls -t handoff_*.md 2>/dev/null | grep -v ARCHIVED | tail -n +4 | while read f; do
  mv "$f" "${f%.md}.ARCHIVED.md"
  echo "Archived: $f → ${f%.md}.ARCHIVED.md"
done
```

### 3c. In iCloud superpowers
Only one HANDOFF.md lives here (the latest). Old ones are overwritten by Phase 2c.

## Phase 4: File Cleanup (Local + iCloud + GitHub)

**Skip this phase if the session was < 30 minutes AND < 5 tasks completed.** For short sessions, cleanup is overhead. Just note "Cleanup skipped — short session" in the verification output.

For full sessions, check and clean:

### 4a. Local project cleanup
```bash
# Stale worktrees
ls -la .claude/worktrees/ 2>/dev/null && echo "REVIEW: stale worktrees found"

# Old log files
find . -maxdepth 2 -name "*.log" -mtime +7 -not -path "./.git/*" 2>/dev/null

# Temp files in /tmp referencing this project
ls /tmp/*$(basename $(pwd))* 2>/dev/null && echo "REVIEW: /tmp artifacts found"
```

### 4b. iCloud superpowers cleanup
```bash
ICLOUD="$HOME/Library/Mobile Documents/com~apple~CloudDocs/superpowers"
# Check for stale files
ls "$ICLOUD"/coder/*.log 2>/dev/null && echo "REVIEW: old orchestrator logs"
ls "$ICLOUD"/HANDOFF_*.md 2>/dev/null && echo "REVIEW: old handoff files in iCloud root"
```

### 4c. GitHub cleanup (during the push in Phase 2d)
- Verify anti-patterns.md and recurring-bugs.md are committed
- Verify no sensitive data (env vars, tokens) in any committed files
- Clean up anything stale before pushing

## Phase 5: Verify Handoff Completeness

```
HANDOFF COMPLETE
================
Document: HANDOFF.md ([X] lines, [17] sections filled)
Previous: [prior handoff filename or "First session"]
Stored: local ✓ | project memory ✓ | iCloud ✓ | GitHub [✓/PENDING]
Archived: [N] old handoffs
Cleaned: [N] stale files removed/archived (or "Skipped — short session")
Anti-patterns updated: [yes/no]
Recurring bugs updated: [yes/no]
Session metrics: [N] tasks, [N] commits, [N] corrections, ~[N] min duration

Next agent: Start by reading HANDOFF.md + anti-patterns.md + recurring-bugs.md
```
