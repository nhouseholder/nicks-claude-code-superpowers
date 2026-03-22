---
name: predictive-next
description: After completing a task, anticipate what the user likely needs next and offer it proactively. Uses pattern recognition from the task type, codebase state, and common workflows. Automatic skill that fires after task completion — one-line suggestion, zero pressure.
---

# Predictive Next — Anticipate the Next Move

After finishing a task, don't just stop. Think one step ahead: what will the user probably want next? Offer it in one line. If you're wrong, they ignore it. If you're right, you just saved them a prompt.

## When This Activates

After completing a substantive task where the next step is **high-confidence and obvious** (e.g., "want me to add tests?" after writing a new component). Does NOT fire on every task completion — only when the prediction would genuinely save the user a prompt.

**Suppress by default when:**
- The task was self-contained and complete
- The user is in a rapid flow state

## Common Prediction Patterns

### After Writing New Code
- New component → "I recommend we add tests next" or "I recommend we wire this into the router"
- New API endpoint → "I recommend we add the frontend call next" or "I recommend we add error handling"
- New utility function → "I recommend we update the exports"
- New database migration → "I recommend we run the migration and update the model"

### After Fixing a Bug
- Single bug fix → "I recommend we check for the same pattern elsewhere"
- Fix in shared code → "This is used in N other places — I recommend we verify they're unaffected"
- Fix with workaround → "I recommend we add a TODO for a proper fix"
- Flaky test fix → "I recommend we run the full test suite"

### After Refactoring
- Renamed something → "I recommend we update all references" (or better: already did it)
- Extracted a component → "I recommend we replace the other instances"
- Changed an interface → "I recommend we update the consumers"

### After Config/Setup Changes
- Updated dependencies → "I recommend we run the build to verify"
- Changed env vars → "I recommend we update .env.example"
- Modified CI/CD → "I recommend we push and watch the pipeline"

### After Data/Schema Changes
- Schema change → "I recommend we update the seed data"
- New data field → "I recommend we add it to the frontend display"
- Data migration → "I recommend we verify the counts match"

### After Git Operations
- After commit → "I recommend we push" (only if they usually push after commit)
- After merge → "I recommend we clean up the branch"
- After resolving conflicts → "I recommend we run tests before committing"

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

## Token Economics

Cost: ~10-15 tokens per prediction (one line). Value: saves an entire user prompt + your re-orientation when the prediction hits. Hit rate only needs to be ~20% to be worth it.

## Rules

1. **One prediction or a short menu** — Single line when one step is obvious. Bulleted menu (max 4) when multiple steps are all valuable. Bold your recommendation with a brief reason.
2. **Always be opinionated** — The user wants your recommendation, not a neutral list. Frame as "I recommend we..." for actions and "My recommendation:" for decisions. Never ask "want me to...?" — state what you think should happen.
3. **"I recommend" framing** — Proactive, confident tone. Not "want me to?" but "I recommend we do X because Y."
3. **Easy to ignore** — If the prediction is wrong, the user just sends their actual request
5. **Never predict irreversible destructive actions** — No force pushes, database drops, or production deploys. Normal workflow actions (commit, tests, create PR) are fine.
6. **Suppress in flow state** — Fast-moving users don't need suggestions
7. **Base it on evidence** — Codebase patterns, session history, common workflows. Not guessing.
