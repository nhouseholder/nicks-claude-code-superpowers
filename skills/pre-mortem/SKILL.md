---
name: pre-mortem
description: Before starting complex tasks, predict the 3 most likely failure modes and plan around them. Prevents approach-level mistakes that no amount of testing catches after the fact. Fires on multi-file changes, data tasks, and anything touching shared logic.
weight: passive
---

# Pre-Mortem — What Will Go Wrong?

Before committing to an approach on complex tasks, spend 10 seconds predicting failures.

## When to Fire

- Multi-file changes where files share state or logic
- Data/math tasks (P/L, stats, predictions, calculations)
- Editing shared functions used by multiple callers
- Refactors that touch more than one subsystem
- Any task where "undo" would be painful

**Skip for:** single-file edits, config changes, cosmetic updates, running commands.

## The Check (3 Questions)

Before writing code, answer silently:

1. **What assumption am I making that could be wrong?**
   - "I assume this function is only called from here" — verify it
   - "I assume this data format is consistent" — check an edge case

2. **What will this break that I'm not currently looking at?**
   - Other callers of the function I'm editing
   - Other bet types / data categories / tabs / pages that share this logic
   - Tests that depend on the current behavior

3. **What's my rollback plan if this makes things worse?**
   - Commit before changing (checkpoint)
   - Know which files to revert
   - Record baseline values before modifying

## Action

- If any answer reveals risk → address it before coding (add a guard, check other callers, record baseline)
- If no risks found → proceed normally, no output needed
- **Never announce the pre-mortem** — just do it silently. Zero token cost when risks are clear.

## Rules

1. Silent by default — only surface a concern if it changes the approach
2. Never skip for shared-logic edits — this is where regressions live
3. Takes 10 seconds of thought, not 10 minutes of analysis
4. If you find a risk, fix the plan before writing code — don't fix it after
