---
name: dispatching-parallel-agents
description: Parallel agent orchestrator with strict safety controls. Max 2 agents for research, max 3 for independent code tasks. Agents share context via briefings that include memory files, anti-patterns, and verified constants. NEVER parallelize data analysis. Sequential-first mindset — only parallelize when genuinely independent AND the overhead is justified.
---

# Parallel Agent Orchestration — Conservative Mode

## The Hard Truth About Parallel Agents

Parallel agents have caused MORE problems than they've solved over the last 2 weeks:
- **Data divergence:** Two agents returned different numbers for the same dataset (26 vs 36 round bets)
- **Research failure cascades:** 5 agents launched, most failed/timed out, Claude proceeded with stale training data
- **Context isolation:** Each agent starts fresh — no memory, no anti-patterns, no session context
- **Silent disagreements:** Agents produce conflicting results that aren't caught until the user notices

**Default posture: Do it yourself.** Only dispatch agents when the task is genuinely large, genuinely independent, and the agents can succeed without shared state.

## Decision Framework: Should I Parallelize?

Ask these questions IN ORDER. If any answer is NO, do it yourself.

### Gate 1: Is this genuinely parallel?
Tasks that share data, state, or files are NOT parallel. They're sequential.
- Reading the same JSON file → NOT parallel
- Computing different stats from the same dataset → NOT parallel
- Frontend component A + Backend API B that A calls → NOT parallel (need B's interface first)
- Two completely separate file edits in different subsystems → parallel OK

### Gate 2: Can each agent succeed independently?
Each agent gets NO conversation history. If an agent needs:
- Context from earlier in this conversation → do it yourself
- Results from another agent → do it sequentially
- Access to project memory/anti-patterns → include in briefing (adds overhead)
- Understanding of domain rules (e.g., prop bet settlement) → include full spec in briefing

### Gate 3: Is the overhead justified?
Each agent costs tokens for: briefing, context loading, result review, conflict resolution.
- If you can do it yourself in <5 minutes → do it yourself
- If the task requires <50 lines of code → do it yourself
- If you'd need to write >200 words of briefing per agent → probably do it yourself

### Gate 4: What happens if an agent fails?
- If one agent's failure blocks everything → don't parallelize (single point of failure)
- If research agents might not find data → have a fallback plan BEFORE dispatching
- If agent timeout kills the task → set explicit timeouts and have a plan B

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

## What CAN Be Parallelized (With Caution)

| Safe to Parallelize | Example |
|---------------------|---------|
| Independent file searches | "Find all uses of X" + "Find all uses of Y" in different codebases |
| Separate subsystem edits | Fix CSS in component A + Fix API in route B (different files, no shared state) |
| Research on different topics | "How does React 19 work?" + "What's the Prisma 6 migration guide?" |
| Independent test suites | Run frontend tests + Run backend tests |

## Agent Briefing Protocol (MANDATORY)

Every agent MUST receive:

### 1. Full Context Package
```
AGENT BRIEF:
- ROLE: "You are a [domain] specialist"
- MISSION: [One specific deliverable]
- CONTEXT FILES TO READ:
  - [List specific files the agent should read]
  - Include anti-patterns.md sections relevant to this task
  - Include project memory relevant to this domain
- VERIFIED CONSTANTS: [If any numbers/stats are already known, pass them as constants]
- CONSTRAINTS: [What NOT to do — critical for preventing agent mistakes]
- OUTPUT FORMAT: [Exact format expected]
- DO NOT: [Specific anti-patterns from prior failures]
```

### 2. Domain Knowledge (when applicable)
If the agent will touch domain logic:
- Include the full spec file content (not just a pointer)
- Include worked examples
- Include anti-patterns for this specific domain

### 3. Anti-Pattern Awareness
Check `~/.claude/anti-patterns.md` for relevant entries and include them in the briefing.
An agent that doesn't know about past failures WILL repeat them.

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
