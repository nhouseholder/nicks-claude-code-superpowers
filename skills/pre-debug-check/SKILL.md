---
name: pre-debug-check
description: Checks known anti-patterns, past error solutions, and familiar barrier patterns BEFORE attempting any fix. Auto-triggers when Claude encounters an error, test failure, or build problem. Also watches for mid-execution barriers — approach repetition, escalating cascades, environment friction, and framework quirks. Prevents wasting tokens on approaches that have already been tried and failed. Must fire before systematic-debugging.
context: fork
allowed-tools: Read, Glob, Grep
---

# Pre-Debug Check — Consult Past Failures First + Barrier Recognition

Before attempting ANY fix for an error, check if this problem (or something similar) has been solved before. Also stay alert for familiar barrier patterns during execution.

## Step 1: Load Known Anti-Patterns AND Recurring Bugs

```bash
cat ~/.claude/anti-patterns.md 2>/dev/null
cat ~/.claude/recurring-bugs.md 2>/dev/null
```

If neither file exists, report "No anti-patterns or recurring bugs found" and proceed with normal debugging.

## Step 2: Search for Matches

Search BOTH files for keywords from the current error:

1. Extract key terms from the error message (package names, error codes, function names, component names)
2. Search anti-patterns for matches
3. **Search recurring bugs tracker** — this is critical for bugs that keep coming back
4. Also search project memory for project-specific patterns:

```bash
# Search anti-patterns
grep -i "KEYWORD" ~/.claude/anti-patterns.md 2>/dev/null

# Search recurring bugs — HIGH PRIORITY
grep -i "KEYWORD" ~/.claude/recurring-bugs.md 2>/dev/null

# Search project memory
grep -ri "KEYWORD" ~/.claude/projects/*/memory/ 2>/dev/null
```

## Step 3: Report Findings

### If a RECURRING BUG match is found (highest priority):

```
⚠️ RECURRING BUG DETECTED — Report #[N]
Bug: [bug title]
Previous fix attempts:
  - [DATE]: [what was done] — DIDN'T HOLD because [reason]
  - [DATE]: [what was done] — DIDN'T HOLD because [reason]

DO NOT re-apply previous fixes. They didn't hold.
ESCALATION REQUIRED: [level based on report count]
Proceeding with deeper root-cause analysis.
```

### If an anti-pattern match is found:

```
KNOWN PATTERN MATCH:
Title: [pattern title]
Failed approach (DO NOT TRY): [what didn't work]
Working fix: [what actually works]
Context: [when this applies]

Recommendation: Apply the known working fix directly. Do not retry the failed approach.
```

### If NO matches found:

```
No known anti-patterns or recurring bugs match this error. Proceeding with fresh debugging.
```

## Step 4: Confidence Assessment

Rate your match confidence:
- **HIGH** (exact error message match, same project/framework) → Apply fix directly
- **HIGH + RECURRING** (recurring bug match) → Do NOT apply previous fix. Escalate per recurrence level.
- **MEDIUM** (similar error, related context) → Suggest fix, note it's a similar-not-identical match
- **LOW** (vague keyword match) → Mention it but proceed with normal debugging

## Mid-Execution Barrier Detection

Beyond the initial check, stay alert for these patterns during any workflow:

### Barrier Signals

| Signal | What It Looks Like | Action |
|--------|-------------------|--------|
| **Error deja vu** | Same error seen before in this session or anti-patterns | Stop. Apply known fix. |
| **Approach repetition** | About to try something that already failed | Skip it. Try documented alternative. |
| **Escalating cascade** | Fix A broke B, fix B broke C | Stop after 2 cascades. Problem is architectural, not local. |
| **Environment friction** | iCloud+git, Node versions, venv, permissions | Check anti-patterns. Usually a known issue. |
| **Framework quirk** | Code looks correct but doesn't behave as expected | Check docs before guessing. |

### Common Environment Barriers

- iCloud + git → clone to /tmp
- Node version mismatch → check .nvmrc
- Python venv not activated → check `which python`
- Permission denied → check ownership, not chmod 777
- Rollup deadlock on Node 25 → set ROLLUP_PARSE_WORKERS=0

### The Redirect Protocol

When a barrier is recognized mid-execution:

1. **STOP** current approach immediately
2. **ANNOUNCE** the recognized pattern to the user: "[Barrier type] detected — [what this means in one sentence]"
3. **CITE** the anti-pattern or past solution
4. **REDIRECT** to the known working fix
5. **VERIFY** the redirect worked
6. If redirect fails → **UPDATE** anti-patterns with new context
7. If NO known fix exists → **ESCALATE**: tell the user what you tried, what pattern you see, and recommend next step (architectural review, different approach, or external help). Don't just stop — always leave the user with a clear path forward.

## Integration

- **error-memory**: Pre-debug-check reads anti-patterns AND recurring-bugs.md; error-memory writes to both. They're the read/write pair of the same knowledge base. Recurring bugs get escalated — never re-apply a fix that didn't hold.
- **systematic-debugging**: Pre-debug-check fires FIRST to catch known patterns. If no match, systematic-debugging takes over for root-cause analysis.
- **fix-loop**: When fix-loop encounters failures, pre-debug-check is consulted before each retry to avoid repeating known-bad approaches.
- **calibrated-confidence**: A HIGH confidence anti-pattern match raises confidence to act immediately. No match lowers confidence and triggers deeper investigation.

## Critical Rules

1. This skill fires BEFORE any fix attempt — and stays alert during execution
2. NEVER skip the initial check — even 5 seconds of lookup saves minutes of failed retries
3. If a HIGH confidence match is found, DO NOT try alternative approaches first
4. If the known fix doesn't work, UPDATE the anti-pattern with new context (trigger error-memory)
5. After 3+ failed fix attempts on the same problem → step back, the issue is likely architectural
6. Announce recognized barriers to the user — "I've seen this before" builds trust and saves tokens
