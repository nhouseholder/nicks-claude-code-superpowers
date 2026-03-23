# Skill Insights — Comprehensive Skill Ecosystem Analysis

Analyze the full skill ecosystem across multiple sessions. Produces a report similar to `/insights` but focused on how skills are performing, where they're failing, and what to improve.

## Data Sources

Gather evidence from ALL of these before generating the report:

1. **Anti-patterns file** — `~/.claude/anti-patterns.md` (what went wrong, which skills should have caught it)
2. **Recurring bugs** — `~/.claude/recurring-bugs.md` (patterns that skills failed to prevent)
3. **Current session** — conversation history (what fired, what didn't, what helped)
4. **Skill files** — `~/.claude/skills/*/SKILL.md` (read descriptions to assess coverage)
5. **CLAUDE.md** — `~/.claude/CLAUDE.md` (rules that exist outside skills)
6. **Project memory** — any `memory/` directories with session learnings
7. **Skill manager** — `~/.claude/skills/skill-manager/SKILL.md` (weight classifications, conflict resolution)

## Report Structure

Generate a comprehensive report with these sections:

### 1. At a Glance
- One paragraph summary: what's working, what's hindering, quick wins
- Total skill count and cap status (X/75)

### 2. Skill Effectiveness Scorecard
| Tier | Skills | Evidence |
|------|--------|----------|
| **High Impact** | Skills with clear evidence of preventing bugs or saving time | Cite specific anti-pattern entries or session moments |
| **Working Quietly** | Passive skills that shape behavior without obvious moments | Note if removing them would likely cause regression |
| **Underperforming** | Skills that exist but haven't prevented their target failure | Cite the anti-pattern entry they should have caught |
| **Dead Weight** | Skills that never fire or duplicate other skills | Recommend merge or removal |

### 3. Where Skills Failed
For each entry in anti-patterns.md and recurring-bugs.md:
- Which skill was supposed to prevent this?
- Did the skill exist at the time?
- Why didn't it fire? (too narrow trigger, wrong weight class, conflict with another skill)
- Has the skill been fixed since? Is the fix sufficient?

### 4. Skill Coverage Map
Map user's primary activities to skill coverage:

| Activity | Frequency | Skills Covering It | Gaps |
|----------|-----------|-------------------|------|
| Bug fixing | High (24 sessions) | pre-debug-check, systematic-debugging, error-memory, fix-loop | ? |
| Data/P&L work | High | data-consistency-check, self-challenge, profit-driven-development | ? |
| Deployment | Medium (5 sessions) | deploy, site-update-protocol | ? |
| Multi-file changes | High (19) | pattern-propagation, dispatching-parallel-agents | ? |
| Coefficient sweeps | Medium | parallel-sweep, backtest | ? |

### 5. Skill Conflicts & Overlaps
- Skills that trigger on the same conditions (which wins?)
- Skills that give contradictory guidance
- Skills that duplicate content unnecessarily
- Merge candidates that would reduce token load

### 6. Token Economics
- Estimate total skill token load (count lines across all SKILL.md files)
- Identify the heaviest skills by line count
- Flag skills where token cost exceeds behavioral value
- Compare passive (always loaded) vs triggered (loaded on demand)

### 7. Missing Capabilities
Based on anti-patterns, recurring bugs, and user friction:
- What failure modes have no skill coverage?
- What user workflows lack skill support?
- What new skills would have the highest impact?

### 8. Top 5 Improvements
Ranked by impact, with specific implementation:
1. [Highest impact change — skill edit, merge, or new rule]
2. [Second]
3. [Third]
4. [Fourth]
5. [Fifth]

Each with: what to change, which file to edit, expected impact, and token cost.

## Rules

1. **Evidence-based** — every claim must cite a specific anti-pattern entry, session moment, or skill file
2. **Quantify when possible** — "X anti-pattern entries that skill Y should have caught"
3. **Actionable** — every finding must have a concrete fix (edit skill X line Y, merge A into B, add rule to CLAUDE.md)
4. **Don't just list skills** — analyze their EFFECTIVENESS, not their existence
5. **Compare to user's actual pain points** — bug fixing (24 sessions), wrong approach (18 friction events), data regressions (5+ recurring), rate limits (7 events)
6. **Ask before implementing** — present the report, then ask "Which improvements should I implement?"
