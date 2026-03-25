# Handoff — OctagonAI/UFC Algs — 2026-03-25 22:30
## Model: Claude Opus 4.6 (1M context)
## Previous handoff: handoff_20260325_2100.md

---

## 1. Session Summary
Multi-phase session that evolved from a routine handoff review into a major incident response and architectural overhaul. Discovered and fixed a catastrophic v10.68 production reversion, then built 5 prevention layers, a dedicated /mmalogic website agent, file freshness rules, and a /reorganize-ufc command to consolidate 5 duplicate UFC directories into one canonical location.

## 2. What Was Done (Completed Tasks)
### Phase 1: Incident Response (v10.68 Reversion)
- **Root cause analysis**: Prior session deployed from stale root `webapp/` (v10.68) instead of `ufc-predict/webapp/` (v11.9.3)
- **CI redeploy**: Triggered GitHub Actions → restored v11.9.3 from correct source
- **Frontend bug fixes** (via /tmp clone → pushed as v11.9.5):
  - FightCard.jsx: "260% conf" → "2.60 diff", R1 KO gating, CMB combo row
  - EventBetsDropdown.jsx: safePnl() computes missing P/L from odds (145 bouts fixed)
  - AdminAlgorithm.jsx: optimizer.current_values fallback, 2 new CATEGORIES
  - HeroStats.jsx: All bet types displayed correctly
- **Root webapp/ archived** → `archive/webapp_ROOT_STALE_v10.68/`
- **Verified live site**: v11.9.5 confirmed at mmalogic.com

### Phase 2: Prevention Layers (5 layers)
| Layer | File | What It Catches |
|-------|------|-----------------|
| CLAUDE.md Rule 21 | ~/.claude/CLAUDE.md | Any deploy without version check |
| /deploy Phase 0 | commands/deploy.md | Mandatory version verification before every deploy |
| site-update-protocol | skills/site-update-protocol/SKILL.md | "CANONICAL DIRECTORY" stop-gate |
| anti-patterns | anti-patterns.md | UFC_WRONG_DIRECTORY_DEPLOY entry |
| shared memory | memory/topics/ufc_canonical_paths.md | Lookup table for every UFC artifact path |

### Phase 3: File Freshness Rules (CLAUDE.md Rule 22)
- Every session touching iCloud files must check local mtime vs GitHub commit date
- If local is older → clone fresh from GitHub to /tmp/
- Never trust iCloud copies are current

### Phase 4: /mmalogic — Dedicated Website Agent (157 lines)
- Self-contained command at `~/.claude/commands/mmalogic.md`
- Loads 6 mandatory knowledge files on every invocation
- Freshness check → route task → execute → learn cycle
- CLAUDE.md Rule 23 ensures it's always invoked for any UFC website task
- Self-improving: updates anti-patterns, display rules, checklist after every task

### Phase 5: Directory Reorganization Prep
- Mapped 5 duplicate UFC directories (iCloud/UFC Algs/ufc-predict/, ~/Projects/ufc-predict-local/, iCloud/octagonai/, iCloud/UFC App 3.0/, GitHub main)
- Created `/reorganize-ufc` command (126 lines) — ready to execute when active sessions close
- Plan: Fresh clone to `~/Projects/ufc-predict/` (NOT iCloud), archive all stale directories
- Updated canonical paths memory to reference post-reorg location
- **NOT YET EXECUTED** — 2 active Claude sessions in UFC Algs/ must close first

## 3. What Failed (And Why)
- **v10.68 production reversion**: Prior session deployed from wrong directory. Root cause: 5 duplicate UFC directories, no version check in deploy pipeline. Now prevented by 5 layers.
- **Initial screenshot review missed 11 bugs**: Agent said "no obvious bugs" while 260% confidence, missing combos, broken P/L were visible. Created 15-point mandatory checklist.

## 4. What Worked Well
- **GitHub CI as single deployment path**: `gh workflow run` cleanly restored correct version
- **/tmp clone workflow**: Reliable for git ops, avoids iCloud issues
- **Layered prevention**: 5 independent layers means no single point of failure
- **/mmalogic agent architecture**: Self-improving loop with mandatory knowledge loading

## 5. What The User Wants (Goals & Priorities)
- **#1**: Consolidate all UFC directories into ONE canonical location (~/Projects/ufc-predict/)
- **#2**: Dedicated /mmalogic agent that carries all domain knowledge and grows over time
- **#3**: File freshness checks — never work from stale files again
- **Standing**: Website correctness, proper deploys, commit all local changes

### User Quotes (Verbatim)
- "I think one reason we keep getting errors is handoff between sessions when i open a new session from a different local folder or icloud folder that isn't synced with github" — context: identifying root cause of cross-session confusion
- "Maybe what we need is a custom agent to handle the mmalogic.com website ONLY, with all the knowledge and memory" — context: requesting dedicated agent architecture
- "Can it be done without ruining local sessions but permanently reorganizing and categorizing everything so that it can never be lost again" — context: directory consolidation safety

## 6. What's In Progress (Unfinished Work)
- **`/reorganize-ufc` execution**: Command is built and ready. Waiting for user to close 2 active Claude sessions (PIDs 81638, 83363) in UFC Algs/. Once closed, run `/reorganize-ufc` to consolidate.
- **Git commit of local changes**: 635 uncommitted files in iCloud working tree. Will be resolved by /reorganize-ufc (fresh clone from GitHub becomes canonical).
- **2nd parlay (High ROI)**: Algorithm only generates 1 parlay per event
- **Backtester prop P/L population**: 145 bouts have null pnl with valid odds
- **AGENTS.md update**: Stale, references pre-v11.9 state

## 7. Blocked / Waiting On
- **Directory reorganization**: 2 active Claude sessions must close before /reorganize-ufc can run safely
- **Firestore sync**: May still serve stale data. Needs firestore_upload.py after reorg

## 8. Next Steps (Prioritized)
1. **Run `/reorganize-ufc`** — close active sessions, execute command, verify fresh clone at ~/Projects/ufc-predict/
2. **Open future UFC sessions from ~/Projects/ufc-predict/** — not iCloud
3. **Fix backtester prop P/L** — ensure future runs write complete bout data
4. **Fix 2nd parlay generation** — investigate algorithm parlay logic
5. **Update Firestore** — run firestore_upload.py
6. **Update AGENTS.md** — rewrite to match current v11.9.5 state

## 9. Agent Observations

### Recommendations
- **Execute /reorganize-ufc ASAP** — every session that opens from iCloud risks working with stale files. The reorg eliminates this entire class of bugs.
- **Consider moving ALL project repos out of iCloud** — not just UFC. iCloud + git is fundamentally broken for collaborative/AI workflows.
- **The /mmalogic agent should be tested** — run it on a real task to verify the knowledge loading and freshness check work correctly.

### Patterns & Insights
- The v10.68 disaster was caused by a chain: stale directory → no version check → wrong deploy → production regression. Five independent prevention layers now break this chain at every link.
- The user's insight about cross-session confusion from stale files was exactly right — this is the root cause of multiple prior bugs, not just the deploy issue.
- The /mmalogic agent architecture (load knowledge → freshness check → route → execute → learn) is a template that could be applied to other projects.

### Where I Fell Short
- Should have caught the stale directory problem at session start (orientation rule exists but wasn't followed rigorously)
- Earlier handoff (18:30) didn't detect the v10.68 regression that was already live

## 10. Miscommunications to Address
None — user and agent were aligned throughout. User identified the root causes correctly and agent built the requested solutions.

## 11. Files Changed This Session

**On GitHub ufc-predict (via /tmp clone — v11.9.5):**
| File | Action | Description |
|------|--------|-------------|
| webapp/frontend/src/components/picks/FightCard.jsx | modified | R1 KO gating, combo row, "2.60 diff" confidence |
| webapp/frontend/src/components/shared/EventBetsDropdown.jsx | modified | safePnl odds-based computation |
| webapp/frontend/src/components/admin/AdminAlgorithm.jsx | modified | current_values fallback, 2 new CATEGORIES |
| webapp/frontend/src/components/landing/HeroStats.jsx | modified | All bet types display |
| webapp/frontend/src/config/version.js | modified | v11.9.3 → v11.9.5 |

**Locally (iCloud + ~/.claude/):**
| File | Action | Description |
|------|--------|-------------|
| webapp/ → archive/webapp_ROOT_STALE_v10.68/ | moved | Archived stale root webapp |
| HANDOFF.md | created | This handoff document |
| ~/.claude/commands/mmalogic.md | created | Dedicated MMALogic website agent (157 lines) |
| ~/.claude/commands/reorganize-ufc.md | created | One-time directory consolidation command (126 lines) |
| ~/.claude/memory/topics/ufc_canonical_paths.md | created | Canonical path lookup for all UFC artifacts |
| ~/.claude/CLAUDE.md | modified | Rules 21 (deploy version check), 22 (file freshness), 23 (/mmalogic routing) |
| ~/.claude/commands/deploy.md | modified | Phase 0 version verification |
| ~/.claude/skills/site-update-protocol/SKILL.md | modified | CANONICAL DIRECTORY stop-gate |
| ~/.claude/anti-patterns.md | modified | 5+ new entries |
| ~/.claude/recurring-bugs.md | modified | 2 new entries |
| ~/.claude/memory/topics/ufc_website_maintenance_rules.md | created | 15-point checklist + 19 display rules |

## 12. Current State
- **Branch (iCloud root)**: fix/method-scoring-v10.69
- **Last commit (iCloud root)**: f36fcc3 — "v10.69: Fix method bet scoring"
- **GitHub ufc-predict main**: bd49a0c (v11.9.5) — **canonical source of truth**
- **Local ufc-predict/ (iCloud)**: 00bd73f (v11.9.2) — **101 commits behind, will be archived by /reorganize-ufc**
- **Deploy status**: v11.9.5 LIVE on mmalogic.com via Cloudflare Pages
- **Uncommitted local changes**: ~635 files (will be moot after /reorganize-ufc — fresh clone replaces)

## 13. Environment State
- **Node.js**: v25.6.1
- **Python**: 3.14.3
- **Running dev servers**: None for UFC (other projects have Next.js, Vite running)
- **Environment variables set this session**: none
- **Active MCP connections**: Claude in Chrome, Desktop Commander, PDF Tools, mcp-registry

## 14. Session Metrics
- **Duration**: ~4 hours total (handoff review → incident response → prevention → agent build → reorg prep)
- **Tasks completed**: 15+ / 15+ attempted
- **User corrections**: 1 (user discovered v10.68 regression)
- **Tool calls**: ~80+
- **Skills/commands invoked**: /full-handoff (3x)
- **Commits made**: 1 to GitHub ufc-predict (v11.9.5), 3 to GitHub superpowers (handoff syncs)

## 15. Memory & Anti-Patterns Updated
- **anti-patterns.md**: 5+ new entries (WRONG_DIRECTORY_DEPLOY, SCREENSHOT_REVIEW, R1_KO_GATING, CONFIDENCE_260, EVENTBETS_NULL_PNL, OPTIMIZER_MISSING_CURRENT)
- **recurring-bugs.md**: 2 new entries (deploy source directory, screenshot review carelessness)
- **ufc_website_maintenance_rules.md**: Created — 15-point checklist + 19 display rules
- **ufc_canonical_paths.md**: Created — lookup table for all UFC artifact locations
- **CLAUDE.md**: Rules 21-23 added (deploy check, file freshness, /mmalogic routing)
- **deploy command**: Phase 0 version verification added
- **site-update-protocol**: CANONICAL DIRECTORY stop-gate added

## 16. Skills & Agents Used
| Skill/Agent | How It Was Used | Was It Helpful? |
|-------------|----------------|-----------------|
| /full-handoff | Generated handoff documents (3x this session) | Yes |
| Claude in Chrome | Verified live site post-deploy | Yes |
| GitHub CLI (gh) | Triggered CI workflow, checked run status | Yes |
| /mmalogic | Created (not yet invoked for a real task) | N/A — test on next UFC task |
| /reorganize-ufc | Created (not yet executed — waiting for session close) | N/A |

## 17. For The Next Agent — Read These First
1. **This HANDOFF.md**
2. `~/.claude/memory/topics/ufc_canonical_paths.md` — where everything lives (or will live after reorg)
3. `~/.claude/memory/topics/ufc_website_maintenance_rules.md` — **MANDATORY** before screenshots
4. `~/.claude/memory/topics/ufc_betting_model_spec.md` — canonical betting rules
5. `~/.claude/anti-patterns.md` — 5+ new entries, especially WRONG_DIRECTORY_DEPLOY
6. `~/.claude/recurring-bugs.md`
7. `~/.claude/commands/mmalogic.md` — dedicated website agent (use for ALL UFC website tasks)
8. `~/.claude/commands/reorganize-ufc.md` — **RUN THIS FIRST** if not yet executed

### CRITICAL ACTIONS FOR NEXT SESSION
1. **Check if /reorganize-ufc has been run** — if not, run it first (close any active UFC sessions)
2. **After reorg, open from ~/Projects/ufc-predict/** — NOT iCloud
3. **For any website task, use /mmalogic** — it loads all domain knowledge automatically
4. **Never deploy without checking version.js** — Rule 21

### Verified P/L (Live Site — v11.9.5, 2026-03-25)
| Bet Type | W-L | P/L |
|----------|-----|-----|
| ML | 303W-113L | +83.01u |
| Method | 148W-185L | +79.45u |
| Round | 29W-49L | +17.36u |
| Combo | 25W-53L | +72.96u |
| Parlay | 32W-32L | +28.93u |
| **Combined** | **969 bets** | **+281.71u (29.1% ROI)** |
