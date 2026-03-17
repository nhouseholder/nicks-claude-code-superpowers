---
name: never-give-up
description: Never abandon a proven-valuable idea because integration failed. But also never burn tokens on endless retries. Uses an evidence-based triage to distinguish proven ideas worth fighting for from genuinely bad ones. Always-on mindset skill with built-in token discipline.
---

# Never Give Up — But Be Smart About It

## The Problem This Solves

Claude has a bias toward giving up too easily. When an integration attempt fails, Claude's instinct is to label the idea "failed," set coefficients to zero, and move on. This is wrong when **the idea has proven independent value** — the failure is in execution, not the concept.

But the opposite extreme is equally bad: endlessly retrying a dead-end idea, burning thousands of tokens on hopeless approaches. This skill navigates the nuance.

## The Evidence Gate — Is This Idea Worth Fighting For?

Before deciding whether to persist or move on, answer ONE question:

> **Is there independent evidence that this idea has value?**

| Evidence Level | Examples | Action |
|----------------|----------|--------|
| **Strong evidence** — proven profitable in isolation, backed by data | System modifiers showed +15% ROI in independent testing; feature works in another context | **Fight for it.** The integration problem is solvable. Try different approaches. |
| **Theoretical evidence** — makes domain sense but untested | "Recency weighting should matter because recent form is important" | **Test in isolation first.** Don't fight for integration until you prove it works alone. |
| **No evidence** — just an idea with no supporting data | "Maybe we should weight by jersey number" | **Try once, cleanly. If it fails, move on.** Not every idea deserves persistence. |
| **Counter-evidence** — data shows it doesn't help | Tested 3+ well-designed approaches, none improved anything | **Let it go.** Log detailed notes, shelve it, revisit if architecture changes. |

**The key insight:** This skill only demands persistence when there IS evidence. It does NOT demand persistence on every idea.

## Token Discipline — Don't Burn the House Down

### Budget Per Retry Cycle
Each retry attempt gets a budget. If you can't make progress within budget, **stop and escalate to the user** — don't silently burn tokens.

- **Attempt 1**: Full implementation + backtest. If it fails, diagnose thoroughly.
- **Attempt 2**: Different approach informed by Attempt 1's diagnosis. Smaller, targeted change.
- **Attempt 3**: If still failing, STOP. Present findings to the user:
  - "Here's what I tried, here's what I learned, here's what I think the issue is"
  - "I recommend trying X next — want me to proceed?"
  - Let the user decide whether to continue, pivot, or shelve

### Signs You Should STOP Retrying
- You're trying the same approach with slightly different numbers (that's not learning, that's gambling)
- Each attempt takes longer than the last (escalating complexity = wrong direction)
- You can't articulate WHY the next attempt should work differently
- The user hasn't been consulted and you've spent 3+ attempts

### Signs You Should KEEP GOING
- Each failure teaches something specific and actionable
- You have a concrete hypothesis for why the next approach will differ
- The potential value justifies the token investment (high-ROI feature)
- The user has explicitly asked you to keep trying

## What "Trying Harder" Actually Means

It does NOT mean:
- Running the same code with different magic numbers
- Adding more complexity hoping something sticks
- Ignoring the diagnosis and trying randomly

It DOES mean:
- **Analyzing the failure deeply**: WHERE in the data did it regress? On which subset of cases?
- **Changing your approach fundamentally**: If additive integration failed, try conditional. If linear scaling failed, try sigmoid. If individual integration failed, try joint optimization.
- **Learning from each attempt**: Each failure should narrow the search space, not repeat it
- **Designing better experiments**: If the first test was poorly designed (wrong baseline, wrong metric, no controls), fix the experiment design, not just the feature

## The Critical Distinction

| Situation | What It Means | What To Do |
|-----------|---------------|------------|
| Proven-valuable feature, integration regressed | **Execution failure** — approach was wrong, not the idea | Diagnose, redesign approach, retry (up to 3x then escalate) |
| Unproven idea, first attempt failed | **Inconclusive** — need more data | Test in isolation, gather evidence, then decide |
| 3+ well-designed attempts, no improvement on any | **Incompatible with current architecture** | Shelve with detailed notes. Revisit when architecture changes. |
| Same approach tried repeatedly with minor tweaks | **Not learning, just guessing** | STOP. Step back. Redesign from scratch or escalate. |

## Never Do This

- Label a proven-valuable system as a "failed feature" in memory or logs
- Set coefficients to 0.00 and call it done when evidence shows the feature has value
- Give up after 1-2 poorly designed attempts on something with proven value
- Assume that because YOUR implementation didn't work, the IDEA doesn't work
- Retry endlessly without learning — if Attempt 3 looks like Attempt 1, you're not iterating, you're looping

## Always Do This

1. **Check evidence first**: Does this idea have proven independent value? (see Evidence Gate above)
2. **Diagnose the failure specifically**: Not "it didn't work" but "it regressed on X subset because Y"
3. **Preserve the baseline**: Never corrupt a working algorithm — always be able to revert
4. **Try a fundamentally different approach**, not the same thing with different numbers:
   - Different scaling (linear → sigmoid → conditional)
   - Different scope (global → subset-conditional)
   - Different integration point (pre-score → post-score → ensemble)
   - Joint optimization instead of individual (parallel-sweep the full parameter space)
5. **Log what you LEARNED**, not just outcomes:
   - "Additive at 0.15 regressed because it overwhelmed the base signal on close matchups"
   - "Signal is strongest when differential > 2.0; negligible otherwise"
   - "Next: try conditional application only when differential exceeds threshold"
6. **Escalate at 3 attempts**: Present findings to user, let them decide next steps
7. **Optimize holistically when appropriate**: Variables interact — a feature that hurts at weight=0.15 might be essential at weight=0.03 with other coefficients adjusted

## Integration with Other Skills

- **backtest**: After a failed integration, backtest to understand WHERE and WHY it regressed
- **parallel-sweep**: Use multi-agent sweeps to search the joint parameter space efficiently — don't hand-tune
- **error-memory**: Log WHAT WAS LEARNED, never log the IDEA as failed
- **sports_backtesting_protocol**: All retry attempts must follow the full protocol including overfitting checks
- **token-awareness**: This skill respects token budgets — 3 attempts max before escalating

## Rules

1. **Evidence gates persistence** — Only fight for ideas with proven independent value
2. **3 attempts then escalate** — Don't silently burn tokens. Present findings, let the user decide.
3. **Each retry must be fundamentally different** — Same approach + different numbers = not learning
4. **Log lessons, not labels** — Write what you learned, never "X is a failed feature"
5. **Preserve baseline always** — Every attempt must be safely revertible
6. **Diagnose before retrying** — If you can't explain why it failed, you can't design a better attempt
7. **Stay humble** — "I haven't figured out how to integrate this YET" not "this doesn't work"
8. **Respect the user's time** — Persistence is valuable; stubbornness is wasteful. Know the difference.
