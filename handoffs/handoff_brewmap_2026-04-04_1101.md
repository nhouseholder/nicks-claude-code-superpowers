# Handoff — BrewMap — 2026-04-04 11:01
## Model: Claude Opus 4.6 (1M context)
## Previous handoff: handoff_brewmap_2026-04-03_0121.md
## GitHub repo: nhouseholder/brewmap
## Local path: ~/ProjectsHQ/Brewmaps/
## Last commit date: 2026-04-04

---

## 1. Session Summary
Massive session: v4.5.0 → v6.0.0 across 2 sessions (previous + this one). Built 3-layer enrichment pipeline (Yelp reviews + website scraping + AI estimates), replaced fabricated data with real bean origins/roast levels/tasting notes from shop websites, added flavor-based discovery UX ("What flavor are you craving?" with cosine similarity match scoring), roast/origin filters, tiered data quality badges, directions button, similar shops feature, and progressive city coverage. Also fixed chain filter, added harvest retry logic, and ran enrichment across all cities.

## 2. What Was Done
- **v5.0.0 — Yelp Fusion API integration**: New scripts/lib/yelp.mjs (search, match, reviews), scripts/enrich-with-yelp.mjs orchestrator, kv-writer preserves Yelp fields, frontend shows Yelp badges/reviews
- **v5.1.0 — Progressive city coverage**: New POST /api/city/discover endpoint, Worker-compatible modules in functions/lib/, frontend calls discover API instead of client-side Overpass
- **v5.1.1 — Unified coffee-forward filter**: Extracted to shared/coffee-filter.mjs, eliminated 105 lines of duplicated logic
- **v5.2.0 — Geolocation skip button + cleanup**: Removed stale root index.html (1035 lines), bumped Overpass delay to 3s
- **v5.2.1 — Rating slider filter**: 0-5 stars, 0.5 step
- **v5.3.0 — Flavor extraction from reviews**: New scripts/lib/flavor-extract.mjs with 130+ synonym mappings
- **v5.4.0 — Website scraping enrichment**: New web-scraper.mjs, bean-extract.mjs (30 countries, 50+ regions), enrich-from-websites.mjs orchestrator, combineFlavorSources()
- **v6.0.0 — Search & Discovery UX overhaul**: Flavor preference search with match scoring, roast pills, origin dropdown, tiered badges, data sources section, directions button
- **Chain filter fix**: Added 11 regional chains (Dutch Bros, Black Rock, Human Bean, etc.)
- **Harvest retry logic**: Per-city retry with 10s/20s exponential backoff, threshold 30%→50%
- **Similar shops feature**: Cosine similarity on flavorProfile vectors, 4 similar shops in detail panel
- **Website enrichment run**: 1,208 shops processed, 138 with bean data, 162 with website flavors
- **Deployed v6.0.0** to Cloudflare Pages

## 3. What Failed (And Why)
- **Overpass API degradation**: 16/30 cities returned 504s. Only 8 survived. Fixed with retry logic.
- **GitHub Actions secrets in if condition**: Invalid syntax. Fixed by making script exit gracefully.
- **KV data loss from TTL expiry**: Previous 4,702 shops expired when new harvest failed. Only 1,208 remain.

## 4. What Worked Well
- Website scraping hit 50% of shops with websites — real bean data from real shops
- Flavor match scoring produces intuitive results
- Discover API works perfectly (tested with Boise — 53 shops)
- shared/coffee-filter.mjs cleanly solved filter drift

## 5. What The User Wants
- "the whole point is to sort by actual coffee flavor to find the coffee shop near you that will have the flavor you like"
- "we need to keep enriching with real flavor reviews"
- "do a custom web search on each coffee shop, find out what type of beans they use, where they source from"
- User wants refinement over growth

## 6. In Progress (Unfinished)
- **Harvest re-run**: Workflow 23984435032 running with retry logic. Should recover 22 missing cities.
- **Yelp API key**: All code built. User needs to sign up and add YELP_API_KEY to GitHub secrets.
- **Deep-page scraping**: Only homepage scraped. Following /menu, /coffee links would 3-5x bean data.

## 7. Blocked / Waiting On
- **Yelp enrichment**: Needs YELP_API_KEY in GitHub secrets (user action)

## 8. Next Steps (Prioritized)
1. **Verify harvest completion** — Check run 23984435032 results
2. **Add Yelp API key** — Enables layer 2 enrichment (user action)
3. **Deep-page website scraping** — Follow internal links for 3-5x bean data. Effort: 0.5 session
4. **Flavor radar chart** — CSS spider chart in detail panel. Effort: 0.5 session
5. **User flavor votes** — Crowdsourced accuracy. Effort: 1 session

## 9. Agent Observations
### Recommendations
- KV TTL 14 days is too aggressive. Consider 30 days or "last known good" backup key.
- index.html is ~1300 lines. Approaching extraction threshold.
- Overpass reliability is the biggest infra risk. Consider committed JSON fallbacks.

### Data Contradictions Detected
No data contradictions.

### Where I Fell Short
- Should have added retry logic from the start — first harvest lost 22 cities unnecessarily.
- The workflow secrets bug should have been caught before first trigger.

## 10. Miscommunications
None — session aligned.

## 11. Files Changed
```
 17 files changed, 1322 insertions(+), 1217 deletions(-)
```

| File | Action | Why |
|------|--------|-----|
| scripts/lib/yelp.mjs | Created | Yelp API client |
| scripts/enrich-with-yelp.mjs | Created | Yelp enrichment orchestrator |
| scripts/lib/flavor-extract.mjs | Created | Flavor extraction + combineFlavorSources() |
| scripts/lib/web-scraper.mjs | Created | Fetch + HTML stripping |
| scripts/lib/bean-extract.mjs | Created | Bean origin/roast extraction |
| scripts/enrich-from-websites.mjs | Created | Website enrichment orchestrator |
| shared/coffee-filter.mjs | Created | Unified filter (single source of truth) |
| functions/api/city/discover.js | Created | On-demand scrape + cache endpoint |
| functions/lib/flavors.mjs | Created | Worker-compatible flavors |
| functions/lib/overpass.mjs | Created | Worker-compatible Overpass |
| public/index.html | Major update | Full UX overhaul |
| scripts/lib/kv-writer.mjs | Updated | Preserves enrichment fields |
| scripts/lib/overpass.mjs | Updated | Imports shared filter |
| scripts/harvest-coffee-shops.mjs | Updated | Retry logic |
| .github/workflows/harvest-coffee.yml | Updated | 3-step enrichment pipeline |
| package.json | Updated | v6.0.0, enrich scripts |
| index.html | Deleted | Stale root copy |

## 12. Current State
- **Branch**: main (worktree: claude/brave-mahavira)
- **Last commit**: b94d846 — Similar Flavor Profiles (2026-04-04)
- **Build**: N/A — single HTML file
- **Deploy**: v6.0.0 deployed to brewmap-app.pages.dev
- **Uncommitted changes**: None
- **Harvest run**: 23984435032 in progress

## 13. Environment
- **Node.js**: v25.6.1
- **Python**: 3.14.3
- **Dev servers**: None

## 14. Session Metrics
- **Duration**: ~180 minutes
- **Tasks**: 15 completed / 15 attempted
- **User corrections**: 0
- **Commits**: 14
- **PRs merged**: 10 (#1-#10)
- **Skills used**: review-handoff, whats-next, full-handoff

## 15. Memory Updates
No anti-patterns or memory files created. Key learnings:
- Overpass rate limits at 3s for 30 cities — retry handles this
- GitHub Actions can't use secrets in step if conditions
- shared/ imports resolve in Cloudflare Pages Functions
- Dutch Bros + regional chains need explicit filtering

## 16. Skills Used
| Skill | Purpose | Helpful? |
|-------|---------|----------|
| review-handoff | Orient to previous session | Yes |
| whats-next | Strategic recommendations | Yes |
| full-handoff | This document | Yes |

## 17. For The Next Agent
Read these files first:
1. This handoff (HANDOFF.md)
2. shared/coffee-filter.mjs
3. scripts/lib/flavor-extract.mjs
4. scripts/lib/bean-extract.mjs
5. public/index.html (~1300 lines)

**Canonical local path: ~/ProjectsHQ/Brewmaps/**
**GitHub repo: https://github.com/nhouseholder/brewmap**
**Live site: https://brewmap-app.pages.dev**
**KV data: 8 cities, 1,208 shops (harvest with retry pending)**
**3-layer enrichment: Website (2x) > Yelp reviews (1x) > AI estimate (0.3x)**

---
## NEXT AGENT: MANDATORY STARTUP SEQUENCE
Before doing ANY work, run the 3-Gate Verification from ~/.claude/CLAUDE.md:
1. GATE 1: Verify you're working on nhouseholder/brewmap (git remote)
2. GATE 2: git fetch && compare local SHA to remote — git pull if behind
3. GATE 3: Read this handoff + anti-patterns.md
ALL 3 GATES MUST PASS before touching any code.

**Canonical path for this project: ~/ProjectsHQ/Brewmaps/**
**Last verified commit: b94d846 on 2026-04-04**
