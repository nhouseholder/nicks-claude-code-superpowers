---
name: auto-handoff
description: Detects when successive context compressions are degrading memory quality and proactively creates a full handoff document before context erodes. Recommends starting a new session with the handoff prepped locally and on GitHub. Always-on awareness skill that fires after the first compaction.
weight: passive
category: meta
---

# Auto-Handoff — Save Context Before It's Lost

## The Problem

Each context compression loses fidelity. After 2+ compressions, nuanced details, user preferences, approach decisions, and subtle context degrade. By the 3rd compression, Claude is working from a skeleton. The user says "continue" and Claude has forgotten what they were doing.

**This skill acts BEFORE the damage — not after.**

## When This Fires

### Compression Counter (Mental Tracking)
Track how many times context has been compressed this session:

| Compression Count | Action |
|---|---|
| **0** | Normal operation |
| **1st compression** | Note it. Start being concise. No action yet. |
| **2nd compression imminent** | **FIRE: Create handoff document NOW.** Don't wait for the compression to happen — you need full context to write a good handoff. |
| **2nd+ compression** | If you didn't handoff before the 2nd, do it immediately. Quality is already degrading. |

### Early Warning Signals
Before compression is forced, watch for:
- Responses getting slower (context pressure)
- You're unsure what the user originally asked (anchor erosion)
- Tool call history feels incomplete (you can't remember what you already tried)
- Large agent results just returned (context spike)

## The Handoff Protocol

**ALL 4 STEPS ARE MANDATORY. Step 3 (notify user) WITHOUT Step 1 (create file) is a FAILURE.**

The handoff document IS the deliverable. Saying "I recommend a new session" without writing the actual file is useless — the next agent has nothing to work from. If you didn't write the file, you didn't do a handoff.

### Step 1: Create the Handoff Document (MANDATORY — do this FIRST)

Write to `~/.claude/projects/<project>/memory/handoff.md`:

```markdown
# Session Handoff — [DATE]

## Original Objective
[User's request — as close to verbatim as possible]

## Current Status
- **Phase**: [planning|implementing|testing|debugging]
- **Progress**: Step [X] of [Y] — [description]
- **What's done**: [completed items]
- **What's next**: [exact next steps with file paths]

## Key Decisions Made
- [Decision]: chose [X] over [Y] because [reason]

## Files Modified This Session
- `path/to/file` — [what changed and why]

## Failed Approaches (Don't Retry)
- [Approach]: failed because [reason]

## User Rules & Preferences Active
- [Any rules set during this session]

## Algorithm/Model State (if applicable)
- [Current coefficients, accuracy numbers, baseline values]

## Exact Resume Instructions
1. [First thing the new session should do]
2. [Second thing]
3. [Continue from here]
```

### Step 2: Commit to GitHub

If working in an iCloud-synced directory, write the handoff to project memory but perform git operations (add, commit, push) from the project's non-iCloud clone (e.g., in /tmp/ or ~/tmp/). See CLAUDE.md git workflow.

```
git add handoff.md
git commit -m "Session handoff: [brief description of work in progress]"
git push
```

This ensures the next agent can access it from any machine.

### Step 3: Notify the User (ONLY after Steps 1-2 are done)

**Do NOT send this message until the file is written and committed.** If you tell the user "I've prepped a handoff document" but the file doesn't exist, you've lied.

Say exactly:

```
Context compression incoming — I recommend starting a new session. I've prepped a
full handoff document with everything we've done, all decisions, and exact next steps.

It's live locally and on GitHub for the new agent to access immediately.

To continue: start a new session and say "read handoff.md and continue"
```

### Step 4: Save to Project Memory Too

Also update `current_work.md` with the quick-reference version so `seamless-resume` can use it.

## Rules

1. **Act BEFORE the 2nd compression** — You need full context to write a good handoff. After compression, the handoff will be incomplete.
2. **Verbatim user requests** — Copy their original words, don't summarize their intent.
3. **Include failed approaches** — The next session MUST know what NOT to try.
4. **Include file paths** — Every file touched, with what changed.
5. **Commit to GitHub** — The handoff must be accessible from any machine/session.
6. **One clear message** — Don't bury the recommendation. Make it obvious: "start a new session."
7. **Don't fight compression** — If context is running low, the handoff IS the deliverable. Writing a good handoff is more valuable than squeezing out one more response.
