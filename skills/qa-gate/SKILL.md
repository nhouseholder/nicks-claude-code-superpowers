---
name: qa-gate
description: Mandatory QA gate before delivering any feature, fix, or component. Dispatches an independent testing agent to exercise the implementation end-to-end before returning results to the user.
weight: heavy
---

# QA Gate — Test It Before You Ship It

## Review Pipeline Coordination

QA gate is ONE part of the review pipeline — avoid stacking:

- **If dispatching-parallel-agents already ran spec + code review**: QA gate does Tier 1 only.
- **If a code review subagent already ran**: QA gate should skip.
- **If neither ran**: QA gate operates at full tier based on change complexity.

Never dispatch more than 2 total review agents for a single change.

## Code Review Triggers & Dispatch

### When to Request Review

**Mandatory:** After each task in subagent-driven development, after completing a major feature, before merge to main.

**Optional:** When stuck (fresh perspective), before refactoring (baseline check), after fixing a complex bug.

### SHA-Based Review Dispatch

```bash
BASE_SHA=$(git rev-parse HEAD~1)  # or origin/main
HEAD_SHA=$(git rev-parse HEAD)
git diff --name-only $BASE_SHA..$HEAD_SHA  # files to review
```

Dispatch with: what was implemented, plan/requirements, base and head SHAs, files changed, areas to scrutinize.

### Acting on Review Feedback

| Priority | Action |
|----------|--------|
| **Critical** | Fix immediately before proceeding |
| **Important** | Fix before proceeding to next task |
| **Minor** | Note for later, don't block progress |
| **Disagree** | Push back with technical reasoning |

## Complexity Tiers

| Tier | Change Type | QA Level |
|------|------------|----------|
| **Tier 3 — Full QA Gate** | New feature (multi-file), full-stack changes, algorithm overhaul, deployment-bound work | Dispatch independent QA subagent, full checklist, fix before delivery |
| **Tier 2 — Inline Verification** | Single-component change, bug fix, API endpoint tweak, algorithm parameter change | Trace code path with real inputs, check edge cases inline, no subagent needed |
| **Tier 1 — Quick Sanity Check** | Small fix (1-2 lines), style/layout tweak, single function change | Mentally verify correctness, check for obvious breakage |
| **Skip** | Config-only, docs, git ops, memory/skill files, unused code deletion, user explicitly requests skip | No QA needed |

## The QA Protocol

### Step 1 — Determine Test Scope

| Change Type | Test Scope |
|-------------|------------|
| **Frontend component** | Render without errors, props/state, user interactions, edge cases (empty, loading, error) |
| **API endpoint** | Request/response shape, error handling, auth, edge cases |
| **Algorithm/scoring** | Input → output correctness, edge cases, regression against known-good values |
| **Database/data** | Schema integrity, query correctness, migration safety |
| **Full feature** | All above + integration between layers |
| **Bug fix** | Specific bug fixed + no regression in surrounding functionality |

### Step 2 — Execute Tests

For non-trivial changes, dispatch an independent QA subagent with: what was built, files changed, expected behavior, specific test cases. Report: pass/fail per scenario, bugs found, edge cases missed.

**When to use subagent vs inline:**
- **Subagent**: Multi-file features, UI components, API endpoints, multiple interaction paths
- **Inline**: Single-function fixes, algorithm tweaks with clear input/output

### Step 3 — Test Checklist

#### Frontend
- [ ] Component renders without console errors
- [ ] Interactive elements respond correctly
- [ ] Loading/empty/error states display properly
- [ ] No regressions in adjacent components

#### Backend/API
- [ ] Correct response shape and status codes
- [ ] Input validation catches bad data
- [ ] Auth/permissions enforced
- [ ] No N+1 queries or performance regressions

#### Algorithm
- [ ] Output matches expected values for known inputs
- [ ] Edge cases handled (zero, null, extreme values, empty arrays)
- [ ] No regression against baseline metrics

#### Data Pipeline
- [ ] Idempotent (running twice doesn't duplicate)
- [ ] Handles missing/malformed data gracefully
- [ ] Output schema matches consumer expectations

### Step 4 — Fix Before Delivering

If ANY test fails: fix immediately, re-run, only deliver when all pass. Mention what you caught: "Found and fixed: [issue] — [resolution]"

Do not deliver known-broken code with a disclaimer.

### Bug Fix Verification Protocol

| Attempt | Minimum Verification |
|---------|---------------------|
| **1st fix** | Tier 2 minimum — trace the exact bug scenario through fixed code with real inputs |
| **2nd fix (same bug)** | Tier 3 mandatory — dispatch QA subagent. First mental trace failed. |
| **3rd+ fix** | Tier 3 + reproduce bug first. Prove you can trigger original failure, fix, prove failure is gone. |

**Rules:**
1. NEVER say "try now" without having tested the exact failure scenario yourself
2. Same bug reported twice = your previous verification was insufficient — escalate
3. Reproduce before fixing on 2nd+ attempts
4. Run the actual code path — don't just read the code
5. Show evidence: "I tested by [action] and got [result]"
6. If you can't test it (requires user's browser, specific device), say so explicitly

### Step 5 — Escalation Status

Don't reduce QA to binary pass/fail. Use escalation statuses:

| Status | Meaning | Action |
|--------|---------|--------|
| **DONE** | All tests pass, no concerns | Ship it |
| **DONE_WITH_CONCERNS** | Tests pass, but something feels off (perf, edge case coverage, design smell) | Ship with noted concerns for future attention |
| **NEEDS_CONTEXT** | Can't fully verify without information you don't have (user's env, specific data, third-party state) | Ship but explicitly state what you couldn't verify and why |
| **BLOCKED** | Tests fail or critical issue found that you cannot resolve | Do NOT ship. Explain the blocker clearly. |

### Step 6 — Report to User

```
Tested: [what was tested]
Status: [DONE | DONE_WITH_CONCERNS | NEEDS_CONTEXT | BLOCKED]
Verified: [key scenarios that passed]
Fixed during QA: [anything caught and fixed]
Concerns/Blockers: [if applicable]
```

Keep to 3-4 lines.

## Subagent QA Brief Template

```
You are an independent QA engineer. Find bugs before the user does.

## What was built
[Description]

## Files to review
[Changed files with brief description]

## Test scenarios
1. [Happy path]
2. [Edge case — empty/null/missing data]
3. [Error path]
4. [Integration with connected components]
5. [Regression — existing functionality]

## How to test
- Read changed files, trace logic with concrete inputs
- Check for: unhandled errors, missing null checks, incorrect state management,
  broken imports, type mismatches, async race conditions
- If dev server is running, test actual endpoint/page
- Report every issue, ranked by severity

## Output format
For each scenario: PASS or FAIL with details
Bugs found: [file:line and description]
Recommendation: SHIP or FIX FIRST
```

## Verification Before Completion (absorbed from verification-before-completion skill)

**Core principle:** Evidence before claims, always.

### Baseline Recording
Before modifying ANY data/values/calculations, record current state:
```
BEFORE: ML = +107.89u (355W-142L), Method = +171.76u...
CHANGING: [what you're about to change]
AFTER: [verify matches or improves — any decrease = regression]
```

### Self-Contradiction Check
Before sending, check WORDS match DATA:
- "Fixed! All bet types correct" while table shows $0.00 = contradiction
- "All N issues addressed" while only 2 of 5 done = contradiction
- **Rule:** Triumphant claim + contradicting evidence = fix data or retract claim

### Output Verification — Check What the User Sees
"I edited the code" is NOT verification. Check the OUTPUT:
- Web/UI: Use Chrome tools, preview, or curl
- Data/tables: Pick one row and manually verify values
- Algorithm: Check actual output file, not just console "success"

### Self-Challenge (for data/math outputs)
Pick ONE suspicious value and trace it source → output. Red flags:
- Round numbers where messy ones expected ($0.00, 100%, exactly 50)
- All values identical in a column that should vary
- "Fixed!" after changing one line of a multi-path function

### Deep Verification Mode (Pre-PR / Pre-Deploy)
1. Build: `npm run build` — fails → STOP
2. Type Check: `npx tsc --noEmit` or `pyright .`
3. Lint: `npm run lint` or `ruff check .`
4. Test Suite: full run with coverage
5. Security Scan: hardcoded secrets, console.log, debug artifacts
6. Diff Review: `git diff --stat` — review for unintended changes

## Rules

1. **Never deliver untested code** — If it changed behavior, test before the user sees it
2. **Fix before delivering** — Don't deliver with "known issues"
3. **Test actual behavior, not just code** — Reading code is not testing
4. **Scope appropriately** — Config changes don't need a QA subagent. New features do.
5. **Edge cases are mandatory** — Happy path + at least one edge case, always
6. **Never say "try now" without evidence** — Bug fixes require proof
7. **Escalate on repeat bugs** — 2nd report = Tier 3 mandatory
8. **Record baselines** — Before changing data, capture BEFORE values
9. **Self-contradict check** — Words must match data before sending
