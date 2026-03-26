# OphthoCards — Session Handoff Document
**Last Updated:** March 24, 2026
**App Version:** 1.8
**Live URL:** Cloudflare Pages (project: `ophtho-cards`)
**GitHub:** Up to date with `origin/main` (14 uncommitted files — see Uncommitted Changes below)

---

## Project Overview

OphthoCards is an ophthalmology flashcard web app built with **Next.js 16** (static export) deployed on **Cloudflare Pages**, with **Firebase/Firestore** (Spark plan) as the backend. It imports ~33,462 cards from Anki `.apkg` decks and provides a spaced-repetition study system tailored to ophthalmology residency training.

**Firebase Project:** `icebreaker-ai-b21dd`
**User UID:** `SnUmKuuPR3Y6IkIwPFCazBQSvu63`
**Single Deck:** "OphthoCards" (ID: `XDr7jfpoEGhRF5SiXQWA`) — 33,462 cards

---

## Current State — What Works

1. **Card import** — Complete. All 33,462 cards are in Firestore under one deck.
2. **Study sessions** — Working. Queries limited to ~270 cards per session (`use-study-session.ts`) to avoid loading all 33K.
3. **Cloze card rendering** — Fixed. `renderer.ts` uses `templateIndex = model.type === 1 ? 0 : ordinal` so all 11 ordinal levels (0-10) render correctly.
4. **Render-time beautification** — Active. 7-step pipeline in `beautifier.ts` + memory enhancement in `memory-enhancer.ts` runs per-card at display time via `useMemo` in `card-content.tsx`. Pre-beautified cards (with `enhancedFields`) skip this step automatically.
5. **Deployment** — Live on Cloudflare Pages.
6. **Deck cleanup** — Done. Duplicates deleted, single deck renamed "OphthoCards."
7. **Dashboard accuracy** — Working. `recentAccuracy` computed from last 7 days of `dailyStats` retention rates via `useDailyStats` hook.
8. **Decks page** — Browse all decks with card counts, study progress, and quick actions.
9. **PGY classifier** — `src/lib/sequencer/pgy-classifier.ts` classifies cards into PGY levels from BCSC tags (new file, untracked).

---

## Uncommitted Changes (IMPORTANT — commit before deploying)

These files have been modified this session but NOT committed:

**Modified (12 files):**
- `AGENT-MEMORY.md` — Updated to reflect current state
- `src/app/(app)/dashboard/page.tsx` — Dashboard improvements
- `src/app/(app)/decks/page.tsx` — Decks page enhancements (+146 lines)
- `src/app/(app)/study/page.tsx` — Study page updates
- `src/components/study/card-content.tsx` — Enhanced card rendering
- `src/components/study/flashcard.tsx` — Flashcard display improvements
- `src/components/study/study-session.tsx` — Enhanced fields detection, media URL replacement
- `src/hooks/use-study-session.ts` — Study queue improvements
- `src/lib/cards/beautifier.ts` — Beautifier docstring fix
- `src/lib/cards/memory-enhancer.ts` — Minor fix
- `src/lib/version.ts` — Version 1.8 (2026-03-21)
- `src/types/card.ts` — Added `enhancedFields` to CardDocument type

**Untracked (2 files):**
- `HANDOFF.md` — This file
- `src/lib/sequencer/pgy-classifier.ts` — PGY level classification

**To commit:**
```bash
cd /tmp && git clone <repo-url> ophtho-commit && cd ophtho-commit
# Copy changed files from iCloud source, then:
git add -A && git commit -m "v1.8: Session updates — decks page, study improvements, PGY classifier"
git push origin main
```

---

## What's In Progress / Not Done

### 1. Pre-Beautification of All Cards (BLOCKED — Firestore quota)

**Goal:** Write beautified HTML directly into each card's `enhancedFields` in Firestore so cards load pre-beautified (faster, no render-time processing).

**Script:** `scripts/beautify-cards.cjs`
- Reads cards from Firestore REST API in pages of 300
- Runs each card's fields through the full beautification pipeline
- Writes an `enhancedFields` map back to each card document
- Tracks progress in `scripts/beautify-progress.json` (auto-resume)
- Stops at 17K writes per run to stay under 20K/day Spark plan quota

**Status:** Script is tested and functional. Firestore daily quota was exhausted during testing.

**To run:**
```bash
cd ophtho-cards && node scripts/beautify-cards.cjs 2>&1 | tee scripts/beautify.log
```
- Day 1: processes ~17K cards
- Day 2: run again, resumes from progress file, processes remaining ~16K cards

### 2. PGY Subdeck Split (NOT STARTED)

**Goal:** Break the single "OphthoCards" deck into 3 subdecks:
- **PGY-1:** Fundamentals, Optics, Anatomy, General Medicine (~5% of cards)
- **PGY-2:** Core clinical — Cornea, Glaucoma, Lens/Cataract, Retina, Neuro-Ophthalmology (~35%)
- **PGY-3/4:** Subspecialty — Pediatrics, Oculofacial, Uveitis, Pathology, WQE prep (~60%)

**Recommended approach:** Tag-based UI filtering (option 3) — zero Firestore writes. Map card tags to PGY levels client-side using `residency-planner.ts` mapping. `use-study-session.ts` already accepts a `pgyFilter` parameter. `pgy-classifier.ts` is already written.

---

## Key Architecture

### File Map

| File | Purpose |
|------|---------|
| `src/lib/apkg/renderer.ts` | Renders card HTML from Anki models + templates. Cloze fix. |
| `src/lib/cards/beautifier.ts` | 7-step beautification pipeline (660+ lines CSS). Category colors: drugs=green, anatomy=blue, diseases=red, surgery=purple, acronyms=teal. |
| `src/lib/cards/memory-enhancer.ts` | Chunking, first-letter cues, contrast highlighting, mnemonic pearl boxes. |
| `src/lib/cards/mnemonics.ts` | Curated ophthalmology mnemonic database (30+ entries, OKAP-relevant). |
| `src/hooks/use-study-session.ts` | `buildStudyQueue()` — fetches 270 cards max, filters into learning/review/new. Accepts `pgyFilter`. |
| `src/hooks/use-stats.ts` | `useDailyStats(days)` — fetches dailyStats for retention chart and accuracy. |
| `src/components/study/card-content.tsx` | Render-time beautification (`useMemo`). Skips when `enhancedHtml` is provided. |
| `src/components/study/flashcard.tsx` | Card display with 3D flip. Injects `OPHTHO_CARD_CSS`. Accepts `enhancedFrontHtml`/`enhancedBackHtml`. |
| `src/components/study/study-session.tsx` | `renderCardFaces()` — renders via Anki templates, returns enhanced HTML when `enhancedFields` exist. |
| `src/lib/scheduler/residency-planner.ts` | PGY-aware study planner. OKAP ramp-up, pace tracking. |
| `src/lib/sequencer/pgy-classifier.ts` | Classifies cards into PGY levels from BCSC tags. |
| `src/lib/utils/sanitize.ts` | DOMPurify config. Allows `<style>`, `<input>`, `<label>` for mnemonic toggles. |
| `src/lib/version.ts` | `APP_VERSION = "1.8"`, date `"2026-03-21"` |
| `src/app/(app)/dashboard/page.tsx` | Dashboard with residency planner. Recent accuracy from dailyStats. |
| `src/app/(app)/decks/page.tsx` | Deck browser with card counts and study actions. |
| `scripts/beautify-cards.cjs` | Bulk card beautification script (REST API). |

### Directory Layout

```
scripts/
├── beautify-cards.cjs          # Active — bulk Firestore beautification
└── archive/                    # Old import scripts (completed, archived)
    ├── direct-import.cjs
    ├── full-import.cjs
    ├── import-batch1.cjs
    ├── import-batch2.cjs
    ├── import-now.cjs
    ├── import-remaining.cjs
    ├── resume-import.cjs
    └── *.log files
```

### Card Data Structure (Firestore)

```
users/{uid}/decks/{deckId}/cards/{cardId}
├── fields: { Text: "...", Extra: "...", "Personal Notes": "", ... }
├── enhancedFields?: { Text: "<beautified>", Extra: "<beautified>" }
├── modelId: "1659060951898" | "1659060951900" | "1659060951892"
├── ordinal: 0-10 (cloze number for cloze cards)
├── tags: ["#Blue::...", ...]
├── fsrs: { state: 0|1|2|3, due: timestamp, ... }
├── sequencing: { difficultyScore, topicPath, examYield }
└── leech?: { isLeech, lapseCount, ... }
```

### Pre-Beautification Data Flow

```
WITHOUT enhancedFields (current state for all 33K cards):
  card.fields -> renderCard() -> frontHtml/backHtml
    -> CardContent: beautifyCardHtml() -> sanitize -> display

WITH enhancedFields (after beautify-cards.cjs runs):
  card.enhancedFields -> renderCard() -> enhancedFront/enhancedBack
    -> CardContent: skip beautify -> sanitize -> display
```

### 3 Card Models

| Model ID | Name | Type | Notes |
|----------|------|------|-------|
| `1659060951898` | AnKing | Cloze (type=1) | 1 template, `{{cloze:Text}}` format, 6 fields |
| `1659060951900` | Basic-AnKing | Standard (type=0) | 1 template, `{{edit:Front}}` format, 5 fields |
| `1659060951892` | Image Occlusion Enhanced | Standard (type=0) | 12 fields |

### Ordinal Distribution
```
{0: 27462, 1: 3942, 2: 893, 3: 218, 4: 85, 5: 35, 6: 14, 7: 9, 8: 2, 9: 1, 10: 1}
```
16% of cards (5,200) have ordinal > 0. These were broken before the cloze fix.

---

## Known Constraints

- **Firestore Spark plan:** 20K writes/day, reads also rate-limited. Resets at midnight Pacific.
- **iCloud Drive + Git:** Never push/pull from iCloud-synced folders. Clone to `/tmp` first.
- **Git lock files:** iCloud creates `.git/*.lock` files. Clean with `find .git -name "*.lock" -exec rm -f {} \;`
- **Static export:** `output: "export"` in `next.config.ts`. Routes use query params (`/study?id=...`).
- **REST API auth:** Uses Firebase CLI refresh token for server-side Firestore access.
- **Build from /tmp:** Always copy/clone to `/tmp` before running `npm run build` — iCloud path causes issues.

---

## Bugs Fixed (All Versions)

| Bug | Root Cause | Fix |
|-----|-----------|-----|
| Study session freezes | `getDocs()` fetched all 33K cards | Added `limit(270)` query in `use-study-session.ts` |
| "No template found" / empty cards | `model.templates[ordinal]` — cloze models only have 1 template | `templateIndex = model.type === 1 ? 0 : ordinal` in `renderer.ts` |
| Duplicate decks (3 shown) | 2x Blue Ophthalmology + AAO deck from separate imports | Deleted 2 via REST API DELETE, renamed remaining |
| Script/comment artifacts in cards | Anki `<script>` blocks stripped but `// comment` lines leaked | Added regex cleanup in `beautifier.ts:cleanupAnkiHtml()` |
| Build error on dynamic routes | `[deckId]` folders missing `generateStaticParams()` | Deleted dynamic route folders; query-param routes already existed |
| Confusing `isPreBeautified` prop threading | Boolean flag passed through 3 components | Replaced with explicit `enhancedFrontHtml`/`enhancedBackHtml` props |
| Misleading beautifier docstring | Said "Applied during import to all 27,000+ cards" | Updated to reflect dual-path: render-time or pre-baked via script |
| Dashboard recentAccuracy always 0 | Hardcoded `recentAccuracy: 0` with TODO | Computed from last 7 days of `dailyStats` retention rates |

---

## Immediate Next Steps (Priority Order)

1. **Commit uncommitted changes** — 14 files modified this session (see Uncommitted Changes above). Clone to `/tmp`, copy files, commit, push.

2. **Deploy to Cloudflare** — After commit:
   ```bash
   cd /tmp/ophtho-commit
   npm run build && npx wrangler pages deploy out --project-name ophtho-cards
   ```

3. **Run beautification script** after Firestore quota resets:
   ```bash
   cd ophtho-cards && node scripts/beautify-cards.cjs 2>&1 | tee scripts/beautify.log
   ```

4. **Implement PGY subdeck split** — Tag-based UI filtering using existing `pgy-classifier.ts` + `residency-planner.ts`. Zero Firestore writes needed.

---

## Beautification Pipeline Reference (7 Steps)

1. **Cleanup** — Strip `<script>` tags, HTML comments, bare JS comments, Anki artifacts
2. **Key terms** — Wrap standalone acronyms (2-6 letter all-caps) in teal `med-acronym` spans
3. **Lists** — Convert dash-prefixed lines to proper `<ul>` with styled `enhanced-list` class
4. **Category highlighting** — Auto-detect and color-code: drugs (green), anatomy (blue), diseases (red), surgery (purple)
5. **Images** — Add `loading="lazy"` attribute
6. **Spacing** — Add sentence-break spans at period-capital boundaries
7. **Memory enhancement** — Chunking (3-sentence breaks), first-letter cues, DDx contrast highlighting, collapsible mnemonic pearl boxes (answer-side only)

---

## Session Cleanup Log (March 24, 2026)

- Removed iCloud duplicate: `public/_redirects 2`
- Archived 7 old import scripts + 4 log files to `scripts/archive/` (import is complete, scripts no longer needed)
- Only `scripts/beautify-cards.cjs` remains active in `scripts/`
