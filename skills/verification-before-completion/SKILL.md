---
name: verification-before-completion
description: Use when about to claim work is complete, fixed, or passing, before committing or creating PRs - requires running verification commands and confirming output before making any success claims; evidence before assertions always
---

# Verification Before Completion

## Overview

Claiming work is complete without verification is dishonesty, not efficiency.

**Core principle:** Evidence before claims, always.

**Violating the letter of this rule is violating the spirit of this rule.**

## Speed Tiers — Match Verification to Risk

Not every change needs a full verification ceremony:

| Change Type | Verification | Example |
|------------|-------------|---------|
| **Config/text/style only** | Mental trace — no command needed | Changed a color, updated a string, edited docs |
| **Single function, clear logic** | One targeted test or quick run | Added a null check, fixed a typo in logic |
| **Multi-file feature or bug fix** | Full verification (run tests, check output) | New endpoint, scoring change, data pipeline fix |
| **Deploy, migration, auth** | Full verification + smoke test | Anything user-facing in production |

**The Iron Law still applies to Tier 3-4**: No completion claims without fresh verification evidence. But Tier 1-2 don't need a command run — mental verification or a quick check is sufficient.

## The Gate Function (Tier 3-4 only)

```
BEFORE claiming any status or expressing satisfaction:

1. IDENTIFY: What command proves this claim?
2. RUN: Execute the FULL command (fresh, complete)
3. READ: Full output, check exit code, count failures
4. VERIFY: Does output confirm the claim?
   - If NO: State actual status with evidence
   - If YES: State claim WITH evidence
5. ONLY THEN: Make the claim

Skip any step = lying, not verifying
```

## Common Failures

| Claim | Requires | Not Sufficient |
|-------|----------|----------------|
| Tests pass | Test command output: 0 failures | Previous run, "should pass" |
| Linter clean | Linter output: 0 errors | Partial check, extrapolation |
| Build succeeds | Build command: exit 0 | Linter passing, logs look good |
| Bug fixed | Test original symptom: passes | Code changed, assumed fixed |
| Regression test works | Red-green cycle verified | Test passes once |
| Agent completed | VCS diff shows changes | Agent reports "success" |
| Requirements met | Line-by-line checklist | Tests passing |

## Red Flags - STOP

- Using "should", "probably", "seems to"
- Expressing satisfaction before verification ("Great!", "Perfect!", "Done!", etc.)
- About to commit/push/PR without verification
- Trusting agent success reports
- Relying on partial verification
- Thinking "just this once"
- Tired and wanting work over
- **ANY wording implying success without having run verification**

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Should work now" | RUN the verification |
| "I'm confident" | Confidence ≠ evidence |
| "Just this once" | No exceptions |
| "Linter passed" | Linter ≠ compiler |
| "Agent said success" | Verify independently |
| "I'm tired" | Exhaustion ≠ excuse |
| "Partial check is enough" | Partial proves nothing |
| "Different words so rule doesn't apply" | Spirit over letter |

## Key Patterns

**Tests:**
```
✅ [Run test command] [See: 34/34 pass] "All tests pass"
❌ "Should pass now" / "Looks correct"
```

**Regression tests (TDD Red-Green):**
```
✅ Write → Run (pass) → Revert fix → Run (MUST FAIL) → Restore → Run (pass)
❌ "I've written a regression test" (without red-green verification)
```

**Build:**
```
✅ [Run build] [See: exit 0] "Build passes"
❌ "Linter passed" (linter doesn't check compilation)
```

**Requirements:**
```
✅ Re-read plan → Create checklist → Verify each → Report gaps or completion
❌ "Tests pass, phase complete"
```

**Agent delegation:**
```
✅ Agent reports success → Check VCS diff → Verify changes → Report actual state
❌ Trust agent report
```

## Why This Matters

From 24 failure memories:
- the user said "I don't believe you" - trust broken
- Undefined functions shipped - would crash
- Missing requirements shipped - incomplete features
- Time wasted on false completion → redirect → rework
- Violates: "Honesty is a core value. If you lie, you'll be replaced."

## When To Apply

**ALWAYS before:**
- ANY variation of success/completion claims
- ANY expression of satisfaction
- ANY positive statement about work state
- Committing, PR creation, task completion
- Moving to next task
- Delegating to agents

**Rule applies to:**
- Exact phrases
- Paraphrases and synonyms
- Implications of success
- ANY communication suggesting completion/correctness

## Deep Verification Mode (Pre-PR / Pre-Deploy)

For major completions (features, PRs, deploys), run the full 6-phase verification:

### Phase 1: Build
```bash
npm run build 2>&1 | tail -20
```
If build fails → STOP. Fix before continuing.

### Phase 2: Type Check
```bash
npx tsc --noEmit 2>&1 | head -30    # TypeScript
pyright . 2>&1 | head -30            # Python
```

### Phase 3: Lint
```bash
npm run lint 2>&1 | head -30         # JS/TS
ruff check . 2>&1 | head -30         # Python
```

### Phase 4: Test Suite
```bash
npm run test -- --coverage 2>&1 | tail -50
```
Report: total, passed, failed, coverage %.

### Phase 5: Security Scan
Check for hardcoded secrets, console.log statements, debug artifacts.

### Phase 6: Diff Review
```bash
git diff --stat
```
Review each changed file for unintended changes, missing error handling, edge cases.

### Verification Report Format
```
VERIFICATION REPORT
==================
Build:     [PASS/FAIL]
Types:     [PASS/FAIL] (X errors)
Lint:      [PASS/FAIL] (X warnings)
Tests:     [PASS/FAIL] (X/Y passed, Z% coverage)
Security:  [PASS/FAIL] (X issues)
Diff:      [X files changed]

Overall:   [READY/NOT READY] for PR
```

### When to Use Deep Mode
- Before creating a PR
- Before deploying to production
- After major refactors
- After completing a multi-file feature

For quick fixes and single-file changes, the standard Gate Function is sufficient.

## Repeat Bug Escalation

When the user reports the SAME issue again after you claimed it was fixed:

| Attempt | What Happened | Required Response |
|---------|--------------|-------------------|
| **1st claim → user says "still broken"** | Your verification was insufficient | Re-verify with ACTUAL testing, not mental trace. Reproduce the failure first. |
| **2nd claim → user says "STILL broken"** | You failed to test the real code path | Full reproduce → fix → prove-fixed cycle. Show exact evidence. |
| **3rd+ claim → user is frustrated** | Something fundamental is wrong with your approach | STOP fixing. Step back. Re-read the entire flow. You're likely fixing symptoms, not the root cause. |

**The escalation rule**: Each repeated bug report DOUBLES your verification obligation. If mental trace was enough the first time and failed, real testing is required. If real testing failed, reproduce-first is required. Never apply the same level of verification that already failed.

## The Bottom Line

**No shortcuts for verification.**

Run the command. Read the output. THEN claim the result.

This is non-negotiable.
