---
name: root-cause-reflection
description: After fixing a significant bug, analyze WHERE Claude's reasoning went wrong — not just what broke, but why Claude built the bug in the first place. Identifies flawed assumptions, missing checks, and reasoning gaps. Saves metacognitive lessons so Claude becomes a better coder over time. Fires after non-trivial bug fixes, not typos. Always-on awareness skill that complements error-memory.
---

# Root Cause Reflection — Learn From Your Mistakes

After fixing a significant bug, don't just move on. Ask: **"Why did I write this bug in the first place? Where did my reasoning fail?"**

error-memory records WHAT broke and HOW to fix it. This skill records WHY Claude's thinking was wrong and HOW to think better next time.

## When This Fires

**After fixing a bug where any of these are true:**
- The fix was non-obvious (took multiple attempts or was surprising)
- The bug affected users or produced wrong output (not just a syntax error)
- The bug revealed a misunderstanding of how the system works
- The same category of mistake has happened before
- The user had to point out the bug (Claude didn't catch it proactively)

**Does NOT fire for:**
- Typos, missing imports, syntax errors (mechanical mistakes)
- Bugs caught and fixed before the user saw them
- Third-party bugs or environment issues (not Claude's reasoning)

## The Reflection Protocol

After the fix is confirmed working, run this analysis:

### Step 1: Identify the Flawed Assumption

Ask: **"What did I believe was true that turned out to be false?"**

| Category | Example |
|----------|---------|
| **Data assumption** | "I assumed the event list was in chronological order" |
| **API/behavior assumption** | "I assumed the function returned sorted results" |
| **Scope assumption** | "I assumed this change only affected one file" |
| **User intent assumption** | "I assumed they wanted X when they meant Y" |
| **Temporal assumption** | "I assumed the cached data was current" |
| **Null/edge assumption** | "I assumed this field would always exist" |

### Step 2: Trace the Reasoning Chain

Walk backwards from the bug to the decision point:

```
Bug: [what went wrong]
  ← Immediate cause: [the code that was wrong]
    ← Decision: [why I wrote it that way]
      ← Assumption: [what I believed that was false]
        ← Root cause: [why I believed something false]
```

The root cause is usually one of:
- **Didn't read the code** — assumed behavior without verifying
- **Didn't check the data** — assumed structure/freshness without looking
- **Didn't think about edge cases** — happy path only
- **Didn't verify the output** — claimed success without checking
- **Carried over wrong context** — applied patterns from a different project/system
- **Trusted without verifying** — assumed algorithm/API/data source was correct

### Step 3: Extract the Lesson

Convert the root cause into an actionable rule:

**Format:**
```
LESSON: [One-line rule in imperative form]
BECAUSE: [What went wrong when I didn't follow this rule]
APPLIES WHEN: [Specific situations where this rule should fire]
```

**Good lessons** are specific and actionable:
- "Always verify event dates against current date before processing pipeline results"
- "When a function returns a list, check the sort order before assuming chronological"
- "After modifying state management, verify all consuming components still render correctly"

**Bad lessons** are vague and obvious:
- "Be more careful" (useless)
- "Test more" (not specific enough)
- "Check everything" (not actionable)

### Step 4: Persist and Improve

Based on the severity and category:

**Always do:**
- Add the lesson to `~/.claude/anti-patterns.md` under a new `## Reasoning Failures` section
- Include the full reasoning chain, not just the fix

**If the root cause points to a skill gap:**
- Identify which skill SHOULD have caught this
- Strengthen that skill with the specific check that was missing
- Note in anti-patterns which skill was updated

**If it's a recurring category:**
- Check anti-patterns for similar reasoning failures
- If 2+ failures share the same root cause category, escalate:
  - Consider a new rule in CLAUDE.md
  - Consider a new check in the relevant skill
  - Flag to the user: "This is the Nth time I've made a [category] error. I've added [specific safeguard]."

## Severity Calibration

Not every bug deserves a deep dive. Match depth to impact:

| Severity | Reflection Depth | Example |
|----------|-----------------|---------|
| **Critical** — wrong data shown to users, money affected | Full 4-step protocol + skill update + CLAUDE.md rule | Wrong event processed, wrong picks published |
| **High** — feature broken, user had to report it | Full 4-step protocol | UI showing stale data, broken form submission |
| **Medium** — bug caught during development, delayed progress | Steps 1-3, save lesson only | Off-by-one error, wrong variable referenced |
| **Low** — quick fix, minimal impact | Mental note only, no formal save | CSS alignment, log message typo |

## Rules

1. **Reflection happens AFTER the fix** — don't slow down the fix with analysis; reflect once it's working
2. **Be honest, not defensive** — the goal is to improve, not to justify. "I didn't check" is more useful than "the API was ambiguous"
3. **Specific over general** — "verify event dates" beats "be more careful"
4. **Don't over-reflect** — low-severity mechanical bugs don't need root cause analysis
5. **Update the system** — a lesson that doesn't change a skill, rule, or anti-pattern is a lesson wasted
6. **Track patterns** — if the same reasoning failure keeps happening, escalate the response
