# Claude Code Settings

@personality.md

## Projects

Python + JS/TS. All projects at `~/Projects/<name>/` (flat). `~/Projects/` symlinks to iCloud `ProjectsHQ/`. GitHub is source of truth. For iCloud dirs, clone to `/tmp/` for git ops.

| Live Site | GitHub Repo | Local Path |
|-----------|-------------|------------|
| mmalogic.com | ufc-predict | ~/Projects/mmalogic |
| diamondpredictions.com | diamond-predictions | ~/Projects/diamondpredictions |
| mystrainai.com | Strain-Finder-Front-Cannalchemy-Back | ~/Projects/mystrainai |
| enhancedhealthai.com | enhanced-health-ai | ~/Projects/enhancedhealthai |
| nestwisehq.com | dad-financial-planner | ~/Projects/nestwisehq |
| courtside-ai.pages.dev | courtside-ai | ~/Projects/courtside-ai |
| researcharia.com | aria-research | ~/Projects/researcharia |

When switching projects: drop all assumptions, read project CLAUDE.md + memory, verify tech stack + git status.

## Session Start: 3-Gate Verification

**All 3 gates must pass before starting work.** Details in `/review-handoff`.
- **GATE 1**: Correct repo (trace from site-to-repo-map.json, verify git remote)
- **GATE 2**: Local matches remote (`git fetch && compare SHAs`, pull if behind)
- **GATE 3**: Read context (project CLAUDE.md, MEMORY.md, HANDOFF.md, anti-patterns.md)

## Rules (non-hook-enforced — these need YOUR attention)

1. **Commit AND push between tasks** — rate limits kill 79% of multi-task sessions. GitHub is the source of truth, not iCloud. Every commit must be pushed.
2. **GitHub-first for git ops** — iCloud corrupts `.git/objects/` on active repos. For any git-heavy work, clone from GitHub to `/tmp/`, do the work there, push, then let iCloud sync passively. Never trust iCloud git state over GitHub.
3. **Use site commands** — `/mmalogic`, `/update-diamond`, `/update-courtside`, `/update-mystrainai`, `/update-enhancedhealth`, `/update-researcharia`, `/update-nestwisehq`
4. **Handoff = /full-handoff always**
5. **Read the spec, not the code** — for domain questions, read the spec file first
6. **Never flip-flop** — read spec before changing your answer
7. **Do it yourself** — never tell user to do something manually if tools can do it
8. **Never delete** — always archive. When in doubt, ask.
9. **NEVER disconnect working integrations** — preserve API calls, webhooks, GitHub Actions triggers
10. **Simplest fix first** — 5-line fix beats 200-line refactor
11. **Stream long-running scripts** — `| tee output.log`
12. **Never poll background tasks** — use `run_in_background` or long timeout

## Hooks Handle These (don't duplicate in context — they fire mechanically)

`impossible-stats-detector.py`, `missing-odds-detector.py`, `surgical-scope.py`, `protect-skills.py`, `agent-limit.py`, `correction-detector.py`, `no-narration-stops.py`, `version-bump-check.py`, `block-dangerous-commands.py`, `deploy-guard.py`, `ufc-context-loader.py`, `memory-migrator.py`, `session-context-loader.py`, `observe.py`, `unpushed-commits-check.py`

## Scheduled Agents (run autonomously — don't duplicate)

- **nightly-memory-consolidation** (3am daily) — prune, dedup, promote observations to memory
- **research-scout** (4am Mon/Wed/Fri) — find new tools/updates, stage in `~/.claude/memory/new-learnings.md`

## Backtest Rules

Walk-forward ONLY. No post-event data leakage. 80%+ accuracy = suspect. Cache all scraped data — commit to GitHub. UFC: 70+ events. NHL/MLB/NBA/CBB: 3 seasons minimum.

## Destructive Write Protection

Before overwriting ANY external store: (1) check existing size, (2) size regression = ABORT, (3) backup first, (4) merge don't replace, (5) post-write verify. **Cloudflare deploys are IRREVERSIBLE** — KV assets purged on every deploy.

## Bug Recording

Every bug fix → `~/.claude/anti-patterns.md`. Check anti-patterns BEFORE attempting any fix. Commit to GitHub.

## Memory

Two systems: (1) Hierarchical (`~/.claude/memory/`), (2) Project-scoped (`~/.claude/projects/.../memory/`).

## Communication

Lead with user impact. Tables for comparisons. One-line status for routine work. Batch stale task notifications into ONE message.

@RTK.md

## Post-Change Report (MANDATORY)

**Website projects:**
```
---
DONE: [1-2 sentence summary]
✅ Version bumped: v[old] → v[new] in [file]
✅ GitHub synced: committed and pushed (commit [SHA])
✅ Deployed: pushed to Cloudflare via [method]
✅ Now live: verified at [URL]
Notes: [or "None"]
```

**Non-website projects:**
```
---
DONE: [summary]
✅ GitHub synced: committed and pushed (commit [SHA])
Version: N/A — [reason]
Deployed: N/A — not a website
Notes: [or "None"]
```

Use ❌ with explanation for any step NOT done. Every ✅ is a sworn truthful confirmation.

## Superpowers Repo Sync

After modifying `~/.claude/skills/`, `CLAUDE.md`, `hooks/`, `commands/`, or `anti-patterns.md`: clone to `/tmp/superpowers-sync`, copy files, commit, push to GitHub (`nhouseholder/nicks-claude-code-superpowers`), clean up.
