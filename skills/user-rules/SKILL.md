---
name: user-rules
description: Captures, persists, and enforces user-defined rules across sessions. When the user sets a hard constraint ("max 70 events", "always use approach X", "never do Y"), it's saved to a rules file and checked before every relevant action. Rules survive compaction, crashes, and session boundaries. Always-on enforcement skill.
---

# User Rules — Hard Constraints That Never Get Forgotten

## The Problem This Solves

The user says "max backtest events is 70" in Tuesday's session. On Thursday, Claude backtests with 200+ events. The rule was lost because it only lived in conversation context, which doesn't survive across sessions.

User rules are NOT preferences (nice-to-have). They are **hard constraints** — things Claude must NEVER violate. They need their own persistent storage AND active enforcement.

## When This Fires

### Detection — Always On

Watch for these signals that the user is setting a rule:

| Signal | Example | Rule Extracted |
|--------|---------|---------------|
| "always [do X]" | "always run tests before committing" | Pre-commit: run tests |
| "never [do Y]" | "never push directly to main" | Git: no direct push to main |
| "max/min [value]" | "max backtest events is 70" | Backtest: NUM_EVENTS ≤ 70 |
| "don't [do X]" | "don't use mocks in integration tests" | Testing: no mocks in integration |
| "use [X] not [Y]" | "use Weedmaps API, not Leafly for pricing" | Data: Weedmaps for pricing |
| "from now on" | "from now on, deploy to staging first" | Deploy: staging before production |
| "remember that" | "remember that the DB is on port 5433 not 5432" | Env: DB port = 5433 |
| "I told you" / "I already said" | "I already said max 70 events" | CRITICAL — rule was set before and violated. Find and re-enforce it. |
| **User correction** (any) | "No, losses should be -1 unit" / "That's wrong, combo needs a column too" | **IMMEDIATE SESSION RULE** — every correction from the user becomes a hard constraint for the rest of the session. Don't just fix this instance — apply it to ALL related work. |
| **Frustrated multi-correction** | User lists 4+ things wrong | Every item in their correction list = a separate rule. Check ALL of them before responding. |

### Enforcement — Before Every Relevant Action

Before executing any action, mentally check: **"Does a user rule apply to what I'm about to do?"**

This is a zero-cost mental check — like a pilot checking instruments. It only fires actively when a rule IS relevant.

## The Rules File

### Location

```
~/.claude/projects/<project>/memory/user_rules.md
```

This file is **project-scoped** — rules for the UFC project don't affect the MyStrainAI project.

For rules that span ALL projects, also write to:
```
~/.claude/user-rules.md
```

### Format

```markdown
# User Rules — [Project Name]
> HARD CONSTRAINTS. Violating a rule is a bug. Last updated: [DATE]
## Data & Backtesting
- **Max backtest events**: 70 UFC events (set 2026-03-17)
## Git & Deploy
- **Never push from iCloud**: Clone to /tmp first (set 2026-03-01)
## Code & Architecture
- **[Rule]**: [Details] (set [DATE])
```

Each rule: clear actionable constraint + date set + category.

## When a Rule Is Detected

- **Confirm if ambiguous** — if clear ("max 70 events"), just save. If vague, ask for the specific limit.
- **Save immediately** — write to `user_rules.md` NOW. Don't wait for session end. Update MEMORY.md index if needed.
- **Acknowledge in one line** — "Saved rule: Max backtest events = 70. I'll enforce this in all future sessions."

## Enforcement Protocol

### At Session Start

When total-recall loads project memory, `user_rules.md` is loaded as part of the standard memory hydration. Rules are available from the first action.

### Before Actions

| Action Type | Check |
|-------------|-------|
| Running a backtest | Check: event count, output streaming rules |
| Git operations | Check: push restrictions, branch rules, commit rules |
| Deploy | Check: staging-first rules, environment rules |
| File edits | Check: architecture rules, coding rules |
| API calls | Check: which API to use, rate limit rules |
| Data operations | Check: data source rules, format rules |

### When a Rule Would Be Violated

If you're about to take an action that violates a user rule:

**STOP. Do not execute.**

Instead:
```
Heads up — you have a rule that [X]. I was about to [Y] which would violate it.
Want me to [correct action] instead, or has the rule changed?
```

This gives the user the chance to either enforce the rule or update it.

### When the User Overrides a Rule

If the user explicitly says "ignore that rule" or "actually, make it 100 events now":
1. Update `user_rules.md` with the new value
2. Note the date of the change
3. Acknowledge: "Updated rule: max events is now 100."

## The "I Already Told You" Protocol

When the user says any of these:
- "I already said..."
- "I told you..."
- "Remember when I said..."
- "You keep doing X when I said not to"
- "Why are you doing X? I said Y"

This is a **CRITICAL FAILURE**. A user rule was either:
1. Never saved (detection failure)
2. Saved but not checked (enforcement failure)
3. Lost during compaction (persistence failure)

**Response protocol:**
1. Apologize once (not profusely): "You're right — I should have remembered that."
2. Fix the immediate violation
3. Check `user_rules.md` — is the rule there?
   - If NO: save it now. The detection step failed.
   - If YES: the enforcement step failed. Note this in error-memory as an anti-pattern.
4. Re-read ALL rules to refresh enforcement

## Rules

1. **Save immediately** — Don't wait for session end. Write the rule to the file the moment the user sets it.
2. **Check before acting** — Rules are constraints on actions. Check them before the action, not after.
3. **Never silently violate** — If you're about to break a rule, stop and tell the user. Let them decide.
4. **One file per project** — All rules in one place. Easy to load, easy to check, easy to audit.
5. **Include dates** — Rules can go stale. Dates help identify which ones to re-confirm.
6. **"I already told you" = critical failure** — Treat it as seriously as a production bug.
7. **Rules survive everything** — Compaction, crashes, session boundaries. The file is the source of truth.
8. **User can always override** — Rules are set BY the user and changed BY the user. Claude never changes a rule unilaterally.
9. **Specific beats vague** — "Max 70 events" is a rule. "Keep it reasonable" is a preference. Clarify if ambiguous.
10. **Cross-project rules go global** — If a rule applies everywhere ("always use tee"), save to `~/.claude/user-rules.md` too.
