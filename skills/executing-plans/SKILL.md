---
name: executing-plans
description: Use when you have a written implementation plan to execute in a separate session with review checkpoints
weight: light
---

# Executing Plans

## Overview

Load plan, review critically, execute all tasks, report when complete.

**Note:** If subagents are available, use dispatching-parallel-agents for parallel execution of independent tasks.

## The Process

### Step 1: Load and Review Plan
1. Read plan file
2. Review critically - identify any questions or concerns about the plan
3. If concerns: Raise them with your user before starting
4. If no concerns: Create TodoWrite and proceed

### Step 2: Execute Tasks

For each task:
1. Mark as in_progress
2. Follow each step exactly (plan has bite-sized steps)
3. Run verifications as specified
4. Mark as completed

### Step 3: UNIFY — Reconcile Plan vs Actual

After all tasks complete, reconcile what was planned vs what actually happened:

1. **Diff the plan** — For each planned task, note: done as planned, modified (why), skipped (why), or added (why)
2. **Record decisions** — Any mid-execution judgment calls that diverged from the plan. Future sessions need to know WHY, not just WHAT.
3. **Log deferred items** — Anything discovered during execution that should be done but wasn't in scope. Add to a `## Deferred` section in the plan file.
4. **Flag drift** — If >30% of tasks were modified or skipped, the plan had a gap. Note what information would have made the plan better.

This step prevents "plan says X but code does Y" confusion in future sessions.

### Step 4: Complete Development

After UNIFY reconciliation:
- Announce: "I'm using the finishing-a-development-branch skill to complete this work."
- **REQUIRED SUB-SKILL:** Use superpowers:finishing-a-development-branch
- Follow that skill to verify tests, present options, execute choice

## When to Stop and Ask for Help

**STOP executing immediately when:**
- Hit a blocker (missing dependency, test fails, instruction unclear)
- Plan has critical gaps preventing starting
- You don't understand an instruction
- Verification fails repeatedly

**Ask for clarification rather than guessing.**

## When to Revisit Earlier Steps

**Return to Review (Step 1) when:**
- Partner updates the plan based on your feedback
- Fundamental approach needs rethinking

**Don't force through blockers** - stop and ask.

## Remember
- Review plan critically first
- Follow plan steps exactly
- Don't skip verifications
- Reference skills when plan says to
- Stop when blocked, don't guess
- Never start implementation on main/master branch without explicit user consent

## Integration

**Required workflow skills:**
- **superpowers:using-git-worktrees** - REQUIRED: Set up isolated workspace before starting
- **superpowers:writing-plans** - Creates the plan this skill executes
- **superpowers:finishing-a-development-branch** - Complete development after all tasks
