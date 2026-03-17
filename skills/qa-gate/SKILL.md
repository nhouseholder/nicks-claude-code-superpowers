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

- **verification-before-completion**: QA gate extends this — verification checks commands pass, QA gate checks the FEATURE works
- **proactive-qa**: Proactive QA anticipates issues during development. QA gate is the final checkpoint before delivery.
- **fix-loop**: If QA gate finds failures, use fix-loop methodology to resolve them
- **screenshot-dissector**: For frontend changes, if a preview is available, use screenshot-dissector to visually verify
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
