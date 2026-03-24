---
name: test-driven-development
description: Use when implementing any feature or bugfix, before writing implementation code
weight: light
---

# Test-Driven Development (TDD)

## Overview

Write the test first. Watch it fail. Write minimal code to pass.

**Core principle:** If you didn't watch the test fail, you don't know if it tests the right thing.

**Violating the letter of the rules is violating the spirit of the rules.**

## When to Use

**Use TDD for:**
- Business logic and domain code
- Bug fixes (write a test that reproduces the bug first)
- Complex algorithms or data transformations
- API endpoints with validation logic

**Skip TDD for:**
- Configuration files, env changes, static data
- UI/styling changes (visual verification is more appropriate)
- One-line fixes with obvious correctness
- Prototypes and throwaway exploration
- Wiring/glue code (imports, route registration, provider setup)
- Generated code or scaffolding

**Use judgment:** TDD is a tool, not a religion. Apply it where it adds value — primarily where logic can be wrong in non-obvious ways.

## The Core Principle

```
FOR BUSINESS LOGIC: Write the test first, watch it fail, then implement.
```

If you wrote implementation code before the test and it's complex logic: consider rewriting test-first. For simple, obviously-correct code: just add the test after and move on. The goal is catching bugs, not ceremony.

## Red-Green-Refactor

### RED - Write Failing Test

Write one minimal test showing what should happen. Use a clear name describing the behavior, test real code (not mocks), and test one thing.

**Requirements:**
- One behavior
- Clear name
- Real code (no mocks unless unavoidable)

### Verify RED - Watch It Fail

**MANDATORY. Never skip.**

```bash
npm test path/to/test.test.ts
```

Confirm:
- Test fails (not errors)
- Failure message is expected
- Fails because feature missing (not typos)

**Test passes?** You're testing existing behavior. Fix test.

**Test errors?** Fix error, re-run until it fails correctly.

### GREEN - Minimal Code

Write the simplest code to pass the test. Don't add features, refactor other code, or over-engineer beyond what the test requires (YAGNI).

### Verify GREEN - Watch It Pass

**MANDATORY.**

```bash
npm test path/to/test.test.ts
```

Confirm:
- Test passes
- Other tests still pass
- Output pristine (no errors, warnings)

**Test fails?** Fix code, not test.

**Other tests fail?** Fix now.

### REFACTOR - Clean Up

After green only:
- Remove duplication
- Improve names
- Extract helpers

Keep tests green. Don't add behavior.

### Repeat

Next failing test for next feature.

## Good Tests

| Quality | Good | Bad |
|---------|------|-----|
| **Minimal** | One thing. "and" in name? Split it. | `test('validates email and domain and whitespace')` |
| **Clear** | Name describes behavior | `test('test1')` |
| **Shows intent** | Demonstrates desired API | Obscures what code should do |

## Why Test-First Matters

Tests-after answer "what does this code do?" Tests-first answer "what should this code do?" Tests-after are biased by your implementation — you test what you built, not what's required. Test-first forces edge case discovery before implementing.

## Common Rationalizations (All Wrong)

Common excuses ("test after", "too simple", "manual tested") are all wrong. Default to TDD.

## Example: Bug Fix

Write a failing test that reproduces the bug. Watch it fail. Fix the code. Watch it pass. The test proves the fix and prevents regression. Never fix bugs without a test.

## Verification Checklist

Before marking work complete:

- [ ] Every new function/method has a test
- [ ] Watched each test fail before implementing
- [ ] Each test failed for expected reason (feature missing, not typo)
- [ ] Wrote minimal code to pass each test
- [ ] All tests pass
- [ ] Output pristine (no errors, warnings)
- [ ] Tests use real code (mocks only if unavoidable)
- [ ] Edge cases and errors covered

Can't check all boxes? You skipped TDD. Start over.

## When Stuck

If you can't write a test: write the wished-for API first. If the test is complicated: the design is complicated — simplify it. If you must mock everything: the code is too coupled, use dependency injection.

## Testing Anti-Patterns

When adding mocks or test utilities, read @testing-anti-patterns.md to avoid common pitfalls:
- Testing mock behavior instead of real behavior
- Adding test-only methods to production classes
- Mocking without understanding dependencies

## Final Rule

```
Default to TDD for all business logic. For trivial changes (config tweaks, copy changes, style fixes),
use judgment — TDD adds overhead without value. When skipping TDD, ensure the change is verified
by other means (manual check, existing tests, type system).
```
