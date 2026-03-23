---
name: dispatching-parallel-agents
description: Parallel agent orchestrator with two modes — simple dispatch for known independent tasks, and complex orchestration for tasks requiring decomposition first. The CEO model — analyze, delegate, coordinate, deliver.
---

# Parallel Agent Orchestration

## Two Modes

### Mode 1: Simple Dispatch
You already KNOW the 2-3 independent tasks (e.g., "fix tests in fileA, fileB, fileC in parallel"). Jump straight to agent briefing and dispatch.

### Mode 2: Complex Orchestration
You need to FIGURE OUT the task decomposition first (e.g., "build this entire feature"). Run the decomposition phase, then dispatch.

**Decision rule:** If you can list the independent tasks in <10 seconds of thought, use Simple Dispatch. If you need to analyze the problem space first, use Complex Orchestration.

## When to Activate

**Use when:**
- 2+ independent tasks with no shared state or sequential dependencies
- Multi-domain work (frontend + backend, research + implementation)
- Each workstream is substantial enough to justify a dedicated agent

**Do NOT use when:**
- Single-file changes or simple bug fixes
- Tasks are strictly sequential (each depends on the previous)
- Agents would edit the same files (merge conflicts)
- Tasks share data or calculations (parallel agents on shared data = regressions)
- The output needs cross-validation across tasks
- You can handle it yourself in <2 minutes

**Activation test:** "Would I be faster doing this myself, or by briefing specialists?" If specialists, activate.

## Phase 1: Decomposition (Complex Orchestration Only)

```
MISSION: [What the user wants — one sentence]
WORKSTREAMS:
  1. [Domain] — [What this agent does] — [Dependencies: none / needs X first]
  2. [Domain] — [What this agent does] — [Dependencies: none / needs X first]
PARALLEL: [Which run simultaneously]
SEQUENTIAL: [Which must wait for others]
```

**How many agents?** Use the MINIMUM needed. 2 for single-domain, 3-4 for multi-domain, max 5 for full-stack. Ask the user before launching >5.

**Research-First vs Execute-First:** If the path is unclear (unknown bugs, library choices), run a research wave first, then implementation. If the path is clear, deploy all agents simultaneously.

**Decomposition examples:**
- Feature build: Frontend agent (component + routing) | Backend agent (API + storage) | Test agent (unit + integration)
- Research + implementation: Research wave first (explore options) → Build wave (execute chosen path)
- Multi-file refactor: One agent per subsystem, all parallel

## Phase 2: Agent Briefing

Each agent gets a focused, SELF-CONTAINED brief (no conversation history):

```
AGENT BRIEF:
- ROLE: "You are a [domain expert] working on [project name]"
- MISSION: [Specific deliverable — not the whole task]
- CONTEXT: [Only the files/info THIS agent needs]
- CONSTRAINTS: [Budget, style conventions, patterns to follow]
- OUTPUT: [Exact format expected back]
```

### Context Budgeting (Mandatory)

Each agent gets the MINIMUM context needed:
- Project conventions from MEMORY.md relevant to the agent's domain
- Anti-patterns from anti-patterns.md that could affect the agent's work
- User preferences affecting code style, naming, or approach
- Recurring bug entries if the agent is touching affected code

NEVER dump the entire codebase context into every agent. A test agent doesn't need deploy config.

## Phase 3: Parallel Dispatch

Launch all independent agents simultaneously using the Agent tool. Dependent workstreams wait for prerequisites and launch in the next wave.

- Use `Agent` tool with `subagent_type: "general-purpose"`
- Launch independent agents in a SINGLE message (parallel execution)
- NEVER launch duplicate agents for the same workstream

**Priority assignment:** CRITICAL = core functionality blocking everything (retry on failure). HIGH = user-facing work (report failure). MEDIUM/LOW = tests, docs, cleanup (note for later).

## Phase 4: Review and Integrate

When agents return:
1. **Review each result** — does it meet the quality bar?
2. **Check for conflicts** — incompatible decisions between agents?
3. **Resolve conflicts** — project conventions as tiebreaker; primary domain agent wins logic conflicts; true conflicts escalate to user
4. **Run builds/tests** — confirm everything works together
5. **Report** — brief the user on what was accomplished

### Quality Gate

Before reporting:
- All agents completed successfully
- No conflicting changes between agents
- Code compiles/builds, tests pass
- Changes consistent with project patterns
- Nothing missed in decomposition

If any check fails, fix it before reporting.

## Plan Execution Mode

When executing an implementation plan with independent tasks:

1. Read plan, extract all tasks
2. **Per Task**: Dispatch implementer -> review -> mark complete
3. After all tasks -> final review of entire implementation

### Implementer Status Handling

| Status | Action |
|--------|--------|
| **DONE** | Proceed to review |
| **DONE_WITH_CONCERNS** | Read concerns, address if correctness/scope, then review |
| **NEEDS_CONTEXT** | Provide missing context, re-dispatch |
| **BLOCKED** | Assess: more context? break into smaller pieces? escalate? |

**Never** force same model to retry without changes. If stuck, something needs to change.

### Cost-Aware Review

- **Simple/isolated changes**: Implementer + self-review sufficient
- **If qa-gate runs after**: Skip code quality reviewer — qa-gate covers it
- **Full pipeline only for**: Multi-file architectural changes with no other review planned

## Verification

After agents return:
1. Review each summary — understand what changed
2. Check for conflicts — did agents edit same code?
3. Run full suite — verify all fixes work together
4. Spot check — agents can make systematic errors

## Rules

1. **Activation test first** — don't orchestrate when you should just execute
2. **Self-contained briefs** — each agent must succeed without conversation history
3. **Parallel by default** — if two things CAN run in parallel, they MUST
4. **Resolve before reporting** — never hand the user conflicting agent outputs
5. **Budget awareness** — estimate token cost; ask for >5 agents
6. **No theater** — brief status, then results
7. **Quality gate** — build/test must pass before declaring success
8. **Focused agents** — each agent does ONE thing well, not everything mediocrely
