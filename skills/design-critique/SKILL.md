---
name: design-critique
description: "Structured UX critique using Nielsen's 10 Heuristics (/40 score), cognitive load assessment (8-item checklist), and persona-based testing (5 archetypes). Use during site-review, site-redesign Phase 7, or any design evaluation. Produces quantitative scores, not just opinions."
weight: light
---

# Design Critique — Quantitative UX Evaluation

Structured design critique framework producing a quantitative UX score (/40), cognitive load assessment, and persona-based testing. Adapted from [pbakaus/impeccable](https://github.com/pbakaus/impeccable) critique system.

## When This Fires

- During `/site-review` — as the design/UX evaluation component
- During `/site-redesign` Phase 7 (Visual QA) — to score the redesign
- When user asks to "critique", "evaluate", or "score" a design
- When `/qa-test` finds UX issues that need deeper analysis

## Step 1: Nielsen's Heuristics Score

Read `reference/heuristics-scoring.md` for the full scoring guide.

Score each of 10 heuristics 0-4. Be honest — a 4 means genuinely excellent.

| # | Heuristic | Score (0-4) |
|---|-----------|-------------|
| 1 | Visibility of System Status | |
| 2 | Match Between System and Real World | |
| 3 | User Control and Freedom | |
| 4 | Consistency and Standards | |
| 5 | Error Prevention | |
| 6 | Recognition Rather Than Recall | |
| 7 | Flexibility and Efficiency of Use | |
| 8 | Aesthetic and Minimalist Design | |
| 9 | Help Users Recover from Errors | |
| 10 | Help and Documentation | |
| | **TOTAL** | **/40** |

**Rating scale:**
| Score | Rating | Action |
|-------|--------|--------|
| 36-40 | Excellent | Minor polish only |
| 28-35 | Good | Address weak areas |
| 20-27 | Acceptable | Significant improvements needed |
| 12-19 | Poor | Major UX overhaul required |
| 0-11 | Critical | Redesign needed |

Tag each issue found with severity: **P0** (blocking), **P1** (major), **P2** (minor), **P3** (polish).

## Step 2: Cognitive Load Assessment

Read `reference/cognitive-load.md` for the full checklist.

Evaluate 8 items — each pass/fail:

- [ ] **Single focus**: Primary task completable without distraction from competing elements?
- [ ] **Chunking**: Information in digestible groups (4 items per group max)?
- [ ] **Grouping**: Related items visually grouped (proximity, borders, shared background)?
- [ ] **Visual hierarchy**: Immediately clear what's most important?
- [ ] **One thing at a time**: User can focus on a single decision before the next?
- [ ] **Minimal choices**: 4 or fewer visible options at each decision point?
- [ ] **Working memory**: User doesn't need to remember info from a previous screen?
- [ ] **Progressive disclosure**: Complexity revealed only when needed?

**Scoring**: 0-1 failures = low load (good). 2-3 = moderate (address soon). 4+ = high load (critical fix).

**Working Memory Rule** (Cowan, 2001): At any decision point, count distinct items user must simultaneously consider. 4 or fewer = manageable. 5-7 = group or disclose progressively. 8+ = overloaded.

## Step 3: Persona Testing

Read `reference/personas.md` for full persona profiles and red flag checklists.

Select 2-3 personas most relevant to the interface type:

| Interface Type | Use Personas |
|---|---|
| Landing page / marketing | Jordan (first-timer), Riley (stress tester), Casey (mobile) |
| Dashboard / admin | Alex (power user), Sam (accessibility) |
| E-commerce / checkout | Casey (mobile), Riley (stress tester), Jordan (first-timer) |
| Onboarding flow | Jordan (first-timer), Casey (mobile) |
| Data-heavy / analytics | Alex (power user), Sam (accessibility) |
| Form-heavy / wizard | Jordan (first-timer), Sam (accessibility), Casey (mobile) |

For each selected persona, walk through the primary user action and report specific red flags — not generic concerns.

**The 5 personas:**
1. **Alex** (Impatient Power User) — Skips onboarding, wants keyboard shortcuts, bulk actions
2. **Jordan** (Confused First-Timer) — Reads everything, hesitates, needs guidance at every step
3. **Sam** (Accessibility-Dependent) — Screen reader, keyboard-only, needs 4.5:1 contrast
4. **Riley** (Deliberate Stress Tester) — Tests edge cases, empty states, long strings, refresh mid-flow
5. **Casey** (Distracted Mobile User) — Thumb-only, interrupted mid-flow, slow connection

## Output Format

```
DESIGN CRITIQUE
===============
Project: [name]
URL: [if applicable]
Date: [date]

HEURISTICS SCORE: [N]/40 — [Rating]
Weakest: [heuristic name] ([score]) — [why]
Strongest: [heuristic name] ([score])

COGNITIVE LOAD: [Low/Moderate/High] ([N]/8 passed)
Key violation: [worst offender]

PERSONA TESTING: [N] personas tested
- [Persona]: [pass/fail] — [key finding]
- [Persona]: [pass/fail] — [key finding]

TOP ISSUES (by severity):
P0: [list or "None"]
P1: [list]
P2: [list]
P3: [list]

RECOMMENDATION: [Ship / Fix P0-P1 first / Major rework needed]
```
