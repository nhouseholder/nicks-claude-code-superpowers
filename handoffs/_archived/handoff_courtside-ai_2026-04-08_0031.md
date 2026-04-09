# Handoff — courtside-ai — 2026-04-08 00:31
## Model: Claude Sonnet 4.6
## Previous handoff: handoff_courtside-ai_2026-04-07.md
## GitHub repo: nhouseholder/courtside-ai
## Local path: /Users/nicholashouseholder/ProjectsHQ/courtside-ai
## Last commit date: 2026-04-08 00:27:45 -0700

---

## 1. Session Summary
User wanted the NBA playoff algorithm to exceed 20% ROI and also add new "Professor MJ" betting systems from local files. Session scraped 250 historical playoff games, discovered round-specific signals (R2: bet favorites; CF: bet underdogs), and implemented PLAYOFF_FAV_R2 (+31.2% ROI) and PLAYOFF_DOG_CF (+39.5% ROI) as the playoff algorithm (v12.42.0). Then added 4 Professor MJ pattern systems — GAME7_HOME, FADE_BLOWOUT, PLAYOFF_BOUNCE_A, PLAYOFF_BOUNCE_B — from 27 seasons of data (v12.43.0). Everything is live on GitHub and Cloudflare Pages.

## 2. What Was Done
- **v12.42.0: NBA Playoff Algorithm** (08756ef): Scraped 250 playoff games (3 seasons) from ESPN Core Odds API. Found round-specific ATS edges: PLAYOFF_FAV_R2 (May 1-15, bet fav spread 1-4.5) = 68.8% ATS, +31.2% ROI, N=32. PLAYOFF_DOG_CF (May 16+, bet dog spread 1-7) = 73.1% ATS, +39.5% ROI, N=26. Portfolio 41W-17L = +35.0% ROI, p=0.001, all 3 seasons profitable. Implemented `getPlayoffRound()`, `bet_side` field for dog-side betting, `betSideOverride` return from `pickNbaFallbackSituationalSystems()`, spread floor 1 for playoff picks, PLAYOFF_AGREE tier. R1 rejected (52.5% fav ATS = coin flip).
- **v12.43.0: Professor MJ Systems** (0990ef6): Read 4 NBA.md systems from local files. Implemented all 4 after confidence check: GAME7_HOME (57.8% ATS, Game 7 only, home team), FADE_BLOWOUT (61.6% ATS, bet against team that just won by 33+), PLAYOFF_BOUNCE_A (56.0% ATS, lost by 12.5+ last playoff game), PLAYOFF_BOUNCE_B (57.1% ATS, lost by 4.5+ in last 2 playoff games). Expanded `teamLastGame` → `teamRecentGames[]` array (3-game history) to support multi-game lookback. Added 7-day playoff lookback (vs 3-day regular season). Added `game_number` extraction from ESPN `notes[0].headline`. Line movement REJECTED (49.4% ATS). Added 4 labels to `src/lib/nba-bets.js`.
- **v12.41.1: Analysis commit** (9a35886): Prop backtest infrastructure (Phase 1+2) from prior session.
- **Docs/sync** (33680aa): Updated `ALGORITHM_VERSION.md` with full v12.42+43 stats, updated `experiment-log.json` with both entries.
- **All changes pushed and live on courtside-ai.pages.dev**.

## 3. What Failed (And Why)
- **Line movement system REJECTED**: Tested ESPN consensus line movement signal for NBA — 49.4% ATS across 3 seasons (p=0.89). Not implemented. Logged in experiment-log.json.
- **R1 playoff system REJECTED**: Round 1 favorite ATS = 52.5% (N=64) — coin flip. Only R2 and CF have actionable edges.
- **Agent limit hit during exploration**: Hook blocked 3rd Explore subagent (max 2 per session). Fixed by switching to direct Grep/Read tool exploration.
- **HANDOFF.md Write error at session end**: Tried to Write HANDOFF.md without reading first — "File has not been read yet." Context compacted mid-handoff. Recovered in next context by reading then writing.

## 4. What Worked Well
- **ESPN Core Odds API for historical scraping**: Clean historical ATS data for 250+ playoff games across 3 seasons. Reusable cache in `scripts/cache/nba_playoff_ats.json`.
- **Round-specific analysis**: Breaking playoffs into R1/R2/CF/Finals (vs. one bucket) revealed the side-switching pattern that blanket analysis would hide.
- **Season-by-season validation**: Filtering to only signals profitable in all 3 seasons eliminated noise. PLAYOFF_FAV_R2 was profitable in 22-23, 23-24, 24-25. PLAYOFF_DOG_CF was profitable in all 3 as well.
- **`teamRecentGames` array expansion**: Clean infrastructure upgrade — 3-game history enables any multi-game lookback system without further refactoring.
- **Direct file read of Professor MJ systems**: User pointed to local path; read markdown directly instead of needing screenshots.

## 5. What The User Wants
User wants the NBA playoff algorithm generating real picks with >20% ROI during the 2026 playoffs. Key quotes:
- "the NBA playoff system needs to be >20% ROI, strategize how we are gonna get there, plan think, research, think, plan"
- "Next, there are new systems that we need to add to our NBA algorithm, they are found on my computer here: /Users/nicholashouseholder/ProjectsHQ/Professor MJ/systems/"
- "get everything synced on github, live on the site, update experiment log"
- "very good, is this synced on github and live on our site?"

User wants algorithm improvements to ship quickly — implemented, tested, and live in same session.

## 6. In Progress (Unfinished)
All v12.42.0 and v12.43.0 tasks are complete. The following are future work items:

- **ODDS_API_KEY not set**: Prop system (`/props` page) requires this env var in Cloudflare Pages → Settings → Environment variables. Without it, prop picks are missing but everything else works.
- **Playoff systems not yet battle-tested in production**: Play-in starts ~April 15, R1 April 19. First live signal opportunity for PLAYOFF_BOUNCE_A/B and GAME7_HOME in R1.

## 7. Blocked / Waiting On
- **ODDS_API_KEY**: User action — must be added to Cloudflare Pages env vars to unblock prop picks.
- **2026 Playoffs starting**: PLAYOFF_FAV_R2 activates May 1-15, PLAYOFF_DOG_CF activates May 16+. GAME7_HOME and PLAYOFF_BOUNCE systems activate during any playoff game.

## 8. Next Steps (Prioritized)
1. **Set ODDS_API_KEY in Cloudflare Pages** — unblocks prop picks. User action, not code change.
2. **Monitor playoff systems starting April 15** — play-in begins. PLAYOFF_BOUNCE_A/B and GAME7_HOME should fire during R1.
3. **Check for NCAAB Professor MJ systems** — the professor's files may include NCAAB systems. Check `/Users/nicholashouseholder/ProjectsHQ/Professor MJ/systems/` for any non-NBA files.
4. **NBA Standings Tracker** — required to unlock Updated Tanking System (tighter filters backtest pending). Aggregate ESPN season W-L records per team.

## 9. Agent Observations
### Recommendations
- The playoff algorithm is activated by date ranges (April=R1, May 1-15=R2, May 16+=CF). No code changes needed — it will auto-activate when the calendar hits the right dates.
- FADE_BLOWOUT fires in regular season too (not just playoffs). If any team wins by 33+ today, the next game fades them. Watch for this in the final regular season games (April 7-13).
- The `teamRecentGames` lookback is 7 days during playoff periods, 3 days during regular season. This is determined by detecting any `season_type === 3` game in today's ESPN lines. Transition happens automatically.

### Data Contradictions Detected
No data contradictions this session.

### Where I Fell Short
- Context compaction interrupted the handoff mid-write. Should have written HANDOFF.md earlier in the session before context grew large.

## 10. Miscommunications
None — session aligned. All requests were implemented as specified.

## 11. Files Changed

```
git diff --stat HEAD~4..HEAD (v12.41.1 → v12.43.0 + docs):
functions/api/nba-cron-generate.js    | +285 lines (teamRecentGames, game_number, playoff systems, MJ systems)
functions/api/nba-generate-picks.js   | +270 lines (same changes mirrored)
functions/lib/nba-systems.js          | +60 lines (getPlayoffRound, PLAYOFF_FAV_R2, PLAYOFF_DOG_CF)
src/lib/nba-bets.js                   | +8 lines (4 MJ system labels)
src/config/version.js                 | +1 line (12.43.0)
package.json                          | +1 line (12.43.0)
CLAUDE.md                             | +1 line (version update)
ALGORITHM_VERSION.md                  | +12 lines (playoff + MJ stats)
scripts/scrape_nba_playoff_ats.py     | Created (250-game playoff scraper)
scripts/cache/nba_playoff_ats.json    | Created (250 playoff games, cached)
scripts/experiments/experiment-log.json | +2 entries (v12.42.0 + v12.43.0)
```

| File | Action | Why |
|------|--------|-----|
| functions/lib/nba-systems.js | Modified | Added `getPlayoffRound()`, PLAYOFF_FAV_R2, PLAYOFF_DOG_CF system configs with `bet_side`/`playoff_round` fields |
| functions/api/nba-cron-generate.js | Modified | teamRecentGames array, 7-day playoff lookback, game_number, dog-side logic, 4 MJ system blocks |
| functions/api/nba-generate-picks.js | Modified | Same as cron-generate (always kept in sync) |
| src/lib/nba-bets.js | Modified | 4 new system name labels for UI |
| scripts/scrape_nba_playoff_ats.py | Created | Playoff ATS scraper using ESPN Core Odds API |
| scripts/cache/nba_playoff_ats.json | Created | 250-game playoff ATS cache |
| scripts/experiments/experiment-log.json | Modified | Added v12.42.0 + v12.43.0 experiment entries |
| ALGORITHM_VERSION.md | Modified | Full stats for playoff algo + Professor MJ |
| package.json + src/config/version.js + CLAUDE.md | Modified | Version bump to 12.43.0 |

## 12. Current State
- **Branch**: main
- **Last commit**: 33680aa1 docs: update experiment log + algorithm version for v12.42.0 and v12.43.0 (2026-04-08)
- **Build**: passing (125/125 tests)
- **Deploy**: live on courtside-ai.pages.dev (auto-deployed via Cloudflare Pages)
- **Uncommitted changes**: `scripts/analysis/system_grades.json` (untracked, auto-generated)
- **Local SHA matches remote**: yes (33680aa1 = 33680aa1)

## 13. Environment
- **Node.js**: v25.6.1
- **Python**: 3.14.3
- **Dev servers**: none running

## 14. Session Metrics
- **Duration**: ~120 minutes
- **Tasks**: 4 completed / 4 attempted (playoff algorithm, MJ systems, sync/deploy, docs)
- **User corrections**: 0
- **Commits**: 4 (08756ef, 0990ef6, 9a35886, 33680aa)
- **Skills used**: /full-handoff

## 15. Memory Updates
No new anti-patterns or memory files created this session. `ALGORITHM_VERSION.md` updated with full v12.42+43 stats. `experiment-log.json` has both new entries.

## 16. Skills Used
| Skill | Purpose | Helpful? |
|-------|---------|----------|
| /full-handoff | Session end documentation | Yes |

## 17. For The Next Agent
Read these files first (in order):
1. This handoff (HANDOFF.md)
2. ALGORITHM_VERSION.md — full algorithm state including playoff + MJ systems
3. ~/.claude/anti-patterns.md
4. CLAUDE.md — project conventions, pipeline docs, common bugs
5. functions/api/nba-cron-generate.js — most complex file, playoff + MJ system logic
6. functions/lib/nba-systems.js — system configs + getPlayoffRound()

**Canonical local path for this project: /Users/nicholashouseholder/ProjectsHQ/courtside-ai**
**Do NOT open this project from iCloud or /tmp/. Use the path above.**

---
## NEXT AGENT: MANDATORY STARTUP SEQUENCE
Before doing ANY work, run the 3-Gate Verification from ~/.claude/CLAUDE.md:
1. GATE 1: Check ~/Projects/site-to-repo-map.json — verify you're in the correct repo
2. GATE 2: git fetch && compare local SHA to remote — git pull if behind
3. GATE 3: Read this handoff + MEMORY.md + anti-patterns.md + recurring-bugs.md
ALL 3 GATES MUST PASS before touching any code.

**Canonical path for this project: /Users/nicholashouseholder/ProjectsHQ/courtside-ai**
**Last verified commit: 33680aa1 on 2026-04-08 00:27:45 -0700**
