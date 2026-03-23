---
name: self-challenge
description: Before delivering high-stakes outputs (data, calculations, fixes that were already attempted), argue against your own answer. Catch reasoning errors before the user sees them. Fires on math, data displays, and re-fix attempts.
weight: passive
---

# Self-Challenge — Am I Actually Right?

Before delivering outputs the user will judge for correctness, challenge your own reasoning.

## When to Fire

- Any output with numbers the user will read (tables, stats, P/L, percentages)
- Fixing something that was already "fixed" once (re-fix = approach was wrong)
- Claims of "all X are correct" or "everything works now"
- Data displays, charts, summaries with calculated values

**Skip for:** prose responses, code-only changes with test coverage, config edits, file organization.

## The Challenge (15 seconds)

Pick ONE concrete data point from your output and verify it manually:

1. **Select the most suspicious value** — the one that's easiest to get wrong
2. **Trace it from source to output** — follow the actual data path, not what you think the code does
3. **Does the number make sense?** — a fighter with 20 wins showing $0 profit is wrong. A 95% accuracy in sports betting is wrong. Trust your domain instincts.

## Red Flags That Demand a Challenge

- Round numbers where messy ones are expected ($0.00, 100%, exactly 50)
- All values identical in a column that should vary
- Output that perfectly matches what you predicted (confirmation bias)
- "Fixed!" after changing only one line of a multi-path function

## Action

- If the check passes → deliver with confidence, no announcement needed
- If it fails → fix before delivering. Say what you caught: "Caught an issue before sending — [X] was wrong because [Y]"
- **Never claim "all correct" without checking at least one value manually**

## Rules

1. Silent when passing — zero token cost on clean outputs
2. Always fires on re-fixes — if it was wrong once, assume it could be wrong again
3. One concrete check beats ten abstract assurances
4. "I edited the code" is not a check. "I traced row 3 and got $47.50 which matches" is a check.
