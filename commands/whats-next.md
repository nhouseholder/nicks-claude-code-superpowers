Expert strategic advisor for your projects. Reviews all context — handoffs, memory, anti-patterns, project state — and produces expert-level recommendations for what to do next across every active project.

Triggers: "what's next", "what should I work on", "out of ideas", "what to improve", "recommendations", "what needs attention"

**This command is READ-ONLY + ANALYSIS. It does not modify any files, deploy anything, or start work. It produces a prioritized recommendation report.**

---

## STEP 0: Gather All Context (Parallel)

Read ALL of the following. Do not skip any source. The quality of recommendations depends on comprehensive context.

### 0a. Global context
```bash
# Project manifest — what exists
cat ~/Projects/project-manifest.json 2>/dev/null | python3 -m json.tool 2>/dev/null

# Site-to-repo mapping — what's live
cat ~/Projects/site-to-repo-map.json 2>/dev/null | python3 -m json.tool 2>/dev/null
```

### 0b. All recent handoffs (last session state for every project)
```bash
cd /tmp && rm -rf whats-next-tmp
git clone --depth 3 https://github.com/nhouseholder/nicks-claude-code-superpowers.git whats-next-tmp 2>&1 | tail -1
ls -t /tmp/whats-next-tmp/handoffs/*.md
```

**Read EVERY handoff found.** Extract from each:
- Section 6 (In Progress) — unfinished work
- Section 7 (Blocked) — things waiting on resolution
- Section 8 (Next Steps) — queued priorities
- Section 9 (Agent Observations) — what the last agent learned

### 0c. Memory systems
Read these files:
1. `~/.claude/memory/core.md` — accumulated domain knowledge
2. `~/.claude/memory/me.md` — user profile and preferences
3. All `~/.claude/memory/topics/*.md` — domain-specific knowledge
4. `~/.claude/anti-patterns.md` — known failures and recurring bugs
5. `~/.claude/recurring-bugs.md` — repeat offenders
6. `~/.claude/CLAUDE.md` — global rules and behavioral patterns

### 0d. Project-specific memory (scan all)
```bash
for dir in ~/.claude/projects/*/memory/; do
  echo "=== $dir ==="
  cat "$dir/MEMORY.md" 2>/dev/null | head -30
  echo "---"
done
```

### 0e. Git activity across all projects
```bash
for proj in ~/Projects/*/; do
  name=$(basename "$proj")
  cd "$proj" 2>/dev/null || continue
  last=$(git log -1 --format='%ci' 2>/dev/null || echo "no-git")
  commits=$(git rev-list --count HEAD 2>/dev/null || echo "0")
  branch=$(git branch --show-current 2>/dev/null || echo "?")
  dirty=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')
  echo "$name | last: $last | commits: $commits | branch: $branch | dirty: $dirty"
done
```

---

## STEP 1: Classify Every Project

For each active project, determine its current state:

| State | Meaning |
|-------|---------|
| **ACTIVE-HOT** | Worked on in last 48 hours, has pending tasks |
| **ACTIVE-WARM** | Worked on in last 7 days, stable but has known improvements |
| **ACTIVE-COLD** | Not touched in 7+ days, may have stale state |
| **BLOCKED** | Has explicit blockers from handoff Section 7 |
| **NEEDS-RECOVERY** | Handoff mentions broken state, failed deploys, or data loss |
| **DORMANT** | No activity in 14+ days, no pending handoff tasks |

---

## STEP 2: Generate Expert Recommendations

For each recommendation, think like a **senior technical advisor** who deeply understands:
- Software architecture and best practices
- Sports betting algorithms (walk-forward backtesting, odds modeling, bankroll management)
- SaaS product development (user acquisition, retention, monetization)
- DevOps and deployment reliability
- AI/ML product strategy
- Frontend UX and performance optimization

**Each recommendation must include:**
1. **What** — the specific action (not vague "improve X")
2. **Why** — the strategic reasoning, citing industry best practices or domain expertise
3. **Impact** — expected outcome (quantified if possible)
4. **Effort** — estimated session count (1 session = ~2 hours of Claude work)
5. **Dependencies** — what must be true before starting

**Recommendation categories:**

### A. URGENT — Fix broken things
Things from handoff Section 6/7 that are broken or regressed. Recovery work.

### B. HIGH-VALUE — Biggest ROI improvements
What would produce the most impact per unit of effort? Think:
- Algorithm accuracy improvements that translate to real P/L
- User-facing features that make products more valuable
- Infrastructure that prevents future incidents
- Automation that saves repeated manual work

### C. STRATEGIC — Platform and portfolio level
Thinking beyond individual projects:
- Cross-project synergies (shared components, unified dashboards)
- Product positioning and differentiation
- Technical debt that compounds across projects
- Skills/tooling improvements that accelerate all future work

### D. LEARNING — Skill gaps and knowledge building
Based on anti-patterns and recurring bugs, what knowledge gaps should be addressed?
What domain expertise would prevent future mistakes?

### E. MAINTENANCE — Keep things healthy
Routine work that prevents decay:
- Dependency updates, security patches
- Cache refreshes, data pipeline health
- Documentation gaps
- Stale state cleanup

---

## STEP 3: Rank and Present

Present recommendations in a single prioritized list, mixing categories. The #1 recommendation should be whatever produces the most value RIGHT NOW.

### Output Format

```
WHAT'S NEXT — Strategic Recommendations
========================================
Generated: [date]
Projects scanned: [count active] active, [count dormant] dormant
Handoffs reviewed: [count]
Context sources: [list]

PROJECT STATUS OVERVIEW
-----------------------
| Project | State | Last Activity | Key Issue |
|---------|-------|---------------|-----------|
| ... | ... | ... | ... |

TOP RECOMMENDATIONS
-------------------

#1. [CATEGORY] [Title]
   Project: [project name]
   What: [specific action]
   Why: [expert reasoning — cite industry practice, domain knowledge, or data]
   Impact: [expected outcome]
   Effort: [session estimate]
   Deps: [prerequisites]

#2. [CATEGORY] ...

... (up to 10 recommendations)

CROSS-PROJECT OBSERVATIONS
--------------------------
[Patterns noticed across the portfolio — shared problems, opportunities for consolidation, systemic issues]

ANTI-PATTERN TRENDS
-------------------
[What the anti-patterns and recurring bugs reveal about systematic weaknesses. Expert advice on addressing root causes, not just symptoms.]

DORMANT PROJECT CHECK
---------------------
[Any dormant projects that should be explicitly archived, revived, or consolidated?]
```

---

## STEP 4: Clean Up

```bash
rm -rf /tmp/whats-next-tmp 2>/dev/null
```

---

## CRITICAL RULES

1. **READ-ONLY.** This command gathers information and advises. It does NOT make changes, deploy, or start work.
2. **Expert-level insights, not generic advice.** "Improve your tests" is useless. "Add walk-forward validation to the NHL model — currently using full-season averages which inflate accuracy by ~15% based on the UFC optimizer mismatch incident" is actionable.
3. **Cite your evidence.** Every recommendation should reference a specific handoff section, anti-pattern entry, memory file, or project state that motivated it.
4. **Be honest about unknowns.** If you can't assess a project's state without opening it, say so. Don't fabricate recommendations from incomplete data.
5. **Prioritize by user values.** The user cares about: (a) not breaking live sites, (b) algorithm accuracy and profitability, (c) shipping features users see, (d) reducing Claude session friction. Rank accordingly.
6. **Think like a CTO advising a solo founder.** The user runs 10+ projects. Bandwidth is the constraint. Recommendations should account for opportunity cost — doing A means NOT doing B-J.
7. **Challenge assumptions.** If a project seems like it should be archived, say so. If two projects should be merged, recommend it. Don't just affirm the current state.
