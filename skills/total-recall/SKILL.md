---
name: total-recall
description: Infinite cross-session memory for projects. Automatically loads all project context at session start and saves everything important at session end. Ensures Claude remembers all decisions, architecture changes, gotchas, user preferences, and project state between sessions — no manual /mem save required. Always-on awareness skill scoped to the current project directory.
---

# Total Recall — Infinite Project Memory Across Sessions

Never lose context between sessions. Automatically remember everything important about the project — decisions, discoveries, gotchas, user preferences, current state — and reload it all when the next session starts.

## Always Active

This skill has two phases that fire automatically:
1. **Session Start** — hydrate context from all memory sources
2. **Session End** — persist everything important from this session

Plus a continuous awareness during the session to capture important moments as they happen.

## Phase 1: Session Start — Full Context Hydration

At the beginning of every session, load project context from ALL available sources:

### Auto-Load Sequence (Lazy Loading)

**Always load (lightweight — index only):**
```
1. Read ~/.claude/projects/<project>/memory/MEMORY.md (index)
2. Check git status (current state)
```

**Load on demand (when the task requires it):**
```
3. Read specific memory files referenced in MEMORY.md — only when relevant to the current task
4. Read ~/.claude/anti-patterns.md — only when debugging or fixing errors
5. Read AGENT-MEMORY.md — only when coordinating with other agents
6. Check git log --oneline -20 — only when context about recent work is needed
```

The MEMORY.md index tells you WHAT memories exist. Only read the full memory files when the current task actually needs that knowledge. This avoids loading thousands of tokens of context that may be irrelevant to a simple "fix this typo" request.

### What to Extract
From loaded sources, build a mental model of what's relevant to the current task. Don't try to hold everything — just know where to find it.

### Don't Announce It
Load silently. Don't say "I've loaded your project memory" — just know it. The user should feel like you've always known this project.

## Phase 2: During Session — Continuous Capture + Crash-Safe Checkpoints

Throughout the session, watch for **capture signals** (moments worth persisting) AND **checkpoint triggers** (moments where progress must be saved in case the session dies).

### Crash-Safe Checkpointing

**The problem**: If the session crashes mid-task (lost WiFi, app crash, token limit), Phase 3 never fires. Everything not yet persisted is lost. The next session starts blind.

**The fix**: Write `current_work.md` checkpoints DURING the session, not just at the end.

#### When to Checkpoint (write/update `current_work.md`):

| Trigger | Why |
|---------|-----|
| **After completing a major step** in a multi-step task | Progress is saved even if the next step crashes |
| **Before a risky operation** (large refactor, deploy, migration) | If it goes wrong and kills the session, you know where you were |
| **Every 15-20 tool calls** on long tasks | Periodic safety net — don't let more than ~5 min of work go unsaved |
| **When the user provides important context** | Their requirements survive even if the session dies immediately after |
| **After a plan is agreed on** | The plan persists even if execution never starts |
| **Before compaction** | This is the MOST CRITICAL checkpoint — everything not in a file is about to degrade |

#### Pre-Compaction Capture (critical for long sessions)

When context is getting long (50+ tool calls, or you sense compaction approaching):

**Write to project memory files — NOT just current_work.md:**

1. **`session_requirements.md`** — The user's EXACT requirements from this session. Not summarized. Near-verbatim. Include:
   - What they asked for originally
   - Every correction or clarification they gave
   - Preferences expressed ("I want it this way", "don't do X")
   - Decisions made ("let's use approach A")

2. **Update `current_work.md`** — Full task state as usual

3. **`session_decisions.md`** — Every "we chose X over Y because Z" from this session. Compaction summaries lose the reasoning.

**Why this matters**: Compaction preserves WHAT you're doing but loses WHY and HOW THE USER WANTS IT. A compacted summary says "implementing feature X" but drops "user specifically said to use approach A, not B, because they tried B last week and it broke."

The files survive compaction perfectly. The conversation doesn't.

#### Checkpoint Format (`current_work.md`):

```markdown
---
name: current-work
description: In-progress task state — read this first when resuming after a crash or new session
type: project
---

## Current Task
[One-line description of what's being done]

## Status
- **Phase**: [planning | implementing | testing | debugging | deploying]
- **Progress**: [Step X of Y — what's done, what's next]
- **Last action**: [The last thing Claude did before this checkpoint]

## Completed So Far
- [x] [Step 1 — done]
- [x] [Step 2 — done]
- [ ] [Step 3 — in progress / next]
- [ ] [Step 4 — not started]

## User's Requirements (near-verbatim)
- [What they originally asked for]
- [Corrections/clarifications they gave]
- [Preferences: "do it this way", "don't do X"]

## Decisions Made
- [Chose X over Y because: user said / technical reason / tested and confirmed]

## Key Context
[Anything else a new session would need — approach chosen, gotchas discovered, failed attempts]

## Files Modified This Session
- `path/to/file.js` — [what was changed]
- `path/to/other.py` — [what was changed]

## Resume Instructions
[Exactly what to do next if picking up from this checkpoint]
```

#### Checkpoint Rules:
1. **Overwrite, don't append** — `current_work.md` is always the LATEST state, not a log
2. **Keep it under 50 lines** — it needs to be fast to read on resume
3. **Include file paths** — the next session needs to know what was being touched
4. **Include the approach** — don't just say "fixing bug", say "fixing bug by adding null check in handleSubmit() in Form.jsx"
5. **Clear it when done** — when the task is complete, update to "No active work" so the next session doesn't try to resume finished work

### Capture Signals (what to persist to memory files)

#### Architecture Decisions
- "Let's use X instead of Y" → Save: what was chosen, what was rejected, and WHY
- "The reason we're doing it this way is..." → Save the reasoning
- New patterns established (new file structure, new convention, new approach)

#### Discoveries & Gotchas
- Bug with a non-obvious root cause → Save the root cause
- Environment quirk → Save the workaround
- "Oh, that's why it wasn't working" → Save the insight
- API/library behavior that surprised you → Save the correct behavior

#### User Preferences (about this project)
- "I prefer X over Y" → Save
- "Don't do X" or "Always do Y" → Save as a rule
- Corrections to your approach → Save so you don't repeat the mistake
- Workflow preferences ("deploy to staging first", "always run tests before committing")

#### Project State Changes
- Version bumps → Update version in memory
- New features added → Update feature list
- Known issues discovered → Add to known issues
- Dependencies changed → Note significant additions/removals

### What NOT to Capture
- Routine code changes (the git log has this)
- Implementation details (the code has this)
- Debugging steps (only save the root cause + fix, not the journey)
- Anything already in CLAUDE.md or MEMORY.md

## Phase 3: Session End — Structured Persist

Before the session ends, persist important context. Use the project memory system at `~/.claude/projects/<project>/memory/`.

### The Session End Checklist

Run through this mentally:

```
□ Were any architecture decisions made this session?
  → Update or create memory file: decisions_<topic>.md

□ Were any gotchas or surprises discovered?
  → Update or create memory file: gotchas.md

□ Did the user correct my approach or express a preference?
  → Update memory file: user_preferences.md or feedback_<topic>.md

□ Did the project state change significantly?
  → Update MEMORY.md index with current state

□ Were any bugs fixed with non-obvious root causes?
  → Already handled by error-memory skill → verify it saved

□ Is there work in progress that the next session should continue?
  → Save to memory: current_work.md with status and next steps
```

### Memory File Format

Each memory file should use the standard format:
```markdown
---
name: [descriptive name]
description: [one-line — specific enough to know when to load it]
type: [project|feedback|user|reference]
---

[Content — structured, concise, actionable]
```

### Update MEMORY.md Index

After creating/updating memory files, ensure MEMORY.md has pointers to all of them. Keep the index under 200 lines (it's always loaded into context).

## Memory Organization

### By Topic, Not Chronology
```
~/.claude/projects/<project>/memory/
├── MEMORY.md                    ← Index (always loaded)
├── architecture.md              ← Stack, patterns, key decisions
├── gotchas.md                   ← Things that trip you up
├── user_preferences.md          ← How the user likes to work
├── current_work.md              ← In-progress tasks and next steps
├── feedback_<topic>.md          ← User corrections and guidance
├── decisions_<topic>.md         ← Why we chose X over Y
└── reference_<topic>.md         ← External resources and pointers
```

### Merge, Don't Duplicate
Before creating a new memory file, check if an existing one covers the topic. Update existing files rather than creating new ones. Keep the total count manageable (aim for 5-15 files, not 50).

### Prune Stale Memories
If a memory entry is clearly outdated (references removed features, old versions, deprecated approaches):
- Update it if the topic is still relevant
- Remove it if the topic is no longer relevant
- Never let stale memories mislead future sessions

## Integration with Existing Memory Systems

This skill orchestrates, not replaces, existing memory infrastructure:

```
total-recall (orchestrator)
    │
    ├─ Reads from:
    │   ├─ MEMORY.md + memory files (project memory)
    │   ├─ anti-patterns.md (error memory)
    │   ├─ AGENT-MEMORY.md (shared agent memory)
    │   └─ git log/status (recent history)
    │
    ├─ Writes to:
    │   ├─ MEMORY.md + memory files (primary store)
    │   └─ anti-patterns.md (via error-memory skill)
    │
    └─ Coordinates with:
        ├─ error-memory (debugging failures → anti-patterns)
        ├─ stop-memory-save.py hook (session end reminder)
        └─ shared-memory (AGENT-MEMORY.md updates)
```

## The "Would I Forget?" Test

Before ending a session, ask: **"If I started a new session tomorrow on this same project, what would I wish I knew?"**

Whatever comes to mind → save it.

## Rules

1. **Load silently** — don't announce memory hydration, just know the project
2. **Save automatically** — don't wait for `/mem save`, capture important moments as they happen
3. **Topic over time** — organize by subject, not by date
4. **Merge, don't duplicate** — update existing memories, don't create parallel files
5. **Prune stale** — outdated memories are worse than no memories (they mislead)
6. **Reasoning matters** — save WHY decisions were made, not just WHAT was decided
7. **User corrections are gold** — if the user corrects you, that's a high-priority save
8. **The "Would I Forget?" test** — run it before every session end
9. **Keep it under 200 lines** in MEMORY.md — it's always loaded, so keep it lean
10. **Never save secrets** — no API keys, passwords, or credentials in memory files
