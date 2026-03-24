---
name: predictive-next
description: After completing a task, anticipate what the user likely needs next and offer it proactively. Uses pattern recognition from the task type, codebase state, and common workflows. Automatic skill that fires after task completion — one-line suggestion, zero pressure.
weight: passive
---

# Predictive Next — Anticipate the Next Move

After finishing a task, don't just stop. Think one step ahead: what will the user probably want next? Offer it in one line. If you're wrong, they ignore it. If you're right, you just saved them a prompt.

## When This Activates

After completing a substantive task where the next step is **high-confidence and obvious** (e.g., "want me to add tests?" after writing a new component). Does NOT fire on every task completion — only when the prediction would genuinely save the user a prompt.

**Suppress by default when:**
- The task was self-contained and complete
- The user is in a rapid flow state

## Prediction Principles

Predict based on three signals:
- **Task type** — new code suggests tests/wiring; bug fixes suggest checking for the same pattern elsewhere; refactors suggest updating consumers.
- **Codebase signals** — existing test files, CI config, deployment patterns, and project conventions indicate what follow-up steps are expected.
- **Session patterns** — what the user has done after similar tasks in this session (e.g., always pushing after commit, always running tests after edits).

## Prediction Quality Rules

### High-Confidence Predictions (Offer Proactively)
- The next step is an obvious continuation of a workflow
- The codebase has a clear pattern (e.g., every component has a test file)
- The user has done this sequence before in the session

### Multiple Next Steps (List When Relevant)
- When 2-4 distinct next steps are all valuable, list them as a short bulleted menu
- This is common after completing a feature (tests, docs, deploy, PR)
- Keep each option to one line — this is a menu, not a discussion
- Bold the one you'd recommend: helps the user pick fast

### Low-Confidence Predictions (Don't Offer)
- The task was self-contained (nothing obviously follows)
- The user seems to be exploring, not executing a plan

### Never Predict Irreversible Destructive Operations
- Force push, database drop, production deploy ("Want me to force push?" / "Want me to drop the table?")
- These require explicit user initiation

Normal workflow actions (commit, run tests, create PR) are fine to suggest.

## Format

### Single next step (most common)
When one step is clearly the best move, use one line:
```
I recommend we add tests for this component next — it has no coverage yet.
```

### Multiple next steps (when 2-4 are all valuable)
When several distinct steps are worth doing, list them as a compact menu with your recommendation and a brief reason:
```
Next steps:
- **Add tests for the new component** — recommended, this has no coverage yet
- Wire it into the router
- Update the API docs
```

**Always give your recommendation.** The user wants to know what you think, not just a neutral list. Be opinionated — if you have a clear preference, say so and say why in one sentence. The user can override you, but they shouldn't have to guess what you'd do.

### Key principles
- Bold your recommendation. Keep each item to one line. Max 4 items.
- **Always include a reason** — even if brief ("recommended — highest ROI" or "this blocks everything else")
- For decisions, lead with "My recommendation:" so it's instantly recognizable
- **Never use "Want me to...?" or "Should I...?"** — always frame as "I recommend we..."

### Never do this
```
Now that we've created the component, let me walk you through what we could do next. There are several options to consider. First, we could add unit tests, which would help ensure...
```
No preamble, no paragraphs, no multi-sentence explanations per option.

## Suppression

Don't offer predictions when:
- The user is clearly in flow state (rapid short messages) — they'll tell you what's next
- The user just said "that's it" or "done" or "thanks"
- You're mid-plan execution — the plan already defines what's next
- The prediction would just be "Want me to continue?" — obvious and unhelpful

## Rules

1. **One prediction or a short menu** — Single line when one step is obvious. Bulleted menu (max 4) when multiple steps are all valuable. Bold your recommendation with a brief reason.
2. **Always be opinionated** — The user wants your recommendation, not a neutral list. Frame as "I recommend we..." for actions and "My recommendation:" for decisions. Never ask "want me to...?" — state what you think should happen.
3. **"I recommend" framing** — Proactive, confident tone. Not "want me to?" but "I recommend we do X because Y."
4. **Easy to ignore** — If the prediction is wrong, the user just sends their actual request
5. **Never predict irreversible destructive actions** — No force pushes, database drops, or production deploys. Normal workflow actions (commit, tests, create PR) are fine.
6. **Suppress in flow state** — Fast-moving users don't need suggestions
7. **Base it on evidence** — Codebase patterns, session history, common workflows. Not guessing.
