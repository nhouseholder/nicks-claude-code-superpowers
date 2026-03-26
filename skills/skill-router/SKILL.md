---
name: skill-router
description: Unified meta-routing — weight limits, task-to-model routing, skill matching, and drift prevention. Replaces skill-manager, task-router, skill-awareness, and prompt-architect. Lightweight passive skill.
weight: passive
replaces: skill-manager, task-router, skill-awareness, prompt-architect
---

# Skill Router — Traffic Control

## 1. Weight Limits

| Weight | Max/Message | Skills |
|--------|-------------|--------|
| Passive (~0 tokens) | Unlimited | Behavioral shaping only |
| Light (50-500 tokens) | 5 | Quick checks, small reads |
| Heavy (1K-50K+ tokens) | 2 | Agent spawns, multi-file ops |

### Conflict Resolution Priority

1. User's explicit instruction
2. Feedback memories (prior corrections)
3. Domain-specific skills (in their domain)
4. Safety/verification skills
5. Process skills (workflow)
6. Enhancement skills (lowest — suppress if busy)

**Key tiebreaker:** Safety beats speed. Specific beats general. Current task beats improvement. Action beats analysis.

### Skill Overload Test

Before executing: is this response shaped by understanding of the task, or by a stack of checklists? If it feels robotic/checklist-y, fewer skills should be active.

| Message Type | Max Active Skills |
|-------------|-------------------|
| Simple (<20 words) | 0-2 |
| Moderate (single task) | 3-5 |
| Complex (multi-part) | 5-8 |

**Golden rule:** Skills enhance Claude's natural intelligence, not replace it. If ignoring a skill produces a better answer, ignore it.

## 2. Task-to-Model Routing

### Opus Tier (DEFAULT — everything goes here unless provably trivial)

Use Opus for tasks requiring reasoning, judgment, or correctness verification:

- Debugging, root cause analysis, hypothesis testing
- Architecture, strategy, system design, tradeoff analysis
- Planning, breaking down features, implementation plans
- Experimentation, coefficient tuning, algorithm design
- Research, evaluating alternatives, domain learning
- Ambiguous requests with multiple valid interpretations
- New feature design with unknowns
- Data/math correctness — any task where numbers must be verified
- Fixing something that was already "fixed" — needs thinking, not more editing
- Website front pages, dashboards, performance displays
- Any scoring, tracking, or results pipeline
- Business logic changes, even one-line formula changes

### Sonnet Tier (EXTREMELY restricted)

Sonnet is ONLY for tasks that meet ALL of these:
1. Zero judgment required — the output is mechanically deterministic
2. Zero domain knowledge — no sports, no betting, no business logic
3. Zero user-facing data — no numbers, tables, or stats that could be wrong
4. A literal intern could do it — "change this color from blue to red"

**Examples that qualify for Sonnet:**
- CSS color/spacing changes with exact values given by the user
- Renaming a variable across files (find/replace)
- Toggling a boolean config flag
- Copying or moving a file
- Adding a comment the user dictated verbatim

**Examples that do NOT qualify (stay on Opus):**
- ANY data display, table, chart, or statistics
- ANY business logic, even "simple" one-line changes
- ANY debugging, even "obvious" bugs
- ANY user-facing text changes (wording matters)
- ANY deployment or infrastructure
- ANY file that touches scoring, predictions, or money
- Anything with numbers that need to be correct
- Anything the user will look at and judge ("does this make sense?")

### Subagent Routing

Every Agent() call must include the model parameter:
- `model: "opus"` — research, debugging, planning, any data work
- `model: "sonnet"` — ONLY mechanical execution of fully-specified instructions
- NEVER use `model: "haiku"` — Haiku is remapped to GLM-5 via Z AI proxy. Only the user switches to it manually when rate-limited.

### Context Window Rules

- Never use `[1m]` extended context unless the user explicitly requests it or the task genuinely requires 200K+ tokens. Standard context handles 99% of tasks.
- If rate limit errors occur: suggest dropping `[1m]` first, then reducing parallel agents, then switching to Sonnet for the current task.

## 3. Skill Matching (Quick Reference)

When you notice a task matches a skill, use it. No mandatory scan required — just pattern-match naturally.

| User request keywords | Check these skills |
|----------------------|-------------------|
| frontend, UI, design, component, layout, style | `frontend-design`, `ui-ux-pro-max` |
| fix, bug, broken, error, failing | `fix-loop`, `systematic-debugging`, `pre-debug-check` |
| deploy, ship, push, release, go live | `deploy` |
| plan, design, architect, break down | `writing-plans`, `brainstorming`, `spec-interview` |
| test, TDD, coverage | `test-driven-development`, `qa-gate` |
| commit, git, branch, merge | `git-sorcery`, `version-bump` |
| research, learn, understand | `deep-research`, `know-what-you-dont-know` |
| backtest, model, accuracy, prediction | `backtest`, `profit-driven-development` |
| website, webapp, site | `website-guardian`, `site-update-protocol` |
| review, audit, scan | `audit`, `reflexion`, `receiving-code-review` |
| parallel, concurrent | `dispatching-parallel-agents`, `parallel-sweep` |

### Intent-to-Command Shortcuts

| User says | Routes to |
|-----------|-----------|
| "ship it", "deploy", "go live" | `/deploy` |
| "run the backtest" | `/backtest` |
| "update the site" | `site-update-protocol` |
| "audit", "check for secrets" | `/audit` |
| "fix all tests" | `/fix-loop` |
| "let's think about..." | `/brainstorm` |
| "make a plan" | `/write-plan` |

Execute automatically at high confidence. Confirm briefly when uncertain.

## 4. Drift Prevention

For tasks taking 10+ tool calls:

**Set anchor:** Distill the task to one specific sentence at start.

**Drift check (every 8-10 tool calls, mental, zero tokens):**
1. What did the user ask?
2. Is my current action advancing that goal?
3. Would they say "yes that's what I need" or "why are you doing that?"

**Outcomes:** On track = continue. Useful detour that blocks main task = fix it, plan the return. Drifting = stop immediately, return to anchor.

**Detour budget:**

| Type | Allow? |
|------|--------|
| Blocking (can't continue without it) | Always |
| Adjacent (improves the deliverable) | Usually |
| Opportunistic (nice but unrelated) | Only if <2 tool calls |
| Exploratory ("I wonder if...") | Never mid-task |

## Rules

1. Everything defaults to Opus unless provably trivial
2. When in doubt, use Opus — wrong model on hard task wastes MORE tokens
3. Never announce routing classifications — just apply them silently
4. Skills enhance Claude, not replace Claude's judgment
5. Weight limits are hard — never exceed them
6. User's explicit instruction overrides all routing
7. Classify silently, route confidently
8. Subagents always get an explicit model parameter
9. Proportional overhead: zero on simple messages, full processing on complex ones
