---
name: context-checkpoint
description: Monitors context window usage, creates compact recovery checkpoints before compaction, and shows progress updates at task milestones. Prevents the #1 cause of broken sessions — losing track of what was done, what was decided, and what's next.
weight: passive
---

# Context Checkpoint — Survive Compaction

## Why This Exists

When Claude's context window fills up, older messages get compacted (summarized and compressed). This destroys:
- What files were changed and why
- Decisions made during the session
- The current task state (what's done, what's next)
- User corrections and preferences expressed during the session

This skill makes Claude proactively create checkpoints so compaction doesn't erase critical state.

## When This Fires (Passive — Always On)

Monitor these signals continuously:

### Checkpoint Triggers
1. **After completing 3+ tasks** in a single session — create a running summary
2. **After any major decision** (architecture choice, approach selection, user correction) — note it
3. **Before starting a large multi-file change** — checkpoint current state
4. **When the conversation feels long** (many back-and-forth exchanges) — create a state snapshot
5. **After any context compaction happens** — immediately re-establish critical state from the todo list, plan file, and any persisted artifacts

### What Goes in a Checkpoint

A checkpoint is NOT a handoff. It's a lightweight, in-session state marker. Keep it to the todo list and a mental model:

```
STATE CHECKPOINT:
- Working on: [current task]
- Completed this session: [list]
- Key decisions: [choices made and why]
- User corrections: [anything the user corrected]
- Files touched: [list with what changed]
- Next up: [what comes after current task]
- Critical context: [anything that would be catastrophic to forget]
```

## How to Checkpoint

### Method 1: Todo List (Primary)
The todo list survives compaction. Keep it updated in real-time:
- Mark tasks completed immediately when done
- Add discovered subtasks as they emerge
- The todo list IS your checkpoint — if compaction hits, the todo list tells you where you are

### Method 2: Plan File
If you're in plan mode or executing a plan, the plan file on disk survives compaction. Write progress to it.

### Method 3: Git Commits
Each commit is a permanent checkpoint. Commit between tasks (Rule 1 from CLAUDE.md). The commit message records what was done and why.

## Recovery Protocol (After Compaction)

If you notice context has been compacted (earlier messages are summarized):

1. **Read the todo list** — it shows what's done and what's pending
2. **Check git log** — see what was committed this session
3. **Read any plan file** — if executing a plan, it has the full roadmap
4. **Check open files** — what was being edited?
5. **DO NOT re-do completed work** — trust your checkpoints
6. **DO NOT ask the user "what were we working on?"** — figure it out from artifacts

## Progress Display (merged from progress-tracker)

At natural milestones (every 2-3 completed tasks, or on failure), show a compact one-line progress update:

```
Progress: 4/7 tasks done | ~12min elapsed | 2 remaining
```

On failure: `Progress: 3/7 tasks done | 1 FAILED (retrying) | 3 remaining`
On completion: `All 7 tasks complete | ~18min total`

**Rules:** One line only. Don't show for <3 tasks. TodoWrite is the source of truth for counts. Don't estimate remaining time. Don't show after every single task — every 2-3 completions.

## Integration

- **user-rules**: Rules captured during the session should be persisted to the rules file immediately, not held in context
- **error-memory**: Debug findings should be written to anti-patterns.md immediately, not held in context

## The Golden Rule

**If losing this information would break the session, persist it NOW — don't hold it in context.**

Ways to persist:
- Todo list (survives compaction)
- Plan file on disk (survives everything)
- Git commit (permanent)
- Memory file (survives across sessions)
- Comment in the code being edited (survives everything)

Context is volatile. Disk is permanent. Act accordingly.
