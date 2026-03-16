---
name: predictive-next
description: After completing a task, anticipate what the user likely needs next and offer it proactively. Uses pattern recognition from the task type, codebase state, and common workflows. Automatic skill that fires after task completion — one-line suggestion, zero pressure.
---

# Predictive Next — Anticipate the Next Move

After finishing a task, don't just stop. Think one step ahead: what will the user probably want next? Offer it in one line. If you're wrong, they ignore it. If you're right, you just saved them a prompt.

## When This Activates

After completing any substantive task (not after answering a question or providing info). Fires as a lightweight suggestion at the end of your response.

## Common Prediction Patterns

### After Writing New Code
- New component → "Want me to add tests?" or "Want me to wire this into the router?"
- New API endpoint → "Want me to add the frontend call?" or "Want me to add error handling?"
- New utility function → "Want me to update the exports?" or "Want me to add this to the existing usage?"
- New database migration → "Want me to run it?" or "Want me to update the model?"

### After Fixing a Bug
- Single bug fix → "Want me to check for the same pattern elsewhere?"
- Fix in shared code → "This is used in N other places — want me to verify they're unaffected?"
- Fix with workaround → "Want me to add a TODO for a proper fix?"
- Flaky test fix → "Want me to run the full test suite?"

### After Refactoring
- Renamed something → "Want me to update all references?" (or better: already did it)
- Extracted a component → "Want me to replace the other instances?"
- Changed an interface → "Want me to update the consumers?"

### After Config/Setup Changes
- Updated dependencies → "Want me to run the build to verify?"
- Changed env vars → "Want me to update the .env.example?"
- Modified CI/CD → "Want me to push and watch the pipeline?"

### After Data/Schema Changes
- Schema change → "Want me to update the seed data?"
- New data field → "Want me to add it to the frontend display?"
- Data migration → "Want me to verify the counts match?"

### After Git Operations
- After commit → "Want me to push?" (only if they usually push after commit)
- After merge → "Want me to clean up the branch?"
- After resolving conflicts → "Want me to run tests before committing?"

## Prediction Quality Rules

### High-Confidence Predictions (Offer Proactively)
- The next step is an obvious continuation of a workflow
- The codebase has a clear pattern (e.g., every component has a test file)
- The user has done this sequence before in the session

### Low-Confidence Predictions (Don't Offer)
- Multiple equally likely next steps
- The task was self-contained (nothing obviously follows)
- The user seems to be exploring, not executing a plan

### Never Predict
- Destructive operations ("Want me to delete the old version?")
- Deployment ("Want me to deploy to production?")
- External communications ("Want me to open a PR?")
- These require explicit user initiation

## Format

Always a single line at the end of your response. Never a paragraph. Never multiple options.

**Good:**
```
Next: want me to add tests for this component?
```

**Bad:**
```
Now that we've created the component, here are some things we could do next:
1. Add unit tests
2. Wire it into the router
3. Add error handling
4. Update the documentation
What would you like to do?
```

The bad example burns tokens, creates decision fatigue, and slows the user down. Pick the ONE most likely next step.

## Suppression

Don't offer predictions when:
- The user is clearly in flow state (rapid short messages) — they'll tell you what's next
- The user just said "that's it" or "done" or "thanks"
- You're mid-plan execution — the plan already defines what's next
- The prediction would just be "Want me to continue?" — obvious and unhelpful

## Token Economics

Cost: ~10-15 tokens per prediction (one line). Value: saves an entire user prompt + your re-orientation when the prediction hits. Hit rate only needs to be ~20% to be worth it.

## Rules

1. **One prediction, one line** — Never list options. Pick the most likely next step.
2. **"Next:" prefix** — Consistent format so the user recognizes it instantly
3. **Easy to ignore** — If the prediction is wrong, the user just sends their actual request
4. **Never predict destructive actions** — No deletes, deploys, or external communications
5. **Suppress in flow state** — Fast-moving users don't need suggestions
6. **Base it on evidence** — Codebase patterns, session history, common workflows. Not guessing.
