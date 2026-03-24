---
name: systematic-debugging
description: Use when encountering any bug, test failure, or unexpected behavior, before proposing fixes
weight: light
---

# Systematic Debugging

## Core Principle

**ROOT CAUSE FIRST** — except for obvious fixes (typos, missing imports, wrong variable names) where the cause IS the fix. For anything non-trivial, complete Phase 1 before proposing fixes.

## The Four Phases

Complete each phase before proceeding to the next.

### Phase 1: Root Cause Investigation

**BEFORE attempting ANY fix:**

1. **Read Error Messages Carefully** — Full stack traces, line numbers, file paths, error codes
2. **Reproduce Consistently** — If not reproducible, gather more data, don't guess
3. **Check Recent Changes** — Git diff, recent commits, new dependencies, config changes, environmental differences
4. **Gather Evidence in Multi-Component Systems**

   When system has multiple components (CI → build → signing, API → service → database):
   ```
   For EACH component boundary:
     - Log what data enters/exits component
     - Verify environment/config propagation
   Run once → analyze evidence → identify failing component → investigate
   ```

5. **Trace Data Flow** — Trace backwards from the symptom: Where does the bad value originate? Keep tracing up until you find the source. Fix at source, not at symptom.

### Phase 2: Pattern Analysis

1. **Find Working Examples** — Locate similar working code in same codebase
2. **Compare Against References** — Read reference implementations COMPLETELY, don't skim
3. **Identify Differences** — List every difference, however small. Don't assume "that can't matter"
4. **Understand Dependencies** — What components, settings, config, environment does this need?

### Phase 3: Hypothesis and Testing

1. **Form Single Hypothesis** — "I think X is the root cause because Y"
2. **Test Minimally** — Smallest possible change, one variable at a time
3. **Verify** — Worked → Phase 4. Didn't work → new hypothesis. Don't stack fixes.
4. **When You Don't Know** — Say so. Research more. Don't pretend.

### Phase 4: Implementation

1. **Create Failing Test Case** — Use `superpowers:test-driven-development` skill
2. **Implement Single Fix** — ONE change at a time. No "while I'm here" improvements.
3. **Verify Fix** — Test passes? No regressions? Issue resolved?
4. **If Fix Doesn't Work**
   - If < 3 attempts: Return to Phase 1, re-analyze with new information
   - **If >= 3 attempts: STOP and question the architecture (step 5)**

5. **If 3+ Fixes Failed: Question Architecture**

   Pattern indicating architectural problem:
   - Each fix reveals new shared state/coupling in different places
   - Fixes require massive refactoring
   - Each fix creates new symptoms elsewhere

   **STOP and question fundamentals:**
   - Is this pattern fundamentally sound?
   - Should we refactor architecture vs. continue fixing symptoms?
   - **Discuss with user before attempting more fixes**

## Red Flags — STOP and Return to Phase 1

- "Quick fix for now, investigate later"
- "Just try changing X and see if it works"
- "Skip the test, I'll manually verify"
- "It's probably X, let me fix that"
- "I don't fully understand but this might work"
- Proposing solutions before tracing data flow
- "One more fix attempt" (when already tried 2+)
- Each fix reveals new problem in different place
- Listing fixes without investigation

**If 3+ fixes failed:** Question the architecture (Phase 4.5)

**Note:** qa-gate escalates to Tier 3 on the 2nd failure — earlier than this threshold. QA escalation catches verification gaps; this 3-fix threshold catches architectural problems. Both can fire.

## Signals You're Doing It Wrong

- "Is that not happening?" — You assumed without verifying
- "Will it show us...?" — You should have added evidence gathering
- "Stop guessing" — You're proposing fixes without understanding
- "Ultrathink this" — Question fundamentals, not just symptoms

**When you see these:** STOP. Return to Phase 1.

## Quick Reference

| Phase | Key Activities | Success Criteria |
|-------|---------------|------------------|
| **1. Root Cause** | Read errors, reproduce, check changes, gather evidence | Understand WHAT and WHY |
| **2. Pattern** | Find working examples, compare | Identify differences |
| **3. Hypothesis** | Form theory, test minimally | Confirmed or new hypothesis |
| **4. Implementation** | Create test, fix, verify | Bug resolved, tests pass |

## When Process Reveals "No Root Cause"

If investigation reveals issue is environmental, timing-dependent, or external:
1. Document what you investigated
2. Implement appropriate handling (retry, timeout, error message)
3. Add monitoring/logging for future investigation

95% of "no root cause" cases are incomplete investigation.
