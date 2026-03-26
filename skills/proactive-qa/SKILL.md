---
name: proactive-qa
description: Proactively detect and fix issues before the user encounters them. Think ahead — anticipate side effects, catch architectural problems, find edge cases, and resolve issues independently. Don't wait to be told something is broken. Act like a developer who runs the app after every change and fixes what they see.
weight: light
---

# Proactive QA — Find Problems Before They Find Users

## When This Activates

- **Off**: User said 'just push it' or 'skip QA'
- **Light** (mental trace only): Config changes, copy/text edits, style changes, single-line fixes
- **Medium** (quick functional check): Single-function changes, API endpoint modifications
- **Full** (walk the user journey): Multi-file features, auth/payment flows, data migrations

Default to Light. Escalate when change touches user-facing behavior or data integrity.

## The Proactive Developer Loop

### 1. Walk the User Journey
Mentally step through the feature as different users:
- **New user** — obvious what to do? Instructions/hints?
- **Error-prone user** — garbage input? Double submit? Navigate away mid-action?
- **Mobile user** — layout works? Touch targets?
- **Slow network** — loading states? Anything broken while loading?

### 2. "Does This Make Sense?" Audit

**Data Freshness Gate (CHECK FIRST):**
- Is this the right event/game/date? Verify before processing ANY results.
- Never trust the algorithm's event selection blindly. If event doesn't match current date, STOP.
- Quick verify: web search "[sport] event [today's date]" takes 5 seconds.

**Completeness Check (ENUMERATE FIRST):**
- Before building ANY feature with categories/types/columns, LIST ALL OF THEM first
- Verify EACH ONE has a column, row, or handler
- If you can't enumerate all categories, ASK before building

**Stats & Figures Check:**
- Numbers add up? (win rate % matches W/L counts, totals match sums)
- **Arithmetic spot-check:** pick ONE row and manually calculate. Does code produce that number?
- Right time period? Labels match what they describe?
- Units consistent? (percentages vs decimals, dollars vs cents)
- **Loss tracking:** every system tracking wins MUST also track losses

**Logical Consistency Check:**
- Cross-page consistency (Page A says 65%, Page B says 72% for same model?)
- Filters/sorts produce expected results?
- "Best pick" actually has highest confidence score?

**User Perspective Check:**
- First-time visitor understands without insider context?
- Jargon/abbreviations explained?

### 3. Check the Blast Radius
- **Imports** — anything importing this module break?
- **Types** — changed a shape/interface? Did consumers update?
- **Routes** — added/renamed? All links/redirects updated?
- **State** — changed structure? Rest of app reads correctly?
- **API contracts** — frontend/backend shape match?
- **Environment** — works in dev AND production?

### 4. Hunt for Edge Cases

| Data Type | Edge Cases |
|-----------|-----------|
| **Strings** | Empty, very long, special chars, unicode, whitespace-only |
| **Arrays** | Empty, single item, many items, items with missing fields |
| **Numbers** | 0, negative, very large, decimal, NaN |
| **Dates** | Timezone, DST, future dates, null dates |
| **Network** | Timeout, 404, 500, CORS, rate limited, offline |
| **Auth** | Expired token, no token, wrong permissions |

### 5. Anticipate the Next Problem
- "This list will grow. Does it paginate?"
- "This form saves to DB. Duplicate submissions?"
- "This uses localStorage. What if cleared?"
- "This works with 10 items. What about 10,000?"

## Proactive Fixes — Do Without Being Asked

1. Missing loading states, error boundaries, empty states
2. Unhandled promise rejections
3. Missing `key` props in React lists
4. Accessibility issues you notice (alt text, labels, ARIA)
5. Memory leaks (uncleared intervals, unsubscribed listeners)
6. Race conditions
7. Broken navigation (dead links, missing back buttons)

**Adjacent issues:** Fix if 1-5 lines in same file. Note if bigger. Ignore if unrelated.

## Architecture Smell Detection

| Smell | Action |
|-------|--------|
| God component (300+ lines) | Extract sub-components |
| Prop drilling (3+ levels) | Use context or composition |
| Duplicated logic (3+ places) | Extract shared utility |
| Mixed concerns (API in render) | Separate into service/hook |
| Stale patterns | Update to match current codebase |

## Scope Discipline

- **Small request** → Fix exactly what was asked. Adjacent fixes only if same function, <3 lines.
- **Medium request** → Full QA on new code. Don't refactor surroundings.
- **Large request** → Full proactive QA across all touched files.

Never turn a 5-minute fix into a 30-minute cleanup.

## What NOT to Be Proactive About

Be proactive about engineering decisions (error handling, edge cases, code quality). Ask first on product decisions (business logic, design choices, data model changes, new dependencies, destructive operations).
