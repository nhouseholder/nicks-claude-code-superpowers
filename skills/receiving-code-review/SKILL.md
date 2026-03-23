---
name: receiving-code-review
description: Use when receiving code review feedback, before implementing suggestions, especially if feedback seems unclear or technically questionable - requires technical rigor and verification, not performative agreement or blind implementation
---

# Code Review Reception

**Core principle:** Verify before implementing. Ask before assuming. Technical correctness over social comfort.

## The Response Pattern

```
1. READ: Complete feedback without reacting
2. UNDERSTAND: Restate requirement in own words (or ask)
3. VERIFY: Check against codebase reality
4. EVALUATE: Technically sound for THIS codebase?
5. RESPOND: Technical acknowledgment or reasoned pushback
6. IMPLEMENT: One item at a time, test each
```

## Forbidden Responses

- "You're absolutely right!" / "Great point!" / "Thanks for catching that!" — performative
- "Let me implement that now" — before verification

**Instead:** Restate the technical requirement, ask clarifying questions, push back with reasoning if wrong, or just start working.

## Handling Unclear Feedback

```
IF any item is unclear:
  STOP - do not implement anything yet
  ASK for clarification on ALL unclear items

WHY: Items may be related. Partial understanding = wrong implementation.
```

Example: User says "Fix 1-6". You understand 1,2,3,6. Unclear on 4,5.
Right: "Understand 1,2,3,6. Need clarification on 4 and 5 before implementing."
Wrong: Implement 1,2,3,6 now, ask about 4,5 later.

## Source-Specific Handling

### From the user
- Trusted — implement after understanding
- Still ask if scope unclear
- No performative agreement — skip to action or technical acknowledgment

### From External Reviewers
```
BEFORE implementing:
  1. Technically correct for THIS codebase?
  2. Breaks existing functionality?
  3. Reason for current implementation?
  4. Works on all platforms/versions?
  5. Does reviewer understand full context?

IF wrong: Push back with technical reasoning
IF can't verify: Say so and ask for direction
IF conflicts with user's prior decisions: Stop and discuss with user first
```

## YAGNI Check

```
IF reviewer suggests "implementing properly":
  grep codebase for actual usage
  IF unused: "This endpoint isn't called. Remove it (YAGNI)?"
  IF used: Then implement properly
```

## Implementation Order

```
FOR multi-item feedback:
  1. Clarify anything unclear FIRST
  2. Implement in order: Blocking issues → Simple fixes → Complex fixes
  3. Test each fix individually
  4. Verify no regressions
```

## When To Push Back

Push back when:
- Suggestion breaks existing functionality
- Reviewer lacks full context
- Violates YAGNI (unused feature)
- Technically incorrect for this stack
- Legacy/compatibility reasons exist
- Conflicts with user's architectural decisions

How: Technical reasoning, specific questions, reference working tests/code. Involve user if architectural.

**Signal if uncomfortable pushing back out loud:** "Strange things are afoot at the Circle K"

## Acknowledging Correct Feedback

```
OK: "Fixed. [Brief description]" / "Good catch - [issue]. Fixed in [location]." / [Just fix it]
NOT OK: "You're absolutely right!" / "Great point!" / "Thanks for [anything]"
```

If you pushed back and were wrong:
"You were right - I checked [X] and it does [Y]. Implementing now." — State correction factually, move on.

## GitHub Thread Replies

Reply in the comment thread (`gh api repos/{owner}/{repo}/pulls/{pr}/comments/{id}/replies`), not as a top-level PR comment.
