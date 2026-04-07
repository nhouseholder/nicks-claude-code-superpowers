---
name: progress-tracker
description: Track and display progress across multi-step tasks. Shows completion percentage, elapsed time, task count, and milestone updates. Fires at natural task boundaries during multi-step work — not after every response. Gives the user visibility into complex work without cluttering simple tasks.
weight: light
---

# Progress Tracker — Multi-Step Visibility

## When This Fires

This skill activates when **all** of these are true:
1. There are 3+ distinct tasks/steps being worked on (use TodoWrite as the signal)
2. A task was just completed or failed
3. The user hasn't received a progress update in the last 2+ task completions

**Does NOT fire** for:
- Single-task work
- Quick fixes or Q&A
- When the user is actively directing each step (they can see progress themselves)

## What to Display

At natural milestones (every 2-3 completed tasks, or on failure), show a compact progress line:

```
Progress: 4/7 tasks done | ~12min elapsed | 2 remaining
```

### On Task Failure

```
Progress: 3/7 tasks done | 1 FAILED (retrying) | 3 remaining
```

### On Completion

```
All 7 tasks complete | ~18min total
```

## Rules

1. **One line only.** Never multi-line progress updates. Never paragraphs explaining progress.
2. **Don't count for the user.** If there are only 2 tasks, don't show progress — it's obvious.
3. **Time is approximate.** Use "~" prefix. Don't track to the second.
4. **Merge with response-recap.** If response-recap is also firing, let response-recap handle it — don't double up. Progress-tracker adds the numbers, response-recap adds the narrative.
5. **TodoWrite is the source of truth.** Read the current todo list to get task counts. Don't maintain a separate counter.
6. **Cost tracking.** If you have cost data from `claude -p` JSON output or from tool results that include cost, include it: `| ~$0.45 cost`. Otherwise omit — don't guess.

## Anti-Patterns

- Showing progress after every single task (too noisy)
- Multi-line progress displays with boxes and bars (save that for the orchestrator CLI)
- Estimating remaining time (unreliable, creates false expectations)
- Tracking progress for trivial work (adds overhead with no value)

## Integration with Orchestrator

When running inside the external `coder/orchestrator.py`, progress tracking is handled by the orchestrator's `print_progress()` function. This skill is for **interactive Claude Code sessions** where the orchestrator isn't running — it fills the same visibility gap but inside the conversation.
