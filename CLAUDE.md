# Claude Code Settings

## Project Context

Primary languages: Python and JavaScript/TypeScript. Active projects include:
- **Sports prediction algorithms**: UFC (mmalogic), MLB+NHL (diamondpredictions), NBA+NCAA (courtside-ai) — Python, walk-forward backtesting, Firestore, Cloudflare
- **MyStrainAI**: Cannabis strain recommendation SaaS — React/Vite frontend, Python backend, Cloudflare Workers, Supabase
- **Enhanced Health AI**: Next.js 15 health tech app — TypeScript, Prisma, Cloudflare Workers
- **NestWise HQ**: Next.js fullstack family finance — TypeScript, Prisma, Cloudflare, Tailwind
- **Research Aria**: AI research platform — Cloudflare Workers, D1

Always commit working checkpoints before attempting optimizations.

## Multi-Project Context Switching

When switching projects: (1) drop all assumptions from the previous project, (2) read the project's CLAUDE.md and memory, (3) verify tech stack, (4) check git status, (5) don't cross-contaminate data between sports projects.

## Core Development Rules

- Stream long-running scripts to stdout + log file (`| tee output.log`)
- Verify background tasks started and producing output within 30 seconds
- Break work into committable chunks — only 21% of multi-task sessions complete fully
- Try the simplest fix first — a 5-line fix beats a 200-line refactor
- For iCloud dirs, clone to `/tmp/` for git operations

## Backtest Rules

- **UFC**: 70+ events (growing). **NHL, MLB, NBA, CBB**: 3 seasons minimum.
- **Walk-forward ONLY** — no post-event data leakage. Point-in-time stats only. 80%+ accuracy on sports = suspect data leakage.
- **Cache all scraped data** — commit caches to GitHub. Never re-scrape existing data.

## Destructive Write Protection

Before overwriting ANY external store: (1) check existing size FIRST, (2) size regression = ABORT, (3) backup before overwrite, (4) merge don't replace, (5) post-write verify counts match. Schema changes need user approval. **Prop odds cache is IRREPLACEABLE** — never trust fresh scrape over cached historical data.

## Sports Betting Payout Rules

Wins pay at REAL ODDS (positive: `stake × odds/100`, negative: `stake × 100/|odds|`). Losses = -1u always. Missing odds = RUN THE SCRAPER. Fighter loss = ALL prop bets lose (-1u each). **Full spec:** `~/.claude/memory/topics/ufc_betting_model_spec.md`

## Data Invariants

Profit > 0 requires Wins > 0. W+L = total bets. 0W-0L with non-zero P/L = bug. 100% win rate = data leakage. **These are enforced by `impossible-stats-detector.py` hook.**

## File Archival

Never delete — always archive. STALE = explicitly replaced. Difference ≠ staleness. When in doubt, ask the user.

## Memory

Two systems: (1) Hierarchical (`~/.claude/memory/`) — me.md, core.md, topics/, projects/. (2) Project-scoped (`~/.claude/projects/.../memory/`).

## Project Structure

All projects at `~/Projects/<name>/` (flat, no categories). `~/Projects/` symlinks to iCloud `ProjectsHQ/`. GitHub is source of truth. See `~/Projects/site-to-repo-map.json` for live site → repo mapping.

## Live Site → Repo Mapping

| Live Site | GitHub Repo | Local Path |
|-----------|-------------|------------|
| mmalogic.com | ufc-predict | ~/Projects/mmalogic |
| diamondpredictions.com | diamond-predictions | ~/Projects/diamondpredictions |
| mystrainai.com | Strain-Finder-Front-Cannalchemy-Back | ~/Projects/mystrainai |
| enhancedhealthai.com | enhanced-health-ai | ~/Projects/enhancedhealthai |
| nestwisehq.com | dad-financial-planner | ~/Projects/nestwisehq |
| researcharia.com | aria-research | ~/Projects/researcharia |
| courtside-ai.pages.dev | courtside-ai | ~/Projects/courtside-ai |

## Session Start: 3-Gate Verification

**All 3 gates must pass before starting work.** Details in `/review-handoff` command.
- **GATE 1**: Correct repo (trace from site-to-repo-map.json, verify git remote)
- **GATE 2**: Local matches remote (`git fetch && compare SHAs`, pull if behind)
- **GATE 3**: Read context (project CLAUDE.md, MEMORY.md, HANDOFF.md, anti-patterns.md)

## Failsafes (enforced by hooks + manual checks)

| # | Failsafe | Enforced By |
|---|----------|-------------|
| 1 | Git freshness — pull before editing | Gate 2 |
| 2 | Archived directory detection | Gate 1 |
| 3 | Version regression detection | `version-bump-check.py` hook |
| 4 | File date comparison (newest wins) | Manual |
| 5 | Commit before deploy | `deploy-guard.py` hook |
| 6 | Live site → repo tracing | site-to-repo-map.json |
| 7 | Check dates before decisions | Manual |
| 8 | Local matches GitHub before editing | Gate 2 |
| 9 | Check Cloudflare before deploying | `deploy-guard.py` hook |

**Cloudflare deploys are IRREVERSIBLE** — KV assets purged on every deploy. No rollback for asset deletion.

## Background Task Notifications

Batch stale task completions into ONE message. Don't repeat results. 1 line max per stale task.

## Bug Recording

Every bug fix → record in `~/.claude/anti-patterns.md`. Check anti-patterns BEFORE attempting any fix. Commit to GitHub. **Enforced by `error-memory` skill + `correction-detector.py` hook.**

## Communication Rules

Lead with user impact. Use tables for comparisons. Flag risks on their own line. One-line status for routine work.

## Behavioral Rules

1. **Search before coding** — check if a solution already exists
2. **Think before acting** — plan first on complex tasks
3. **Verify before claiming done** — run tests/builds
4. **Save learnings** — persist to memory when reusable
5. **Do it yourself** — never tell user to do something manually if tools can do it
6. **Simplest fix first** — 5-line fix before 200-line refactor
7. **Commit between tasks** — rate limits kill 79% of multi-task sessions
8. **Use commands when they exist** — site-specific commands MUST be used:
   `/mmalogic`, `/update-diamond`, `/update-courtside`, `/update-mystrainai`, `/update-enhancedhealth`, `/update-researcharia`, `/update-nestwisehq`
9. **Handoff = /full-handoff always**
10. **Read before running scripts** — check for cache/fast/dry-run flags first
11. **Never poll background tasks** — use `run_in_background` or long timeout
12. **Read the spec, not the code** — for domain questions, read the spec file first
13. **Never flip-flop** — read spec before changing your answer. Getting it wrong once is normal. Changing 4 times without checking the source is a system failure.
14. **Never propose code changes to fix a misunderstanding** — read spec first, ask user to confirm
15. **Extreme results = bug in your analysis** — 0%/100% rates, profit with 0 wins = your query is wrong. **Enforced by `impossible-stats-detector.py` hook.**
16. **Validate on known data before concluding** — spot-check 1-2 events manually
17. **Scan output for impossible data** — duplicates, >100%, negative counts = fix before presenting
18. **Never delete commands, skills, or hooks without user confirmation** — archive instead
    **PROTECTED SKILLS (aitmpl.com — NEVER modify):** `frontend-design`, `code-reviewer`, `senior-architect`, `senior-backend`, `senior-frontend`, `skill-creator`, `ui-design-system`, `ui-ux-pro-max`, `webapp-testing`, `senior-prompt-engineer`, `brainstorming`. **Enforced by `protect-skills.py` hook.**
19. **Never end a turn with only narration** — always include tool calls
20. **Verify deploy directory** — check version matches expected. **Enforced by `version-bump-check.py` hook.**
21. **SURGICAL SCOPE** — only touch files directly related to your task. **Enforced by `surgical-scope.py` hook.**
22. **NEVER disconnect working integrations** — preserve API calls, webhooks, GitHub Actions triggers
23. **NEVER rename directories with active sessions** — kills all sessions. **Enforced by `block-dangerous-commands.py` hook.**
24. **Max 2 subagents, Opus only** — separate output files, sequential parameter sweeps. **Enforced by `agent-limit.py` hook.**
25. **User correction = MANDATORY triple-write** — project memory + anti-patterns + GitHub superpowers. **Enforced by `correction-detector.py` hook.**

@RTK.md

## API Routing Banner
Session start: 🟢 Z AI (GLM-5) if haiku, 🔵 Anthropic if opus/sonnet.

## Post-Change Report (MANDATORY)

After ANY code change, DO all steps then end with:

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

Use ❌ with explanation for any step NOT done. Every ✅ is a sworn truthful confirmation. **Version bump enforced by `version-bump-check.py` hook.**

**Non-website projects:**
```
---
DONE: [summary]
✅ GitHub synced: committed and pushed (commit [SHA])
Version: N/A — [reason]
Deployed: N/A — not a website
Notes: [or "None"]
```

## Superpowers Repo Sync

After modifying `~/.claude/skills/`, `CLAUDE.md`, `hooks/`, `commands/`, or `anti-patterns.md`: clone to `/tmp/superpowers-sync`, copy files, commit, push to GitHub (`nhouseholder/nicks-claude-code-superpowers`), clean up.
