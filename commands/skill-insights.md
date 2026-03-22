# Skill Insights — Which Skills Help, Which Hurt

Analyze skill effectiveness from THIS session's actual behavior. Don't rely on the tracker file — observe directly from the conversation history, anti-patterns, and outcomes.

## When Called

User runs `/skill-insights` to get a skill performance report.

## Step 1: Analyze This Session

Review the current conversation and answer these questions:

**Which skills FIRED and helped?**
- Look for moments where a skill's guidance was followed and produced good results
- Example: "zero-iteration caught an off-by-one before writing" = zero-iteration helped

**Which skills SHOULD HAVE fired but didn't?**
- Look for bugs, mistakes, or wasted effort that an existing skill was supposed to prevent
- Example: "processed wrong event without checking date" = sanity-check + proactive-qa failed to fire

**Which skills fired but HURT?**
- Look for moments where following a skill's guidance caused overthinking, token waste, or wrong actions
- Example: "deep-research triggered on a simple task and wasted 5 minutes reading docs" = deep-research over-triggered

**Which skills are dead weight?**
- Skills that exist but never fire in practice across multiple sessions

## Step 2: Check Anti-Patterns for Skill Gaps

```bash
cat ~/.claude/anti-patterns.md 2>/dev/null
```

For each anti-pattern entry, check: was a skill supposed to prevent this? Did it fail? Why?

## Step 3: Generate Report

```
## Skill Insights Report — [DATE]

### Helped This Session
| Skill | What It Did | Impact |
|-------|------------|--------|
| [name] | [specific moment it helped] | [time/tokens saved] |

### Failed to Fire (should have caught something)
| Skill | What It Missed | Root Cause | Fix |
|-------|---------------|------------|-----|
| [name] | [the mistake it should have prevented] | [why it didn't fire] | [specific change to make] |

### Over-Triggered or Hurt
| Skill | Problem | Fix |
|-------|---------|-----|
| [name] | [what went wrong] | [adjust trigger conditions] |

### Underused / Possibly Dead
| Skill | Last Known Firing | Recommendation |
|-------|------------------|----------------|
| [name] | [estimate] | [keep / merge / remove] |

### Session Efficiency
- User corrections needed: [count — lower is better]
- Bugs caught proactively vs reported by user: [ratio]
- Token waste incidents: [count of spiraling, polling, redundant actions]

### Top 3 Skill Improvements
1. [Most impactful skill change to make]
2. [Second]
3. [Third]
```

## Step 4: Implement Fixes

For any skill in "Failed to Fire":
- Read the skill file
- Identify why the trigger condition didn't match
- Propose a specific edit (stronger trigger, additional check, etc.)
- Ask user: "Should I apply these improvements now?"

## Rules

1. **Evidence-based only** — every claim must point to a specific moment in the session
2. **Don't guess** — if you can't identify a specific firing/failure, don't list it
3. **Actionable fixes** — every "failed to fire" entry must have a concrete fix proposal
4. **Compare against anti-patterns** — the anti-patterns file IS the ground truth of what went wrong
