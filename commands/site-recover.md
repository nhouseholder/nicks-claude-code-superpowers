Recover the last working version of a site after a destructive deploy, accidental overwrite, or data loss. This is the EMERGENCY command — use when production is broken and you need to get back to a known-good state.

Triggers: "recover the site", "rollback", "site is broken", "deploy destroyed it", "revert to working version", "undo the deploy"

**This command tries EVERY recovery vector. Do NOT give up after one fails.**

---

## Phase 0: Stop the Bleeding (~30 seconds)

Do NOT deploy anything else. Do NOT make changes. Assess first.

```bash
PROJECT_NAME=$(basename "$(pwd)")
echo "=== EMERGENCY RECOVERY ==="
echo "Project: $PROJECT_NAME"
echo "Directory: $(pwd)"
echo "Git branch: $(git branch --show-current 2>/dev/null)"
echo "Last commit: $(git log -1 --format='%ci %s' 2>/dev/null)"
echo "Git status: $(git status --short 2>/dev/null | wc -l | tr -d ' ') changed files"
```

## Phase 1: Try ALL Recovery Vectors (in order of speed)

### Vector 1: Cloudflare Deployment Rollback (~1 min)
**This is the fastest recovery.** Cloudflare keeps deployment history.

For **Cloudflare Pages** projects:
```bash
# List recent deployments
npx wrangler pages deployment list --project-name=<PROJECT_NAME> 2>/dev/null | head -20

# Rollback to a specific deployment
npx wrangler pages deployment rollback --project-name=<PROJECT_NAME> <DEPLOYMENT_ID>
```

For **Cloudflare Workers** projects:
```bash
# List recent deployments (Workers keeps versions)
npx wrangler deployments list 2>/dev/null | head -20

# Rollback to previous deployment
npx wrangler rollback
# OR rollback to a specific version
npx wrangler rollback <DEPLOYMENT_ID>
```

**Check the timestamps.** Find the deployment from BEFORE the bad deploy. Roll back to that one.

### Vector 2: Git History Recovery (~2 min)
If the good version WAS committed to git at some point:

```bash
# Search for the last commit that touched frontend/public files
git log --oneline --all -- "public/" "dist/" "src/" "*.html" "*.css" "*.js" | head -20

# Check all branches — the good version might be on a feature branch
git branch -a

# Check stashes
git stash list

# Check reflog — even deleted commits are recoverable for 90 days
git reflog --all | head -20

# If you find the good commit:
git show <COMMIT_SHA>:path/to/file > recovered_file
# OR checkout the entire state:
git checkout <COMMIT_SHA> -- public/ src/
```

### Vector 3: Cloudflare KV/R2 Asset Recovery (~3 min)
Workers Sites stores assets in KV. Even if marked "stale," they may still exist.

```bash
# List KV namespaces
npx wrangler kv namespace list 2>/dev/null

# List ALL keys in the assets namespace (stale ones may still be there)
npx wrangler kv key list --namespace-id=<NAMESPACE_ID> 2>/dev/null

# Download a specific asset by key
npx wrangler kv key get --namespace-id=<NAMESPACE_ID> "<KEY>" > recovered_asset
```

For R2-based sites:
```bash
# List R2 buckets
npx wrangler r2 bucket list 2>/dev/null

# List objects in bucket
npx wrangler r2 object list <BUCKET_NAME> 2>/dev/null
```

### Vector 4: Local Machine Recovery (~2 min)
The good files might still be on the local machine — iCloud, /tmp, old worktrees.

```bash
# Check iCloud for copies
find ~/Library/Mobile\ Documents/com~apple~CloudDocs/ -path "*${PROJECT_NAME}*" -name "*.html" -o -name "*.jsx" -o -name "*.css" 2>/dev/null | head -20

# Check _archived_projects
find ~/Library/Mobile\ Documents/com~apple~CloudDocs/_archived_projects/ -path "*${PROJECT_NAME}*" 2>/dev/null | head -10

# Check /tmp for old clones
find /tmp -path "*${PROJECT_NAME}*" -name "*.html" -o -name "*.jsx" 2>/dev/null | head -10

# Check worktrees
ls .claude/worktrees/ 2>/dev/null
git worktree list 2>/dev/null

# Check macOS Time Machine (if available)
ls /Volumes/Time\ Machine\ Backups/ 2>/dev/null && echo "Time Machine available!"
tmutil listbackups 2>/dev/null | tail -5
```

### Vector 5: Browser Cache / CDN Cache Recovery (~3 min)
The old version may still be cached somewhere.

```bash
# Check if Cloudflare CDN still has cached version
curl -sI "https://<SITE_URL>" | grep -i "cf-cache\|age\|last-modified"

# Google Cache — might have a snapshot
echo "Check: https://webcache.googleusercontent.com/search?q=cache:<SITE_URL>"

# Wayback Machine — might have a recent snapshot
echo "Check: https://web.archive.org/web/*/<SITE_URL>"
```

Also use Claude in Chrome to check:
- Browser cache (navigate to the site with dev tools open, check cached resources)
- Service worker cache (if the site has a SW, old assets may be cached)

### Vector 6: GitHub Actions Artifacts (~2 min)
If the site was built by CI, the build artifacts may still be downloadable.

```bash
# List recent workflow runs
gh run list --limit 10 2>/dev/null

# Download artifacts from a specific run
gh run download <RUN_ID> 2>/dev/null
```

### Vector 7: Reconstruct from Screenshots/Memory (~varies)
Last resort. If the user has screenshots, handoff documents, or the site was described in detail:
- Read all handoff documents for this project
- Read project memory files
- Check if any agent took screenshots during the prior session
- Ask the user for any screenshots they have
- Rebuild from those references

## Phase 2: Verify Recovery

After ANY recovery vector succeeds:

1. **Check the live site** — use Claude in Chrome or curl to verify the correct version is showing
2. **Compare to what the user expects** — ask them to confirm it's right
3. **Commit the recovered state to git immediately** — so this never happens again
4. **Push to GitHub** — git is the source of truth, make it match production

```bash
git add -A
git commit -m "RECOVERY: restore [version] after accidental overwrite

Recovered via: [which vector worked]
Previous bad deploy: [commit SHA or deployment ID]
Verified: [how you confirmed it's correct]"
git push origin main
```

## Phase 3: Post-Recovery

1. **Snapshot the current production state** — download all production assets locally as a backup
2. **Log the incident** in anti-patterns.md
3. **Verify all deploy safeguards are in place** — run through FAILSAFE 3, 5, 9

## Output

```
SITE RECOVERY COMPLETE
======================
Site: [URL]
Recovery vector: [which one worked]
Recovered from: [source — CF rollback, git SHA, local files, etc.]
Verified: [how confirmed — screenshot, curl, browser check]
Committed: [git SHA] → pushed to GitHub ✓
Time to recover: [N] minutes

Safeguards verified:
  - FAILSAFE 3 (version check): ✓
  - FAILSAFE 5 (commit before deploy): ✓
  - Deploy guard hook: ✓
```

## Design Principles

- **Try EVERY vector before declaring unrecoverable.** The other agent tried 1 vector (KV) and gave up. There are 7.
- **Speed matters.** Cloudflare rollback is fastest — try it first.
- **Commit immediately after recovery.** The whole reason this happened was uncommitted production code.
- **Never say "no recovery path"** without trying all 7 vectors. If all 7 genuinely fail, THEN say it — with evidence of what you tried.
- **Believe the user.** If they say the site is broken, it's broken. Don't argue. Recover.
