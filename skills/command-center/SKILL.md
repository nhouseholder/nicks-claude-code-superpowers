---
name: command-center
description: Master AI agent orchestrator. Automatically decomposes complex tasks into parallel workstreams, assigns specialist subagents with expert lenses, launches them concurrently, and unifies results. Claude becomes the CEO — analyzing, delegating, coordinating, and delivering. Activates on complex multi-domain tasks that benefit from parallel execution.
---

# Command Center — You Talk to the Boss, the Boss Runs the Army

You don't manage agents. You give Claude the mission. Claude figures out the team, the plan, the execution, and the delivery. One prompt in, complete result out.

## When This Activates

**Automatic activation** when a task meets ALL of these criteria:

1. **Decomposable** — The task has 2+ independent workstreams that don't block each other
2. **Multi-domain** — The task spans different areas (frontend + backend, research + implementation, analysis + writing)
3. **Substantial** — Each workstream is complex enough to justify a dedicated agent (not a 5-line change)

**Do NOT activate for:**
- Single-file changes
- Simple bug fixes
- Quick questions
- Tasks where steps are strictly sequential (each depends on the previous)
- Anything the main agent can handle in <2 minutes

**The activation test:** "Would I be faster doing this myself, or by briefing 3 specialists?" If specialists → activate. If myself → just do it.

## The Command Center Protocol

### Phase 1: Mission Analysis (~100 tokens)

Read the user's request and decompose it:

```
MISSION: [What the user wants — in one sentence]
WORKSTREAMS:
  1. [Domain] — [What this agent does] — [Dependencies: none / needs X first]
  2. [Domain] — [What this agent does] — [Dependencies: none / needs X first]
  3. [Domain] — [What this agent does] — [Dependencies: none / needs X first]
PARALLEL: [Which can run simultaneously]
SEQUENTIAL: [Which must wait for others]
```

### Phase 2: Agent Briefing

Each agent gets a focused, complete briefing:

```
AGENT BRIEF:
- ROLE: "You are a [domain expert] working on [project name]"
- MISSION: [Specific deliverable — not vague, not the whole task]
- CONTEXT: [Only the files/info THIS agent needs — not the whole codebase]
- EXPERT LENS: [Domain mental models to apply]
- QUALITY BAR: [What "done" looks like for this workstream]
- CONSTRAINTS: [Budget, style conventions, patterns to follow]
- OUTPUT: [Exact format expected back]
```

**Critical:** Each agent brief must be SELF-CONTAINED. The agent doesn't have the main conversation history. Include everything it needs to succeed independently.

### Phase 3: Parallel Dispatch

Launch all independent agents simultaneously using the Agent tool:

```
┌─────────────────────────────────────────────┐
│              COMMAND CENTER                   │
│                                               │
│   ┌──────────┐  ┌──────────┐  ┌──────────┐  │
│   │ Agent 1  │  │ Agent 2  │  │ Agent 3  │  │
│   │ Frontend │  │ Backend  │  │ Tests    │  │
│   │ Expert   │  │ Expert   │  │ Expert   │  │
│   └────┬─────┘  └────┬─────┘  └────┬─────┘  │
│        │              │              │        │
│        └──────────────┼──────────────┘        │
│                       │                       │
│              UNIFIED RESULT                   │
└─────────────────────────────────────────────┘
```

- Use `Agent` tool with `subagent_type: "general-purpose"`
- Launch all independent agents in a SINGLE message (parallel execution)
- If some agents depend on others, wait for dependencies first, then launch the next wave

### Phase 4: Result Integration

When agents return:

1. **Review each result** — Does it meet the quality bar from the brief?
2. **Check for conflicts** — Did Agent 1 and Agent 2 make incompatible decisions?
3. **Resolve conflicts** — Use the project's established patterns as the tiebreaker
4. **Integrate** — Merge results into a coherent whole
5. **Verify** — Run builds/tests to confirm everything works together
6. **Report** — Brief the user on what was accomplished

### Phase 5: Quality Gate

Before reporting to the user:
```
□ All agents completed successfully
□ No conflicting changes between agents
□ Code compiles / builds
□ Tests pass (if applicable)
□ Changes are consistent with project patterns
□ Nothing was missed in decomposition
```

If any check fails → fix it before reporting. The user should receive a polished result, not a pile of agent outputs.

## Decomposition Patterns

### Feature Build
```
"Add a user profile page with avatar upload"
→ Agent 1: Frontend (React component, routing, UI states)
→ Agent 2: Backend (API endpoint, file upload, storage)
→ Agent 3: Tests (unit + integration tests for both)
```

### Research + Implementation
```
"Optimize our recommendation algorithm"
→ Agent 1: Research (analyze current perf, identify bottlenecks, propose solutions)
→ Agent 2: Benchmark (set up metrics, create baseline measurements)
→ [Wait for both] → Agent 3: Implement (apply best solution from research)
```

### Multi-File Refactor
```
"Migrate from REST to GraphQL"
→ Agent 1: Schema (design GraphQL schema from existing REST endpoints)
→ Agent 2: Resolvers (implement resolvers matching current business logic)
→ Agent 3: Client (update frontend API calls to use GraphQL)
→ Agent 4: Tests (update test suite)
```

### Content + Code
```
"Build a landing page for our new feature"
→ Agent 1: Copy (write compelling, accurate marketing copy)
→ Agent 2: Design (component structure, responsive layout, animations)
→ Agent 3: Integration (wire to real data, CTA actions, analytics)
```

### Analysis
```
"Audit our codebase for performance issues"
→ Agent 1: Frontend perf (bundle size, render cycles, lazy loading)
→ Agent 2: Backend perf (query optimization, caching, N+1)
→ Agent 3: Infrastructure (CDN, compression, caching headers)
```

## Resource Management — The CEO's Playbook

### How Many Agents?

The number of agents is a strategic decision, not "more is better":

```
SIZING GUIDE:
┌────────────────────────────────┬──────────┬────────────────────────────┐
│ Task Type                      │ Agents   │ Why                        │
├────────────────────────────────┼──────────┼────────────────────────────┤
│ Feature (1 domain)             │ 1-2      │ Main + tests               │
│ Feature (multi-domain)         │ 2-3      │ Frontend + backend + tests │
│ Major refactor                 │ 3-4      │ One per subsystem          │
│ Full-stack feature build       │ 3-5      │ UI + API + DB + tests + docs│
│ Research + implement           │ 2-3      │ Research wave, then build  │
│ Codebase-wide audit            │ 2-4      │ One per audit dimension    │
└────────────────────────────────┴──────────┴────────────────────────────┘

RULE: Use the MINIMUM agents needed. 2 focused agents > 5 fragmented ones.
```

### Research-First vs Execute-First

Before deploying, decide the strategy:

```
RESEARCH-FIRST (use when uncertain):
  Wave 1: Research agent(s) → gather info, analyze, propose
  Wave 2: Implementation agent(s) → build based on research findings

  Examples: "optimize performance", "choose the best library", "fix an unknown bug"

EXECUTE-FIRST (use when the path is clear):
  All agents deploy simultaneously → each executes independently

  Examples: "add user profile page", "migrate to TypeScript", "add tests for module X"

HYBRID (use for complex features):
  Wave 1: Research + scaffold agents in parallel
  Wave 2: Implementation agents use research + scaffold as input

  Examples: "build a recommendation engine", "add payment processing"
```

### Priority Assignment

Not all agents are equal. Assign priority to manage attention:

```
CRITICAL:  Core functionality — blocks everything else if it fails
HIGH:      Direct user-facing — quality must be production-grade
MEDIUM:    Supporting work — tests, docs, utilities
LOW:       Nice-to-have — optimization, cleanup, minor improvements

On failure: Retry CRITICAL. Report HIGH. Note MEDIUM/LOW for later.
```

### Agent Monitoring

After deployment, the Command Center tracks each agent:

```
MONITORING (lightweight — no polling):
- Check each agent result as it returns
- If an agent fails → assess impact on other agents
- If an agent's result conflicts with another → resolve before proceeding
- If an agent is taking too long → it's autonomous, wait for it
- NEVER launch duplicate agents for the same workstream
```

### Context Budgeting

Each agent gets the MINIMUM context needed:

```
CONTEXT BUDGET PER AGENT:
- Project overview:     ~100 tokens (from MEMORY.md / CLAUDE.md)
- Relevant files:       Read only the files THIS agent needs
- Conventions:          Only patterns relevant to this agent's domain
- Dependencies:         Only what this agent's output connects to

NEVER: Dump the entire codebase context into every agent.
ALWAYS: Curate context per agent. A test agent doesn't need the deploy config.
```

### Merge Strategy

When agents return, merge intelligently:

```
NO CONFLICTS:   Combine outputs, run build/tests, done
STYLE CONFLICTS: Use project conventions as tiebreaker
LOGIC CONFLICTS: The agent working on the PRIMARY domain wins
TRUE CONFLICTS:  Escalate to user with both options + recommendation
```

## Agent Specialization

Each agent inherits the full skill stack but FOCUSES on its domain:

| Agent Role | Primary Skills Activated |
|-----------|------------------------|
| **Frontend Expert** | coding-standards, proactive-qa (UI focus), zero-iteration |
| **Backend Expert** | coding-standards, zero-iteration, systematic-debugging |
| **Test Expert** | test-driven-development, verification-loop |
| **Research Expert** | deep-research, search-first, expert-lens |
| **Data Expert** | expert-lens (statistician), precision-reading |
| **Design Expert** | expert-lens (designer), proactive-qa (UX focus) |
| **DevOps Expert** | process-monitor, deploy, git-sorcery |

## Token Economics

### Cost Model
```
Command Center overhead:     ~200 tokens (decomposition + briefing)
Per agent:                   ~2000-8000 tokens (depends on task complexity)
Integration:                 ~500 tokens (review + merge + verify)
```

### When It Saves Tokens
- **3 parallel agents** finish in ~1/3 wall-clock time vs sequential
- Each agent has FOCUSED context (reads fewer files, makes fewer mistakes)
- Specialist agents produce higher-quality first drafts (fewer revision cycles)

### When It Wastes Tokens
- Task is too small (overhead > savings)
- Task is strictly sequential (no parallelism possible)
- Context is heavily shared (agents duplicate reads)

### Budget Guard
Before launching agents, estimate total cost:
- **< 3 agents** → Always worth it if task is decomposable
- **3-5 agents** → Worth it for substantial features
- **> 5 agents** → Ask the user: "This is a big task — I'd deploy [N] specialists. Proceed?"

## Communication Style

### To the User (Before)
Brief announcement, not a dissertation:
```
Deploying 3 specialists in parallel:
• Frontend: profile page component + routing
• Backend: avatar upload API + storage
• Tests: unit + integration coverage

Working...
```

### To the User (After)
Results-focused summary:
```
Done. All 3 agents completed:
• Frontend: ProfilePage component with avatar upload, all states handled
• Backend: /api/upload endpoint with S3 storage, size validation
• Tests: 12 tests passing (8 unit, 4 integration)
• Build: ✓ passing

[response-recap if complex enough]
```

### Don't Say
- "I'm orchestrating an army of AI agents..."
- "As the command center, I'm deploying..."
- "My specialized agents are working on..."

Just say what's happening. The user doesn't care about the metaphor — they care about the result.

## Integration with Existing Skills

```
command-center (orchestrator)
    │
    ├─ Uses: dispatching-parallel-agents (agent launch mechanics)
    ├─ Uses: expert-lens (agent specialization)
    ├─ Uses: iterative-retrieval (agent context assembly)
    ├─ Uses: pattern-propagation (cross-agent consistency)
    ├─ Uses: verification-before-completion (quality gate)
    ├─ Uses: git-sorcery (atomic commits per workstream)
    └─ Uses: response-recap (unified result summary)
```

## Rules

1. **Activation test first** — Don't orchestrate when you should just execute
2. **Self-contained briefs** — Each agent must succeed without conversation history
3. **Parallel by default** — If two things CAN run in parallel, they MUST
4. **Resolve before reporting** — Never hand the user conflicting agent outputs
5. **Budget awareness** — Estimate token cost. Ask for >5 agents.
6. **No theater** — Don't dramatize the orchestration. Brief status, then results.
7. **Quality gate** — Build/test must pass before declaring success
8. **Focused agents** — Each agent does ONE thing well, not everything mediocrely
