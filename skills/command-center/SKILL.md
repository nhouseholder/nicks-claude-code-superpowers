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

Launch all independent agents simultaneously using the Agent tool. Independent workstreams run concurrently; dependent workstreams wait for their prerequisites and launch in the next wave.

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

### Example: Feature Build
```
"Add a user profile page with avatar upload"
→ Agent 1: Frontend (React component, routing, UI states)
→ Agent 2: Backend (API endpoint, file upload, storage)
→ Agent 3: Tests (unit + integration tests for both)
```

Other common patterns: Research + Implementation (research wave then build wave), Multi-File Refactor (one agent per subsystem), Content + Code (copy, design, integration agents), Analysis (one agent per audit dimension).

## Resource Management — The CEO's Playbook

### How Many Agents?

The number of agents is a strategic decision, not "more is better". Use 2 agents for single-domain features, 3-4 for multi-domain, max 5 for full-stack builds. Use the MINIMUM agents needed — 2 focused agents beat 5 fragmented ones.

### Research-First vs Execute-First

Use **Research-First** when the path is unclear (unknown bugs, library choices, optimization targets): run a research wave first, then an implementation wave. Use **Execute-First** when the path is clear (add feature, migrate code, write tests): deploy all agents simultaneously. Use **Hybrid** for complex features — research + scaffold in parallel, then implementation uses those outputs.

### Priority Assignment

Assign CRITICAL to core functionality that blocks everything, HIGH to direct user-facing work, MEDIUM/LOW to tests, docs, and cleanup. On failure: retry CRITICAL, report HIGH, note MEDIUM/LOW for later.

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
- Anti-patterns:        ALWAYS include relevant entries from anti-patterns.md
- Known gotchas:        ALWAYS include project gotchas relevant to this agent's domain

NEVER: Dump the entire codebase context into every agent.
ALWAYS: Curate context per agent. A test agent doesn't need the deploy config.

MANDATORY CONTEXT (every agent gets these, non-negotiable):
1. Project conventions from MEMORY.md relevant to the agent's domain
2. Known anti-patterns from anti-patterns.md that could affect the agent's work
3. User preferences that affect code style, naming, or approach
4. Recurring bug entries from error-memory if the agent is touching affected code

This prevents subagents from repeating mistakes the main session already learned from.
```

### Merge Strategy

When agents return, merge intelligently:

```
NO CONFLICTS:   Combine outputs, run build/tests, done
STYLE CONFLICTS: Use project conventions as tiebreaker
LOGIC CONFLICTS: The agent working on the PRIMARY domain wins
TRUE CONFLICTS:  Escalate to user with both options + recommendation
```

## Token Economics

Parallel agents save wall-clock time and produce focused, higher-quality first drafts. Orchestration wastes tokens when the task is too small, strictly sequential, or context is heavily shared across agents. Before launching, estimate: under 3 agents is always worth it for decomposable tasks; 3-5 for substantial features; over 5 → ask the user before proceeding.

## Rules

1. **Activation test first** — Don't orchestrate when you should just execute
2. **Self-contained briefs** — Each agent must succeed without conversation history
3. **Parallel by default** — If two things CAN run in parallel, they MUST
4. **Resolve before reporting** — Never hand the user conflicting agent outputs
5. **Budget awareness** — Estimate token cost. Ask for >5 agents.
6. **No theater** — Don't dramatize the orchestration. Brief status, then results.
7. **Quality gate** — Build/test must pass before declaring success
8. **Focused agents** — Each agent does ONE thing well, not everything mediocrely
