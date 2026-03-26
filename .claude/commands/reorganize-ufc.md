One-time reorganization of all UFC/MMALogic directories into a single canonical location. Run this ONCE after closing all UFC-related Claude sessions.

**Prerequisites:** Close ALL Claude sessions in `UFC Algs/` first. Check with:
```bash
lsof +D "/Users/nicholashouseholder/Library/Mobile Documents/com~apple~CloudDocs/UFC Algs/" 2>/dev/null | grep claude
# Must return empty
```

## Step 1: Fresh Clone to Canonical Location

```bash
# Create the ONE canonical location
cd ~/Projects
rm -rf ufc-predict  # Remove if exists (it shouldn't yet)
git clone https://github.com/nhouseholder/ufc-predict.git ufc-predict
cd ufc-predict
echo "Canonical clone: $(git log --oneline -1)"
echo "Version: $(cat webapp/frontend/src/version.js 2>/dev/null)"
```

## Step 2: Archive All Stale Directories

```bash
ICLOUD="/Users/nicholashouseholder/Library/Mobile Documents/com~apple~CloudDocs"
ARCHIVE="$ICLOUD/UFC Algs/archive"
mkdir -p "$ARCHIVE/legacy-scripts"
mkdir -p "$ARCHIVE/legacy-apps"

# 2a. Archive the stale iCloud clone (101 commits behind)
mv "$ICLOUD/UFC Algs/ufc-predict" "$ICLOUD/UFC Algs/ufc-predict.ARCHIVED"
echo "# ARCHIVED $(date)" > "$ICLOUD/UFC Algs/ufc-predict.ARCHIVED/ARCHIVED_README.md"
echo "# Superseded by ~/Projects/ufc-predict/ (fresh GitHub clone)" >> "$ICLOUD/UFC Algs/ufc-predict.ARCHIVED/ARCHIVED_README.md"
echo "# This directory was 101 commits behind GitHub as of 2026-03-25" >> "$ICLOUD/UFC Algs/ufc-predict.ARCHIVED/ARCHIVED_README.md"

# 2b. Archive the very stale ~/Projects clone (v10.71)
mv ~/Projects/ufc-predict-local ~/Projects/ufc-predict-local.ARCHIVED
echo "# ARCHIVED $(date) — was at v10.71, hundreds of commits behind" > ~/Projects/ufc-predict-local.ARCHIVED/ARCHIVED_README.md

# 2c. Archive octagonai (loose files, no git)
mv "$ICLOUD/octagonai" "$ICLOUD/octagonai.ARCHIVED"
echo "# ARCHIVED $(date) — loose scripts, no git repo, data files may be stale" > "$ICLOUD/octagonai.ARCHIVED/ARCHIVED_README.md"

# 2d. Archive UFC App 3.0 (ancient prototype)
mv "$ICLOUD/UFC App 3.0" "$ICLOUD/UFC App 3.0.ARCHIVED"
echo "# ARCHIVED $(date) — ancient prototype, no git repo" > "$ICLOUD/UFC App 3.0.ARCHIVED/ARCHIVED_README.md"

# 2e. Move loose .py files to archive
for f in "$ICLOUD/A UFC"*.py "$ICLOUD/UFC backtester"*.py "$ICLOUD/UFC system"*.py "$ICLOUD/__UFC"*.py "$ICLOUD/_UFC"*.py "$ICLOUD/UFC Backtester"*.py; do
  [ -f "$f" ] && mv "$f" "$ARCHIVE/legacy-scripts/"
done
echo "Moved loose .py files to archive/legacy-scripts/"
```

## Step 3: Clean /tmp/ Clones

```bash
rm -rf /tmp/ufc-predict-* /tmp/ufc-build /tmp/ufc-push /tmp/octagonai-* /tmp/mmalogic-fresh
rm -f /tmp/ufc_pred_*.log /tmp/mmalogic_*.log /tmp/mmalogic_*.html /tmp/prediction_output.log
echo "Cleaned /tmp/"
```

## Step 4: Preserve .claude/ Settings

The `UFC Algs/.claude/` directory has project-specific settings. Copy them to the new location:
```bash
cp -r "$ICLOUD/UFC Algs/.claude" ~/Projects/ufc-predict/.claude 2>/dev/null
# Merge any settings, don't overwrite if ufc-predict already has .claude/
```

## Step 5: Update References

Update canonical paths memory:
```bash
# The new canonical path is ~/Projects/ufc-predict/
# Webapp: ~/Projects/ufc-predict/webapp/frontend/
# Algorithm: ~/Projects/ufc-predict/
# Data: ~/Projects/ufc-predict/webapp/frontend/public/data/
```

Update `~/.claude/memory/topics/ufc_canonical_paths.md` with the new location.

## Step 6: Verify

```bash
echo "=== Canonical ==="
cd ~/Projects/ufc-predict && git log --oneline -1
cat webapp/frontend/src/version.js 2>/dev/null

echo ""
echo "=== Archived ==="
ls -d "$ICLOUD"/*.ARCHIVED "$ICLOUD/UFC Algs"/*.ARCHIVED ~/Projects/*.ARCHIVED 2>/dev/null

echo ""
echo "=== /tmp clean ==="
ls /tmp/*ufc* /tmp/*mma* /tmp/*octagon* 2>/dev/null || echo "Clean"
```

## Post-Reorganization

After running this:
1. Open new Claude sessions from `~/Projects/ufc-predict/` (NOT iCloud)
2. The `/mmalogic` command will clone fresh from GitHub anyway, so it works regardless
3. If you need to find old files, they're in `UFC Algs/archive/` or the `.ARCHIVED` directories
4. Nothing is deleted — everything is archived and findable

## Final Directory Structure

```
~/Projects/
  ufc-predict/                    ← CANONICAL (fresh GitHub clone)
    webapp/frontend/              ← deploy from here
    .claude/                      ← project settings

~/Library/Mobile Documents/com~apple~CloudDocs/
  UFC Algs/
    archive/
      legacy-scripts/             ← all loose .py files
      legacy-apps/                ← if needed
    ufc-predict.ARCHIVED/         ← old iCloud clone (DO NOT USE)
    HANDOFF.md
  octagonai.ARCHIVED/             ← old loose files (DO NOT USE)
  UFC App 3.0.ARCHIVED/           ← ancient prototype (DO NOT USE)

~/Projects/
  ufc-predict-local.ARCHIVED/     ← very old clone (DO NOT USE)
```
