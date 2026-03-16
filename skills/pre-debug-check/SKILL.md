---
name: pre-debug-check
description: Checks known anti-patterns and past error solutions BEFORE attempting any fix. Auto-triggers when Claude encounters an error, test failure, or build problem. Prevents wasting tokens on approaches that have already been tried and failed. Must fire before systematic-debugging.
context: fork
allowed-tools: Read, Glob, Grep
---

# Pre-Debug Check — Consult Past Failures First

Before attempting ANY fix for an error, check if this problem (or something similar) has been solved before.

## Step 1: Load Known Anti-Patterns

```bash
cat ~/.claude/anti-patterns.md 2>/dev/null
```

If the file doesn't exist, report "No anti-patterns file found" and exit — let the normal debugging flow proceed.

## Step 2: Search for Matches

Search the anti-patterns file for keywords from the current error:

1. Extract key terms from the error message (package names, error codes, function names)
2. Search anti-patterns for matches
3. Also search project memory for project-specific patterns:

```bash
# Search project memory
grep -ri "KEYWORD" ~/.claude/projects/*/memory/ 2>/dev/null
```

## Step 3: Report Findings

If matches found, output:

```
KNOWN PATTERN MATCH:
Title: [pattern title]
Failed approach (DO NOT TRY): [what didn't work]
Working fix: [what actually works]
Context: [when this applies]

Recommendation: Apply the known working fix directly. Do not retry the failed approach.
```

If NO matches found, output:

```
No known anti-patterns match this error. Proceeding with fresh debugging.
```

## Step 4: Confidence Assessment

Rate your match confidence:
- **HIGH** (exact error message match, same project/framework) → Apply fix directly
- **MEDIUM** (similar error, related context) → Suggest fix, note it's a similar-not-identical match
- **LOW** (vague keyword match) → Mention it but proceed with normal debugging

## Critical Rules

1. This skill should fire BEFORE any fix attempt
2. NEVER skip this check — even 5 seconds of lookup saves minutes of failed retries
3. If a HIGH confidence match is found, DO NOT try alternative approaches first
4. If the known fix doesn't work, UPDATE the anti-pattern with new context (trigger error-memory skill)
