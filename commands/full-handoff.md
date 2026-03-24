Generate a comprehensive handoff document, sync across all locations, archive old handoffs, and clean up stale files. This is the LAST thing you do before ending a session. Triggers on: "get handoff document ready", "full handoff", "prepare handoff", "session handoff".

**This is NOT optional. Every section must be filled with real content, not placeholders.**

## Phase 1: Generate HANDOFF.md

Create `HANDOFF.md` in the current project directory. EVERY section below is mandatory.

```markdown
# Handoff — [Project Name] — [Date] [Time]
## Model: [which model was used this session]

---

## 1. Session Summary
[2-4 sentences: what was the user's goal, what was accomplished, what's the current state]

## 2. What Was Done (Completed Tasks)
- [Task]: [files changed] — [outcome]
- [Task]: [files changed] — [outcome]
[List EVERY completed task with specific file paths]

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

## 6. What's In Progress (Unfinished Work)
- [Task]: [current state] → [what's left to do] → [files involved]
[Include enough detail that another agent can pick up exactly where this left off]

## 7. Next Steps (Prioritized)
1. [Most important next task] — [why it's #1]
2. [Second priority] — [why]
3. [Third priority] — [why]

## 8. AI-Generated Recommendations
Based on this session, I recommend:
- [Technical recommendation]: [reasoning]
- [Process recommendation]: [reasoning]
- [Architecture/design recommendation]: [reasoning]
[These are the agent's own suggestions — not just what the user asked for]

## 9. AI-Generated Insights
Patterns and observations from this session:
- [Insight about the codebase]: [evidence]
- [Insight about the user's workflow]: [evidence]
- [Insight about recurring issues]: [evidence]
[What did the agent learn that isn't obvious from the code alone?]

## 10. Points to Improve
- [Where the agent fell short]: [what should be done differently]
- [Where the codebase needs attention]: [technical debt, fragile areas]
- [Where the process broke down]: [communication gaps, tool failures]

## 11. Miscommunications to Address
- [Misunderstanding that occurred]: [what the user meant vs. what the agent did]
- [Correction the user had to make]: [what the next agent should know]
- [Assumption that was wrong]: [the correct understanding]
[If no miscommunications, write "None — session was well-aligned"]

## 12. Files Changed This Session
| File | Action | Description |
|------|--------|-------------|
| path/to/file | created/modified/deleted | what changed |

## 13. Current State
- **Branch**: [current git branch]
- **Last commit**: [hash + message]
- **Build status**: [passing/failing/untested]
- **Deploy status**: [deployed/not deployed/needs deploy]
- **Uncommitted changes**: [yes/no — list if yes]

## 14. Memory & Anti-Patterns Updated
- [What was saved to ~/.claude/anti-patterns.md]: [entry summary]
- [What was saved to ~/.claude/recurring-bugs.md]: [entry summary]
- [What was saved to project memory]: [entry summary]
- [What was saved to ~/.claude/memory/topics/]: [entry summary]

## 15. Skills & Agents Used
| Skill/Agent | How It Was Used | Was It Helpful? |
|-------------|----------------|-----------------|
| [skill name] | [what it did] | [yes/no/partially] |

## 16. For The Next Agent — Read These First
1. This HANDOFF.md
2. ~/.claude/anti-patterns.md
3. ~/.claude/recurring-bugs.md
4. [Project-specific memory files if any]
5. [Any CLAUDE.md in the project directory]
```

## Phase 2: Store in 3 Locations

### 2a. Current project directory
The HANDOFF.md created in Phase 1 stays here.

### 2b. Project memory
```bash
mkdir -p ~/.claude/projects/[project-path]/memory/
cp HANDOFF.md ~/.claude/projects/[project-path]/memory/handoff_$(date +%Y%m%d_%H%M).md
```

### 2c. iCloud superpowers repo
```bash
cp HANDOFF.md ~/Library/Mobile\ Documents/com~apple~CloudDocs/superpowers/HANDOFF.md
```

### 2d. GitHub
```bash
cd /tmp && rm -rf superpowers-handoff
git clone https://github.com/nhouseholder/nicks-claude-code-superpowers.git superpowers-handoff
cp [project]/HANDOFF.md /tmp/superpowers-handoff/HANDOFF.md
cd /tmp/superpowers-handoff
git add -A
git commit -m "Handoff: [project] — [date] — [1-line summary]

Co-Authored-By: Claude Opus 4.6 (1M context) <noreply@anthropic.com>"
git push origin main
rm -rf /tmp/superpowers-handoff
```

## Phase 3: Archive Old Handoffs

### 3a. In the project directory
```bash
# Rename any existing HANDOFF.md before overwriting
# Keep only the current one active — archive all others
for f in HANDOFF_*.md HANDOFF_*.ARCHIVED.md; do
  # Already archived, skip
done
# Any HANDOFF.md that isn't the one we just created → rename with date
```

### 3b. In project memory
```bash
# Keep only the 3 most recent handoff_*.md files
# Archive older ones: handoff_[date].md → handoff_[date].ARCHIVED.md
```

### 3c. In iCloud superpowers
Only one HANDOFF.md lives here (the latest). Old ones are overwritten.

## Phase 4: File Cleanup (Local + iCloud + GitHub)

Before ending the session, check for and clean up:

### 4a. Local project cleanup
- [ ] Stale worktrees in `.claude/worktrees/`
- [ ] Old log files (orchestrator_*.log, *.log in project root)
- [ ] Temp files left by scripts (/tmp artifacts referenced from this project)
- [ ] Duplicate files (same content, different names)
- [ ] Files marked as TODO or FIXME that are now done

### 4b. iCloud superpowers cleanup
- [ ] `skills/_archived/` — properly marked?
- [ ] Old HANDOFF.md files — archived?
- [ ] Any stale files in `coder/` (old orchestrator logs)
- [ ] Hooks that were replaced — old versions cleaned up?

### 4c. GitHub cleanup (during the push in Phase 2d)
- [ ] Same checks as 4b — clean up anything stale before pushing
- [ ] Verify anti-patterns.md and recurring-bugs.md are committed
- [ ] Verify no sensitive data (env vars, tokens) in any committed files

## Phase 5: Verify Handoff Completeness

```
HANDOFF COMPLETE
================
Document: HANDOFF.md ([X] lines, [16] sections filled)
Stored: local ✓ | project memory ✓ | iCloud ✓ | GitHub ✓
Archived: [N] old handoffs
Cleaned: [N] stale files removed/archived
Anti-patterns updated: [yes/no]
Recurring bugs updated: [yes/no]

Next agent: Start by reading HANDOFF.md + anti-patterns.md + recurring-bugs.md
```
