---
name: model-router
description: Automatically routes tasks to Opus 4.6 or Sonnet 4.6 based on complexity. Opus for debugging, planning, strategy, experimentation. Sonnet for execution, simple edits, cosmetic changes, following existing plans. Fires on every message to classify and route.
weight: passive
category: meta
---

# Model Router — Right Model for the Right Task

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

## Sonnet Tier (straightforward execution)

Use Sonnet 4.6 for tasks where the path is clear and thinking is minimal:

- **Executing a plan** — following steps already laid out by Opus
- **Simple edits** — cosmetic changes, typo fixes, variable renames
- **Repetitive operations** — applying the same pattern across files
- **Config changes** — updating values, toggling flags, env vars
- **Running commands** — tests, builds, deploys with known outcomes
- **Data formatting** — JSON updates, file moves, template fills
- **Code review execution** — applying specific review feedback

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

## Rules

1. **Classify silently** — never announce the classification unless suggesting a model switch
2. **Subagents always get routed** — every Agent call should have an explicit `model` parameter
3. **Don't over-suggest switches** — suggest once when tier changes, then stop. The user can override.
4. **Opus plans, Sonnet executes** — the most common pattern is Opus writes a plan, then Sonnet-tier agents execute it
5. **When in doubt, use Opus** — wrong model on a hard task wastes more tokens than wrong model on an easy task
