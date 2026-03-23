---
name: pattern-propagation
description: When a pattern is changed in one place, automatically find and update all instances across the codebase. Covers renames, API changes, style updates, config changes, and structural refactors. Automatic skill that fires when modifying shared patterns.
---

# Pattern Propagation — Change One, Update All

When you change a pattern in one place, the change isn't done until every instance is updated. Don't leave the codebase in an inconsistent state. Find every occurrence, update them all, and verify nothing broke.

## When This Activates

Automatically when modifying anything that could have multiple instances:
- Renaming a function, variable, component, or file
- Changing an API contract (request/response shape)
- Updating a shared style, class name, or design token
- Modifying a data structure that's used in multiple places
- Changing a convention or pattern that exists across files

## The Propagation Protocol

### Step 1: Detect the Pattern Scope

Before changing anything, assess the blast radius:

```
SCOPE CHECK:
- Is this name/pattern used elsewhere? → Grep for it
- Is this exported? → Check consumers
- Is this a convention? → Check if other files follow the same pattern
- Is this a type/interface? → Check all implementations
```

### Step 2: Collect All Instances

Use targeted search to find every occurrence:

```
1. Exact matches (grep for the literal string)
2. Related matches (grep for variations — camelCase, kebab-case, SCREAMING_CASE)
3. Indirect references (imports, re-exports, dynamic references)
4. Documentation/comments that reference the old pattern
5. Test files that test the old behavior
6. Config files that reference the pattern
```

### Step 3: Update Systematically

Apply changes in dependency order:

```
1. Source of truth (the definition)
2. Direct consumers (files that import/use it)
3. Indirect consumers (files that use the consumers)
4. Tests (update expectations to match new behavior)
5. Documentation/comments (if they reference the pattern)
6. Config (if applicable)
```

### Step 4: Verify Consistency

After all updates:
```
1. Grep for the OLD pattern — should return zero results
2. Check for TypeScript/lint errors — type system catches missing updates
3. Verify imports resolve — no broken references
4. Run tests if available — catch behavioral regressions
```

## Common Propagation Patterns

| Pattern | Find | Don't Forget |
|---------|------|-------------|
| **Rename** (`getUserData` → `fetchUserProfile`) | All imports, call sites, test refs, comments | No "unused import" warnings left behind |
| **API Shape** (`{ data }` → `{ results, total }`) | Every fetch/destructure/property access | Error handling paths, TypeScript types |
| **Component Props** (`color` → `variant`) | Every component usage across files | Default props, storybook, tests |
| **Config/Env** (`DATABASE_URL` → `DB_CONNECTION_STRING`) | Every env reference, .env files, docker-compose | CI/CD pipelines, deployment configs |
| **File Move** (`src/utils/` → `src/lib/`) | Every import referencing old path | Path aliases in tsconfig/vite, test configs |

## What NOT to Propagate

- **Style preferences** — If you reformatted one file, don't reformat the whole codebase
- **Unrelated improvements** — If you found a better pattern, only apply it where asked
- **Optional migrations** — Old pattern works fine? Don't force-update everything just for consistency
- **Comments** — Don't hunt down every comment mentioning the old way unless it's misleading

## Rules

1. **Never leave partial updates** — If you change a pattern, update ALL instances or none
2. **Grep before declaring done** — The old pattern should return zero results
3. **Dependency order** — Update source first, consumers second, tests third
4. **Ask for large propagations** — 10+ files? Confirm with the user before proceeding
5. **Include tests** — Tests that reference the old pattern are broken tests
6. **Skip cosmetic propagation** — Only propagate functional/behavioral changes
