---
name: type-aware-rigor
description: Match brainstorming depth, QA tier, and planning granularity to the TYPE of work. Site updates get lite treatment, new builds and algorithms get deep treatment. Influences brainstorming, qa-gate, writing-plans, and deploy decisions. Always-on enhancement layer.
weight: passive
---

# Type-Aware Rigor — Match Depth to Work Type

## When This Fires

During brainstorming, planning, QA, or deployment decisions. This skill overrides default "size-based" heuristics with "type-based" ones across multiple downstream skills.

## Rigor Levels

| Project Type | Rigor | Brainstorm | QA Tier | Plan Detail | Deploy Gate |
|-------------|-------|------------|---------|-------------|-------------|
| **Site update** | Tight | Lite only | Tier 1 (spot-check) | Bullet list | Visual verify |
| **New feature** | Standard | Lite or Full | Tier 2 (functional) | Step-by-step | Baseline + verify |
| **New build** | Deep | Full mandatory | Tier 3 (comprehensive) | Detailed with alternatives | Full smoke test |
| **Algorithm/model** | Deep | Full mandatory | Tier 3 + data validation | Detailed + hypothesis | Backtest + verify |
| **Campaign/one-off** | Creative | Lite | Tier 1 (it works) | Minimal | Run once, confirm |

## How to Detect Type

Look at the user's request + project context:

- "Add dark mode" in an existing app → **Site update** (Tight)
- "Build a new prediction model" → **Algorithm** (Deep)
- "Create a new site for X" → **New build** (Deep)
- "Write a script to migrate the data" → **Campaign** (Creative)
- "Add a leaderboard feature" → **New feature** (Standard)

When ambiguous, default to **Standard**.

## Downstream Influence

### Brainstorming
- Tight/Creative → force Lite brainstorm regardless of file count
- Deep → force Full brainstorm regardless of apparent simplicity
- Standard → use brainstorming's existing complexity gate

### QA Gate (qa-gate skill)
- **Tier 1** (Tight/Creative): Does it work? Quick spot-check. No regression sweep.
- **Tier 2** (Standard): Functional test of the new feature + baseline verification of surrounding features. Check one happy path and one edge case.
- **Tier 3** (Deep): Full regression across all affected pages/components. Data validation. Visual comparison. Load the actual page and verify every element.

### Planning Depth (writing-plans skill)
- **Tight**: Bullet list of changes. No alternatives section. Skip dependency analysis.
- **Standard**: Step-by-step with file paths and commands. Brief consideration of alternatives.
- **Deep**: Detailed plan with alternatives analysis, risk assessment, rollback strategy, and explicit verification criteria for each step.
- **Creative**: Minimal plan — just enough to not lose track. Speed > thoroughness.

### Deploy Decisions (deploy skill)
- **Tight**: Deploy after visual verification of changed pages only.
- **Standard**: Deploy after baseline comparison of changed pages + spot-check of related pages.
- **Deep**: Full smoke test of all pages. Data consistency check. Version regression check. Canary period if available.
- **Creative**: Deploy and verify once. No canary needed for throwaway code.

## The Key Insight

The COST of getting it wrong scales with project type:

| Type | Cost of a Bug | Cost of Over-Planning |
|------|--------------|----------------------|
| Site update | Low (quick fix) | Medium (wasted time) |
| New feature | Medium (users affected) | Low (better safe) |
| New build | High (architecture debt) | Low (investment pays off) |
| Algorithm | Very high (weeks of bad data) | Very low (always worth it) |
| Campaign | Very low (throwaway code) | High (defeats the purpose) |

Match your effort to the cost of failure, not the size of the change.
