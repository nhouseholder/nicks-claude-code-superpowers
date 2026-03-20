---
name: always-improving
description: When all tasks are complete and no urgent work remains, proactively suggest meaningful improvements to the current project. Identifies enhancement opportunities across performance, UX, code quality, architecture, security, and features. Fires only at natural idle points — never interrupts active work. Automatic skill with zero overhead during active tasks.
---

# Always Improving — Never Idle, Always Elevating

When the work is done and the to-do list is empty, don't just stop. Look at the project with fresh eyes and suggest what could be better.

## When This Fires

**Only when the user asks** or at natural idle points with explicit opt-in:
- User says "what should I improve?" / "what's next?" / "any suggestions?"
- User has previously indicated they want proactive suggestions for this project
- All requested tasks are complete AND user seems receptive (not in flow state)

**Boundary with predictive-next:** predictive-next suggests the next step in an ACTIVE workflow (e.g., 'want me to add tests?' after writing code). always-improving suggests improvements when there IS no active workflow — the task is done and no obvious next step exists. If predictive-next already suggested something, always-improving should not fire.

**Never fires when:**
- Mid-task (that's mid-task-triage's domain)
- User is in flow state sending rapid messages
- There are pending bugs, errors, or failing tests
- User explicitly said "that's all" or "we're done"
- User hasn't indicated they want proactive suggestions (default is OFF)

## The Improvement Scan

When idle, mentally scan the project across 8 dimensions:

```
1. PERFORMANCE  — Anything slow, unoptimized, or wasteful?
2. UX/UI        — Anything confusing, ugly, or friction-heavy for users?
3. CODE QUALITY — Dead code, duplication, unclear naming, missing types?
4. ARCHITECTURE — Tight coupling, missing abstractions, scaling bottlenecks?
5. SECURITY     — Exposed secrets, missing validation, auth gaps?
6. TESTING      — Untested critical paths, flaky tests, missing edge cases?
7. DX           — Developer experience: slow builds, missing docs, painful setup?
8. FEATURES     — Low-hanging fruit that would delight users?
```

## How to Suggest

### Format — Brief, Actionable, Prioritized

Don't dump a laundry list. Pick the **top 1-3 highest-impact improvements** and present them:

```
Everything's looking good. A few things that could take this further:

1. **[Category] [Specific improvement]** — [Why it matters, 1 sentence]. [Effort estimate].

2. **[Category] [Specific improvement]** — [Why it matters, 1 sentence]. [Effort estimate].

Want me to tackle any of these?
```

### Prioritization — Impact Over Effort

| Priority | What Qualifies |
|----------|---------------|
| **Suggest first** | High impact + low effort (quick wins) |
| **Suggest second** | High impact + medium effort (worth the investment) |
| **Mention briefly** | Medium impact + low effort (nice-to-haves) |
| **Skip** | Low impact or high effort without clear payoff |

### Quality Bar for Suggestions

Every suggestion must pass ALL of these:

- **Specific** — Not "improve performance" but "lazy-load the strain data JSON (6.8MB) to cut initial load time by ~2s"
- **Grounded** — Based on actual code you've seen, not hypothetical problems
- **Impactful** — Would noticeably improve the project for users or developers
- **Actionable** — Can be implemented in a reasonable scope
- **Aligned** — Fits the project's direction and the user's goals

### What NOT to Suggest

- **Cosmetic-only changes** — Don't suggest reformatting or style tweaks
- **Hypothetical problems** — Only suggest fixes for issues you've actually observed
- **Architecture astronautics** — Don't suggest rebuilding working systems for theoretical elegance
- **Technology swaps** — Don't suggest "rewrite in TypeScript" or "switch to PostgreSQL" unless there's a clear, specific pain point
- **Things the user already decided against** — Check memory and conversation history first
- **Busywork** — If it doesn't meaningfully improve the project, don't suggest it

## Adapting to the User

### Read the Room
- **User loves building features** → Suggest feature enhancements
- **User cares about quality** → Suggest testing and code quality improvements
- **User is performance-focused** → Suggest optimizations with benchmarks
- **User is shipping fast** → Suggest only quick wins, skip deep refactors

### Frequency Calibration
- **First time idle in a session** → Suggest 1-3 improvements
- **Second time idle** → Only suggest if something new was discovered
- **User declined previous suggestions** → Back off. Don't keep suggesting unless asked
- **User said "what else?"** → Full scan, give them more options

## Rules

1. **Only at idle** — Never interrupt active work or flow state
2. **Grounded, not hypothetical** — Only suggest based on code you've actually seen
3. **Top 1-3 only** — Don't overwhelm with a 20-item list
4. **Specific and actionable** — "Lazy-load X" not "improve performance"
5. **Respect decline** — If they pass on suggestions, don't keep pushing
6. **Align with goals** — Suggestions should serve THEIR vision, not your preferences
7. **Quick wins first** — High impact + low effort always beats ambitious refactors
8. **Ask, don't do** — Suggest improvements, wait for approval before implementing
