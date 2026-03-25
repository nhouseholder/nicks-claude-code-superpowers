# Handoff — OctagonAI/UFC Algs — 2026-03-25 21:00
## Model: Claude Opus 4.6 (1M context)
## Previous handoff: handoff_20260325_1830.md

---

## 1. Session Summary
Started as a handoff review, then discovered a **catastrophic production regression**: the live site had been reverted from v11.9.3 → v10.68 because a prior session deployed from the wrong directory (root `webapp/` instead of `ufc-predict/webapp/`). Fixed the regression, deployed v11.9.5 with all frontend bug fixes, archived the stale root webapp/, and logged anti-patterns to prevent recurrence.

## 2. What Was Done (Completed Tasks)
- **Root cause analysis**: Identified dual webapp/ directory as the cause of v10.68 reversion
- **CI redeploy**: Triggered GitHub Actions to restore v11.9.3 from correct `ufc-predict/webapp/frontend/`
- **Archived stale root webapp/**: Moved to `archive/webapp_ROOT_STALE_v10.68/` — can never accidentally deploy again
- **FightCard.jsx fixes** (in /tmp clone → pushed to GH):
  - Confidence: "260% conf" → "2.60 diff" with "score differential" label
  - R1 KO gating: round/combo bets only when method=KO && round=1
  - Added CMB (combo) row on fight cards
- **EventBetsDropdown.jsx fixes**: safePnl() computes missing P/L from odds (fixes 145 bouts with null pnl)
- **AdminAlgorithm.jsx fixes**: optimizer.current_values fallback for Current column, 2 new CATEGORIES
- **HeroStats.jsx fixes**: Shows all bet types correctly
- **Version bumped to v11.9.5**: Pushed commit 48e2f50, CI auto-deployed
- **Anti-patterns logged**: 5 new entries (WRONG_DIRECTORY_DEPLOY, SCREENSHOT_REVIEW, R1_KO_GATING, CONFIDENCE_260, EVENTBETS_NULL_PNL, OPTIMIZER_MISSING_CURRENT)
- **Recurring-bugs.md updated**: 2 new entries (deploy source, screenshot carelessness)
- **Deploy skill updated**: Added Step 0 — verify version.js before building
- **Created ufc_website_maintenance_rules.md**: 15-point checklist + 19 display rules
- **Verified live site**: Screenshot confirmed v11.9.5 live with +281.71u, 71 events, all 4 cards

## 3. What Failed (And Why)
- **A prior session deployed from wrong directory**: Root `webapp/` (v10.68) was deployed instead of `ufc-predict/webapp/` (v11.9.3). The AI assumed the nearest `webapp/` was correct without checking version.js. **Root cause**: Two webapp/ directories exist in the project — this is now prevented by archiving the stale one.
- **Initial screenshot review missed 11 bugs**: Agent said "no obvious bugs" while 260% confidence, missing combos, broken prop P/L, empty optimizer values, wrong event count (25 vs 71) were all visible. **Root cause**: Glancing instead of checking against the 15-point checklist. Now mandatory.

## 4. What Worked Well
- **GitHub CI as single deployment path**: Once we established that CI deploys from `ufc-predict/`, triggering a workflow run was the cleanest fix
- **Working in /tmp clone for git ops**: Sidestepped iCloud git issues completely
- **safePnl frontend safety net**: Computes missing P/L from odds without needing a full backtest re-run
- **Structured bug catalog before coding**: Listed all bugs with rule violations before touching code

## 5. What The User Wants (Goals & Priorities)
- **Primary**: Website must correctly display ALL betting data per the 12+ immutable rules
- **#1 frustration**: Claude deploying from wrong directory, reverting production. NEVER deploy without checking version.js first
- **#2 frustration**: Careless screenshot reviews — must use 15-point checklist every time
- **Standing goals**: Commit all local changes, fix backtester prop P/L, fix 2nd parlay generation

### User Quotes (Verbatim)
- "why did the site get its version number reverted to 10.68? and many fixes were reverted from the home page? what happened?" — context: discovered the v10.68 regression
- "proceed with fix and prevention" — context: after root cause was presented
- "continue the fix" — context: after CI redeploy restored v11.9.3, wanted frontend bug fixes too

## 6. What's In Progress (Unfinished Work)
- **Git commit of local changes**: 635 uncommitted files in iCloud working directory. Must clone to /tmp to commit. This is CRITICAL — multiple sessions of work are at risk.
- **Local ufc-predict/ is behind GitHub**: Local shows v11.9.2, GitHub has v11.9.5 (from /tmp clone push). Need to pull latest in `ufc-predict/`.
- **2nd parlay (High ROI)**: Algorithm only generates 1 parlay. Needs investigation in prediction mode parlay section.
- **Backtester prop P/L population**: 145 bouts have null pnl with valid odds. Frontend safety net handles display but backtester should write complete data.

## 7. Blocked / Waiting On
- **Git push from iCloud**: Direct git operations fail in iCloud Drive. Must clone to /tmp first. This has been the case for multiple sessions and continues to block proper git workflow.
- **Firestore sync**: May still serve stale data. Needs firestore_upload.py run after git commit.

## 8. Next Steps (Prioritized)
1. **Commit all local changes to git** — clone to /tmp, structured multi-commit push. 635 files uncommitted. This is overdue by multiple sessions.
2. **Pull latest into local ufc-predict/** — local is v11.9.2, remote is v11.9.5
3. **Fix backtester prop P/L** — ensure future runs write complete bout records
4. **Fix 2nd parlay generation** — investigate algorithm parlay logic for high-ROI parlay
5. **Update Firestore** — run firestore_upload.py
6. **Update AGENTS.md** — stale, references pre-v11.9 state

## 9. Agent Observations

### Recommendations
- **Eliminate dual webapp/ permanently**: The root `webapp/` is now archived, but `ufc-predict/webapp/` data files are sometimes synced TO the root. This sync pattern should be abolished — all reads and deploys from `ufc-predict/webapp/` only.
- **Git commit is critically overdue**: 635 uncommitted files spanning multiple sessions. Every session adds more risk. Next session's #1 priority.
- **Consider moving project out of iCloud**: The iCloud git friction has cost multiple sessions of time. A symlink or dedicated git repo in `~/Projects/` would eliminate the clone-to-/tmp workaround.

### Patterns & Insights
- The /tmp clone workflow works reliably for pushes but creates local/remote divergence (v11.9.2 local vs v11.9.5 remote)
- Deploy skill now has Step 0 (version check) — this should prevent wrong-directory deploys going forward
- Frontend safePnl is a solid safety net but masks a real backend issue (backtester writing incomplete data)

### Where I Fell Short
- The initial handoff earlier today didn't account for the v10.68 regression that had already happened — it was discovered only when the user asked about it
- Should have verified live site state proactively at session start instead of just reading git state

## 10. Miscommunications to Address
None this portion — session was well-aligned after root cause was explained. User approved every step.

## 11. Files Changed This Session
**On GitHub (via /tmp clone push — commit 48e2f50):**
| File | Action | Description |
|------|--------|-------------|
| ufc-predict/webapp/frontend/src/components/picks/FightCard.jsx | modified | R1 KO gating, combo row, "2.60 diff" confidence |
| ufc-predict/webapp/frontend/src/components/shared/EventBetsDropdown.jsx | modified | safePnl odds-based computation, fighter-loss enforcement |
| ufc-predict/webapp/frontend/src/components/admin/AdminAlgorithm.jsx | modified | current_values fallback, 2 new CATEGORIES |
| ufc-predict/webapp/frontend/src/components/landing/HeroStats.jsx | modified | All bet types displayed correctly |
| ufc-predict/webapp/frontend/src/config/version.js | modified | v11.9.3 → v11.9.5 |

**Locally (iCloud working tree):**
| File | Action | Description |
|------|--------|-------------|
| webapp/ → archive/webapp_ROOT_STALE_v10.68/ | moved | Archived stale root webapp to prevent wrong-directory deploys |
| HANDOFF.md | created | This handoff document |
| ~/.claude/anti-patterns.md | modified | 5 new entries |
| ~/.claude/recurring-bugs.md | modified | 2 new entries |
| ~/.claude/memory/topics/ufc_website_maintenance_rules.md | created | 15-point checklist + 19 display rules |

## 12. Current State
- **Branch (iCloud root)**: fix/method-scoring-v10.69
- **Last commit (iCloud root)**: f36fcc3 — "v10.69: Fix method bet scoring"
- **Branch (ufc-predict/)**: main — local v11.9.2, **remote v11.9.5** (divergent)
- **Build status**: CI build passed for v11.9.5 (commit 48e2f50)
- **Deploy status**: v11.9.5 LIVE on mmalogic.com via Cloudflare Pages
- **Uncommitted changes**: ~635 files in iCloud working tree (CRITICAL)

## 13. Environment State
- **Node.js**: v25.6.1
- **Python**: 3.14.3
- **Running dev servers**: None for this project (other projects have Next.js, Vite running)
- **Environment variables set this session**: none
- **Active MCP connections**: Claude in Chrome, Desktop Commander, PDF Tools, mcp-registry

## 14. Session Metrics
- **Duration**: ~3 hours total (including prior handoff portion + incident response)
- **Tasks completed**: 12 / 12 attempted
- **User corrections**: 1 (user discovered the v10.68 regression — agent should have caught it)
- **Tool calls**: ~50+
- **Skills/commands invoked**: /full-handoff
- **Commits made**: 1 to GitHub (48e2f50 via /tmp clone), 0 to local iCloud repo

## 15. Memory & Anti-Patterns Updated
- **anti-patterns.md**: 5 new entries (WRONG_DIRECTORY_DEPLOY, SCREENSHOT_REVIEW_MISSED_11_BUGS, R1_KO_GATING, CONFIDENCE_260, EVENTBETS_NULL_PNL, OPTIMIZER_MISSING_CURRENT)
- **recurring-bugs.md**: 2 new entries (deploy source directory, screenshot review carelessness)
- **ufc_website_maintenance_rules.md**: Created — 15-point checklist + 19 display rules
- **site-update-protocol SKILL.md**: Updated with 4 new bug items + Phase 4.5 data sync
- **deploy SKILL.md**: Updated with Step 0 — verify version.js before building
- **Project MEMORY.md**: Added website maintenance pointer

## 16. Skills & Agents Used
| Skill/Agent | How It Was Used | Was It Helpful? |
|-------------|----------------|-----------------|
| /full-handoff | Generated handoff documents (2x this session) | Yes |
| Claude in Chrome | Verified live site screenshots post-deploy | Yes — caught that v11.9.5 was correctly live |
| GitHub CLI (gh) | Triggered CI workflow, checked run status | Yes — clean deploy path |

## 17. For The Next Agent — Read These First
1. **This HANDOFF.md** — current state as of 2026-03-25 21:00
2. `~/.claude/memory/topics/ufc_website_maintenance_rules.md` — **MANDATORY** before reviewing any screenshot
3. `~/.claude/memory/topics/ufc_betting_model_spec.md` — canonical betting rules
4. `~/.claude/anti-patterns.md` — 5 new entries from this session, especially WRONG_DIRECTORY_DEPLOY
5. `~/.claude/recurring-bugs.md` — deploy source and screenshot review entries
6. `ufc-predict/AGENTS.md` — stale but has useful model overview (needs update)

### CRITICAL WARNING FOR NEXT AGENT
- **NEVER deploy from root `webapp/`** — it's archived at `archive/webapp_ROOT_STALE_v10.68/`. All deploys from `ufc-predict/webapp/frontend/` only.
- **Local ufc-predict/ is BEHIND GitHub** — pull latest before any work
- **635 uncommitted files** — commit to git is #1 priority
- **Always check version.js** before any deploy command

### Verified P/L (Live Site — v11.9.5, 2026-03-25)
| Bet Type | W-L | P/L |
|----------|-----|-----|
| ML | 303W-113L | +83.01u |
| Method | 148W-185L | +79.45u |
| Round | 29W-49L | +17.36u |
| Combo | 25W-53L | +72.96u |
| Parlay | 32W-32L | +28.93u |
| **Combined** | **969 bets** | **+281.71u (29.1% ROI)** |
