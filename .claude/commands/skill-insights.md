# Skill Insights — Comprehensive Skill Ecosystem Analysis

Analyze the skill ecosystem. Produces a report on how skills are performing, where they're failing, and what to improve.

## Arguments
- `$ARGUMENTS` = `fast` (quick scan) or `full` (comprehensive). Default: `fast`

## Fast Mode (default)
Reads only high-signal sources, scores relevant skills. Use this for routine check-ins.

1. Read `~/.claude/anti-patterns.md` — identify which skills SHOULD have caught each entry
2. Read `~/.claude/recurring-bugs.md` — identify repeat failures
3. For each identified skill, read ONLY that skill's SKILL.md to assess if it's been fixed
4. Skip: full skill directory scan, token economics, coverage mapping
5. Output: sections 3, 5, and 8 only (Where Skills Failed, Conflicts, Top 5 Improvements)

## Full Mode (`/skill-insights full`)
Comprehensive analysis. Use for quarterly reviews or after major skill changes.

### Data Sources
Gather evidence from ALL of these:
1. **Anti-patterns file** — `~/.claude/anti-patterns.md`
2. **Recurring bugs** — `~/.claude/recurring-bugs.md`
3. **Current session** — conversation history
4. **Skill files** — `~/.claude/skills/*/SKILL.md` (read descriptions only — first 10 lines each)
5. **CLAUDE.md** — `~/.claude/CLAUDE.md`
6. **Project memory** — any `memory/` directories
7. **Skill manager** — `~/.claude/skills/skill-manager/SKILL.md`

**Token budget warning:** Do NOT read every SKILL.md in full. Read the first 10 lines (name + description) for the directory scan, then read full content ONLY for skills flagged as problematic.

### Report Structure

#### 1. At a Glance
- One paragraph: what's working, what's failing, quick wins
- Total skill count (no cap — cap was removed)

#### 2. Skill Effectiveness Scorecard
| Tier | Skills | Evidence |
|------|--------|----------|
| **High Impact** | Clear evidence of preventing bugs or saving time | Cite specific anti-pattern entries |
| **Working Quietly** | Passive skills shaping behavior without obvious moments | Would removing them cause regression? |
| **Underperforming** | Exist but haven't prevented their target failure | Cite the anti-pattern they missed |
| **Dead Weight** | Never fire or duplicate other skills | Recommend merge or removal |

#### 3. Where Skills Failed
For each entry in anti-patterns.md and recurring-bugs.md:
- Which skill was supposed to prevent this?
- Why didn't it fire?
- Has it been fixed? Is the fix sufficient?

#### 4. Skill Coverage Map
| Activity | Frequency | Skills Covering It | Gaps |
|----------|-----------|-------------------|------|
| Bug fixing | High | pre-debug-check, systematic-debugging, error-memory, fix-loop | ? |
| Data/P&L work | High | data-consistency-check, profit-driven-development | ? |
| Deployment | Medium | deploy, site-update-protocol | ? |
| Multi-file changes | High | pattern-propagation, dispatching-parallel-agents | ? |
| Coefficient sweeps | Medium | parallel-sweep, backtest | ? |

#### 5. Skill Conflicts & Overlaps
- Skills triggering on same conditions (which wins?)
- Contradictory guidance
- Merge candidates

#### 6. Token Economics
- Total lines across all SKILL.md files: `find ~/.claude/skills -name "SKILL.md" | xargs wc -l | tail -1`
- Top 10 heaviest skills by line count
- Passive (always loaded) vs triggered (on-demand) ratio

#### 7. Missing Capabilities
Based on anti-patterns, recurring bugs, and user friction:
- What failure modes have no skill coverage?
- What new skills would have highest impact?

#### 8. Top 5 Improvements
Ranked by impact with specific implementation:
1. [Change] — [file to edit] — [expected impact]
2-5. Same format.

## Rules
1. **Evidence-based** — every claim cites a specific anti-pattern, session moment, or skill file
2. **Quantify** — "X anti-pattern entries that skill Y should have caught"
3. **Actionable** — every finding has a concrete fix (edit skill X, merge A into B, add rule)
4. **Effectiveness over existence** — don't just list skills, analyze performance
5. **Ask before implementing** — present the report, then ask "Which improvements should I implement?"
