---
source: Instagram post by "AI With Anushka" (5 screenshots, shared by user); official docs at https://code.claude.com/docs/en/ultraplan
date_captured: 2026-04-09
tags: [claude-code, ultraplan, planning, research-preview, cli]
---

# Claude Code Ultraplan (research preview)

## Claim (from the screenshots)

- Claude Code has a new "Ultra Plan" feature that runs parallel research agents.
- Architecture: "3 explorer agents + 1 critic agent".
- Performance: "14 min vs 45 min" for producing a plan.
- Runs Opus 4.6, ~30 min cap.

## Verified (official docs — https://code.claude.com/docs/en/ultraplan)

- Feature name: **Ultraplan**. Status: **research preview**.
- Invocation: `/ultraplan <prompt>` or include the word "ultraplan" in a prompt.
- Requirements: Claude Code **≥ 2.1.91**, Claude Pro/Max subscription, a GitHub repo.
- Platforms: **CLI only**. Not available in Desktop app or VS Code extension.
- Purpose: cloud-based planning with autonomous exploration agents.

## NOT verified in official docs

- "3 explorer + 1 critic" architecture — appears only in secondary blogs.
- "14 min vs 45 min" and "30 min cap" performance numbers — secondary blogs.
- "Opus 4.6 specifically" — not in official docs.

Do not cite these secondary details as fact. Treat them as community folklore until Anthropic confirms.

## Relevance to my workflow

- Replaces the **Opus-plan / Sonnet-execute** loop for CLI sessions on complex multi-file tasks.
- Does NOT replace Desktop planning (feature unavailable there).
- Currently **unusable** on this machine: Claude Code 2.1.89 installed; Ultraplan needs 2.1.91+.
- After upgrading, the `using-ultraplan` skill suggests `/ultraplan` when all conditions are met.

## Risks / why it might not stick

- Research preview — Anthropic may rename, restructure, or pull the feature.
- CLI-only limits usefulness for Desktop-heavy workflow.
- Cloud execution means no local debugging if it misbehaves.
- Third-party blog hype exceeds what official docs actually promise.
