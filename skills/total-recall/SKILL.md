---
name: total-recall
description: Infinite cross-session memory for projects. Automatically loads all project context at session start and saves everything important at session end. Ensures Claude remembers all decisions, architecture changes, gotchas, user preferences, and project state between sessions — no manual /mem save required. Always-on awareness skill scoped to the current project directory.
---

# Total Recall — Infinite Project Memory Across Sessions

## Always Active

Two automatic phases plus continuous awareness during the session:
1. **Session Start** — hydrate context from memory sources
2. **Session End** — persist everything important

## Phase 1: Session Start — Full Context Hydration

### Auto-Load Sequence (Lazy Loading)

**Always load (lightweight — index only):**
```
1. Read ~/.claude/projects/<project>/memory/MEMORY.md (index)
2. Check git status (current state)
3. Read ~/.claude/anti-patterns.md (past mistakes — applies to ALL tasks, not just debugging)
```

**Load on demand (when the task requires it):**
```
4. Read specific memory files referenced in MEMORY.md — only when relevant
5. Read AGENT-MEMORY.md — only when coordinating with other agents
6. Check git log --oneline -20 — only when context about recent work is needed
```

Load silently. Build a mental model of what's relevant. Know where to find things, don't hold everything.

## Phase 2: During Session — Continuous Capture + Crash-Safe Checkpoints

### Crash-Safe Checkpointing

Write `current_work.md` checkpoints DURING the session, not just at the end.

#### When to Checkpoint:

| Trigger | Why |
|---------|-----|
| After completing a major step | Progress saved if next step crashes |
| Before a risky operation (large refactor, deploy, migration) | Know where you were if it kills the session |
| Every 15-20 tool calls on long tasks | Periodic safety net |
| When user provides important context | Requirements survive session death |
| After a plan is agreed on | Plan persists even if execution never starts |
| **Before compaction** | MOST CRITICAL — everything not in a file is about to degrade |

#### Pre-Compaction Capture

When context is getting long (50+ tool calls, or compaction approaching):

**Write to project memory files — NOT just current_work.md:**

1. **`session_requirements.md`** — The user's EXACT requirements. Near-verbatim. Include original ask, corrections, preferences, decisions.
2. **Update `current_work.md`** — Full task state
3. **`session_decisions.md`** — Every "we chose X over Y because Z." Compaction loses reasoning.

**Why:** Compaction preserves WHAT but loses WHY and HOW THE USER WANTS IT.

#### Checkpoint Format (`current_work.md`):

```markdown
## Current Task
[One-line description]
## Status
- **Phase**: [planning|implementing|testing|debugging] — Step X of Y
- **Last action**: [last thing done]
## Progress
- [x] [Done steps]
- [ ] [Next steps]
## User Requirements (near-verbatim)
- [Original ask + corrections + preferences]
## Decisions & Context
- [Key decisions with reasoning, gotchas, failed approaches]
## Files Modified
- `path/to/file` — [what changed]
## Resume Instructions
[Exactly what to do next]
```

#### Checkpoint Rules:
1. **Overwrite, don't append** — always the LATEST state, not a log
2. **Keep it under 50 lines**
3. **Include file paths** — next session needs to know what was being touched
4. **Include the approach** — "fixing bug by adding null check in handleSubmit() in Form.jsx"
5. **Clear it when done** — update to "No active work" when task is complete

### Capture Signals (what to persist)

#### Architecture Decisions
- "Let's use X instead of Y" → Save what, what was rejected, and WHY
- New patterns established (file structure, convention, approach)

#### Discoveries & Gotchas
- Bug with non-obvious root cause → Save the root cause
- Environment quirk → Save the workaround
- API/library behavior that surprised you → Save correct behavior

#### User Preferences (about this project)
- "I prefer X over Y" / "Don't do X" / "Always do Y" → Save as rule
- Corrections to your approach → Save so you don't repeat

#### Project State Changes
- Version bumps, new features, known issues, significant dependency changes

### What NOT to Capture
- Routine code changes (git log has this)
- Implementation details (the code has this)
- Debugging steps (only save root cause + fix)
- Anything already in CLAUDE.md or MEMORY.md

## Phase 3: Session End — Structured Persist

### Session End Checklist

```
□ Architecture decisions made? → decisions_<topic>.md
□ Gotchas or surprises discovered? → gotchas.md
□ User corrected my approach or expressed preference? → user_preferences.md
□ Project state changed significantly? → Update MEMORY.md index
□ Bugs fixed with non-obvious root causes? → Verify error-memory saved
□ Work in progress? → current_work.md with status and next steps
```

### Curation Rules (Quality Gate)

| Filter | Test |
|--------|------|
| **Relevance** | Will this help in future sessions for THIS project? |
| **Non-redundancy** | Duplicates something already in memory? Merge or skip. |
| **Atomicity** | One idea per bullet. Short, self-contained. |
| **Verifiability** | Backed by code evidence or repeated observation? |
| **Stability** | Will this remain true? Call out version-specifics. |

**Categorize by impact:** Critical (prevents major issues) → always save. High → save. Medium → save if space. Low → skip unless pattern repeats.

### Memory File Format

```markdown
---
name: [descriptive name]
description: [one-line — specific enough to know when to load]
type: [project|feedback|user|reference]
---
[Content — structured, concise, actionable]
```

Update MEMORY.md index after creating/updating files. Keep index under 200 lines.

## Memory Organization

- **Merge, don't duplicate** — Check existing files first. Aim for 5-15 files, not 50.
- **Prune stale memories** — Update or remove outdated entries. Never let stale memories mislead.

## Rules

1. **Load silently, save automatically** — don't announce hydration
2. **Merge, don't duplicate; prune stale**
3. **Save reasoning and user corrections** — WHY + corrections are high-priority saves
4. **"Would I Forget?" test** — "If I started tomorrow, what would I wish I knew?" Save it.
5. **Never save secrets** — no API keys, passwords, or credentials
6. **Review anti-patterns proactively** — scan for reasoning failures relevant to today's task, not just when debugging
