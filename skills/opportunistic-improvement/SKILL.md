---
name: opportunistic-improvement
description: While working on any task, notice code smells, inefficiencies, and obvious improvements in files you're already touching or reading. Fix no-brainers silently, flag bigger opportunities, and report all improvements at the end of the response. Always-on mini-audit with zero overhead when code is clean.
---

# Opportunistic Improvement — Every Touch Makes It Better

Every file Claude reads is a chance to make the project better. Not a full audit — just sharp eyes while you work. If you stumble across something that's clearly subpar, fix it or flag it. The project should get better with every interaction, not just when explicitly asked.

## Always Active — But Lightweight

This skill runs passively while you work on other tasks. It does NOT:
- Add a separate scanning step
- Read files beyond what the current task requires
- Slow down the primary objective
- Burn tokens on comprehensive audits

It DOES:
- Notice problems in files you're already reading
- Fix obvious issues while you're already editing a file
- Flag bigger opportunities for the end of the response
- Stack improvements over time — every session leaves the project cleaner

## The Opportunistic Window

While reading/editing files for your current task, notice issues and fix no-brainers in-place (marginal cost is near zero since you're already there). Report all improvements at the end.

## What Counts as a No-Brainer

Fix these without asking — they're universally good and risk-free:

| Category | Examples |
|----------|---------|
| **Dead code** | Unused imports, commented-out blocks, unreachable code, unused variables |
| **Obvious bugs** | Unclosed resources, missing awaits, wrong comparison operators |
| **Performance freebies** | Unnecessary re-renders, missing keys in React lists, N+1 patterns in plain sight |
| **Naming clarity** | `data` → `strainResults`, `temp` → `pendingScore`, `x` → `terpeneWeight` |
| **Consistency** | Mixing `const`/`let` for same pattern, inconsistent quote styles, mixed naming conventions |
| **Security basics** | Console.log with sensitive data, hardcoded secrets, missing input sanitization |
| **DX improvements** | Missing helpful comments on non-obvious logic, outdated TODO comments |

### The No-Brainer Test

```
1. Is the fix obviously correct? (No judgment calls)
2. Can it break anything? (No side effects)
3. Is it in a file I'm already touching? (No extra file reads)
4. Would ANY developer agree this is better? (Universal improvement)

All 4 = YES → Fix it silently
Any = NO → Flag it, don't fix
```

## What Requires Permission

Flag these at the end — don't fix without asking:

| Category | Why Ask |
|----------|---------|
| **Refactoring patterns** | Changing how something works, even if cleaner |
| **API changes** | Renaming exports, changing function signatures |
| **Architecture shifts** | Moving files, restructuring modules |
| **Dependency changes** | Adding/removing/updating packages |
| **Logic changes** | Altering behavior, even if current behavior seems wrong |
| **Large-scale consistency** | Renaming used across many files |

### The Flag Format

At the end of your response, after completing the primary task:

```
---
Improvements made while working:
- Removed 3 unused imports in QuizResults.jsx
- Fixed missing await on fetchStrainData() in useStrains.js
- Renamed `data` → `matchResults` for clarity in recommend.js

Also noticed (needs your call):
- dispensaryService.js has duplicated geocoding logic (lines 45-67 and 112-134) — want me to extract a shared helper?
```

## Token Economics

```
Code is clean:     ~0 tokens (nothing to notice)
Minor fixes:       ~10-20 tokens (fix + one-line report)
Flagged issues:    ~30-50 tokens (description + recommendation)
Average per task:  ~5-15 tokens (most code is fine)
```

**Net impact:** Strongly negative token cost over time. Clean code = fewer bugs = fewer debugging sessions = massive token savings.

## What This Does NOT Do

- **Not a linter** — Doesn't enforce style rules or formatting
- **Not a full audit** — Doesn't scan files beyond the current task
- **Not a refactoring engine** — Doesn't propose architectural changes
- **Not opinionated** — Only fixes things that are objectively wrong or clearly better
- **Never derails the task** — Primary objective always comes first. Improvements are marginal additions, never distractions.

## Rules

1. **Primary task first** — Never let improvements delay or distract from the actual request
2. **No-brainer test** — All 4 criteria must pass before silently fixing
3. **Already there** — Only notice things in files you're already reading/editing for the task
4. **Report at the end** — Always tell the user what you improved, even if it was trivial
5. **Flag, don't force** — Anything beyond a no-brainer gets flagged, not fixed
6. **Compound over time** — Small consistent improvements beat occasional big cleanups
7. **Zero overhead when clean** — If the code is good, this skill is invisible
