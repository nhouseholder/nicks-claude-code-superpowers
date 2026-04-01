---
name: dispatching-parallel-agents
description: Parallel agent orchestrator with strict safety controls. Max 2 agents for research, max 3 for independent code tasks. Agents share context via briefings that include memory files, anti-patterns, and verified constants. NEVER parallelize data analysis. Sequential-first mindset — only parallelize when genuinely independent AND the overhead is justified.
weight: heavy
---

# Parallel Agent Orchestration — Conservative Mode

## The Hard Truth About Parallel Agents

Parallel agents have caused MORE problems than they've solved over the last 2 weeks:
- **Data divergence:** Two agents returned different numbers for the same dataset (26 vs 36 round bets)
- **Research failure cascades:** 5 agents launched, most failed/timed out, Claude proceeded with stale training data
- **Context isolation:** Each agent starts fresh — no memory, no anti-patterns, no session context
- **Silent disagreements:** Agents produce conflicting results that aren't caught until the user notices

**Default posture: Do it yourself.** Only dispatch agents when the task is genuinely large, genuinely independent, and the agents can succeed without shared state.

## The One Gate: "Can This Hurt Us?"

Before dispatching ANY subagent, ask ONE question:

**"If this agent gets it wrong, produces bad data, or fails silently — can it hurt us?"**

| Answer | Action |
|--------|--------|
| **YES it can hurt us** | Do it yourself. No agents. Period. |
| **NO it cannot hurt us** | Safe to dispatch — but make it a GREAT agent (see briefing protocol below) |

### What CAN hurt us (never parallelize):
- Anything involving numbers, stats, P/L, ROI, counting
- Anything that writes to files, registries, databases
- Anything requiring domain expertise (betting, finance, scoring)
- Anything where wrong output gets reported to the user as fact
- Anything where two agents might disagree and we can't tell which is right
- Bug diagnosis (need single chain of reasoning)

### What CANNOT hurt us (safe to parallelize):
- **Read-only exploration** — "find files matching X", "search for Y across the codebase"
- **Independent research on different topics** — "how does React 19 routing work?" + "what's the Prisma migration guide?" (different topics, neither affects the other)
- **Truly independent file edits** — different files, different subsystems, no shared state
- **Code search / grep across repos** — read-only, returns file paths

### Supporting gates (ask these too):

**Gate 2: Can each agent succeed independently?**
Each agent gets NO conversation history. If it needs context from this session, results from another agent, or domain knowledge — either include it ALL in the briefing or do it yourself.

**Gate 3: Is the overhead justified?**
If you can do it yourself in <5 minutes, do it yourself. Agent briefing, dispatch, waiting, review, and reconciliation cost tokens too.

**Gate 4: What's the fallback if the agent fails?**
If failure means "proceed with stale training data" — don't dispatch. If failure means "try a different search" — acceptable.

## Agent Limits (HARD CAPS)

| Task Type | Max Agents | Why |
|-----------|-----------|-----|
| **Data analysis** | 0 (do it yourself) | Two agents counting the same data WILL disagree |
| **Research** | 2 | More agents = more failures, harder to reconcile |
| **Code tasks** | 3 | Beyond 3, merge conflicts and context loss outweigh speed |
| **Full-stack** | 3 (1 per layer) | Frontend, backend, infrastructure — max |

**NEVER launch more than 3 agents total.** The NFL Draft disaster used 5 — most failed. 2 reliable agents > 5 flaky ones.

## What NEVER Gets Parallelized

These tasks MUST be done by you, in a single chain, never delegated:

1. **Anything involving numbers/data** — counting, aggregating, P/L, ROI, statistics
2. **Anything requiring domain expertise** — betting logic, financial calculations, scoring rules
3. **Anything that touches the profit registry** — reads, writes, analysis
4. **Decision-making** — "should we gate R2 bets?" requires one consistent analysis
5. **Bug diagnosis** — need to trace one path through the code
6. **Data file modifications** — registry, cache, odds data
7. **Anything where getting it wrong costs the user hours** — when in doubt, do it yourself

## Making Damn Good Agents (When Dispatch Passes the Gate)

When a task passes the "can this hurt us?" gate and agents ARE dispatched, they must be excellent. A lazy agent is worse than no agent.

### The Agent Intelligence Checklist

Before dispatching, build the agent's briefing. If you can't fill in ALL of these, the agent isn't ready:

```
AGENT BRIEF:
─────────────────────────────────────
ROLE: "You are a [domain] specialist working on [project]"
MISSION: [One specific deliverable — be precise]

CONTEXT (the agent's entire world):
- FILES TO READ: [List exact file paths — not "check the repo"]
- ANTI-PATTERNS: [Paste relevant entries from anti-patterns.md — not just "check anti-patterns"]
- PROJECT MEMORY: [Paste relevant sections — agent can't access ~/.claude/memory/]
- DOMAIN RULES: [If touching domain logic, paste the FULL spec — not a pointer]

VERIFIED FACTS (constants the agent must NOT re-derive):
- [Any numbers, stats, decisions already established in this session]
- [E.g., "There are 71 events in the backtest. Do not count them yourself."]

GUARDRAILS:
- DO NOT: [Specific things that have gone wrong before]
- DO NOT: modify, overwrite, or delete any data files
- DO NOT: re-derive numbers that are given as verified facts above
- IF UNCERTAIN: return "UNCERTAIN: [what you're unsure about]" instead of guessing

OUTPUT FORMAT:
- [Exact structure expected — e.g., "Return a JSON object with keys: ..."]
- [If returning numbers, include how you computed each one]
- [Include confidence level: HIGH/MEDIUM/LOW for each finding]

SELF-CHECK BEFORE RETURNING:
- Did I answer the specific mission, not a related-but-different question?
- Do my numbers match the verified facts I was given?
- Did I flag anything I'm uncertain about?
─────────────────────────────────────
```

### The Agent Quality Bar

An agent dispatch is only worth it if the agent will be BETTER than doing it yourself. That means:

1. **Full context** — paste actual file contents and memory entries, not file paths the agent might fail to read
2. **Anti-pattern awareness** — paste the specific entries, not "check anti-patterns.md"
3. **Guardrails** — explicitly tell it what NOT to do based on past failures
4. **Self-check** — the agent verifies its own output before returning
5. **Confidence signals** — agent must flag uncertainty, not present guesses as facts
6. **No re-derivation** — verified facts are passed as constants, never recomputed

## Post-Dispatch Protocol

### When agents return:

1. **Cross-check ALL numbers** — if any agent produced numbers, verify them yourself
2. **Check for contradictions** — do agents agree on facts, names, dates, counts?
3. **If agents disagree on anything factual** — STOP. Verify from raw data yourself. Never report either agent's numbers until verified.
4. **Merge results** — combine outputs, resolve any style/format differences
5. **Run the result through data-consistency-check** — before reporting to user

### When agents FAIL:

1. **Do NOT proceed with stale data** — if a research agent fails, you don't have the research
2. **Tell the user** — "Agent failed to fetch X. Options: I try directly, you provide it, or we skip it."
3. **Never substitute training data for failed research** — this caused the NFL Draft disaster
4. **Don't retry the same agent** — if it failed once, the approach is wrong. Try a different approach (direct WebSearch, different URL, ask user)

## Communication Between Sequential Agents

When agents must be sequential (Agent B needs Agent A's output):

```
# Agent A runs first, returns results
agent_a_results = {
  "verified_count": 36,
  "verified_pnl": "+42.21u",
  "key_finding": "R2 bets are -10.4% ROI"
}

# Agent B gets Agent A's results as CONSTANTS in its briefing
AGENT B BRIEF:
- VERIFIED INPUT (from prior analysis):
  - Round bets: 36 total, +42.21u
  - R2 ROI: -10.4%
- YOUR TASK: Build a display table using THESE numbers (do not recompute)
```

## Rules (Updated)

1. **Sequential by default** — only parallelize when genuinely independent AND justified
2. **Max 3 agents** — never more, period
3. **Max 2 for research** — more agents = more failures
4. **NEVER parallelize data analysis** — one chain of custody through the numbers
5. **Full context in every briefing** — agents don't have your memory
6. **Failed agents = STOP** — don't proceed with missing data
7. **Cross-check before reporting** — verify all agent outputs agree
8. **Do it yourself if <5 minutes** — agent overhead isn't free
9. **Include anti-patterns** — agents that don't know past failures will repeat them
10. **When in doubt, don't parallelize** — the cost of a wrong parallel result exceeds the time saved
