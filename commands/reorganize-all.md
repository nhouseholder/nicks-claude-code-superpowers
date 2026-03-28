One-time reorganization of ALL project directories into `~/Projects/` with fresh GitHub clones. Archives stale iCloud copies. Nothing is deleted.

**SECURITY: Revoke the GitHub PAT exposed in Recipes AI/recipes-app remote URL (ghp_C9EC...) at https://github.com/settings/tokens BEFORE running this.**

**Prerequisites:**
1. Close ALL Claude sessions except one (the one running this command)
2. Verify no sessions running in project directories:
```bash
lsof 2>/dev/null | grep "Mobile Documents.*claude" | grep -v "superpowers" | head -10
# Must return empty (superpowers session is fine)
```

## The Plan

### Target Structure
```
~/Projects/
├── sports/
│   ├── ufc-predict/              ← nhouseholder/ufc-predict
│   ├── diamond-predictions/      ← nhouseholder/diamond-predictions (MLB)
│   ├── mlb-predict/              ← nhouseholder/mlb-predict
│   ├── courtside-ai/             ← nhouseholder/courtside-ai (NBA/NCAA)
│   ├── icebreaker-ai/            ← nhouseholder/icebreaker-ai (NHL)
│   ├── collegeedge-ai/           ← nhouseholder/collegeedge-ai (NCAA)
│   ├── march-madness-2026/       ← nhouseholder/march-madness-2026
│   ├── significant-bets/         ← nhouseholder/significant-bets
│   ├── nfl-draft-predictor/      ← nhouseholder/nfl-draft-predictor
│   └── loss-analyst/             ← nhouseholder/loss-analyst
├── health/
│   ├── enhanced-health-ai/       ← nhouseholder/enhanced-health-ai
│   └── ophtho-cards/             ← nhouseholder/ophtho-cards
├── cannabis/
│   ├── strain-finder/            ← nhouseholder/Strain-Finder-Front-Cannalchemy-Back
│   ├── strain-finder-real/       ← nhouseholder/strain-finder-real
│   └── cannalchemy-v2/           ← nhouseholder/cannalchemy-v2
├── apps/
│   ├── dad-financial-planner/    ← nhouseholder/dad-financial-planner
│   ├── aria-research/            ← nhouseholder/aria-research
│   ├── all-things-ai/            ← nhouseholder/all-things-ai (already here)
│   ├── recipe-cards/             ← nhouseholder/recipe-cards
│   └── recipes-app/              ← nhouseholder/recipes-app
├── tools/
│   ├── claude-glm-router/        ← nhouseholder/claude-glm-router
│   └── windsurf-skills-only/     ← nhouseholder/windsurf-skills-only (already here)
├── friends-bday/                 ← (no remote, keep as-is)
└── strain-tracker/               ← (2incertus org, move from ~/ root)

iCloud Drive (AFTER cleanup):
├── Personal files (resumes, medical, photos, etc.) ← UNTOUCHED
├── superpowers/                   ← skills repo, stays here
└── _archived_projects/            ← ALL old project directories moved here
    ├── UFC Algs.ARCHIVED/
    ├── UFC App 3.0.ARCHIVED/
    ├── octagonai.ARCHIVED/
    ├── MLB Algs.ARCHIVED/
    ├── NBA Alg.ARCHIVED/
    ├── NBA AI.ARCHIVED/
    ├── NHL Alg.ARCHIVED/
    ├── NCAA Alg.ARCHIVED/
    ├── Dad App.ARCHIVED/
    ├── SignificantBets.ARCHIVED/
    ├── Strains AI.ARCHIVED/
    ├── strain finder.ARCHIVED/
    ├── enhanced health ai.ARCHIVED/
    ├── Recipes AI.ARCHIVED/
    ├── New Anki.ARCHIVED/
    ├── All Things AI.ARCHIVED/
    ├── NFL Draft.ARCHIVED/
    ├── ARIA.ARCHIVED/
    ├── march madness 2026.ARCHIVED/
    └── legacy-scripts/             ← loose .py files
```

## Step 1: Create Directory Structure

```bash
mkdir -p ~/Projects/{sports,health,cannabis,apps,tools}
```

## Step 2: Fresh Clone All Active Repos

```bash
# Sports
cd ~/Projects/sports
git clone https://github.com/nhouseholder/ufc-predict.git
git clone https://github.com/nhouseholder/diamond-predictions.git
git clone https://github.com/nhouseholder/mlb-predict.git
git clone https://github.com/nhouseholder/courtside-ai.git
git clone https://github.com/nhouseholder/icebreaker-ai.git
git clone https://github.com/nhouseholder/collegeedge-ai.git
git clone https://github.com/nhouseholder/march-madness-2026.git
git clone https://github.com/nhouseholder/significant-bets.git
git clone https://github.com/nhouseholder/nfl-draft-predictor.git
git clone https://github.com/nhouseholder/loss-analyst.git

# Health
cd ~/Projects/health
git clone https://github.com/nhouseholder/enhanced-health-ai.git
git clone https://github.com/nhouseholder/ophtho-cards.git

# Cannabis
cd ~/Projects/cannabis
git clone https://github.com/nhouseholder/Strain-Finder-Front-Cannalchemy-Back.git strain-finder
git clone https://github.com/nhouseholder/strain-finder-real.git
git clone https://github.com/nhouseholder/cannalchemy-v2.git

# Apps
cd ~/Projects/apps
git clone https://github.com/nhouseholder/dad-financial-planner.git
git clone https://github.com/nhouseholder/aria-research.git
git clone https://github.com/nhouseholder/recipe-cards.git
git clone https://github.com/nhouseholder/recipes-app.git

# Tools
cd ~/Projects/tools
git clone https://github.com/nhouseholder/claude-glm-router.git
```

## Step 3: Move Existing ~/Projects/ Items

```bash
# all-things-ai already exists in ~/Projects/ — move to apps/
mv ~/Projects/all-things-ai ~/Projects/all-things-ai

# windsurf-skills-only — move to tools/
mv ~/Projects/windsurf-skills-only ~/Projects/windsurf-skills-only

# friends-bday — keep at root
# (already at ~/Projects/friends-bday)

# strain-tracker from ~/ root — move to ~/Projects/
mv ~/strain-tracker ~/Projects/strain-tracker

# ufc-predict from ~/ root — archive (ancient v10.70)
mv ~/ufc-predict ~/ufc-predict.ARCHIVED
echo "# ARCHIVED $(date) — v10.70, hundreds of commits behind" > ~/ufc-predict.ARCHIVED/ARCHIVED_README.md
```

## Step 4: Preserve .claude/ Settings

```bash
ICLOUD="/Users/nicholashouseholder/Library/Mobile Documents/com~apple~CloudDocs"

# Copy .claude/ project settings from iCloud locations to new canonical locations
# Only copy if the new location doesn't already have .claude/
for pair in \
  "UFC Algs:sports/ufc-predict" \
  "enhanced health ai:health/enhanced-health-ai" \
  "NHL Alg:sports/icebreaker-ai" \
  "NBA Alg:sports/courtside-ai" \
  "MLB Algs:sports/mlb-predict" \
  "Dad App:apps/dad-financial-planner" \
  "SignificantBets:sports/significant-bets" \
  "NCAA Alg:sports/collegeedge-ai"; do

  src="${pair%%:*}"
  dst="${pair##*:}"
  if [ -d "$ICLOUD/$src/.claude" ] && [ ! -d "$HOME/Projects/$dst/.claude" ]; then
    cp -r "$ICLOUD/$src/.claude" "$HOME/Projects/$dst/.claude"
    echo "Copied .claude/ settings: $src → $dst"
  fi
done
```

## Step 5: Archive ALL iCloud Project Directories

```bash
ICLOUD="/Users/nicholashouseholder/Library/Mobile Documents/com~apple~CloudDocs"
ARCHIVE="$ICLOUD/_archived_projects"
mkdir -p "$ARCHIVE/legacy-scripts"

# Archive project directories (rename, don't delete)
for dir in \
  "UFC Algs" "UFC App 3.0" "octagonai" \
  "MLB Algs" "NBA Alg" "NBA AI" "NHL Alg" "NCAA Alg" "NCAA test" \
  "Dad App" "SignificantBets" \
  "Strains AI" "strain finder" \
  "enhanced health ai" \
  "Recipes AI" "New Anki" \
  "All Things AI" "NFL Draft" "ARIA" \
  "march madness 2026" "screenprism ai" \
  "Nest Wise" "Anahit App PHD" \
  "super powers" "ai-summary"; do

  if [ -d "$ICLOUD/$dir" ]; then
    mv "$ICLOUD/$dir" "$ARCHIVE/${dir}.ARCHIVED"
    echo "# ARCHIVED $(date)" > "$ARCHIVE/${dir}.ARCHIVED/ARCHIVED_README.md"
    echo "# Canonical location: ~/Projects/ (fresh GitHub clone)" >> "$ARCHIVE/${dir}.ARCHIVED/ARCHIVED_README.md"
    echo "# DO NOT open Claude sessions from this directory" >> "$ARCHIVE/${dir}.ARCHIVED/ARCHIVED_README.md"
    echo "Archived: $dir"
  fi
done

# Move loose .py files
for f in "$ICLOUD/A UFC"*.py "$ICLOUD/A MLB"*.py "$ICLOUD/UFC backtester"*.py "$ICLOUD/UFC system"*.py "$ICLOUD/__UFC"*.py "$ICLOUD/_UFC"*.py "$ICLOUD/UFC Backtester"*.py; do
  [ -f "$f" ] && mv "$f" "$ARCHIVE/legacy-scripts/"
done
echo "Moved loose scripts to archive"

# Move loose UFC PDFs
for f in "$ICLOUD/UFC Backtester"*.pdf "$ICLOUD/_UFC"*.pdf; do
  [ -f "$f" ] && mv "$f" "$ARCHIVE/legacy-scripts/"
done
```

## Step 6: Archive Stale ~/Projects/ Items

```bash
mv ~/Projects/ufc-predict-local ~/Projects/ufc-predict-local.ARCHIVED 2>/dev/null
echo "# ARCHIVED $(date) — v10.71" > ~/Projects/ufc-predict-local.ARCHIVED/ARCHIVED_README.md 2>/dev/null

# ~/Projects/SignificantBets (no git) — archive
mv ~/Projects/SignificantBets ~/Projects/SignificantBets.ARCHIVED 2>/dev/null

# ~/Projects/loss-analyst (no git, if it exists separately)
# Only archive if we successfully cloned a fresh one
[ -d ~/Projects/loss-analyst ] && [ -d ~/Projects/loss-analyst ] && \
  mv ~/Projects/loss-analyst ~/Projects/loss-analyst.ARCHIVED 2>/dev/null
```

## Step 7: Clean /tmp/

```bash
rm -rf /tmp/ufc-predict-* /tmp/ufc-build /tmp/ufc-push /tmp/octagonai-* /tmp/mmalogic-fresh
rm -rf /tmp/superpowers-sync /tmp/superpowers-handoff /tmp/ehai-* /tmp/diamond-*
rm -f /tmp/ufc_pred_*.log /tmp/mmalogic_*.log /tmp/mmalogic_*.html /tmp/prediction_output.log
rm -f /tmp/diamond-predict-daily.*
echo "Cleaned /tmp/"
```

## Step 8: Fix Security Issue

```bash
# Fix the exposed token in recipes-app (the new clone won't have it, but verify)
cd ~/Projects/recipes-app
git remote set-url origin https://github.com/nhouseholder/recipes-app.git
echo "Fixed recipes-app remote URL (removed exposed PAT)"
```

## Step 9: Verify

```bash
echo "=== CANONICAL PROJECTS ==="
for category in sports health cannabis apps tools; do
  echo ""
  echo "--- $category ---"
  for dir in ~/Projects/$category/*/; do
    name=$(basename "$dir")
    sha=$(cd "$dir" && git log -1 --format="%h" 2>/dev/null || echo "no git")
    echo "  $name ($sha)"
  done
done

echo ""
echo "=== ARCHIVED ==="
ls "$ICLOUD/_archived_projects/" 2>/dev/null | head -25

echo ""
echo "=== HOME ROOT (should be clean) ==="
ls -d ~/ufc-predict* ~/strain-tracker 2>/dev/null || echo "Clean"

echo ""
echo "=== /tmp (should be clean) ==="
ls /tmp/*ufc* /tmp/*mma* /tmp/*octagon* /tmp/*superpowers* /tmp/*ehai* 2>/dev/null || echo "Clean"
```

## Step 10: Update Memory & Canonical Paths

After reorganization, update `~/.claude/memory/topics/ufc_canonical_paths.md` and all references to use `~/Projects/mmalogic/` as the canonical path.

Also update `~/.claude/CLAUDE.md` session orientation rules to reference `~/Projects/` structure.

## Post-Reorganization Rules

1. **ALL new sessions open from `~/Projects/<category>/<repo>/`** — never from iCloud
2. **GitHub is the source of truth** — if local is behind, `git pull` or re-clone
3. **iCloud is for personal files only** — resumes, medical records, photos, documents
4. **`_archived_projects/` is read-only** — never open sessions from there
5. **One repo = one directory** — no more -1, -2, -3 suffixes
6. **`superpowers/` stays in iCloud** — it's the skills repo, synced via /tmp clones
