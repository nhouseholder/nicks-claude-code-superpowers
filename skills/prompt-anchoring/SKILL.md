---
name: prompt-anchoring
description: Keeps Claude anchored to the original prompt objective during long, complex sessions. Periodic self-checks prevent drift without reducing proactivity. Fires on complex/multi-step tasks — invisible on simple ones. The antidote to "Claude ADHD" where too many proactive skills cause loss of focus.
---

# Prompt Anchoring — Stay On Task Without Losing Intelligence

Prevents drift during long sessions where proactive skills collectively pull attention away from the user's actual objective.

## When This Fires

**Active on:**
- Tasks expected to take 10+ tool calls
- Multi-step implementations with several files
- Long-running backtests or parameter explorations
- Debugging sessions that have gone through 3+ hypotheses
- Any task where Claude has been working for a while

**Silent on:**
- Quick fixes, config changes, simple edits
- Tasks that complete in 1-5 tool calls
- Clear, single-objective requests

## The Anchor

At the start of any complex task, Claude mentally sets an **anchor** — a one-sentence statement of the user's core objective. This anchor is the North Star for the entire session.

### Setting the Anchor

When work begins on a complex task, distill the user's request to its essence:

- "User wants the quiz results page to show terpene breakdowns" — NOT "user wants UI work"
- "User wants to test whether home-court advantage improves future predictions" — NOT "user wants backtesting"
- "User wants the dispensary map to load faster" — NOT "user wants performance work"

The anchor must be **specific enough to evaluate drift against**. "Fix the bug" is too vague. "Fix the infinite re-render on the Compare page when switching strains" is an anchor.

## Anchor Persistence — Surviving Context Pressure

The anchor MUST survive context compaction, agent returns, and session interruptions. If you lose the anchor, you lose the user's goal.

### How to Persist the Anchor
- **Write it to TodoWrite** — The first task should be the anchor itself (e.g., "Build AI post-event analysis system")
- **Write it to current_work.md** — For crash recovery
- **After agent calls return** — Immediately re-read the anchor before doing anything else

### Post-Agent Recovery
When a spawned agent completes:
1. Re-read your TodoWrite tasks — what was the user's original request?
2. Report the agent's results
3. Continue the ORIGINAL task, not random other work

**The #1 failure mode:** Agent returns → Claude picks up unrelated smaller tasks instead of continuing the original request. This happens because the agent result fills context and pushes the original request out of immediate memory. The TodoWrite anchor prevents this.

## The Drift Check — Automatic and Invisible

### When to Check

Perform a silent drift check:
- Every 8-10 tool calls during sustained work (every 20+ calls, do an explicit re-anchor: what was the original request? what's done? what remains?)
- When about to start working on something that feels tangentially related
- After completing a sub-task, before starting the next action
- When you notice you're 3+ files away from where you started
- After fixing a bug you discovered mid-task

### The Check (Mental, Zero Tokens)

Ask yourself:
1. **What did the user ask me to do?** (recall the anchor)
2. **Is what I'm doing RIGHT NOW advancing that goal?**
3. **If I explained my current action to the user, would they say "yes, that's what I need" or "why are you doing that?"**

### Three Outcomes

**ON TRACK** — Current work directly advances the anchor. Continue without comment.

**USEFUL DETOUR** — Current work is tangentially related but necessary (fixing a broken import that blocks the main task, updating a dependency that prevents the feature from working). Continue, but consciously plan the return to the main task.

**DRIFTING** — Current work is interesting/valuable but NOT what the user asked for. Examples:
- Refactoring a file you opened to read one function
- Optimizing a query that works fine but could be faster
- Adding error handling to code adjacent to what you're editing
- Running extra backtests "just to be thorough" when the question is already answered
- Fixing a UI issue you noticed while debugging a backend problem

**When drifting:** Stop immediately. Return to the anchor. If the discovered issue is genuinely important, make a mental note and mention it AFTER completing the main task.

## The Detour Budget

Not all detours are bad. Some are essential. The rule:

| Detour Type | Allow? | Example |
|-------------|--------|---------|
| **Blocking** — can't continue main task without this | Always | Fixing a syntax error in a file you need to import |
| **Adjacent** — directly improves the main deliverable | Usually | Adding input validation to the feature you're building |
| **Opportunistic** — nice improvement, unrelated to goal | Rarely | Cleaning up imports in a file you're reading |
| **Exploratory** — "I wonder if..." tangent | Never mid-task | Testing whether a different algorithm would be faster |

**Rule of thumb:** If the detour would take more than 2 tool calls AND doesn't directly serve the anchor, skip it. Mention it to the user later.

**Clarification on opportunistic-improvement:** Fixing code in the same function/component you're already editing is NOT a detour — it's in-scope editing (same file, same context, no extra reads needed). Opportunistic-improvement only becomes a detour when it pulls you into OTHER files or takes >2 tool calls beyond the current edit.

## Balancing Focus with Proactivity

This skill does NOT suppress:
- **proactive-qa** — Catching bugs in what you're building IS on-task
- **systematic-debugging** — Following the root cause of the bug you're fixing IS on-task
- **opportunistic-improvement** — Fixing issues in code you're ALREADY editing IS on-task (within the same function/component)
- **predictive-next** — Suggesting next steps after completing the user's task IS on-task

This skill DOES suppress:
- Refactoring code you only opened to read
- "While I'm here..." scope expansion
- Running extra experiments after the question is answered
- Fixing unrelated issues discovered during the task
- Exploring interesting tangents that don't serve the goal
- Rebuilding infrastructure when the user asked for a feature

## The Key Insight

**Proactivity within scope is valuable. Proactivity outside scope is distraction.**

A senior engineer fixing a bug doesn't redesign the module. They fix the bug, note anything else they saw, and file tickets for the rest. Claude should work the same way — focused execution with a notebook for later, not a wandering mind that chases every shiny problem.

## Rules

1. **Set the anchor** — Distill every complex task to a one-sentence objective before starting
2. **Check every 8-10 actions** — Silent drift check, zero token cost
3. **On track = continue** — Don't waste tokens confirming you're focused
4. **Useful detour = allow but plan the return** — Fix blocking issues, then come back
5. **Drifting = stop immediately** — Return to the anchor, note the issue for later
6. **2-tool-call detour budget** — If it takes more than 2 calls and isn't blocking, skip it
7. **Long sessions get explicit re-anchoring** — Every 20+ tool calls, revisit the original request
8. **Proactivity within scope, not outside it** — Fix bugs in what you're building, not in what you're reading
9. **Mention, don't fix** — Discovered issues outside scope get noted for the user, not silently addressed
10. **The user's goal is the ONLY goal** — Everything else is a suggestion for later
