# Handoff — MyStrainAI — 2026-03-28 10:45
## Model: Claude Opus 4.6 (1M context)
## Previous handoff: handoff_Strain-Finder-Front-Cannalchemy-Back_2026-03-27_0411.md
## GitHub repo: nhouseholder/Strain-Finder-Front-Cannalchemy-Back
## Local path: ~/Library/Mobile Documents/com~apple~CloudDocs/ProjectsHQ/mystrainai
## Last commit date: 2026-03-28 10:17:38 -0700

---

## 1. Session Summary
Massive session covering 8 features: standardized AI strain reviews, flavor profile accuracy fix, CBD pain relief boost, CBD data cap, dual Find Near Me buttons, dispensary price display, community-sourced high intensity scoring system (new feature), and complete scoring engine restructure. The scoring engine was rebuilt from a 5-pillar/7-sublayer architecture to a flat 8-category weight system per user specification.

## 2. What Was Done
- **Standardized AI strain reviews**: Restructured both AI prompt (`promptBuilder.js`) and deterministic fallback (`strainExperience.js`) to follow Smell > Visual > Taste > Effect > Best Uses flow. Cache prefix bumped exp4 to exp5, max tokens 200 to 350.
- **Flavor profile accuracy fix**: Fixed AllBud scraper to remove user review over-scraping. Fixed enrichment script to prioritize AllBud source data (8.0 weight) over terpene-derived flavors (0.25 weight). Threshold raised 4.0 to 6.0.
- **CBD pain relief boost**: Added `CBD_BENEFICIAL_EFFECTS` set and goal-aware CBD scoring in `calcCannabinoidScore()`. Updated pharmacology scaffold pain pathway CBD weight 0.15 to 0.25.
- **CBD data cap at 2%**: Fixed 184 strains with impossible CBD values (up to 30%) in DB. Added safety cap in export script. Rescaled all pharmacology scaffold CBD thresholds and quiz scoring to real 0-2% range.
- **Dual Find Near Me buttons**: Kept existing top-right button on strain cards, added full-width bottom CTA in `StrainCardExpanded.jsx`.
- **Dispensary price display**: Enhanced "on menu" banner to show prominent `$XX/3.5g` price badge. Added client-side `extractMenuItemPrice()` for location-mode. Shows "Price not listed" fallback.
- **High Intensity scoring (NEW FEATURE)**: Built entire pipeline. `scrape_intensity.py` scrapes AllBud reviews, applies NLP keyword analysis, combines with chemical entourage data (THC + terpene amplification - CBD dampening). `strain_intensity` DB table stores per-strain 1-10 scores. 3,695 strains scored (137 with community reviews, rest chemistry-only). UI shows color-coded intensity bar on strain detail pages.
- **Scoring engine restructure**: Flattened from 5-pillar/7-sublayer to direct 8-category weights: Effects 50%, Avoid 15%, Flavor 10%, Tolerance 10%, Location 5%, Commonness 5%, Cannabinoid 2.5%, Strain Type 2.5%. Removed budget scoring entirely. Intensity is now primary tolerance signal (70% of tolerance blend).

## 3. What Failed (And Why)
- **Dev server in /tmp**: Duplicate React issue when running `preview_start` from /tmp working clone. iCloud source + /tmp node_modules creates two React copies. Workaround: verified via production build.
- **CBD boost first attempt**: Sigmoid with floor of 65 penalized all strains equally. Fixed with additive bonus approach.
- **git push to wrong branch**: Early pushes went to `origin main` but deploy branch is `nicks-redesign`. Fixed with `git push origin main:nicks-redesign`. 6 commits were briefly only on a non-deploy branch.

## 4. What Worked Well
- Chemical-only intensity scoring as a fast bootstrapping approach while full scrape runs in background.
- Test batch of 20 known strains validated the intensity algorithm intuitively (GDP 24.5% THC scored 2.8 intensity, Northern Lights 19.6% THC scored 8.3).
- Flat scoring architecture is much easier to reason about than nested pillars.

## 5. What The User Wants
- "sometimes high thc strains with low terpenes have weak highs, thc % alone isn't the only thing"
- "the community source intensity ratings should map towards the tolerance/experience aspect of the quiz, more so than raw thc % values"
- User specified exact scoring weights: "Effects 50%, Avoid Effects: 15%, Flavor: 10%, Tolerance: 10%, Location: 5%, Commonness: 5%, then fit the rest in the final 10%. Remove the budget aspect."
- Wants prices visible when comparing dispensaries via Find Near Me.

## 6. In Progress (Unfinished)
- **Full community scrape**: Only 137/3,695 strains have AllBud review data. 368 reviews are cached in `data/intensity-cache.json`. Run `python3 scripts/scrape_intensity.py` to complete (~30-45 min). Then re-export and redeploy.
- **Leafly review scraping**: The scraper supports it architecturally but no Leafly review scraping is implemented yet.

## 7. Blocked / Waiting On
Nothing blocked.

## 8. Next Steps (Prioritized)
1. **Complete the intensity scrape** — Run `python3 scripts/scrape_intensity.py` for full AllBud review data on all 3,695 strains. Then `python3 scripts/export_strain_data.py`, rebuild, push to `nicks-redesign`.
2. **Add Leafly review scraping** — Would double coverage for intensity data.
3. **Quiz UX for intensity** — Consider showing users what intensity range matches their tolerance level.

## 9. Agent Observations
### Recommendations
- The `nicks-redesign` branch is the deploy branch, not `main`. Future sessions MUST push to `nicks-redesign`.
- The /tmp working clone approach works for git ops but prevents dev server preview. Consider cloning to a non-iCloud location that supports both.
- The intensity scoring would benefit from strain description text in the DB as an additional signal source (no scraping needed).

### Where I Fell Short
- Pushed to `origin main` instead of `origin nicks-redesign` for 6 commits. Caught and fixed at handoff time, but deploys may have been delayed.
- Dev server verification was skipped throughout due to iCloud/React duplicate issues.

## 10. Miscommunications
None. Session was well-aligned. User provided clear weight specifications.

## 11. Files Changed
| File | Action | Why |
|------|--------|-----|
| `cannalchemy/data/schema.py` | Modified | Added `strain_intensity` table |
| `scripts/scrape_intensity.py` | Created | AllBud review scraper + NLP keyword intensity scorer |
| `scripts/scrape_allbud_flavors.py` | Modified | Removed user review over-scraping |
| `scripts/fix_strain_flavors.py` | Modified | Prioritized AllBud source, reduced terpene override |
| `scripts/export_strain_data.py` | Modified | Added CBD cap, intensity export, intensity loader |
| `frontend/functions/api/v1/quiz/recommend.js` | Modified | CBD boost, intensity scoring, full weight restructure |
| `frontend/functions/_data/pharmacology-scaffold.js` | Modified | CBD thresholds rescaled to 0-2% range |
| `frontend/functions/_data/strain-data.js` | Modified | Re-exported with CBD fix + intensity data |
| `frontend/src/data/strains.json` | Modified | Re-exported with CBD fix + intensity data |
| `frontend/src/components/results/StrainCardExpanded.jsx` | Modified | Bottom Find Near Me CTA, intensity bar UI |
| `frontend/src/components/strain-detail/ExperienceDescription.jsx` | Modified | Cache prefix exp4 to exp5, max tokens 200 to 350 |
| `frontend/src/services/promptBuilder.js` | Modified | Standardized AI prompt to sensory journey flow |
| `frontend/src/utils/strainExperience.js` | Modified | Standardized fallback generator |
| `frontend/src/routes/DispensaryPage.jsx` | Modified | Price display, client-side price extraction |
| `frontend/src/utils/constants.js` | Modified | Version bumped v5.103 through v5.109 |
| `frontend/package.json` | Modified | Version synced |

## 12. Current State
- **Branch**: main (local) pushed to nicks-redesign (remote deploy)
- **Last commit**: 1728ceb refactor: Restructure scoring weights per user spec (2026-03-28 10:17:38 -0700)
- **Build**: passing (npm run build succeeds)
- **Deploy**: deployed to Cloudflare via nicks-redesign push
- **Uncommitted changes**: `.claude/launch.json`, `frontend/package-lock.json`, `_qa/` dir
- **Local SHA matches remote**: yes (1728ceb on both)

## 13. Environment
- **Node.js**: v25.6.1
- **Python**: 3.14.3
- **Dev servers**: none running

## 14. Session Metrics
- **Duration**: ~120 minutes
- **Tasks**: 8 / 8 completed
- **User corrections**: 2 (intensity should map to tolerance more; scoring weight restructure)
- **Commits**: 18 this session (a745a97 through 1728ceb)
- **Skills used**: none invoked via /skill

## 15. Memory Updates
No memory files written. Key decisions to persist next session:
- Scoring weights (Effects 50%, Avoid 15%, etc.) are user-specified
- CBD max is 2% — all values above are data errors
- `nicks-redesign` is the deploy branch, not `main`

## 16. Skills Used
| Skill | Purpose | Helpful? |
|-------|---------|----------|
| N/A | Direct implementation | N/A |

## 17. For The Next Agent
Read these files first (in order):
1. This handoff
2. `handoffs/handoff_Strain-Finder-Front-Cannalchemy-Back_2026-03-27_0411.md`
3. `~/.claude/anti-patterns.md`
4. Project `CLAUDE.md` at repo root
5. `frontend/functions/api/v1/quiz/recommend.js` — the scoring engine (heavily modified)
6. `scripts/scrape_intensity.py` — the new intensity scraper

**Canonical local path: ~/Library/Mobile Documents/com~apple~CloudDocs/ProjectsHQ/mystrainai**
**Git working clone: /tmp/mystrainai-work (use for git ops, never git from iCloud)**
**Deploy branch: nicks-redesign (NOT main)**

---
## NEXT AGENT: MANDATORY STARTUP SEQUENCE
Before doing ANY work, run the 3-Gate Verification from ~/.claude/CLAUDE.md:
1. GATE 1: Check ~/Projects/site-to-repo-map.json — verify you're in the correct repo
2. GATE 2: git fetch && compare local SHA to remote — git pull if behind
3. GATE 3: Read this handoff + MEMORY.md + anti-patterns.md + recurring-bugs.md
ALL 3 GATES MUST PASS before touching any code.

**Canonical path: ~/Library/Mobile Documents/com~apple~CloudDocs/ProjectsHQ/mystrainai**
**Last verified commit: 1728ceb on 2026-03-28 10:17:38 -0700**
**Deploy branch: nicks-redesign**
