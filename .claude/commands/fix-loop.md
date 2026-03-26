Self-healing CI loop: run the test suite, diagnose failures, fix source code (never tests), re-run until all pass, then commit. Max 3 iterations.

## Arguments
- `$ARGUMENTS` = test command, file pattern, or specific test to fix (default: auto-detect)

## Phase 1: Pre-checks
```bash
# Detect test framework and command
ls jest.config* vitest.config* pytest.ini pyproject.toml .mocharc* 2>/dev/null | head -5
grep -E '"test"' package.json 2>/dev/null | head -1
[ -f pytest.ini ] && echo "pytest"
[ -f pyproject.toml ] && grep -q "pytest" pyproject.toml 2>/dev/null && echo "pytest"
```

Auto-detect:
- `npm test` / `npx jest` / `npx vitest` for JS/TS
- `pytest` / `python -m pytest` for Python
- Or use `$ARGUMENTS` if specific command given

Check `~/.claude/anti-patterns.md` for known test-related issues in this project.

## Phase 2: Fix Loop (Max 3 Iterations)
For each iteration:

1. **Run full test suite** with visible output: `[cmd] 2>&1 | tee test_output.log`
2. **All pass → done.** Go to Phase 3.
3. **Failures:**
   a. Parse errors — identify failing tests and messages
   b. Diagnose root cause in **SOURCE code** (never modify tests unless explicitly asked)
   c. Apply targeted fix (smallest change possible)
   d. Re-run failing tests first (fast feedback)
   e. If those pass, re-run full suite (regression check)
   f. Log: "Iteration N: fixed [file] — [what was wrong]"

**Hard stop at 3 iterations.** If still failing after 3:
- Report what was fixed, what still fails, and why
- The remaining failures likely need a different approach

## Phase 3: Report & Commit
```
FIX LOOP COMPLETE
=================
Iterations: [N] / 3 max
Tests: [N passed] / [N total] ([N fixed this session])

Fixes applied:
- [file:line]: [what was wrong] → [what was changed]

Still failing: [list, or "none — all passing"]
```

All pass → commit with message describing fixes.
Some fail → DO NOT commit. Report remaining failures.
