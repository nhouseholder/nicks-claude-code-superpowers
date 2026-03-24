---
name: fix-loop
description: Self-healing CI loop — run test suite, diagnose failures, fix source code, re-run until all tests pass, then commit. Operates autonomously in a test-driven fix cycle. Use when asked to fix all tests, make tests pass, run a fix loop, or do self-healing CI.
weight: light
---

# Fix Loop — Self-Healing CI

## Workflow

### 1. Run Full Test Suite
```bash
# Python
pytest --tb=short 2>&1 | tee test_results.log

# JavaScript
npm test 2>&1 | tee test_results.log
```

Parse output for:
- Total tests, passing, failing, skipped
- Names of failing tests
- Error messages and stack traces

### 2. For Each Failing Test

For each failure, in order:

1. **Read the test** — Understand what behavior it expects
2. **Read the source** — Find the code being tested
3. **Diagnose** — Identify the root cause (not just symptoms)
4. **Fix the source code** — Prefer not to modify test files (see Safety Rules)
5. **Re-run ONLY the fixed test** to confirm:
   ```bash
   pytest <test_file>::<test_name> -v
   # or
   npm test -- --testNamePattern="<test_name>"
   ```
6. **Move to next failure**

### 3. Handling Special Cases

**Tests requiring external APIs or network access:**
- Skip and note them separately
- Do NOT mock external calls to make tests pass

**Tests that are genuinely wrong:**
- Only modify if the test is verifiably incorrect (testing wrong behavior, outdated assertions, or broken test setup)
- Explain WHY the test was wrong, not just that it failed
- If unsure whether the test or the source is wrong, report to user and ask

**Circular failures** (fixing A breaks B):
- Stop the loop
- Report the conflict to the user
- Suggest a resolution approach

### 4. Final Regression Check
After all individual fixes:
```bash
# Run full suite one final time
pytest --tb=short 2>&1 | tee final_test_results.log
# or
npm test 2>&1 | tee final_test_results.log
```

If new failures appear → go back to step 2 for the new failures (max 3 iterations).

### 5. Commit
Only commit when ALL tests pass:
```bash
git add <all_fixed_files>
git commit -m "fix: resolve N test failures

Fixed:
- <test_1>: <one-line description of fix>
- <test_2>: <one-line description of fix>
...

Skipped (external/network):
- <test_name>: requires external API"
```

## Safety Rules

1. **PREFER not to modify test files** — Only modify tests when the test itself is verifiably incorrect (testing wrong behavior, outdated assertions, or broken test setup). If you must modify a test, explain WHY the test was wrong, not just that it failed.
2. **NEVER suppress test output** — always use `| tee`
3. **NEVER commit with failing tests** — the loop continues until green
4. **Max 3 full-suite iterations** — if tests still fail after 3 rounds, stop and report
5. **Skip flaky/network tests** — note them but don't try to fix external dependencies
6. **Track every fix** — the commit message must list all changes

## Headless Mode
Run as a batch job:
```bash
claude -p "Run the fix-loop: execute all tests, fix failing source code (not tests), re-run until green, then commit. Skip network-dependent tests." \
  --allowedTools "Read,Edit,Bash,Grep" > fix_loop.log 2>&1
```
