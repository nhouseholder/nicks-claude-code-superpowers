# Handoff — Diamond Predictions — 2026-03-28 10:15
## Model: Claude Opus 4.6 (1M context)
## Previous handoff: handoff_diamond-predictions_2026-03-28_0015.md
## GitHub repo: nhouseholder/diamond-predictions
## Local path: ~/Projects/diamondpredictions/
## Last commit date: 2026-03-28 10:13:44 -0700

---

## 1. Session Summary
User wanted to fix MLB pick breakdown not showing specific system names, verify NHL pipeline was producing picks, and ensure both pipelines are working for tomorrow. Fixed a key mismatch bug (`systems` vs `systems_fired`) that caused all `sys_names` to be empty arrays. Investigated NHL pipeline — found 3 days of 0 picks was caused by missing season archive symlinks (already fixed last session) plus a timing issue. Discovered and fixed critical NHL bet history data loss (686 bets → 1 bet) caused by `bet_history.json` not existing in git when the pipeline first ran from this repo.

---

## 2. What Was Done

- **MLB sys_names fix (run.py)**: Fixed key mismatch — `systems.py` outputs system names under key `"systems"` but `run.py` read `"systems_fired"` (signal_aggregator key). Updated all 3 consensus paths + conglomerate output + prediction log to use fallback `sp.get("systems_fired") or sp.get("systems") or []`. Commit `84fa6c5`.
- **NHL bet history recovery**: Restored 686 bets from `nhl_bet_history.json` (the full backtest history file), merged the new FLA PLATINUM pick, wrote to both `bet_history.json` and `nhl-bet-history.json` webapp file. Added recovery safeguard in `_append_bet_history()` and `grade_yesterday()` — if `bet_history.json` has <10 bets, auto-seeds from `nhl_bet_history.json`. Commit `9202bc2`.
- **NHL pipeline investigation**: Traced 3 days of 0 picks through CI logs. Found: (1) 3/26-3/27 season archives were missing in git (fixed by `2d6ee9d` in prior session), (2) 3/28 morning run had odds but model didn't find qualifying picks, (3) 3/28 afternoon run found 1 pick (FLA PLATINUM +165). Pipeline is now working correctly.
- **Both pipelines verified**: Confirmed MLB (cron 14:00 UTC) and NHL (cron 11:00 UTC) are running daily, auto-grading, auto-generating, auto-deploying, and auto-committing.

---

## 3. What Failed (And Why)

- **NHL bet history data loss not caught earlier**: The `bet_history.json` file didn't exist in git before the NHL consolidation. When `_append_bet_history()` loaded it, `load_json()` returned `None` → defaulted to `{"bets": []}` → only the 1 new pick was saved. 686 historical bets were silently lost. The root `nhl_bet_history.json` still had the full data.
- **3-day NHL pick drought diagnosis took multiple queries**: Had to check 10+ CI run logs to piece together the timeline. Could have started with checking the engine build lines immediately.

---

## 4. What Worked Well

- Tracing the `sys_names` bug through 3 layers (systems.py → run.py → daily_pipeline.py → picks.json → React component) identified the exact key mismatch.
- Using `gh run view --log` with grep filters efficiently diagnosed the NHL pipeline issues across multiple runs.
- The `nhl_bet_history.json` file serving as a recovery source — having the full backtest history committed to git saved the data.

---

## 5. What The User Wants

- Full pick details visible in admin dropdown for both MLB and NHL (sys_names fix addresses this for MLB; NHL already worked).
- User quote: "the drop down menu doesn't show me which systems specifically are active, i want to see the full pick details as admin, for both MLB and NHL"
- User quote: "last few days no NHL pick, just make sure it's working properly"
- User quote: "ensure both pipelines are working for tomorrow and autonomously grading and tracking picks as well as auto generating"
- Confidence that both pipelines are autonomous and self-healing.

---

## 6. In Progress (Unfinished)

**3 items from the site review (carried over from previous handoff):**

1. **`trigger-pipeline.js:111` crypto auth bypass** — 1-line fix. `return payload` → `return null` when HMAC verification throws. File: `mlb_predict/webapp/frontend/functions/api/trigger-pipeline.js` line ~111.

2. **Pipeline failure alerting** — Add `if: failure()` notification step to `daily-pipeline.yml` and `nhl-daily-pipeline.yml`. Currently silent failures.

3. **React Error Boundaries** — No Error Boundaries around any routes. If a component throws, the whole app goes blank. Wrap routes in `App.jsx` or `main.jsx`.

---

## 7. Blocked / Waiting On

Nothing blocked.

---

## 8. Next Steps (Prioritized)

1. **Fix `trigger-pipeline.js` crypto bypass** — P1 security. 1-line fix: `return payload` → `return null`.
2. **Add pipeline failure alerting** — Silent failures are dangerous. Add `if: failure()` step to both daily pipeline workflows.
3. **Add React Error Boundaries** — Prevent full-app blank screens.
4. **Verify sys_names populated in tomorrow's picks** — After the next MLB pipeline run, check `picks.json` has non-empty `sys_names`.
5. **Grade the FLA PLATINUM pick** — Tomorrow's NHL pipeline should auto-grade it (FLA @ NYI 3/28, +165). Verify grading works with the restored bet history.
6. **Node.js upgrade in workflows** — GitHub warns Node 20 deprecated June 2, 2026.

---

## 9. Agent Observations

### Recommendations
- The `bet_history.json` vs `nhl_bet_history.json` duality is fragile. Consider having the pipeline always use `nhl_bet_history.json` as the source of truth and remove `bet_history.json` as an intermediary.
- The NHL pipeline cron at 11:00 UTC (7 AM ET) runs before most game-day odds are posted. Consider adding a second scheduled run at ~17:00 UTC (1 PM ET) to catch game-day odds, or adjusting the cron to run later.
- The `data/season_*.json.gz` symlinks pointing to `../nhl_data/` work but are fragile. Consider replacing them with actual copies or using the `nhl_data/` path directly in the registry loader.

### Where I Fell Short
- Should have immediately checked `bet_history.json` vs `nhl_bet_history.json` file sizes when verifying the pipeline — the 1-bet history would have been an obvious red flag before digging through CI logs.
- The sys_names bug was a straightforward key name mismatch — could have found it faster by starting at the data file (`picks.json`) and grepping for `sys_names` assignment sites.

---

## 10. Miscommunications

None — session aligned. User requests were clear and directly actionable.

---

## 11. Files Changed

```
mlb_predict/run.py                                 | 18 +++++++++++-------
VERSION                                            |  2 +-
bet_history.json                                   | 10312 ++++++++++++++++++-
mlb_predict/webapp/frontend/public/data/nhl-bet-history.json | 10312 ++++++++++++++++++-
mlb_predict/webapp/frontend/public/data/version.json |  2 +-
mlb_predict/webapp/frontend/src/version.js         |  2 +-
scripts/nhl/daily_pipeline.py                      | 26 +
```

| File | Action | Why |
|------|--------|-----|
| `mlb_predict/run.py` | Modified | Fix sys_names key mismatch: read both `systems_fired` and `systems` keys |
| `bet_history.json` | Restored | Recovered 687 bets from nhl_bet_history.json (was overwritten to 1 bet) |
| `nhl-bet-history.json` | Restored | Webapp copy of restored bet history |
| `scripts/nhl/daily_pipeline.py` | Modified | Added recovery safeguard: auto-seed from nhl_bet_history.json if <10 bets |
| `VERSION` | Modified | 13.2.26 → 13.2.28 |
| `version.js` | Modified | Bump to 13.2.28 |
| `version.json` | Modified | Bump to 13.2.28 |

---

## 12. Current State

- **Branch**: main
- **Last commit**: `9202bc2` — v13.2.28: Restore NHL bet history (687 bets) + add recovery safeguard (2026-03-28 10:13:44 -0700)
- **Build**: Untested locally (Node 25.6.1 incompatible with Vite 7). CI (Node 22) triggered via push.
- **Deploy**: Triggered — `deploy-cloudflare-pages.yml` running from push of `9202bc2`.
- **Uncommitted changes**: Local has modified files matching the push (iCloud sync lag); no new uncommitted work.
- **Local SHA matches remote**: No — local is at `84fa6c5`, remote is at `9202bc2` (pushed via /tmp clone). Run `git pull` to sync.

---

## 13. Environment

- **Node.js**: v25.6.1 (local — incompatible with Vite 7; CI uses Node 22)
- **Python**: 3.14.3
- **Dev servers**: None running

---

## 14. Session Metrics

- **Duration**: ~60 minutes
- **Tasks**: 3 completed / 3 attempted (sys_names fix, NHL investigation, bet history recovery)
- **User corrections**: 0
- **Commits**: 2 (`84fa6c5`, `9202bc2`)
- **Skills used**: review-handoff, full-handoff

---

## 15. Memory Updates

- No new memory files written this session.
- Anti-patterns: The sys_names key mismatch (`systems` vs `systems_fired`) and the bet_history.json data loss are documented in commit messages but not added to anti-patterns.md.

---

## 16. Skills Used

| Skill | Purpose | Helpful? |
|-------|---------|----------|
| `review-handoff` | Session orientation | Yes — identified prior session's unfinished work |
| `full-handoff` | Session wrap-up | Yes |

---

## 17. For The Next Agent

Read these files first (in order):
1. This handoff (HANDOFF.md)
2. `handoff_diamond-predictions_2026-03-28_0015.md` (previous — has site review findings)
3. `~/.claude/anti-patterns.md` — especially `LANDING_PAGE_WRONG_FETCH_URL`
4. `~/Projects/diamondpredictions/CLAUDE.md`
5. `~/Projects/diamondpredictions/WEBSITE_UPDATE_HANDOFF.md`
6. `~/Projects/diamondpredictions/_review/` — site review findings (P0/P1 items in Section 6)

**Canonical local path for this project: ~/Projects/diamondpredictions/**
**Do NOT open this project from iCloud or /tmp/. Use the path above.**

---
## NEXT AGENT: MANDATORY STARTUP SEQUENCE
Before doing ANY work, run the 3-Gate Verification from ~/.claude/CLAUDE.md:
1. GATE 1: Check ~/Projects/site-to-repo-map.json — verify you're in the correct repo
2. GATE 2: git fetch && compare local SHA to remote — git pull if behind
3. GATE 3: Read this handoff + MEMORY.md + anti-patterns.md + recurring-bugs.md
ALL 3 GATES MUST PASS before touching any code.

**Canonical path for this project: ~/Projects/diamondpredictions/**
**Last verified commit: 9202bc2 on 2026-03-28 10:13:44 -0700**
