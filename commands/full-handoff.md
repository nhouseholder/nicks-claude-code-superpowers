Generate a comprehensive handoff document, sync it across all locations, and clean up stale artifacts. This is the LAST thing you do before ending a session or before the next agent takes over.

## What This Command Does

1. Generate a handoff document capturing everything from this session
2. Store it in 3 places (local, iCloud, GitHub)
3. Archive old/outdated handoffs
4. Clean up stale files across all locations
5. Verify the handoff is complete and accessible

## Phase 1: Generate Handoff Document

Create `HANDOFF.md` in the current project directory with this structure:

```markdown
# Handoff — [Project Name] — [Date] [Time]

## Session Summary
[1-3 sentences: what was accomplished this session]

## What Was Done
- [Bullet list of completed tasks with file locations]

## What's In Progress
- [Anything started but not finished, with current state]

## What's Left To Do
- [Remaining tasks the next agent should pick up]

## Key Decisions Made
- [Technical decisions, trade-offs chosen, approaches selected]

## Files Changed
[List every file created, modified, or deleted this session]

## Bugs Found & Fixed
- [Bug]: [Root cause] → [Fix applied] → [Logged in anti-patterns.md: yes/no]

## Gotchas for Next Agent
- [Things that aren't obvious — env setup, build quirks, data caching, etc.]
- [Anything that caused confusion this session]

## Current State
- Branch: [current git branch]
- Last commit: [hash + message]
- Build status: [passing/failing/untested]
- Deploy status: [deployed/not deployed/needs deploy]

## Memory Updates
- [What was saved to memory this session]
- [What anti-patterns were logged]
```

## Phase 2: Store in 3 Locations

### 2a. Local (current project directory)
```bash
# Already created in Phase 1
# Verify: ls -la HANDOFF.md
```

### 2b. Project Memory
```bash
# Copy to project memory directory
cp HANDOFF.md ~/.claude/projects/[project-path]/memory/handoff_[date].md
```

### 2c. iCloud (superpowers repo)
```bash
# Copy to superpowers repo for cross-session access
cp HANDOFF.md ~/Library/Mobile\ Documents/com~apple~CloudDocs/superpowers/HANDOFF.md
```

### 2d. GitHub (superpowers repo)
Follow the standard iCloud→/tmp→GitHub sync:
```bash
cd /tmp && rm -rf superpowers-handoff
git clone https://github.com/nhouseholder/nicks-claude-code-superpowers.git superpowers-handoff
cp [project]/HANDOFF.md /tmp/superpowers-handoff/HANDOFF.md
cd /tmp/superpowers-handoff && git add -A && git commit -m "Handoff: [project] [date]" && git push
rm -rf /tmp/superpowers-handoff
```

## Phase 3: Archive Old Handoffs

### 3a. Archive old HANDOFF.md files in the project
```bash
# If a HANDOFF.md already exists, rename it before overwriting
if [ -f HANDOFF.md ]; then
    mv HANDOFF.md HANDOFF_[previous-date].ARCHIVED.md
fi
```

### 3b. Clean up project memory
```bash
# Archive handoffs older than 7 days
# Keep only the 3 most recent handoff_*.md files in project memory
# Rename older ones: handoff_[date].md → handoff_[date].ARCHIVED.md
```

### 3c. Clean up superpowers repo
Check for and archive:
- Old HANDOFF.md files (keep only the latest)
- Stale worktrees in `.claude/worktrees/`
- Old orchestrator log files in `coder/`
- Any `/tmp` artifacts left from prior sessions

## Phase 4: Registry Cleanup

### 4a. Check for stale files locally
- [ ] Any `.ARCHIVED.` files that should be in `_archived/` directory?
- [ ] Any duplicate skill files (same skill in both `skills/` and `.claude/skills/`)?
- [ ] Any old log files, temp files, or debug output?

### 4b. Check iCloud superpowers
- [ ] `skills/_archived/` — are archived skills properly marked?
- [ ] Any skills that were deleted from global but still in superpowers?
- [ ] CLAUDE.md and HANDOFF.md up to date?

### 4c. Verify GitHub sync
- [ ] `git status` shows no uncommitted changes in superpowers
- [ ] Latest handoff is pushed
- [ ] anti-patterns.md and recurring-bugs.md are committed

## Phase 5: Verify Handoff Completeness

Before declaring handoff complete, check:
```
[ ] HANDOFF.md exists in project directory
[ ] HANDOFF.md is in project memory
[ ] HANDOFF.md is pushed to GitHub
[ ] Old handoffs are archived (not deleted)
[ ] No stale files that could confuse the next agent
[ ] Memory files (anti-patterns.md, recurring-bugs.md) are current
[ ] All uncommitted changes are either committed or documented in "What's In Progress"
```

## Output

When done, report:
```
HANDOFF COMPLETE
================
Document: HANDOFF.md ([X] lines)
Stored: local ✓ | project memory ✓ | GitHub ✓
Archived: [N] old handoffs
Cleaned: [N] stale files
Next agent: read HANDOFF.md + ~/.claude/anti-patterns.md before starting
```
