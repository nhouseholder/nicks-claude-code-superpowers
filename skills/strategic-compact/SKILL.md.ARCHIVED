---
name: strategic-compact
description: Suggests manual context compaction at logical intervals to preserve context through task phases rather than arbitrary auto-compaction.
weight: light
origin: ECC
---

# Strategic Compact Skill

Suggests manual `/compact` at strategic points in your workflow rather than relying on arbitrary auto-compaction.

## When to Activate

- Running long sessions that approach context limits (200K+ tokens)
- Working on multi-phase tasks (research → plan → implement → test)
- Switching between unrelated tasks within the same session
- After completing a major milestone and starting new work
- When responses slow down or become less coherent (context pressure)
- **BEFORE spawning large agents** — If context is already substantial, compact first. A large agent response can fill remaining context, making "continue" impossible.

## The #1 Rule: Files Are More Reliable Than Memory After Compaction

Files are more reliable than conversation memory after compaction. Write critical state (current progress, decisions, blockers) to files before compaction. But compaction summaries still help with orientation — they're complementary, not useless.

Before any compaction or handoff, ask: **"What do I know right now that exists ONLY in conversation context?"** Write it to a file. Then compact.

This is the difference between a useful compaction and a lossy one:
- **Bad**: Compact → summary says "user wants feature X" → loses all the nuance
- **Good**: Write user requirements to `session_requirements.md` → compact → summary can be vague because the file has everything

## Why Strategic Compaction?

Auto-compaction triggers at arbitrary points:
- Often mid-task, losing important context
- No awareness of logical task boundaries
- Can interrupt complex multi-step operations

Strategic compaction at logical boundaries:
- **After exploration, before execution** — Compact research context, keep implementation plan
- **After completing a milestone** — Fresh start for next phase
- **Before major context shifts** — Clear exploration context before different task

## How It Works

The `suggest-compact.js` script runs on PreToolUse (Edit/Write) and:

1. **Tracks tool calls** — Counts tool invocations in session
2. **Threshold detection** — Suggests at configurable threshold (default: 50 calls)
3. **Periodic reminders** — Reminds every 25 calls after threshold

## Configuration

Environment variables:
- `COMPACT_THRESHOLD` — Tool calls before first suggestion (default: 50)

## Auto-Handoff: Better Than Repeated Compaction

**The problem with repeated compaction**: Each compaction loses fidelity. After 2-3 compactions, nuanced details, user preferences, approach decisions, and subtle context degrade. The summary of a summary of a summary is a skeleton.

**The solution**: When context is running low, create a full handoff document and advise starting a fresh session instead of compacting again.

### When to Trigger Auto-Handoff (instead of compaction)

| Situation | Action |
|-----------|--------|
| **First time context is low** | Compact — fidelity loss is minimal |
| **After 2+ compactions in a session** | Suggest a handoff document — fidelity is degrading |
| **After 3+ compactions in a session** | Strongly recommend pausing and resuming in a fresh session — context quality degrades significantly beyond this point |
| **Complex multi-step task still in progress** | Auto-handoff — too much state to survive compaction |
| **User has given detailed requirements this session** | Auto-handoff — requirements MUST survive intact |
| **Debugging session with deep context** | Auto-handoff — root cause analysis needs full detail |

### Handoff Protocol

When auto-handoff triggers, follow the `auto-handoff` skill's handoff document protocol — it owns the template, format, and delivery message. Write to `~/.claude/projects/<project>/memory/handoff.md` and commit to GitHub.

## Compaction Decision Guide

Use this table when compaction (not handoff) is appropriate:

| Phase Transition | Compact? | Why |
|-----------------|----------|-----|
| Research → Planning | Yes | Research context is bulky; plan is the distilled output |
| Planning → Implementation | Yes | Plan is in TodoWrite or a file; free up context for code |
| Implementation → Testing | Maybe | Keep if tests reference recent code; compact if switching focus |
| Debugging → Next feature | Yes | Debug traces pollute context for unrelated work |
| Mid-implementation | No | Losing variable names, file paths, and partial state is costly |
| After a failed approach | Yes | Clear the dead-end reasoning before trying a new approach |
| **Already compacted once** | **No — use auto-handoff instead** | **Compounding fidelity loss** |

## What Survives Compaction

Understanding what persists helps you compact with confidence:

| Persists | Lost |
|----------|------|
| CLAUDE.md instructions | Intermediate reasoning and analysis |
| TodoWrite task list | File contents you previously read |
| Memory files (`~/.claude/memory/`) | Multi-step conversation context |
| Git state (commits, branches) | Tool call history and counts |
| Files on disk | Nuanced user preferences stated verbally |

## Pre-Agent Compaction

**Before spawning any agent that will produce large output** (research, planning, code generation), check:
- Has this session already had 30+ tool calls?
- Have multiple large files been read?
- Has a previous agent already returned results this session?

If yes to any → **compact first, then spawn the agent.** An agent that consumes remaining context leaves the user unable to say "continue" — Claude literally cannot respond.

This is the #1 cause of the "continue gets no response" bug.

## Pre-Compact Checkpoint (MANDATORY)

**Before EVERY `/compact`, save a checkpoint file.** This is the difference between safe compaction and lossy compaction.

Write to `~/.claude/projects/<project>/memory/pre_compact_checkpoint.md` (overwritten each time):

```markdown
# Pre-Compact Checkpoint — <timestamp>

## What we were doing
<1-2 sentence summary of current task>

## Key numbers / data computed this session
<Any stats, counts, P/L figures, measurements — these WILL be lost in compaction>

## Decisions made
<Approach choices, user preferences stated this session, "we decided X because Y">

## Current progress
<What's done, what's next, any blockers>

## Files modified this session
<List of files changed and why>
```

**After compaction, the first thing to do is re-read this file.** It costs ~200 tokens to read but saves thousands in re-discovery.

**When NOT to checkpoint** (skip the file, just compact):
- Very short sessions (<10 tool calls)
- No data or decisions to preserve
- Session was purely exploratory with no conclusions

## Best Practices

1. **Checkpoint then compact** — Write the checkpoint file, then `/compact`
2. **Compact after planning** — Once plan is finalized in TodoWrite, compact to start fresh
3. **Compact after debugging** — Clear error-resolution context before continuing
4. **Don't compact mid-implementation** — Preserve context for related changes
5. **Read the suggestion** — The hook tells you *when*, you decide *if*
6. **Use `/compact` with a summary** — Add a custom message: `/compact Focus on implementing auth middleware next`
7. **Compact before large agents** — If context is substantial, compact before spawning agents that will produce heavy output
8. **Re-read checkpoint after compaction** — First action post-compact: read `pre_compact_checkpoint.md`

## Related

- [The Longform Guide](https://x.com/affaanmustafa/status/2014040193557471352) — Token optimization section
- Memory persistence hooks — For state that survives compaction
- `continuous-learning` skill — Extracts patterns before session ends
