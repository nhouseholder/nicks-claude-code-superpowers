# UFC Predict Handoff — 2026-03-24 (Session 3 COMPLETE)

## Status: All Done — Deployed to Production (v11.9.4)

### What Was Done This Session (10 commits: 8e704e6 → b7bf40a)

#### 1. Repo Cleanup & Data Sync
- Archived 21 stale log/output files (~85MB) to `archive/logs/`
- Removed 5 stale `.bak` backup files
- Synced `algorithm_stats.json` and `optimizer_results.json` to webapp
- Fixed version consistency (was 11.10/11.11/11.9.2 → now 11.9.3 everywhere)

#### 2. Predictions Regenerated
- UFC Fight Night: Adesanya vs. Pyfer (March 28)
- Adesanya vs Pyfer: PASS (diff=0.13)
- 6 picks, 6 placed bets (BFO only has 6/13 ML odds — prelims not posted yet)
- Cleared stale `__NO_PROPS__` cache entries, re-scraped live odds
- Note: Chiesa opponent changed to Niko Price

#### 3. UI/UX Upgrade (Fira Code/Sans + Accessibility)
- Typography: Fira Sans body + Fira Code for all numbers/data
- CRITICAL: Chart accessible alternative (role="figure", sr-only data table)
- HIGH: Progress bars with role="progressbar" + ARIA values
- 12 MEDIUM fixes: aria-labels, focus-visible, reduced-motion, cursor-pointer
- Recent events: changed from 3-across squeeze to full-width stacked tables

#### 4. Backend Security Hardening (16 of 29 audit findings fixed)
- Timing-safe admin key comparison (was `===`)
- Rate limiting: auth (10 login/5min, 5 signup/hr), narrative (20/hr/IP)
- Subprocess env whitelist (no longer leaks JWT_SECRET, STRIPE keys)
- Firebase JWT auth on `/api/narrative` (was unauthenticated)
- Stripe error messages sanitized (was leaking internals)
- SQLite WAL mode, stripe_customer_id index
- Legacy SHA-256 → bcrypt auto-upgrade on login
- Task store 24hr TTL cleanup (memory leak fix)
- Shared `getAdminEmails()` + `timingSafeEqual()` in firebase-lite.js
- Unbounded query params capped (public.py, ncaa.py, admin.py)
- Payload validation on odds import

#### 5. CRITICAL Data Fix
- Registry `totals` was missing parlay_pnl/parlay_wins/parlay_losses
- Hero showed +252.78u instead of correct +281.71u
- Parlay card showed +0.00u instead of +28.93u (32W-32L)
- algorithm_stats.json synced to registry truth (was showing divergent backtest numbers)
- Now: Hero +281.71u, all cards correct, chart and hero agree

### Final Numbers (v11.9.4 — from registry)

| Bet Type | W-L | P/L |
|----------|-----|-----|
| ML | 303W-113L (72.8%) | +83.01u |
| Method | 148W-185L (44.4%) | +79.45u |
| Round | 29W-49L (37.2%) | +17.36u |
| Combo | 25W-53L (32.1%) | +72.96u |
| Parlay | 32W-32L (50.0%) | +28.93u |
| **Combined** | **969 bets** | **+281.71u (29.1% ROI)** |

### Deployed
- GitHub: `b7bf40a` on main, tagged `v11.9.4`
- Cloudflare: auto-deployed from GitHub push → mmalogic.com

### What Could Be Done Next (not started)
- **Remaining 8 CF functions**: Migrate to shared `getAdminEmails()` helper (only loss-protection.js done)
- **CBB engine fix**: Stop modifying source code at runtime, use env vars instead
- **DB connection pooling**: Current setup opens new SQLite conn per request
- **Mobile responsive pass**: Test at 375px, 768px breakpoints
- **Admin refresh-odds button**: Verify GITHUB_TOKEN is set in Cloudflare env vars
- **Odds auto-refresh**: The Wed/Thu/Fri/Sat cron should catch prelim odds as they post
- **E2E smoke tests**: signup → login → free pick → pricing flow

### R2 KO Combo Analysis (confirmed this session)
- 0/72 R2 KO combos would have won (9 hits, 63 misses, estimated -18u / -25% ROI)
- Gate stays: both round AND combo are R1-KO-only

### Critical Rules (PERMANENT)
1. **12 scoring rules** — see `~/.claude/memory/topics/ufc_betting_model_spec.md`
2. **R1 KO gating** — round AND combo bets only on R1 KO predictions
3. **Registry is source of truth** for actual results (not algorithm_stats backtest numbers)
4. **Parlay totals must be in registry `totals`** — was missing, now fixed
5. **constants.json is single source of truth** for parameters
6. **Backtest = cache-only by default**
7. **Never overwrite registry with fewer events**
