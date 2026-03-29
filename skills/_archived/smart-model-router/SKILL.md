---
name: smart-model-router
description: Classifies each prompt as Sonnet-tier, Opus-tier, or Opus-1M-tier based on task complexity and context requirements. Injects model recommendation when current model is mismatched. Passive skill with near-zero overhead — only fires a visible recommendation when a mismatch is detected.
weight: passive
---

# Smart Model Router — Right Model for the Job

## How It Works

The `smart-model-router.py` hook (UserPromptSubmit) classifies each prompt and recommends a model tier. If the current model matches, nothing happens (zero overhead). If mismatched, it injects a recommendation.

## Classification Tiers

### Sonnet Tier (fast, cheap — ~5% of prompts)
Simple tasks where Opus is overkill:
- Single-file formatting, renaming, or trivial edits
- "What does X do?" questions about visible code
- Running a command and reporting output
- Git status, git log, simple git operations
- Reading/summarizing a file
- Answering factual questions about the codebase

**Signals:** Short prompt (<50 words), no multi-step reasoning, no domain expertise, no creative work, single tool call expected.

### Opus Tier (standard — ~85% of prompts)
Most development work:
- Multi-file changes, feature implementation
- Debugging, architecture decisions
- Code review, refactoring
- Planning, spec writing
- Any domain-specific logic (betting, finance, etc.)
- Creative design work
- Multi-step tasks

**Signals:** Requires reasoning, judgment, or multi-step execution.

### Opus 1M Tier (extended context — ~10% of prompts)
Tasks requiring massive context:
- Full codebase audits (`/site-review`, `/site-audit`, `/audit`)
- Reviewing 10+ files simultaneously
- Large refactors spanning many files
- Comparing entire codebases or large diffs
- `/site-redesign` (multi-phase agent pipeline)
- Understanding complex data flows across many modules
- Sessions that have been running long and context is filling up

**Signals:** Task explicitly involves "all files", "entire codebase", "full audit", or references 10+ files. Also triggered when the conversation has been running long and nearing context limits.

## Model IDs

| Tier | Model Picker | Model ID |
|---|---|---|
| Sonnet | Sonnet 4.6 | `claude-sonnet-4-6` |
| Opus | Opus 4.6 | `claude-opus-4-6` |
| Opus 1M | Opus 4.6 (1M) | `claude-opus-4-6` with extended context |

## Recommendation Behavior

- **Current = Opus, Task = Sonnet:** "This is a simple task — Sonnet would handle it faster. Switch via model picker if you want to save tokens."
- **Current = Sonnet, Task = Opus:** "This task needs Opus-level reasoning. Switch to Opus via model picker."
- **Current = Opus, Task = 1M:** "This task involves large context — consider switching to Opus 1M via model picker for full codebase visibility."
- **Match:** Silent. No recommendation injected.

## Important Limitations

- Hooks cannot programmatically switch models — the user must use the model picker
- The recommendation is injected as `additionalContext` on `UserPromptSubmit`
- Classification is heuristic — when uncertain, defaults to current model (no recommendation)
- Never recommends downgrading mid-task (only at task boundaries)
