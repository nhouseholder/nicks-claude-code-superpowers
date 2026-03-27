Expert strategic advisor scoped to the CURRENT PROJECT ONLY. Reviews this project's handoff, memory, anti-patterns, git state, and codebase — then produces expert-level recommendations for what to do next.

Triggers: "what's next", "what should I work on", "out of ideas", "what to improve", "recommendations", "what needs attention"

**This command is READ-ONLY + ANALYSIS. It does not modify any files, deploy anything, or start work. It produces a prioritized recommendation report for the current project.**

---

## STEP 0: Identify Current Project

Determine the project from the current working directory:

```bash
# Where are we?
pwd

# What's the git remote? (source of truth for project identity)
git remote get-url origin 2>/dev/null || echo "no-git-remote"

# Current branch and dirty state
git branch --show-current 2>/dev/null
git status --porcelain 2>/dev/null | head -20
```

**Extract:** project name, GitHub repo, live site URL (from `~/Projects/site-to-repo-map.json` if exists).

If the current directory is NOT inside a project (e.g., `~/.claude/` or `~/`), tell the user: "Navigate to a project directory first, then run /whats-next."

---

## STEP 1: Gather Project Context (Parallel)

Read ALL of the following for THIS project only:

### 1a. Most recent handoff for this project
```bash
# Clone superpowers to get handoffs (if not already in /tmp)
cd /tmp && rm -rf whats-next-tmp
git clone --depth 3 https://github.com/nhouseholder/nicks-claude-code-superpowers.git whats-next-tmp 2>&1 | tail -1

# Find handoff matching this project name
ls -t /tmp/whats-next-tmp/handoffs/*[PROJECT_NAME]* 2>/dev/null | head -1
```

**Read the handoff.** Extract:
- Section 6 (In Progress) — unfinished work
- Section 7 (Blocked) — things waiting on resolution
- Section 8 (Next Steps) — queued priorities
- Section 9 (Agent Observations) — what the last agent learned

### 1b. Project-specific memory
Read the project's memory index:
```bash
# Find the project memory directory (sanitized cwd path)
ls ~/.claude/projects/*/memory/MEMORY.md 2>/dev/null
```
Read the matching MEMORY.md and any referenced memory files.

### 1c. Anti-patterns relevant to this project
```bash
cat ~/.claude/anti-patterns.md 2>/dev/null
```
Filter for entries mentioning this project name or its tech stack.

### 1d. Git activity for this project
```bash
# Recent commits
git log --oneline -20

# What's changed since last deploy/tag
git log --oneline --since="7 days ago"

# Uncommitted work
git diff --stat
git diff --cached --stat
```

### 1e. Project structure and health
```bash
# Package info
cat package.json 2>/dev/null | python3 -c "import json,sys; d=json.load(sys.stdin); print(f'name: {d.get(\"name\")}, version: {d.get(\"version\")}')" 2>/dev/null

# Does it build?
ls -la dist/ build/ .next/ 2>/dev/null | head -5

# Project CLAUDE.md (project-specific rules)
cat CLAUDE.md 2>/dev/null | head -50
```

### 1f. Live site status (if this is a website project)
If a live URL exists for this project, check it:
```bash
curl -sI [LIVE_URL] 2>/dev/null | head -5
```

---

## STEP 2: Assess Project State

Classify this project's current state:

| State | Meaning |
|-------|---------|
| **ACTIVE-HOT** | Worked on in last 48 hours, has pending tasks |
| **ACTIVE-WARM** | Worked on in last 7 days, stable but has known improvements |
| **ACTIVE-COLD** | Not touched in 7+ days, may have stale state |
| **BLOCKED** | Has explicit blockers from handoff Section 7 |
| **NEEDS-RECOVERY** | Handoff mentions broken state, failed deploys, or data loss |

---

## STEP 3: Generate Expert Recommendations

Think like a **senior technical advisor** who deeply understands this project's domain. Each recommendation must be specific to THIS project — no generic advice.

**Each recommendation must include:**
1. **What** — the specific action (not vague "improve X")
2. **Why** — strategic reasoning, citing handoff state, anti-patterns, or domain expertise
3. **Impact** — expected outcome (quantified if possible)
4. **Effort** — estimated session count (1 session = ~2 hours of Claude work)
5. **Dependencies** — what must be true before starting

**Recommendation categories:**

### A. URGENT — Fix broken things
From handoff Section 6/7 — broken features, failed deploys, regressions.

### B. HIGH-VALUE — Biggest ROI for this project
What would produce the most impact per unit of effort? Think:
- Algorithm accuracy improvements (sports projects)
- User-facing features that make the product more valuable
- Infrastructure that prevents future incidents
- Performance improvements users would notice

### C. TECHNICAL DEBT — Things that will compound
- Recurring bugs from anti-patterns
- Architectural issues noted in handoffs
- Missing tests for critical paths
- Dependencies that need updating

### D. FEATURES — What would users want next?
Based on the project's purpose and current state, what features are missing or incomplete?

### E. MAINTENANCE — Keep it healthy
- Dependency updates, security patches
- Cache/data freshness
- Stale state cleanup

---

## STEP 4: Present

```
WHAT'S NEXT — [Project Name]
=============================
Generated: [date]
State: [ACTIVE-HOT / ACTIVE-WARM / etc.]
Last commit: [date + message]
Live site: [URL or N/A]
Version: [current version]
Handoff: [found / not found]

CURRENT STATE
-------------
[2-3 sentence summary of where this project stands right now]

IN-PROGRESS WORK (from handoff)
-------------------------------
[Bulleted list of unfinished work, or "None — clean state"]

BLOCKED ITEMS
-------------
[Bulleted list of blockers, or "None"]

TOP RECOMMENDATIONS
-------------------

#1. [CATEGORY] [Title]
   What: [specific action]
   Why: [expert reasoning — cite handoff, anti-pattern, or domain knowledge]
   Impact: [expected outcome]
   Effort: [session estimate]
   Deps: [prerequisites]

#2. [CATEGORY] ...

... (up to 7 recommendations, ranked by value)

ANTI-PATTERN WATCH
------------------
[Known bugs and failure patterns specific to this project. What to avoid.]

SUGGESTED SESSION PLAN
----------------------
[If the user starts working now, what's the optimal sequence? List 2-3 tasks in order.]
```

---

## STEP 5: Clean Up

```bash
rm -rf /tmp/whats-next-tmp 2>/dev/null
```

---

## CRITICAL RULES

1. **SCOPED TO CURRENT PROJECT ONLY.** Do not scan all projects. Do not recommend work on other projects. Focus entirely on the repo/site the session is in.
2. **READ-ONLY.** Gather information and advise. Do NOT make changes, deploy, or start work.
3. **Expert-level insights, not generic advice.** "Improve your tests" is useless. "Add error boundary around the fight card component — it crashed twice in the last 3 sessions when API returns null matchup data" is actionable.
4. **Cite your evidence.** Every recommendation should reference a specific handoff section, anti-pattern entry, memory file, or git state.
5. **Be honest about unknowns.** If the handoff is stale or missing, say so.
6. **Prioritize by user values.** (a) don't break live sites, (b) algorithm accuracy/profitability, (c) ship features users see, (d) reduce session friction.
7. **End with a session plan.** The user wants to know "what should I do RIGHT NOW in this session?"
