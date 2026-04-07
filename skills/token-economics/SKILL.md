---
name: token-economics
description: Optimizes token spend across model tiers, effort levels, and plan/execute splits. Recommends Sonnet for simple tasks, promotes Opus-plan/Sonnet-execute workflow for complex work, and calibrates effort to task complexity. Always-on awareness that shapes every response.
weight: passive
---

# Token Economics — Spend Smart, Not Big

Make every token count. Match model capability and effort level to actual task complexity.

## Three Levers

1. **Model tier** — Opus for thinking, Sonnet for executing, Haiku for trivial
2. **Effort level** — Deep thinking for architecture, fast output for renames
3. **Plan/Execute split** — Think hard once in Opus, execute mechanically in Sonnet

## Task Classification

| Tier | Signal Patterns | Model | Effort | Plan Mode |
|------|----------------|-------|--------|-----------|
| **TRIVIAL** | Rename, fix typo, "what does X do?", format, add comment | Sonnet or /fast | Low | No |
| **SIMPLE** | Single-file edit, add field/prop, quick bug fix, run command | Sonnet | Normal | No |
| **MODERATE** | Multi-file feature, new component, refactor, API integration | Opus | Normal | Optional |
| **COMPLEX** | Architecture decision, debug cascade, new system, multi-step | Opus | High | Recommended |
| **CRITICAL** | Data migration, production deploy, security fix, schema change | Opus | Max | Required |

## When to Recommend Model Switch

Suggest switching to Sonnet when ALL of these are true:
- Task is TRIVIAL or SIMPLE tier
- No ambiguity in what to do
- No architectural decisions required
- No risk of data loss or breaking changes
- A written plan already exists (for SIMPLE tasks from a prior planning step)

Suggest switching to Opus when ANY of these are true:
- Task requires reasoning about tradeoffs
- Multiple valid approaches exist and one must be chosen
- Debugging with unknown root cause
- User says "think about", "brainstorm", "architect", "design"
- Previous Sonnet attempt failed or produced poor results

## The Opus-Plan / Sonnet-Execute Workflow

When a COMPLEX or CRITICAL task arrives and the user is on Opus:

1. **Recognize the opportunity**: "This is complex enough to benefit from the plan-then-execute workflow."
2. **Write a Sonnet-proof plan**: A plan so specific that Sonnet can execute it mechanically.
3. **Prompt the switch**: "Plan complete. You can switch to Sonnet to execute — every step is specific enough."

### What Makes a Plan "Sonnet-Proof"

A Sonnet-proof plan has ZERO ambiguity. Every step must be mechanical:

- **Exact file paths** — not "the config file" but `/src/config/database.ts`
- **Exact line numbers** — not "near the top" but "line 42-58"
- **Exact code blocks** — full code to write, not pseudocode or descriptions
- **Exact commands** — `npm test -- --grep "auth"` not "run the tests"
- **Exact verification** — "After step 3, run X and confirm output contains Y"
- **No decision points** — if a step requires judgment, it's not Sonnet-proof
- **Ordered dependencies** — step N only uses outputs from steps 1 through N-1

Bad (requires thinking):
```
3. Update the auth middleware to handle the new token format
```

Good (mechanical):
```
3. Edit /src/middleware/auth.ts line 28-35:
   Replace the existing validateToken function body with:
   [exact code block]
   This changes JWT validation from HS256 to RS256.
```

### When NOT to Use This Workflow

- Task is TRIVIAL or SIMPLE — just do it directly
- Task is exploratory — "try different approaches" needs Opus throughout
- Task requires real-time judgment — debugging where each step depends on the last
- User is iterating rapidly — switching models adds friction

## Effort Level Guidelines

**Low effort / /fast:**
- Answering factual questions about the codebase
- Simple renames, typo fixes, formatting
- Running commands and reporting output
- Reading files and summarizing

**Normal effort:**
- Single-file feature additions
- Writing tests for existing code
- Standard CRUD operations
- Configuration changes

**High effort:**
- Multi-file refactors
- Debugging with unknown root cause
- Performance optimization
- API design decisions

**Max effort (ULTRATHINK-level):**
- Architecture decisions affecting multiple systems
- Security-critical changes
- Data migration planning
- Anything where "getting it wrong costs hours"

## How to Prompt the User

Keep recommendations brief and actionable. Examples:

**Suggesting Sonnet:**
> "This is a straightforward rename across 3 files — Sonnet would handle this well if you want to save tokens. `/model sonnet`"

**Suggesting plan mode:**
> "This is a multi-step feature. Want me to write a detailed plan first? You could then switch to Sonnet to execute it."

**Suggesting effort change:**
> "This needs deep thinking — make sure /fast is off for this one."

**After plan is written:**
> "Plan complete — 8 steps, all mechanical. Safe to execute on Sonnet if you want to switch. `/model sonnet`"

## Anti-Patterns

- **Never auto-downgrade mid-task** — if Opus is working on something complex, don't suggest switching partway through
- **Never suggest Sonnet for debugging** — debugging requires reasoning about unknowns
- **Never suggest Sonnet for the FIRST implementation of a new system** — only for executing a pre-written plan
- **Never pressure** — one recommendation per task, not repeated nudging
- **Never sacrifice quality for tokens** — if unsure, stay on Opus
