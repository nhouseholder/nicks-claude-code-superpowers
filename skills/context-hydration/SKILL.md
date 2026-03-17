---
name: context-hydration
description: Ensures all relevant files and context are loaded before making any edits — read before write enforcement
---

# Context Hydration

**Purpose**: Ensure all relevant files and context are loaded before making changes.

**Trigger**: Active at all times (automatic, before any Edit/Write operation).

---

## Core Rule

**Never edit or write code without first reading the relevant files.**

---

## Hydration Checklist

Before ANY Edit or Write, verify:

1. **I have read the file I'm editing**
   - If editing `app.tsx`, I must first `Read app.tsx`
   - No exceptions — no "I remember from earlier"

2. **I have read related files**
   - Parent components that render this component
   - Child components that depend on this component
   - Shared types/utilities this file imports
   - Test files if modifying behavior

3. **I understand the current state**
   - What's the current implementation?
   - What are the existing patterns?
   - Are there dependencies I need to preserve?

4. **I have the full context**
   - CLAUDE.md for project-specific rules
   - package.json/requirements.txt for dependencies
   - Any config files if relevant

---

## File Dependency Heuristics

| When editing... | Also read... |
|-----------------|---------------|
| `Component.tsx` | `Component.test.tsx`, `index.ts` |
| `util.js` | Files that import this utility |
| `types.ts` | Files that use these types |
| `api.js` | Routes that call this API |
| config file | Files that depend on config |

---

## Anti-Patterns

❌ "I'll add a function to utils.ts" — **without reading utils.ts first**

❌ "I'll fix the render logic" — **without reading the component**

❌ "I'll update the API call" — **without reading the API file**

---

## Pro-Patterns

✅ "Let me read `utils.ts` first, then add the function."

✅ "I see `Button.tsx` imports from `Button.test.tsx` — let me read both."

✅ "I'll read `api.js` and `routes.js` to understand the flow."

---

## Parallel Reading is OK

You can read multiple files in one response:

```
Read frontend/src/components/Button.tsx
Read frontend/src/components/Button.test.tsx
Read frontend/src/types/button.ts
```

---

## Summary

**Read → Understand → Edit** — always in that order.
