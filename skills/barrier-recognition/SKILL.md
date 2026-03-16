---
name: barrier-recognition
description: Automatically detects when Claude is hitting a familiar barrier or repeating a known failure pattern mid-execution. Intercepts the loop before tokens are wasted and redirects to the known solution. Fires continuously during all tool use — not just at debug time. Complements pre-debug-check (which fires before debugging) by catching patterns during ANY workflow.
---

# Barrier Recognition — Intelligent Mid-Execution Redirect

Detect familiar barriers in real-time and redirect before wasting tokens on approaches that won't work.

## When This Fires

This is an **always-on awareness** skill. It activates whenever Claude:

1. **Sees an error it has seen before** — even if not explicitly debugging
2. **Is about to try an approach that previously failed** — catches it BEFORE execution
3. **Notices a familiar pattern of escalating failures** — e.g., fix A breaks B breaks C
4. **Is looping** — same fix attempted twice, or oscillating between two approaches
5. **Encounters environmental friction** — iCloud git issues, Node version problems, package conflicts

## Recognition Signals

Watch for these patterns that indicate a known barrier:

### Signal 1: Error Message Déjà Vu
The current error message contains keywords matching an entry in `~/.claude/anti-patterns.md`.
→ **Action:** Stop immediately. Read anti-patterns. Apply known fix.

### Signal 2: Approach Repetition
You're about to try something you (or a previous session) already tried.
→ **Action:** Check anti-patterns AND project memory. If the approach is listed as failed, skip it entirely and try the documented working fix.

### Signal 3: Escalating Failure Cascade
Each fix introduces a new error. The error count is growing, not shrinking.
→ **Action:** Stop after 2 cascading failures. Step back. Read the broader context. The problem is likely architectural, not local.

### Signal 4: Environment/Tooling Friction
Issues with git, npm, Python venv, iCloud sync, file permissions, etc.
→ **Action:** These are almost always known problems. Check anti-patterns first. Common ones:
  - iCloud + git → clone to /tmp
  - Node version mismatch → check .nvmrc
  - Python venv not activated → check which python
  - Permission denied → check file ownership, not chmod 777

### Signal 5: Framework/API Behavior Mismatch
The code looks correct but doesn't behave as expected — often a framework quirk or API change.
→ **Action:** Check if this framework/API has a known quirk in anti-patterns. If not, search docs before guessing.

## The Redirect Protocol

When a barrier is recognized:

```
1. STOP current approach immediately
2. ANNOUNCE: "I recognize this pattern — [description of the barrier]"
3. CITE: Reference the specific anti-pattern or past solution
4. REDIRECT: Apply the known working solution
5. VERIFY: Confirm the redirect worked
6. If redirect fails → UPDATE anti-patterns with new context
```

## Self-Monitoring Checklist

Before executing ANY fix or workaround, ask yourself:

- [ ] Have I seen this exact error before? → Check anti-patterns
- [ ] Have I tried this approach before in this session? → Don't repeat it
- [ ] Is this the 3rd+ attempt at the same problem? → Step back, rethink
- [ ] Am I fighting the environment instead of solving the problem? → Known friction pattern?
- [ ] Would a senior dev recognize this instantly? → It's probably documented

## Integration with Other Skills

```
barrier-recognition (always-on, catches patterns mid-execution)
    │
    ├─ Feeds into → pre-debug-check (consults anti-patterns at debug start)
    ├─ Feeds into → error-memory (saves new barriers after resolution)
    ├─ Triggers → systematic-debugging (only if barrier is NOT recognized)
    └─ Overrides → any approach that matches a known-failed pattern
```

## Key Difference from pre-debug-check

| | pre-debug-check | barrier-recognition |
|---|---|---|
| **When** | Before debugging starts | During ANY workflow, continuously |
| **What** | Checks anti-patterns file | Checks anti-patterns + session history + behavioral patterns |
| **Scope** | Explicit errors | Errors + friction + loops + cascades + déjà vu |
| **Action** | Suggests known fix | Actively STOPS and REDIRECTS mid-execution |

## Rules

1. **Never fight a recognized barrier** — redirect immediately
2. **Announce the recognition** — tell the user "I've seen this before" so they know tokens aren't being wasted
3. **Update anti-patterns** if the barrier is new — every barrier recognized once should never surprise again
4. **Don't over-trigger** — only activate on genuine pattern matches, not superficial keyword overlap
5. **Trust the documented fix** — if anti-patterns says "do X", do X. Don't second-guess past evidence.
