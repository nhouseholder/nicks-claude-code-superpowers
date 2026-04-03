---
name: autoresearch
description: Systematic skill and prompt optimization using Karpathy's autoresearch method. Diagnose failure patterns, build scoring checklists, run one-change-at-a-time improvement loops, and extract reusable rules from the changelog. Use when asked to improve a skill, optimize a prompt, or make any repeatable task consistently better.
weight: heavy
---

# Autoresearch — Systematic Optimization Loop

Applies the autoresearch scoring loop to improve any skill, prompt, or repeatable task. One change at a time, scored against a checklist, until it hits 90%+ consistently.

## When This Fires

- "improve this skill/prompt"
- "optimize [skill name]"
- "this skill isn't working well"
- "make this more consistent"
- "autoresearch [anything]"

## The 5-Phase Pipeline

### Phase 1: Diagnose — Find Why It Fails

Before fixing anything, understand what's broken.

1. Ask the user for the skill/prompt to optimize
2. Run it against 5 different test inputs and score each output
3. Identify the most common failure patterns — vague instructions, missing constraints, weak output format
4. Rank failures by frequency and impact (not obviousness)
5. Deliver a plain-language diagnosis BEFORE suggesting any fixes

**Rules:**
- Diagnose before fixing — never jump to solutions without evidence
- Every failure pattern must be specific — not "output is inconsistent"
- Baseline score must be established before any changes are made

**Gate:** Diagnosis complete → ranked failure patterns → root cause per pattern

### Phase 2: Build the Scoring Checklist

Turn vague quality feelings into precise yes/no questions.

1. Ask what a great output looks and feels like — extract the user's instincts
2. Convert every vague preference into a specific yes/no question
3. Test each question against 3 sample outputs — does it score consistently?
4. Remove any question that produces different answers on the same output
5. Deliver a final 3-6 question checklist

**Rules:**
- Every question must be yes or no — no ratings, no scales
- 3-6 questions maximum — more than 6 and the skill games the checklist
- Each question must check one specific thing — no compound questions
- Vague questions like "is it good quality?" are banned

**Gate:** Final checklist passes consistency test on 3 sample outputs

### Phase 3: Run the Optimization Loop

One change per round. Score. Keep or revert. Repeat.

1. Establish baseline — run the skill and score against the checklist
2. Identify the lowest-scoring checklist item — that's the first target
3. Make ONE specific change to address it — nothing else
4. Re-run and re-score — keep the change if score improves, revert if it doesn't
5. Log every change with: what changed, why, kept or reverted
6. Repeat until the skill hits 90%+ three times in a row

**Rules:**
- One change per round — never fix two things simultaneously
- Every change must be logged with the reason it was tried
- Reverted changes must be documented — they are as valuable as kept ones
- Original skill stays untouched — save improved version separately

**Gate:** 90%+ on checklist, 3 consecutive rounds

### Phase 4: Extract Rules from the Changelog

Turn optimization history into reusable knowledge.

1. Review the changelog from Phase 3
2. Identify patterns across kept changes — what types of additions consistently improved scores?
3. Identify patterns across reverted changes — what types consistently hurt?
4. Extract 5-10 universal rules from the patterns
5. Flag which rules are skill-specific vs. universally applicable
6. Build a personal prompt writing guide

**Rules:**
- Rules must come from evidence in the changelog — not general advice
- Every rule must have a specific example from the optimization history
- Skill-specific rules kept separate from universal rules

**Output:** Kept Change Patterns → Reverted Change Patterns → Universal Rules → Personal Prompt Guide

### Phase 5: Apply to Any Repeatable Task

The autoresearch loop isn't just for prompts — apply it to any repeatable task.

1. Ask the user for the repeatable task they want to optimize
2. Define what success looks like — extract measurable outcomes from vague goals
3. Build a 3-6 question yes/no scoring checklist specific to this task
4. Design the iteration loop — what changes, what gets tested, what gets scored
5. Run the first 3 rounds manually to establish the pattern
6. Document the system so it runs without involvement after setup

**Rules:**
- Task must be repeatable — one-off tasks cannot be autoresearched
- Scoring checklist must be consistent across every iteration
- Changes must be isolated — one variable at a time
- System must be documentable so anyone or any agent can run it

## Relationship to Other Skills

- **skill-creator**: Creates skills from scratch. Autoresearch IMPROVES existing skills/prompts.
- **qa-gate**: Tests individual outputs. Autoresearch optimizes the system that produces outputs.
- **error-memory**: Logs what went wrong. Autoresearch systematically prevents it from happening again.
