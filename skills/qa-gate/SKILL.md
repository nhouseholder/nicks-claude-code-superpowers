---
name: qa-gate
description: Mandatory QA gate before delivering any feature, fix, or component. Dispatches an independent testing agent to exercise the implementation end-to-end before returning results to the user. The user should never be the one finding bugs — Claude finds them first.
---

# QA Gate — Test It Before You Ship It

## The Problem This Solves

Claude delivers a feature, says "done," and the user immediately finds bugs. This is unacceptable. The user should NEVER be the first person to discover that something doesn't work. Claude must be its own QA department — testing every deliverable before handing it back.

## When This Fires

### Complexity Tiers — Match QA Effort to Change Size

| Tier | Change Type | QA Level |
|------|------------|----------|
| **Tier 3 — Full QA Gate** | New feature (multi-file), full-stack changes, algorithm overhaul, deployment-bound work | Dispatch independent QA subagent, full checklist, fix before delivery |
| **Tier 2 — Inline Verification** | Single-component change, bug fix, API endpoint tweak, algorithm parameter change | Trace the code path with real inputs, check edge cases inline, no subagent needed |
| **Tier 1 — Quick Sanity Check** | Small fix (1-2 lines), style/layout tweak, single function change | Mentally verify correctness, check for obvious breakage, move on |
| **Skip** | Config-only, docs, git ops, memory/skill files, unused code deletion, user says "just push it" | No QA needed |

**The rule:** Tier 3 is the mandatory full gate. Tiers 1-2 scale down proportionally. Never skip entirely on behavioral changes.

## The QA Protocol

### Step 1 — Determine Test Scope

Based on what changed, identify what needs testing:

| Change Type | Test Scope |
|-------------|------------|
| **Frontend component** | Render without errors, props/state work, user interactions, edge cases (empty data, loading, error states) |
| **API endpoint** | Request/response shape, error handling, auth, edge cases (missing params, invalid input) |
| **Algorithm/scoring** | Input → output correctness, edge cases, regression against known-good values |
| **Database/data** | Schema integrity, query correctness, migration safety |
| **Full feature** | All of the above + integration between layers |
| **Bug fix** | The specific bug is fixed + no regression in surrounding functionality |

### Step 2 — Execute Tests (dispatch subagent when beneficial)

For non-trivial changes, dispatch an independent QA subagent:

```
Agent brief: "You are a QA engineer. Test the following implementation:
- What was built: [description]
- Files changed: [list]
- Expected behavior: [what it should do]
- Test these scenarios: [specific test cases]
Report: pass/fail for each scenario, any bugs found, any edge cases missed."
```

**When to use a subagent vs test inline:**
- **Subagent**: Multi-file features, UI components, API endpoints, anything with multiple interaction paths
- **Inline**: Single-function fixes, algorithm tweaks with clear input/output, simple config changes that still need verification

### Step 3 — Test Checklist (mental or actual, based on scope)

#### Frontend Changes
- [ ] Component renders without console errors
- [ ] All interactive elements respond correctly (clicks, inputs, navigation)
- [ ] Loading states display properly
- [ ] Empty/null data doesn't crash the component
- [ ] Error states are handled (API failure, invalid data)
- [ ] Mobile/responsive layout isn't broken (if applicable)
- [ ] No regressions in adjacent components

#### Backend/API Changes
- [ ] Endpoint returns correct response shape
- [ ] Error cases return appropriate status codes
- [ ] Input validation catches bad data
- [ ] Auth/permissions enforced correctly
- [ ] No N+1 queries or performance regressions

#### Algorithm Changes
- [ ] Output matches expected values for known inputs
- [ ] Edge cases handled (zero, null, extreme values, empty arrays)
- [ ] No regression against baseline metrics
- [ ] Performance acceptable (not 10x slower)

#### Data Pipeline Changes
- [ ] Idempotent (running twice doesn't duplicate data)
- [ ] Handles missing/malformed source data gracefully
- [ ] Output schema matches consumer expectations
- [ ] Error reporting works (failures don't fail silently)

### Step 4 — Fix Before Delivering

If ANY test fails:
1. Fix the issue immediately
2. Re-run the failed tests
3. Only proceed to delivery when all tests pass
4. Mention what you caught and fixed: "Found and fixed: [issue] — [how it was resolved]"

This is NOT optional. Do not deliver known-broken code with a disclaimer.

### Bug Fix Verification — The "Try Now" Ban

**When fixing a reported bug, you MUST prove the fix works before telling the user to try it.**

This is the #1 trust-destroying failure mode: user reports a bug → Claude changes code → Claude says "try now, it should work" → it still doesn't work → repeat 3-4 times → user loses faith.

#### Bug Fix Verification Protocol

| Attempt | Minimum Verification | Rationale |
|---------|---------------------|-----------|
| **1st fix** | Tier 2 minimum — trace the EXACT bug scenario through the fixed code with real inputs. Run the app/tests if possible. | Standard diligence |
| **2nd fix (same bug)** | Tier 3 mandatory — dispatch QA subagent. The mental trace clearly failed the first time. | Escalation — your first fix didn't work |
| **3rd+ fix (same bug)** | Tier 3 + reproduce the bug first. Before fixing, PROVE you can trigger the original failure. Then fix. Then prove the failure is gone. | Full red-green cycle — something fundamental was missed |

#### The Rules of Bug Fix Verification

1. **NEVER say "try now" or "it should work" without having tested the exact failure scenario yourself**
2. **If the user reports the same bug twice, your previous verification was insufficient** — escalate, don't repeat the same level of checking
3. **Reproduce before fixing on 2nd+ attempts** — if you can't trigger the bug, you can't confirm you fixed it
4. **Run the actual code path** — don't just read the code and think it looks right. Start the server, hit the endpoint, render the component, upload the file, whatever the bug involves
5. **Show your evidence** — "I tested this by [exact action] and got [exact result]" not "this should work now"
6. **If you can't test it yourself** (e.g., requires user's browser, specific device, auth credentials), say so explicitly: "I've verified X and Y, but I can't test Z from here — please verify that specific part"

#### What "Testing a Bug Fix" Actually Means

```
❌ BAD: Change code → "Try now, it should be working"
❌ BAD: Change code → Run build → "Build passes, should be fixed"
❌ BAD: Change code → Read the code → "The logic looks correct now"

✅ GOOD: Change code → Run the app → Trigger the exact bug scenario → Confirm it no longer fails → "Tested: [action] now produces [result] instead of [old failure]"
✅ GOOD: Change code → Write a test for the exact failure → Run test → Green → "Regression test passes"
✅ GOOD: Change code → Can't test end-to-end → "I've fixed [root cause] and verified [what I could check], but please test [specific user action] since I can't simulate your browser environment"
```

### Step 5 — Report to User

When delivering, include a brief QA summary:
```
Tested: [what was tested]
Verified: [key scenarios that passed]
Fixed during QA: [anything caught and fixed, if applicable]
```

Keep this to 2-3 lines. Don't write a QA novel — just enough so the user knows it was tested.

## What "Testing" Actually Means

It does NOT mean:
- Just running `npm run build` and seeing no errors
- Just reading the code and thinking it looks right
- Just running existing test suites (those may not cover the new feature)
- Saying "I've verified this works" without actually verifying

It DOES mean:
- **Actually exercising the code path** — trace real inputs through the logic
- **Checking the output** — does it produce the right result?
- **Testing edge cases** — empty data, null values, error conditions
- **Verifying integration** — does it work with the components it connects to?
- **Running the app** (when possible) — start the dev server, hit the endpoint, render the component
- **Reading console/terminal output** — don't just run a command, read what it said

## Subagent QA Brief Template

When dispatching a QA subagent, give it everything it needs:

```
You are an independent QA engineer. Your job is to find bugs before the user does.

## What was built
[Description of the feature/fix]

## Files to review
[List of changed files with brief description of each change]

## Test scenarios
1. [Happy path — normal expected usage]
2. [Edge case — empty/null/missing data]
3. [Error path — what happens when things go wrong]
4. [Integration — does it work with connected components]
5. [Regression — does existing functionality still work]

## How to test
- Read the changed files
- Trace the logic with concrete inputs
- Check for: unhandled errors, missing null checks, incorrect state management,
  broken imports, type mismatches, async race conditions
- If a dev server is running, test the actual endpoint/page
- Report every issue found, ranked by severity

## Output format
For each scenario: PASS or FAIL with details
Bugs found: [list with file:line and description]
Recommendation: SHIP or FIX FIRST
```

## Token Economics — QA Must Be Efficient

QA is not an excuse to burn tokens. Match testing effort to the tier:

| Tier | Token Budget | Method |
|------|-------------|--------|
| **Tier 1** (quick sanity) | ~10-20 tokens | Mental trace only, no output |
| **Tier 2** (inline verify) | ~50-100 tokens | Trace code with real inputs, check 2-3 scenarios |
| **Tier 3** (full gate) | ~200-500 tokens | Subagent with focused brief, structured report |

**Efficiency rules:**
- Don't re-test what you just built and know works — focus on integration points and edge cases
- Don't test obvious things (does a React component render JSX? Yes, that's what React does)
- Do test non-obvious things (does the component handle null props? Does the API validate input?)
- Subagent briefs should be FOCUSED — don't send the entire codebase context, send the changed files and specific test scenarios
- One well-designed test that covers 3 scenarios > three separate tests that each cover one

**Net impact**: Finding a bug before delivery costs ~50 tokens. The user finding it, reporting it, and Claude diagnosing + fixing it costs 500+. QA is always net-positive on tokens.

## Integration

- **verification-before-completion**: They fire in sequence: qa-gate DURING development (does the feature work?), then verification-before-completion as the FINAL gate before delivery (proof the commands pass, proof the claim is true). Order: build → qa-gate → fix → verification-before-completion → deliver.
- **proactive-qa**: Proactive QA anticipates issues during development. QA gate is the structured checkpoint after development. They don't overlap — proactive-qa is a mindset, qa-gate is a process.
- **fix-loop**: If QA gate finds failures, use fix-loop methodology to resolve them
- **screenshot-dissector**: For frontend changes, if a preview is available, use screenshot-dissector to visually verify. For Tier 2 frontend changes where visual rendering is critical (layout, styling, responsive), run screenshot-dissector in parallel with code verification.
- **calibrated-confidence**: If confidence is at GUESSING level on the change being tested, escalate from Tier 2 (inline) to Tier 3 (full subagent). Lack of confidence = lack of testing confidence.
- **zero-iteration**: Zero-iteration catches bugs mentally before writing code. QA gate catches bugs that slipped through after writing code.
- **test-driven-development**: TDD writes tests first. QA gate verifies the COMPLETE feature works, including aspects tests don't cover.

## Rules

1. **Never deliver untested code** — If it changed behavior, it gets tested before the user sees it
2. **The user should never find bugs first** — That's Claude's job
3. **Fix before delivering** — Don't deliver with "known issues." Fix them.
4. **Test the actual behavior, not just the code** — Reading code is not testing. Exercise the code path.
5. **Scope appropriately** — Config changes don't need a QA subagent. New features do.
6. **Report what you tested** — Brief QA summary so the user knows it was verified
7. **Subagent for non-trivial work** — Independent eyes catch what the builder misses
8. **Edge cases are mandatory** — Happy path + at least one edge case, always
9. **Never say "try now" without evidence** — Bug fixes require proof. "Should work" is not proof.
10. **Escalate on repeat bugs** — 2nd report of the same bug = Tier 3 mandatory. Your first fix failed; your verification was insufficient.
