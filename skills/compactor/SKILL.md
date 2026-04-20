---
name: compactor
description: Unified context management and session continuity skill. Combines total-recall, strategic-compact, /ledger, and session continuity. Runs in background to preserve critical context across compaction and sessions.
use_when: >
  The user explicitly says "use compactor", "call compactor", "run compactor",
  "use context manager", "call context manager", "use ledger", "call ledger",
  "use state saver", "call state saver", "use memory", "call memory".
  OR context is getting long, session is about to end, user says "compact", "save context",
  "ledger", "remember this", or starting a new session that needs prior context.
  OR you detect context pressure (responses slowing, tool call count > 50, approaching token limits).
---

# COMPACTOR — Unified Context Management

The single context/continuity skill. Replaces total-recall, strategic-compact, /ledger.

## CRITICAL: Compaction vs Handoff Decision

**This is the #1 cause of sessions getting stuck at 145k+ context.** Follow this decision tree:

| Situation | Action |
|-----------|--------|
| **First time context is low** | Compact — fidelity loss is minimal |
| **After 2+ compactions in a session** | HANDOFF — write handoff.md, start new session |
| **After 3+ compactions in a session** | STRONGLY RECOMMEND new session — context quality degrades significantly |
| **Complex multi-step task still in progress** | HANDOFF — too much state to survive compaction |
| **User has given detailed requirements this session** | HANDOFF — requirements MUST survive intact |
| **Debugging session with deep context** | HANDOFF — root cause analysis needs full detail |
| **Before spawning large agent on heavy context** | Compact first, then spawn — prevents "continue" being impossible |

**Never use extended context to fight compression.** It burns per-minute rate limits. Handoff to a new session instead.

## Background Behavior (always active)

### Context Preservation Points
At logical boundaries (after completing a task, before switching topics, after significant code changes):

```bash
# Capture current state
git status --short
git log --oneline -5
pwd
```

Save a compact state snapshot to `thoughts/ledgers/CONTINUITY_$(date +%Y-%m-%d_%H%M).md`:

```markdown
# Continuity Ledger — [Project] — [Date Time]

## Current Task
[What we're working on right now]

## Key Decisions Made
- [Decision 1]: [rationale]
- [Decision 2]: [rationale]

## Critical Context (survives compaction)
- [File paths that matter]
- [Variables/constants that must not change]
- [Patterns/conventions in use]
- [Open questions pending]

## Anti-Patterns to Avoid
- [Specific to this session/project]

## Next Action
[Exactly where to pick up]
```

## Compaction Protocol (Two-Phase)

### Phase 1: Memory Extract (BEFORE summary — MANDATORY)

**Extract durable knowledge into persistent memory FIRST.** This is the whole point of compaction — if you skip this, the knowledge dies with the context window.

For each learning, decision, and user preference discovered this session, save to MCP memory:

```
For each LEARNING (anti-pattern, gotcha, discovery):
  → engram_mem_save(title="...", type="bugfix|pattern|discovery|learning", content="**What**: ... **Why**: ... **Where**: ...")

For each DECISION (choice with rationale):
  → brain-router_brain_save(title="...", content="...", type="decision", topic_key="...")

For each USER PREFERENCE (not in any config file):
  → brain-router_brain_save(title="...", content="...", type="config", topic_key="user-prefs")

For the SESSION SUMMARY:
  → engram_mem_session_summary(project="...", content=full summary from Phase 2)
```

**Skip Phase 1 only when:**
- Session was <10 tool calls with no decisions or learnings
- Session was purely exploratory with no conclusions
- Already saved mid-session after a major decision

### Phase 2: Write Compaction Summary (AFTER memory saves)

Write the compaction summary using the **exact format below**. This is what survives in the context window after compaction — keep it tight and high-yield.

**Target: 600-1000 words. Hard cap: 1000 words.**

```markdown
# Session: [Project Name] — [YYYY-MM-DD]

## Learnings
<!-- Things discovered this session that will matter again. Be specific. -->
- [Anti-pattern]: [what happened, why it's bad, how we fixed it]
- [Gotcha]: [non-obvious thing that will trip us up again + workaround]
- [Discovery]: [something learned about the codebase, tools, or process]

## Decisions
<!-- Choices made this session with rationale. One sentence each. -->
- [Decision]: [rationale]
- [Decision]: [rationale]

## User Preferences
<!-- Stated preferences NOT in any config file. Skip if none. -->
- [Preference]: [value]

## Current State
<!-- Factual snapshot. No narrative. -->
- **Project:** [path]
- **Repo:** [name] (branch: [branch])
- **Last commit:** [hash] "[message]"
- **Files changed:** [key files only, not every file]
- **Pushed:** [yes/no]
- **Uncommitted work:** [what, if anything]

## What's Next
<!-- Single next action. Delete if session is complete. -->
- [action]
```

#### Word Budget Per Section

| Section | Budget | Guidance |
|---|---|---|
| Learnings | ~200 words | Only include things that will matter in a future session. Skip exploration dead-ends. |
| Decisions | ~100 words | One sentence per decision. Focus on "why", not "what" — the what is in git. |
| User Preferences | ~50 words | Only preferences NOT already in CLAUDE.md, AGENTS.md, or config files. |
| Current State | ~100 words | Factual only. No narrative. Git log gives you the history. |
| What's Next | ~25 words | Single action or "complete". |
| Header + formatting | ~50 words | Project name, date. |
| **Total** | **~525-1000** | **If you're over 1000, you're including narrative. Cut it.** |

#### What to CUT (never include)

- File read/write logs ("we read README.md on line 16")
- Explained-and-rejected approaches (unless the rejection itself is a learning)
- Step-by-step narrative of what happened ("first we edited X, then we checked Y")
- Error messages (keep root cause only, as a learning)
- System prompt content (survives compaction already — never duplicate it)
- Todo/progress tracking (already completed items are dead text)
- Verbose rationale (one sentence per decision, not a paragraph)

## Auto-Handoff Protocol (when compaction is NOT appropriate)

When the decision table above says HANDOFF:

1. **Write** `handoff.md` in project memory (`~/.claude/projects/<project>/memory/handoff.md`):
   ```markdown
   # Handoff — [Project] — [Date Time]

   ## Objective
   [What we're trying to achieve]

   ## Current Status
   [Where we are, what's done, what's pending]

   ## Key Decisions
   - [Decision]: [rationale]

   ## Files Modified
   - [path]: [what changed]

   ## Failed Approaches
   - [What we tried and why it didn't work]

   ## Resume Instructions
   [Exactly what to do next, step by step]
   ```

2. **Commit** to GitHub (from /tmp clone if iCloud repo)
3. **Notify** user: "Context compression incoming — handoff prepped. Start new session and say 'read handoff.md and continue'"
4. **Update** `current_work.md` too

## Session Continuity Protocol

### On Session Start:
```bash
# Find most recent ledger for this project
ls -t thoughts/ledgers/ 2>/dev/null | head -3
# Read project CLAUDE.md, AGENTS.md
# Read recent handoffs
git log --oneline -10
```

### On Session End:
1. Update continuity ledger with current state
2. Commit ledger changes
3. Output: "Ledger saved. Next session will pick up from: [path]"

## Memory Persistence

### Save Rhythm (compaction-paired, NOT scattered)

Memory saves are batched with compaction events — not saved after every task.

**ORDER MATTERS: Memory extract → Summary write.** Always save to persistent memory BEFORE writing the compaction summary. The summary is what stays in-context; the MCP saves are what persists across sessions.

| Event | Phase 1: Memory Extract | Phase 2: Summary |
|---|---|---|
| **Before compaction** | `engram_mem_save` each learning + `brain-router_brain_save` each decision/preference | Write compaction summary (600-1000 words, exact format) |
| **Session end** | `engram_mem_session_summary` + `brain-router_brain_save` final state | Write to handoff.md if session was complex |
| **Major decision mid-session** | `engram_mem_save` + `brain-router_brain_save` (skip if already saved) | No summary needed — just the memory saves |
| **NEVER** | Do NOT write to mempalace. It's read-only. Checkpoint/ledger files handle verbatim storage. | Do NOT duplicate system prompt content or file read logs |

### Project-Level Memory (disk files)
Each project maintains:
- `thoughts/ledgers/` — session continuity files
- `handoffs/` — end-of-session summaries
- `docs/superpowers/specs/` — design decisions
- `docs/superpowers/plans/` — implementation plans

### Global Memory
- `~/.claude/anti-patterns.md` — recurring mistakes across all projects
- `~/.claude/projects/*/memory/MEMORY.md` — project-specific long-term memory

## Compaction Rules

1. **Memory extract FIRST** — always save to engram + brain-router before writing the summary
2. **Use the exact format** — headers are: Learnings, Decisions, User Preferences, Current State, What's Next
3. **600-1000 words, hard cap at 1000** — if you're over, you're including narrative. Cut it
4. **Extract knowledge, not narrative** — "never use parenthetical aliases" > "we edited line 16 of USAGE.md"
5. **One sentence per decision** — focus on "why", not "what" — the what is in git
6. **Current State is factual only** — paths, hashes, status. No story.
7. **What's Next is a single action** — delete the section if the session is complete
8. **Handoff over extended context, always** — never fight compression with rate-limited extended context
9. **Track compaction count** — at 2+ compactions in a session, switch to handoff
10. **Pre-agent compaction** — compact before spawning large agents on heavy context
11. **Never duplicate system prompt content** — it survives compaction already
12. **Never include file read/write logs** — git tracks what changed, not how you got there

## Compaction Decision Guide

| Phase Transition | Compact? | Why |
|-----------------|----------|-----|
| Research → Planning | Yes | Research context is bulky; plan is the distilled output |
| Planning → Implementation | Yes | Plan is in TodoWrite or a file; free up context for code |
| Implementation → Testing | Maybe | Keep if tests reference recent code; compact if switching focus |
| Debugging → Next feature | Yes | Debug traces pollute context for unrelated work |
| Mid-implementation | No | Losing variable names, file paths, and partial state is costly |
| After a failed approach | Yes | Clear the dead-end reasoning before trying a new approach |
| **Already compacted once** | **No — use auto-handoff instead** | **Compounding fidelity loss** |

## Example: Good Compaction Output

```markdown
# Session: opencode-agent-system — 2026-04-20

## Learnings
- Parenthetical aliases next to @agent references (e.g. "@explorer (codebase exploration)") cause ProviderModelNotFoundError in opencode. Never use them — just @explorer.
- Commander is Desktop Commander MCP server, not an opencode agent. Octto is Claude Code CLI built-in tool system. Neither should appear in agent routing config.
- opencode.json is the source of truth for registered agents — if a name isn't in this file, routing fails silently. Rebase conflicts can silently overwrite it.

## Decisions
- Structural anti-loop guards (table-based processing with required outputs) over advisory text — advisory guidelines get ignored by LLMs in analysis mode.
- Mempalace is read-only in save rhythm — checkpoint/ledger files on disk already serve verbatim storage, mempalace is for semantic search only.
- Shipper merged into generalist instead of re-registering — it was already broken (not in opencode.json), and generalist already handles medium operational tasks.

## User Preferences
- Commit and push after every change, not batched
- Sync to both repos: 10-agent-team (primary) and superpowers (mirror)
- Valid agent names are the only 9: orchestrator, explorer, strategist, researcher, designer, auditor, council, generalist, refiner

## Current State
- **Project:** ~/.config/opencode/
- **Repo:** nhouseholder/10-agent-team (main)
- **Last commit:** d74a8cc "docs: purge all stale agent references"
- **Files changed:** compactor/SKILL.md, README.md, docs/*, examples/*.json
- **Pushed:** yes
- **Uncommitted work:** compactor/SKILL.md (this edit)

## What's Next
- Commit compactor update and push to both repos
```

**Word count: ~180.** This is a minimal session — most sessions will be 600-1000 words. The point: even a complex session should feel this organized and scannable.

## What Survives Compaction

| Persists | Lost |
|----------|------|
| CLAUDE.md instructions | Intermediate reasoning and analysis |
| TodoWrite task list | File contents you previously read |
| Memory files (`~/.claude/memory/`) | Multi-step conversation context |
| Git state (commits, branches) | Tool call history and counts |
| Files on disk | Nuanced user preferences stated verbally |
