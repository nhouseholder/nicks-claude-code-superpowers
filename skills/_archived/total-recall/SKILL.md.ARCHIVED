---
name: total-recall
description: Cross-session memory, crash-safe checkpointing, automatic handoff before context degrades, and instant resume. Handles all persistence across sessions. Always-on.
weight: passive
---

# Total Recall — Memory, Handoff, and Resume

## Three Phases

1. **Session Start** — hydrate context from memory
2. **During Session** — checkpoint progress, detect context pressure
3. **Session End / Resume** — persist or pick up seamlessly

## Phase 1: Session Start

**Always load (lightweight):**
- `MEMORY.md` index in project memory
- `git status` (current state)
- `~/.claude/anti-patterns.md` (past mistakes)

**Load on demand:** specific memory files from MEMORY.md index, AGENT-MEMORY.md, git log — only when the task needs them. Load silently.

## Phase 2: During Session

### Crash-Safe Checkpointing

Write `current_work.md` checkpoints DURING the session:
- After completing major steps
- Before risky operations (refactor, deploy, migration)
- Every 15-20 tool calls on long tasks
- **Before compaction** (MOST CRITICAL)

**Pre-compaction capture:** Write `session_requirements.md` (user's exact requirements near-verbatim) and `session_decisions.md` (every "chose X over Y because Z"). Compaction preserves WHAT but loses WHY.

**Checkpoint format:** Current task, status/phase, progress checklist, user requirements, decisions, files modified, resume instructions. Keep under 50 lines. Overwrite (latest state), don't append.

### What to Capture
- Architecture decisions (what, what was rejected, WHY)
- Bug root causes and workarounds
- User preferences and corrections for this project
- Significant project state changes

### What NOT to Capture
- Routine code changes (git log has this)
- Implementation details (the code has this)
- Anything already in CLAUDE.md or MEMORY.md

## Phase 3: Auto-Handoff (Before Context Degrades)

### When to fire
Track context compressions mentally:
- **1st compression:** Note it, be concise
- **2nd compression imminent:** CREATE HANDOFF NOW (you need full context to write a good one)

**Never use `[1m]` extended context to fight compression.** It burns per-minute rate limits. Handoff to a new session instead.

### Handoff Protocol (ALL steps mandatory)
1. **Write** `handoff.md` in project memory (objective, status, decisions, files modified, failed approaches, resume instructions)
2. **Commit** to GitHub (from /tmp clone if iCloud repo)
3. **Notify** user: "Context compression incoming — handoff prepped. Start new session and say 'read handoff.md and continue'"
4. **Update** `current_work.md` too

## Phase 4: Seamless Resume

### When user sends "continue" / "go" / "keep going"

**Same session (after pause/compaction):**
- Check what was in progress → continue immediately
- One-line status max if context was lost, then execute
- Never re-explain, re-read unnecessarily, or say "welcome back"

**New session:**
1. Check `handoff.md` → follow its resume instructions
2. No handoff? Check `current_work.md` → pick up at first incomplete step
3. Neither? Check git log, ask user what to work on

**After resuming:** Clear handoff.md and current_work.md so next session doesn't re-resume.

## Rules

1. Load silently, save automatically
2. Merge, don't duplicate; prune stale memories
3. Save reasoning and user corrections (WHY is high-priority)
4. "Would I Forget?" test — if starting tomorrow, what would I wish I knew?
5. Never save secrets (API keys, passwords)
6. Act BEFORE 2nd compression — you need full context to write a good handoff
7. "Continue" means GO — one line confirming what you're resuming ('Continuing with [task] from [step]'), then execute. No preamble beyond that.
8. Handoff over extended context, always
