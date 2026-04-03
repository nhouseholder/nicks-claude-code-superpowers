---
name: design-sprint
description: Run a structured 5-phase design sprint — problem framing, sketching, deciding, prototyping, testing. Use at the START of a project or feature, not the end. Triggers on "run a design sprint", "ideation workshop", "validate this idea", "new product", or any greenfield project kickoff.
weight: heavy
---

# Design Sprint — Structured Product Ideation

A compressed 5-phase design sprint adapted for AI-assisted development. Based on Google Ventures' Sprint methodology — problem framing through testing in one session instead of five days.

## When This Fires

- "run a design sprint"
- "ideation workshop"
- "validate this idea"
- Starting a new product or major feature from scratch
- "I have an idea for..." followed by something that needs validation
- Any greenfield project where requirements are unclear

## When NOT to Use

- Bug fixes, maintenance, or incremental features
- Clear requirements already exist (use structured-build instead)
- Redesign of existing product (use site-redesign instead)

## Phase 1: FRAME — Define the Problem (10 min)

### Map the Challenge
1. **Long-term goal:** What does success look like in 6 months?
2. **Sprint questions:** What must be true for this to work? List the riskiest assumptions.
3. **Target user:** Who exactly is this for? Be specific (not "everyone").
4. **Map the journey:** Sketch the user's current path from need → solution. Where does it break?

### Ask the User (use AskUserQuestion)
- What problem are you solving?
- Who has this problem? How do they solve it today?
- What's the riskiest assumption — the thing that, if wrong, kills the idea?

**Gate:** Problem statement, target user, and top 3 risks must be written down before continuing.

## Phase 2: SKETCH — Generate Solutions (15 min)

### Diverge: Multiple Approaches
Generate 3 distinct approaches. Each must be meaningfully different — not variations of the same idea.

For each approach, define:
- **Core interaction:** What does the user DO? (one sentence)
- **Key screen/view:** What does the main interface look like?
- **Differentiation:** Why would someone choose this over existing solutions?

### Use These Skills
- Load `ui-ux-pro-max` for style/palette/font recommendations
- Load `frontend-design` for anti-slop visual direction
- Reference `hooked-ux` for retention considerations

**Gate:** 3 distinct approaches documented. Each has a core interaction, key screen concept, and differentiation.

## Phase 3: DECIDE — Pick the Winner (5 min)

### Evaluate Against
| Criteria | Approach A | Approach B | Approach C |
|----------|-----------|-----------|-----------|
| Solves the core problem? | | | |
| Feasible in current stack? | | | |
| User would understand in 5 seconds? | | | |
| Addresses riskiest assumption? | | | |
| Simplest to build? | | | |

Present the table to the user. Let them pick — or recommend with rationale.

**Gate:** One approach selected. User has approved it.

## Phase 4: PROTOTYPE — Build the Minimum Testable Version (bulk of session)

### Build Rules
- **Facade, not product.** Build enough to test the hypothesis — not a production app.
- **One flow only.** The critical user journey. No settings, no edge cases, no auth.
- **Real content.** No lorem ipsum. Use realistic data for the target domain.
- **Style matters.** Run `refactoring-ui` audit. First impressions drive feedback.

### Use These Skills
- `frontend-design` — anti-slop visual direction
- `impeccable-design` — slop detection checklist
- `refactoring-ui` — visual audit before showing to anyone
- `react-best-practices` — if building in React/Next.js

**Gate:** Prototype runs. Core flow works. Looks real enough to get honest feedback.

## Phase 5: TEST — Validate or Kill (10 min)

### Self-Test Protocol
Since you're testing with the user, not external users:

1. **Walk through the core flow.** Does it feel right? Where do you hesitate?
2. **5-second test:** Look at the main screen for 5 seconds, look away. What do you remember? What was confusing?
3. **Assumption check:** Does this prototype actually test the riskiest assumption from Phase 1?
4. **Kill question:** "If this existed today, would you use it?" (honest answer)

### Capture the Verdict
```
SPRINT RESULT
Idea: [one line]
Hypothesis tested: [the riskiest assumption]
Verdict: VALIDATED / NEEDS PIVOT / KILLED
Evidence: [what you learned]
Next step: [build it / pivot to X / abandon]
```

## Output

At the end of the sprint, deliver:
1. Problem statement + target user
2. The 3 approaches considered (and why the winner was picked)
3. Working prototype
4. Sprint verdict with evidence
5. Recommended next steps

## Relationship to Other Skills

- **brainstorming**: Lighter weight — explores options but doesn't prototype or test. Use for features, not products.
- **spec-interview**: Captures requirements. Design sprint VALIDATES the idea before writing a spec.
- **structured-build**: Executes an approved plan. Design sprint comes BEFORE you have a plan.
- **site-redesign**: Redesigns existing products. Design sprint creates new ones.
