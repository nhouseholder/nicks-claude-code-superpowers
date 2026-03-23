---
name: verification-before-completion
description: Use when about to claim work is complete, fixed, or passing, before committing or creating PRs - requires running verification commands and confirming output before making any success claims; evidence before assertions always
---

# Verification Before Completion

**Core principle:** Evidence before claims, always.

## Speed Tiers — Match Verification to Risk

| Change Type | Verification | Example |
|------------|-------------|---------|
| **Config/text/style only** | Mental trace — no command needed | Changed a color, updated a string |
| **Single function, clear logic** | One targeted test or quick run | Added a null check, fixed a typo |
| **Multi-file feature or bug fix** | Full verification (run tests, check output) | New endpoint, scoring change |
| **Deploy, migration, auth** | Full verification + smoke test | Anything user-facing in production |

Tier 1-2: mental verification sufficient. **Tier 3-4: no completion claims without fresh verification evidence.**

## Baseline Before Changing

**Before modifying ANY data, values, or calculations, record the current state.**

```
BEFORE: ML = +107.89u (355W-142L), Method = +171.76u (205W-150L), ...
CHANGING: [what you're about to change]
AFTER: [verify these match or improve on BEFORE — any decrease = regression]
```

If you don't record BEFORE values, you cannot detect regressions.

## Re-Read Your Own Output

Before sending ANY response that contains data:
1. Read the table/data you're about to send
2. Ask: "Does row X make mathematical sense?" Pick the most suspicious one.
3. If any number looks wrong → fix before sending
4. If you can't verify → say "I'm not confident in these numbers"

## Self-Contradiction Check

Before sending, check that WORDS match DATA:
- "Fixed! All bet types show correct P/L" while table shows $0.00 = self-contradiction
- "All N issues addressed" while only 2 of 5 done = self-contradiction

**Rule:** Triumphant claim + contradicting evidence = fix the data or retract the claim.

## Multi-Item Completion Check

When request contains N distinct items:
1. **Enumerate** all N items before starting
2. **Track** completion of each
3. **Verify count** before claiming done — items listed must match items addressed

If you can't complete all: "Completed items 1-3 of 5. Items 4-5 (X, Y) still need to be addressed."

## The Gate Function (Tier 3-4 only)

```
1. IDENTIFY: What command proves this claim?
2. RUN: Execute the FULL command (fresh, complete)
3. READ: Full output, check exit code, count failures
4. VERIFY: Does output confirm the claim?
   - NO: State actual status with evidence
   - YES: State claim WITH evidence
5. ONLY THEN: Make the claim
```

## Output Verification — Check What the User Sees

**"I edited the code" is NOT verification. Check the OUTPUT.**

- Web/UI: Use Chrome tools, preview, or curl to check the rendered page
- Data/tables: Pick one row and manually verify values. Verify totals match sums.
- Algorithm/pipeline: Check actual output file, not just console "success"

### Self-Challenge (for data/math outputs)

Before delivering ANY output with numbers, pick ONE concrete data point and verify it:
1. **Select the most suspicious value** — the one easiest to get wrong
2. **Trace it from source to output** — follow the actual data path
3. **Does it make sense?** — 20 wins with $0 profit is wrong. 95% accuracy in sports is wrong.

**Red flags that demand a challenge:**
- Round numbers where messy ones are expected ($0.00, 100%, exactly 50)
- All values identical in a column that should vary
- "Fixed!" after changing only one line of a multi-path function
- Output that perfectly matches your prediction (confirmation bias)

**Always fires on re-fixes** — if it was wrong once, assume it could be wrong again.

## Common Failures

| Claim | Requires | Not Sufficient |
|-------|----------|----------------|
| Tests pass | Test output: 0 failures | Previous run, "should pass" |
| Build succeeds | Build command: exit 0 | Linter passing |
| Bug fixed | Test original symptom | Code changed, assumed fixed |
| UI looks right | Screenshot or DOM check | "I updated the component" |
| Table is correct | Verify actual cell values | "I added the column" |

## Red Flags — STOP

- Using "should", "probably", "seems to"
- Expressing satisfaction before verification ("Great!", "Done!")
- About to commit/push/PR without verification
- Trusting agent success reports without checking
- **ANY wording implying success without having run verification**

## Deep Verification Mode (Pre-PR / Pre-Deploy)

For major completions, run 6-phase verification:

1. **Build**: `npm run build 2>&1 | tail -20` — fails → STOP
2. **Type Check**: `npx tsc --noEmit` or `pyright .`
3. **Lint**: `npm run lint` or `ruff check .`
4. **Test Suite**: `npm run test -- --coverage` — report total, passed, failed, coverage %
5. **Security Scan**: Check for hardcoded secrets, console.log, debug artifacts
6. **Diff Review**: `git diff --stat` — review each file for unintended changes

Use Deep Mode before PRs, deploys, major refactors, multi-file features. Standard Gate Function sufficient for quick fixes.

## Repeat Bug Escalation

When user reports the SAME issue after you claimed it fixed:

| Attempt | Required Response |
|---------|-------------------|
| 1st "still broken" | Re-verify with ACTUAL testing, not mental trace. Reproduce first. |
| 2nd "STILL broken" | Full reproduce → fix → prove-fixed cycle. Show exact evidence. |
| 3rd+ | STOP fixing. Re-read the entire flow. You're fixing symptoms, not root cause. |

Each repeated report DOUBLES verification obligation. Never apply the same level of verification that already failed.

Escalation cap: After 3 escalations, flag to user as possible flaky test or infrastructure issue. External failures (network, CI infra) do NOT trigger escalation.
