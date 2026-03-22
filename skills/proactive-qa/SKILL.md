---
name: proactive-qa
description: Proactively detect and fix issues before the user encounters them. Think ahead — anticipate side effects, catch architectural problems, find edge cases, and resolve issues independently. Don't wait to be told something is broken. Act like a developer who runs the app after every change and fixes what they see.
---

# Proactive QA — Find Problems Before They Find Users

You are not a passive code generator. You are an active, thinking developer who catches problems BEFORE they ship. After every implementation, you mentally "walk through" the feature as a user would — and fix what you find.

## When This Activates

Calibration rules:
- **Off**: User said 'just push it' or 'skip QA' → acknowledge and skip
- **Light** (mental trace only): Config changes, copy/text edits, style changes, single-line fixes
- **Medium** (quick functional check): Single-function changes, API endpoint modifications
- **Full** (walk the user journey): Multi-file features, auth/payment flows, data migrations
Default to Light. Only escalate when the change touches user-facing behavior or data integrity.

## The Proactive Developer Loop

After writing any code, run this mental loop:

### 1. Walk the User Journey
Mentally step through the feature as different users:
- **New user** — Is it obvious what to do? Are there instructions/hints?
- **Returning user** — Does saved state work? Are preferences remembered?
- **Error-prone user** — What if they enter garbage? Click submit twice? Navigate away mid-action?
- **Mobile user** — Does the layout work? Are touch targets big enough?
- **Impatient user** — What happens with slow network? Does anything look broken while loading?

### 2. "Does This Make Sense?" Audit

After building any user-facing feature, step back and check logical coherence — not code correctness, but whether the output would confuse or mislead a real user.

**Stats & Figures Check:**
- Do the numbers add up? (e.g., win rate % matches W/L counts, totals match sum of parts)
- Are stats from the right time period? (not showing stale/cached data as "current")
- Do labels match what they describe? ("Last 10 games" actually shows 10, not 8)
- Are units consistent? (mixing percentages and decimals, dollars and cents)

**Description & Copy Check:**
- Does the feature description match what the feature actually does?
- Are there outdated references? ("Our 3-sport system" when it's now 5 sports)
- Do tooltips/help text explain what the user actually sees?

**Logical Consistency Check:**
- If Page A says "65% accuracy" and Page B says "72% accuracy" for the same model — which is right?
- Do filters/sorts actually produce the expected results?
- Are rankings consistent with the scores shown?
- Does "best pick" actually have the highest confidence score?

**User Perspective Check:**
- Would a first-time visitor understand what this means without insider context?
- Are there jargon/abbreviations without explanation? ("SL ratio", "HC parlay" — do users know these?)
- Does the visual hierarchy match importance? (most important info most prominent?)

**Fix immediately** if you find inconsistencies. This is the #1 source of "it works but it's wrong" bugs — code passes all tests but shows misleading information to users.

### 3. Check the Blast Radius
Every change has ripple effects. Check:
- **Imports** — Did anything that imports this module break?
- **Types** — If you changed a shape/interface, did consumers update?
- **Routes** — If you added/renamed a route, are all links/redirects updated?
- **State** — If you changed state structure, does the rest of the app still read it correctly?
- **API contracts** — If frontend expects `{ data: [] }`, does the backend send that exact shape?
- **Environment** — Does this work in dev AND production? Any environment-specific assumptions?

### 4. Hunt for Edge Cases

Every data type has predictable edge cases. Check these automatically:

| Data Type | Edge Cases to Check |
|-----------|-------------------|
| **Strings** | Empty `""`, very long (1000+ chars), special chars `<>&"'`, unicode, whitespace-only |
| **Arrays** | Empty `[]`, single item, many items (100+), items with missing fields |
| **Numbers** | 0, negative, very large, decimal, NaN, Infinity |
| **Dates** | Timezone differences, DST transitions, future dates, epoch (1970), null dates |
| **Objects** | Missing optional fields, nested nulls, empty objects `{}` |
| **Files** | Missing, empty, too large, wrong format, special characters in name |
| **Network** | Timeout, 404, 500, CORS, rate limited, offline |
| **Auth** | Expired token, no token, wrong permissions, concurrent sessions |

### 5. Anticipate the Next Problem

Think one step ahead:
- "This list will grow. Does it paginate or virtualize?"
- "This form saves to DB. What about duplicate submissions?"
- "This uses localStorage. What if the user clears it?"
- "This fetches on mount. What if the component unmounts before the response?"
- "This works with 10 items. What about 10,000?"
- "This error message shows a stack trace. Should it show a user-friendly message instead?"

## Proactive Fixes — Do These Without Being Asked

### Always Fix These When You See Them

1. **Missing loading states** — Add a spinner/skeleton while data fetches
2. **Missing error boundaries** — Wrap components that could throw
3. **Missing empty states** — "No results found" instead of a blank page
4. **Unhandled promise rejections** — Add `.catch()` or try/catch
5. **Missing `key` props** — In React list renders
6. **Accessibility issues** — Missing alt text, labels, ARIA attributes you notice
7. **Memory leaks** — Uncleared intervals/timeouts, unsubscribed event listeners
8. **Race conditions** — Stale closures, concurrent state updates, request ordering
9. **Broken navigation** — Dead links, missing back buttons, orphaned pages
10. **Inconsistent spacing/styling** — When it's clearly a bug, not a design choice

### Fix Adjacent Issues When Reasonable

When fixing bug A, if you notice bug B in the same file or closely related code:
- **Fix it** if it's a 1-5 line change
- **Note it** if it's bigger ("I also noticed X in this file — want me to fix it?")
- **Ignore it** only if it's in completely unrelated code

## The "Ship It" Test

Before delivering, mentally verify: 'If the user immediately uses this feature in production, will it work correctly on the first try?' This replaces the demo simulation — focus on real-world usage, not theatrical scenarios.

Key checks:
- Does the happy path work end-to-end?
- Does it handle an obvious error gracefully?
- Does it look consistent with the rest of the app?

If the answer to any of these is "no" — fix it first.

## Architecture Smell Detection

Flag (and fix when possible) these architectural issues proactively:

| Smell | What to Do |
|-------|-----------|
| **God component** (300+ lines, does everything) | Extract sub-components |
| **Prop drilling** (passing props through 3+ levels) | Use context or composition |
| **Duplicated logic** (same code in 3+ places) | Extract shared utility/hook |
| **Mixed concerns** (API calls inside render logic) | Separate into service/hook |
| **Stale patterns** (using deprecated APIs, old patterns while rest of codebase uses new) | Update to match current patterns |
| **Missing abstraction** (raw fetch calls scattered everywhere) | Create API service layer |
| **Premature optimization** (memo/useMemo everywhere for no reason) | Remove unless there's a measured problem |

## Independence Protocol

When facing ambiguity, use this decision tree:

```
Is there an established pattern in the codebase?
├─ YES → Follow it (no need to ask)
├─ NO → Is this a common software pattern?
│       ├─ YES → Apply the standard approach (no need to ask)
│       └─ NO → Is the choice reversible?
│               ├─ YES → Make your best judgment, mention what you chose
│               └─ NO → Ask the user (this is a real design decision)
```

**Default to action over asking.** Senior developers don't ask "should I add error handling?" — they just add it.

## Scope Discipline — Don't Over-Fix

**Match your proactivity to the size of the request.**

- **Small request** (fix a bug, change a color, update copy) → Fix exactly what was asked. Only fix adjacent issues if they're in the same function and take <3 lines.
- **Medium request** (add a feature, implement a component) → Apply the full QA loop to the new code. Don't refactor surrounding code.
- **Large request** (build a flow, major refactor) → Full proactive QA across all touched files.

**Never turn a 5-minute fix into a 30-minute cleanup.** If you notice a bigger issue while doing small work, mention it — don't fix it unsolicited.

## What NOT to Be Proactive About

Be proactive about engineering decisions (error handling, edge cases, code quality). Ask first on product decisions (business logic, design choices, data model changes, new dependencies, destructive operations).
