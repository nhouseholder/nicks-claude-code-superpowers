---
name: task-router
description: Automatically routes tasks to Opus 4.6 or Sonnet 4.6 based on complexity. Opus for debugging, planning, strategy, experimentation. Sonnet for execution, simple edits, cosmetic changes, following existing plans. Fires on every message to classify and route.
weight: passive
category: meta
---

# Task Router — Right Model for the Right Task

Classify every task and route to the optimal model. Opus thinks. Sonnet executes.

## Always Active

On every message, mentally classify the task into one of two tiers before acting.

## Opus Tier (complex thinking required)

Use Opus 4.6 for tasks that require reasoning, judgment, or experimentation:

- **Debugging** — root cause analysis, multi-file investigation, hypothesis testing
- **Architecture & strategy** — system design, tradeoff analysis, refactoring decisions
- **Planning** — writing implementation plans, breaking down complex features
- **Experimentation** — trying approaches, coefficient tuning, algorithm design
- **Research** — deep-research, evaluating alternatives, domain learning
- **Ambiguous requests** — intent is unclear, multiple valid interpretations
- **New feature design** — first-time implementations with unknowns
- **Data/math correctness** — any task where numbers must be verified, formulas validated, or calculations checked. "Fix the P/L table" is NOT execution — it requires understanding how payouts work and verifying the math.
- **Fixing something that was already "fixed"** — if the user says "still broken," the first approach was wrong. This needs thinking, not more mechanical editing.

## Sonnet Tier (ONLY when output correctness is trivially verifiable)

Use Sonnet 4.6 ONLY when the task meets ALL of these criteria:
1. The path is completely clear (no judgment calls)
2. Output correctness is obvious at a glance (no math, no domain knowledge needed)
3. No user-facing data that could be wrong in non-obvious ways

**Sonnet-safe tasks:**
- **Cosmetic edits** — CSS changes, copy updates, variable renames
- **Repetitive mechanical ops** — applying the same rename across files
- **Config changes** — toggling flags, updating env vars, version bumps
- **Running commands** — tests, builds, deploys with known outcomes
- **File organization** — moves, template fills, boilerplate generation

**NOT Sonnet-safe (route to Opus even if they seem "simple"):**
- Anything with numbers that need to be correct (P/L, stats, percentages)
- Anything the user will look at and judge ("does this make sense?")
- Fixing something that was already attempted and failed
- Any table, chart, or data display — the DATA must be right, not just the code
- Business logic changes — even one-line changes to formulas or conditions
- **Website front pages, dashboards, or performance displays** — these are the user's public-facing product. Every number must be verified against data invariants (see CLAUDE.md). ALWAYS Opus.
- **Any scoring, tracking, or results pipeline** — the code that PRODUCES the stats is as critical as the display

## How to Apply

### For Subagents (automatic)
When spawning agents via the Agent tool, set the `model` parameter:
- Research/planning/debugging agents → `model: "opus"`
- Execution/formatting/simple-edit agents → `model: "sonnet"`

Example:
```
Agent(description="Debug auth failure", model="opus", ...)
Agent(description="Apply rename across 5 files", model="sonnet", ...)
```

### For the Main Conversation
If the current main model doesn't match the task tier:
- If on Opus and task is Sonnet-tier → suggest: "This is straightforward — switch to Sonnet with `/model sonnet` to save tokens."
- If on Sonnet and task is Opus-tier → suggest: "This needs deeper thinking — switch to Opus with `/model opus`."
- Only suggest once per tier-change, not on every message.

### Quick Classification Test

Ask: **"Could a junior dev follow written instructions to do this?"**
- Yes → Sonnet (execution)
- No → Opus (thinking)

**Second test for data tasks:** "Do the output numbers need to make sense?"
- Yes → Opus (must verify math/logic, not just edit code)
- No → Sonnet (formatting, display, cosmetic)

## Context Window Rules

- **Never use `[1m]` extended context** unless the user explicitly requests it or the task genuinely requires reading 200K+ tokens of source material. The 1M window sends the entire context on every request, burning through per-minute rate limits and causing "Rate limit reached" errors even at low quota usage.
- **Standard context is the default.** It handles 99% of tasks. If context gets large, use `/compact` or start a new session — don't switch to `[1m]`.
- **If the user hits rate limit errors:** suggest dropping `[1m]` first, then reducing parallel agents, then switching to Sonnet for the current task.

## Rules

1. **Classify silently** — never announce the classification unless suggesting a model switch
2. **Subagents always get routed** — every Agent call should have an explicit `model` parameter
3. **Don't over-suggest switches** — suggest once when tier changes, then stop. The user can override.
4. **Opus plans, Sonnet executes** — the most common pattern is Opus writes a plan, then Sonnet-tier agents execute it
5. **When in doubt, use Opus** — wrong model on a hard task wastes more tokens than wrong model on an easy task
