# Skill Insights — Which Skills Help, Which Hurt

Generate a skill performance report based on session observations. Read the tracker file, analyze patterns, and produce actionable insights.

## When Called

User runs `/skill-insights` to get a report on skill effectiveness.

## Step 1: Read the Tracker

```bash
cat ~/.claude/skill-tracker.md 2>/dev/null
```

If the file doesn't exist or is empty, report: "No skill tracking data yet. The tracker builds automatically during sessions. Run a few tasks and try again."

## Step 2: Analyze and Generate Report

Read the tracker entries and produce this report format:

```
## Skill Insights Report — [DATE]

### Helping (keep these)
| Skill | Evidence | Sessions Observed |
|-------|----------|-------------------|
| [name] | [what it did well] | [count] |

### Hurting (rework or remove)
| Skill | Problem | Recommendation |
|-------|---------|----------------|
| [name] | [what went wrong — overthinking, token waste, wrong action] | [fix / merge / remove] |

### Underused (potentially dead weight)
| Skill | Last Fired | Consider |
|-------|-----------|----------|
| [name] | [date or "never observed"] | [keep / merge / remove] |

### Efficiency Metrics
- **Average task completion**: [fast / moderate / slow]
- **Token waste incidents**: [count of overthinking / confusion / pointless actions caught]
- **User corrections this period**: [count of "I already told you" / "don't do that" / approach corrections]
- **Rules violated**: [count from user-rules enforcement]

### Top 3 Recommendations
1. [Most impactful change to make]
2. [Second most impactful]
3. [Third most impactful]
```

## Step 3: Suggest Actions

For any skill in the "Hurting" category, suggest one of:
- **Rework**: specific change to make
- **Merge**: which skill to merge it into
- **Remove**: if it's net-negative and no fix is obvious

For "Underused" skills older than 30 days with no observations:
- Flag as candidates for removal to free up skill slots
