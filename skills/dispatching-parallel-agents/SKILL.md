---
name: dispatching-parallel-agents
description: Use when facing 2+ independent tasks that can be worked on without shared state or sequential dependencies
---

# Dispatching Parallel Agents

## Overview

You delegate tasks to specialized agents with isolated context. By precisely crafting their instructions and context, you ensure they stay focused and succeed at their task. They should never inherit your session's context or history — you construct exactly what they need. This also preserves your own context for coordination work.

When you have multiple unrelated failures (different test files, different subsystems, different bugs), investigating them sequentially wastes time. Each investigation is independent and can happen in parallel.

**Core principle:** Dispatch one agent per independent problem domain. Let them work concurrently.

## Boundary with command-center

Use dispatching-parallel-agents when you already KNOW the 2-3 independent tasks (e.g., 'fix tests in fileA, fileB, fileC in parallel'). Use command-center when you need to FIGURE OUT the task decomposition first (e.g., 'build this entire feature' requires analysis before parallelization). If in doubt, default to dispatching-parallel-agents — it's simpler and cheaper.

## When to Use

Decision flow: Multiple failures? -> If independent and no shared state -> parallel dispatch. If related -> single agent. If shared state -> sequential agents.

**Use when:**
- 3+ test files failing with different root causes
- Multiple subsystems broken independently
- Each problem can be understood without context from others
- No shared state between investigations

**Don't use when:**
- Failures are related (fix one might fix others)
- Need to understand full system state
- Agents would interfere with each other
- **Tasks share data or calculations** — if fixing bet type A uses the same payout function as bet type B, do them sequentially. Parallel agents on shared data = regressions. One agent's "fix" silently breaks the other's results.
- **Tasks touch the same files** — two agents editing the same component/function = merge conflicts and lost work
- **The output needs cross-validation** — if you need to check "do all columns add up to the total?", a single agent must see all columns

## The Pattern

### 1. Identify Independent Domains

Group failures by what's broken:
- File A tests: Tool approval flow
- File B tests: Batch completion behavior
- File C tests: Abort functionality

Each domain is independent - fixing tool approval doesn't affect abort tests.

### 2. Create Focused Agent Tasks

Each agent gets:
- **Specific scope:** One test file or subsystem
- **Clear goal:** Make these tests pass
- **Constraints:** Don't change other code
- **Expected output:** Summary of what you found and fixed
- **Anti-patterns:** Relevant entries from anti-patterns.md (so the agent doesn't repeat known-bad approaches)
- **Project conventions:** Key patterns from MEMORY.md relevant to this agent's scope

### 3. Dispatch in Parallel

```typescript
// In Claude Code / AI environment
Task("Fix agent-tool-abort.test.ts failures")
Task("Fix batch-completion-behavior.test.ts failures")
Task("Fix tool-approval-race-conditions.test.ts failures")
// All three run concurrently
```

### 4. Review and Integrate

When agents return:
- Read each summary
- Verify fixes don't conflict
- Run full test suite
- Integrate all changes

## Agent Prompt Structure

Good agent prompts are:
1. **Focused** - One clear problem domain
2. **Self-contained** - All context needed to understand the problem
3. **Specific about output** - What should the agent return?

```markdown
Fix the 3 failing tests in src/agents/agent-tool-abort.test.ts:

1. "should abort tool with partial output capture" - expects 'interrupted at' in message
2. "should handle mixed completed and aborted tools" - fast tool aborted instead of completed
3. "should properly track pendingToolCount" - expects 3 results but gets 0

These are timing/race condition issues. Your task:

1. Read the test file and understand what each test verifies
2. Identify root cause - timing issues or actual bugs?
3. Fix by:
   - Replacing arbitrary timeouts with event-based waiting
   - Fixing bugs in abort implementation if found
   - Adjusting test expectations if testing changed behavior

Do NOT just increase timeouts - find the real issue.

Return: Summary of what you found and what you fixed.
```

## Common Mistakes

**❌ Too broad:** "Fix all the tests" - agent gets lost
**✅ Specific:** "Fix agent-tool-abort.test.ts" - focused scope

**❌ No context:** "Fix the race condition" - agent doesn't know where
**✅ Context:** Paste the error messages and test names

**❌ No constraints:** Agent might refactor everything
**✅ Constraints:** "Do NOT change production code" or "Fix tests only"

**❌ Vague output:** "Fix it" - you don't know what changed
**✅ Specific:** "Return summary of root cause and changes"

## When NOT to Use

**Related failures:** Fixing one might fix others - investigate together first
**Need full context:** Understanding requires seeing entire system
**Exploratory debugging:** You don't know what's broken yet
**Shared state:** Agents would interfere (editing same files, using same resources)

## Plan Execution Mode (from subagent-driven-development)

When executing an implementation plan with independent tasks:

1. Read plan, extract all tasks, create TodoWrite
2. **Per Task**: Dispatch implementer → review → mark complete
3. After all tasks → final review of entire implementation

### Cost-Aware Review

Not every task needs the full review pipeline:
- **Simple/isolated changes**: Implementer + self-review sufficient
- **If qa-gate runs after**: Skip code quality reviewer — qa-gate covers it
- **Full pipeline only for**: Multi-file architectural changes with no other review planned

### Implementer Status Handling

| Status | Action |
|--------|--------|
| **DONE** | Proceed to review |
| **DONE_WITH_CONCERNS** | Read concerns, address if correctness/scope, then review |
| **NEEDS_CONTEXT** | Provide missing context, re-dispatch |
| **BLOCKED** | Assess: more context? more capable model? break into smaller pieces? escalate? |

**Never** force same model to retry without changes. If stuck, something needs to change.

## Verification

After agents return:
1. **Review each summary** — understand what changed
2. **Check for conflicts** — did agents edit same code?
3. **Run full suite** — verify all fixes work together
4. **Spot check** — agents can make systematic errors

