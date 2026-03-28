---
name: spec-interview
description: Interview the user about a feature before writing any code. Produces a reusable SPEC.md artifact. Use when starting any non-trivial feature.
weight: light
triggers:
  - "spec"
  - "plan this"
  - "interview me"
  - "before we code"
  - "help me think through"
---

# Spec Interview

Before writing code, interview the user to surface all requirements, constraints, and edge cases. Then write a SPEC.md they can hand to a new session.

## When to Trigger

- User says "spec this", "plan this out", "help me think through X before coding"
- Feature touches 3+ files or has unclear requirements
- User explicitly asks for an interview before implementation

## Protocol

**Step 1 — Context Load**
Read any existing SPEC.md, README, or plan files in the current directory. Don't re-ask what's already documented.

**Step 2 — Structured Interview**
Ask targeted questions using AskUserQuestion. Cover:

1. **Core behavior** — What does it do? What does success look like?
2. **Inputs & outputs** — What data comes in? What gets returned/displayed?
3. **Edge cases** — What should happen on empty input, errors, timeouts, invalid state?
4. **Constraints** — Performance requirements? Auth/permissions? Backwards compatibility?
5. **Integration points** — What systems does this touch? APIs, databases, other services?
6. **UI/UX** (if applicable) — What does the user see? Any existing patterns to follow?
7. **Out of scope** — What explicitly should NOT be in this version?

Ask in batches (2-3 questions at a time), not one at a time. Stop when you have full clarity.

**Step 3 — Write SPEC.md**

```markdown
# Spec: [Feature Name]
Date: [today]

## Summary
[1-2 sentence description]

## Requirements
- [Bullet list of concrete requirements]

## Out of Scope
- [What this version explicitly doesn't do]

## Edge Cases
- [List of edge cases and expected behavior]

## Technical Constraints
- [Performance, auth, compatibility requirements]

## Integration Points
- [Systems, APIs, databases this touches]

## Acceptance Criteria (BDD)
For each requirement, write at least one acceptance criterion:
```
Given [precondition]
When [action]
Then [expected outcome]
```
Example:
```
Given a user with no saved addresses
When they reach the checkout page
Then they see an "Add Address" form instead of an address selector
```

## Open Questions
- [Any unresolved decisions]

## Implementation Notes
- [Anything Claude should know before starting]
```

**Step 4 — Recommend fresh session**
Tell the user: "SPEC.md is ready. Start a new session and paste: `Implement per SPEC.md`" — this gives the implementer full context window.

## Rules

- Never start coding during the interview. The spec is the deliverable.
- If the user has already partially specced something, fill the gaps — don't re-ask covered ground.
- Keep questions concrete and answerable, not philosophical.
