---
name: type-aware-rigor
description: Match brainstorming and planning depth to the TYPE of work — site updates get lite treatment, new builds and algorithms get deep treatment. Enhancement layer for brainstorming skill.
weight: passive
---

# Type-Aware Rigor — Match Depth to Work Type

## When This Fires

During brainstorming or planning, before deciding between Lite and Full brainstorm. This skill overrides the default "size-based" heuristic with a "type-based" one.

## Rigor Levels

| Project Type | Rigor | Brainstorm Depth | Examples |
|-------------|-------|-----------------|----------|
| **Site update** | Tight | Lite brainstorm only. Confirm approach, execute. Don't over-discuss cosmetic changes. | Content swap, styling tweak, minor feature add, dependency bump |
| **New feature** | Standard | Lite or Full depending on ambiguity. Focus on integration with existing code. | Add dark mode, new API endpoint, dashboard widget |
| **New build** | Deep | Full brainstorm mandatory. Architecture decisions are expensive to reverse. | Greenfield app, new service, new site from scratch |
| **Algorithm/model** | Deep | Full brainstorm mandatory. Wrong approach = weeks of wasted backtesting. | Scoring model, prediction pipeline, data processing overhaul |
| **Campaign/one-off** | Creative | Lite brainstorm. Optimize for speed, not longevity — this code won't live long. | Migration scripts, one-time audits, data backfills, throwaway tools |

## How to Detect Type

Look at the user's request + the project context:

- "Add dark mode" in an existing app → **Site update** (Tight)
- "Build a new prediction model" → **Algorithm** (Deep)
- "Create a new site for X" → **New build** (Deep)
- "Write a script to migrate the data" → **Campaign** (Creative)
- "Add a leaderboard feature" → **New feature** (Standard)

When ambiguous, default to **Standard**.

## Integration

This skill informs brainstorming's Lite vs Full decision. When brainstorming fires:

1. Identify the project type from the table above
2. Apply the corresponding rigor level
3. If rigor = Tight or Creative → force Lite brainstorm regardless of file count
4. If rigor = Deep → force Full brainstorm regardless of apparent simplicity
5. If rigor = Standard → use brainstorming's existing complexity gate
