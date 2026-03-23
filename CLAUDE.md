# Superpowers — Claude Code Skills Repository

All universal rules (backtesting, walk-forward, caching, debugging, memory, behavioral rules) are in `~/.claude/CLAUDE.md`. Do NOT duplicate them here.

## This Project

This repo contains the custom skills system installed at `~/.claude/skills/`. It syncs to GitHub at `nhouseholder/nicks-claude-code-superpowers`.

## Skill Management Rules

- **Stack cap: 75 skills maximum.** Adding past 75 requires merging or removing an existing one.
- **Three-location sync:** Edit in `~/.claude/skills/` (live) → clone to `/tmp/` → push to GitHub. Never git push from iCloud.
- **Weight classes:** Passive (unlimited), Light (max 5/msg), Heavy (max 2/msg). See skill-manager for classifications.
- **No skill is sacred.** If a skill consistently makes output worse, remove it.
- **Merge before adding.** Before creating a new skill, check if an existing skill can absorb the behavior.
