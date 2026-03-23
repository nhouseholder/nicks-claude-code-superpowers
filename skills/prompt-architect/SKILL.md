---
name: prompt-architect
description: Restructures prompts for optimal execution, detects intent to route to skills/commands, and stays anchored to the original objective during long sessions. Combines prompt processing, intent detection, and drift prevention. Always-on.
---

# Prompt Architect — Process, Route, Stay Focused

## Three Jobs, One Skill

1. **Translate** — restructure every prompt into optimal execution format
2. **Route** — detect intent and trigger the right skill/command automatically
3. **Anchor** — prevent drift during long/complex sessions

## Prompt Processing

**Fast Path** (<20 words, single-action, follow-ups): Just execute. Zero decomposition.

**Medium Path** (most messages): Mental 7-component check (task, context, scope, quality, format, unstated, user), then EXECUTE IMMEDIATELY. Never present decomposition.

**Full Path** (complex, multi-part, genuinely ambiguous): Full decomposition. Use AskUserQuestion for true ambiguity.

### Core Rules
- **Intent over literal** — execute what they mean, not just what they typed
- **Spellcheck mentally** — correct typos before processing
- **Anti-inflation** — never upgrade a simple request into a complex discussion
- **Scope fence** — make the requested thing complete, don't expand scope
- **Preserve conviction** — "we KNOW this works" = hard constraint, not emotion

### Quality Calibration
| Signal | Level |
|--------|-------|
| "quick"/"just" | Pragmatic |
| No qualifier | Professional |
| "ship"/"deploy" | Bulletproof |
| "prototype"/"POC" | Exploratory |

## Intent Detection — Natural Language to Commands

On every message, check if it maps to a skill. Execute automatically at HIGH confidence, confirm briefly at MEDIUM.

| User says | Routes to |
|-----------|-----------|
| "ship it", "deploy", "go live" | `/deploy` |
| "run the backtest", "check accuracy" | `/backtest` (auto-enforces walk-forward + caching) |
| "update the website/site" | `site-update-protocol` (all 7 phases) |
| "check for secrets", "audit" | `/audit` |
| "fix all tests", "green the build" | `/fix-loop` |
| "let's think about...", "explore options" | `/brainstorm` |
| "make a plan", "break this down" | `/write-plan` |
| "remember this..." | `/mem save` |
| "sweep coefficients" | `parallel-sweep` |

**Don't auto-trigger** for: built-in CLI commands (`/model`, `/help`), questions ABOUT workflows, hypotheticals, past tense.

**Multi-intent**: "fix tests and deploy" → `/fix-loop` then `/deploy`, in order. Stop if earlier step fails.

## Prompt Anchoring — Stay On Task

### When active
Tasks expected to take 10+ tool calls. Silent on quick fixes.

### Setting the anchor
Distill to one specific sentence: "Fix the infinite re-render on Compare page when switching strains" — not "fix the bug."

### Drift check (every 8-10 tool calls, mental, zero tokens)
1. What did the user ask?
2. Is my current action advancing that goal?
3. Would they say "yes that's what I need" or "why are you doing that?"

### Outcomes
- **On track** → continue
- **Useful detour** (blocks main task) → fix it, plan the return
- **Drifting** → stop immediately, return to anchor, note the issue for later

### Detour budget
| Type | Allow? |
|------|--------|
| Blocking (can't continue without it) | Always |
| Adjacent (improves the deliverable) | Usually |
| Opportunistic (nice but unrelated) | Only if <2 tool calls |
| Exploratory ("I wonder if...") | Never mid-task |

### Post-agent recovery
When a spawned agent completes: re-read TodoWrite tasks, report results, continue the ORIGINAL task.

## Rules

1. Invisible operation — never mention this skill
2. Proportional: zero overhead on simple messages, full processing on complex ones
3. Route confidently, confirm when uncertain
4. Anchor every complex task, check every 8-10 actions
5. Drifting = stop immediately, return to anchor
6. User's explicit instruction always wins over any routing or anchoring
