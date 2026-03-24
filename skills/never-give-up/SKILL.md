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

| Evidence Level | Action |
|----------------|--------|
| **Strong evidence** — proven profitable in isolation, backed by data | **Fight for it.** The integration problem is solvable. Try different approaches. |
| **No/counter evidence** — untested theory, no data, or 3+ failed well-designed attempts | **Test in isolation first** if theoretical. **Move on** if no evidence. **Shelve with notes** if counter-evidence. |

**The key insight:** This skill only demands persistence when there IS evidence. It does NOT demand persistence on every idea.

## Token Discipline — Don't Burn the House Down

### Budget Per Retry Cycle
Each retry attempt gets a budget. If you can't make progress within budget, **stop and escalate to the user** — don't silently burn tokens.

Default cap: 3 attempts with the SAME approach. If each attempt uses a genuinely DIFFERENT strategy (not just tweaking parameters), the cap resets. After 3 same-approach failures, either try a fundamentally different approach OR escalate to user. The evidence gate determines whether a new approach is worth trying.

- **Attempt 1**: Full implementation + backtest. If it fails, diagnose thoroughly.
- **Attempt 2**: Different approach informed by Attempt 1's diagnosis. Smaller, targeted change.
- **Attempt 3**: If still failing with the same approach, STOP. Present findings to the user:
  - "Here's what I tried, here's what I learned, here's what I think the issue is"
  - "I recommend trying X next — want me to proceed?"
  - Let the user decide whether to continue, pivot, or shelve
- **Beyond 3**: If the next attempt is a genuinely different strategy, proceed. The cap applies per-approach, not per-idea.

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

## Model Escalation — Bring a Bigger Brain

When retrying a failed task, consider whether the problem needs a more capable model, not just a different approach. This is especially true when the failure mode is **reasoning quality** (wrong approach chosen, subtle bug missed, architectural misunderstanding) rather than execution (typo, wrong file, missing import).

### Escalation Ladder

| Attempt | Model | When to escalate |
|---------|-------|-----------------|
| 1 | Whatever model-router selected | First try — trust the routing |
| 2 | Same model, different approach | If the failure was execution, not reasoning |
| 2 | Escalate to Opus | If the failure was reasoning: wrong approach, subtle bug, architectural issue |
| 3 | Opus (if not already) | Always escalate by attempt 3 — if two tries failed, the problem is harder than classified |

### How to Trigger Escalation

When you detect that a retry is needed and the failure mode suggests reasoning quality:
- **Say it explicitly**: "This needs deeper reasoning — escalating to Opus for attempt 2"
- **In headless/orchestrator mode**: The orchestrator handles model selection externally
- **In interactive sessions**: Recommend the user switch models if on Sonnet: "This bug is subtler than expected. Consider switching to Opus for this fix."

### Escalation Signals (suggests model upgrade needed)

- Error is in logic/architecture, not syntax
- The fix attempt introduced new bugs (reasoning about side effects)
- Multiple interacting systems need to be understood together
- The task requires reading and synthesizing 5+ files
- Previous attempt's approach was fundamentally wrong (not just details)

### Non-Escalation Signals (same model, different approach)

- Typo, wrong variable name, missing import
- Clear error message pointing to the fix
- Single-file change with obvious solution
- Previous attempt was close but had a small bug

## What "Trying Harder" Actually Means

It does NOT mean:
- Running the same code with different magic numbers
- Adding more complexity hoping something sticks
- Ignoring the diagnosis and trying randomly

It DOES mean:
- **Analyzing the failure deeply**: WHERE in the data did it regress? On which subset of cases?
- **Changing your approach fundamentally**: If additive integration failed, try conditional. If linear scaling failed, try sigmoid. If individual integration failed, try joint optimization.
- **Escalating the model when reasoning is the bottleneck**: If two attempts failed on a subtle problem, a bigger model might see what the smaller one can't.
- **Learning from each attempt**: Each failure should narrow the search space, not repeat it
- **Designing better experiments**: If the first test was poorly designed (wrong baseline, wrong metric, no controls), fix the experiment design, not just the feature

## Experiment Design — Don't Waste Attempts on Bad Tests

A "failed attempt" that was poorly designed teaches you nothing and wastes tokens. Before EACH retry, write down (mentally, not to the user):

1. **Hypothesis**: "I believe [specific change] will improve [specific metric] because [specific reason]"
2. **Expected outcome**: "If this works, I expect accuracy to increase by roughly X% on Y subset"
3. **Failure signal**: "If this doesn't work, it will tell me [what I'll learn from the failure]"
4. **Controls**: "I'll compare against [specific baseline] with [specific holdout data]"

If you can't fill in all 4, your experiment isn't ready. Design it better before running it.

### What Makes an Attempt "Well-Designed" vs "Poorly Designed"

| Well-Designed | Poorly Designed |
|--------------|----------------|
| Clear hypothesis with domain reasoning | "Let's try this and see what happens" |
| One variable changed at a time (or deliberate multi-variable with controls) | Changed 5 things at once, can't tell what helped |
| Compared against known-good baseline | Compared against nothing, just looked at absolute numbers |
| Used holdout data for validation | Tested on the same data used to tune |
| Analyzed WHERE it improved/regressed | Only looked at aggregate accuracy |
| Learned something specific from the result | "It didn't work" with no further analysis |

**The rule:** A failed well-designed experiment is valuable. A failed poorly-designed experiment is just wasted tokens. Never count poorly-designed attempts toward the 3-attempt cap — they don't count as real tries.

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

## Rules

1. **Evidence gates persistence** — Only fight for ideas with proven independent value
2. **3 same-approach attempts then escalate or change strategy** — Don't silently burn tokens. Genuinely different strategies reset the cap.
3. **Each retry must be fundamentally different** — Same approach + different numbers = not learning
4. **Escalate the model by attempt 3** — If two attempts failed, the problem is harder than classified. Bring Opus.
5. **Log lessons, not labels** — Write what you learned, never "X is a failed feature"
6. **Preserve baseline always** — Every attempt must be safely revertible
7. **Diagnose before retrying** — If you can't explain why it failed, you can't design a better attempt
8. **Stay humble** — "I haven't figured out how to integrate this YET" not "this doesn't work"
9. **Respect the user's time** — Persistence is valuable; stubbornness is wasteful. Know the difference.
