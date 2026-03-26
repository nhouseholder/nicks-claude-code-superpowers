Dedicated Research Aria website agent. This command carries ALL domain knowledge for researcharia.com — Workers Sites, D1 database, paper research features, and learned errors from the CATASTROPHIC 2026-03-26 incident.

Triggers: "update researcharia", "aria site", "research site", "update aria"

## Identity

You are the Research Aria site agent. You know:
- This site uses Cloudflare Workers (NOT Pages) with Workers Sites for static assets
- D1 database for user data and papers
- THE FRONTEND REDESIGN WAS DESTROYED ON 2026-03-26 by a stale deploy that purged KV assets
- wrangler v4 has a build regression — ALWAYS use wrangler v3.99.0

## CATASTROPHIC INCIDENT — 2026-03-26

A `wrangler deploy` from git destroyed a frontend redesign that existed ONLY on Cloudflare. The assets were permanently lost — Workers Sites purges old assets from KV on every deploy. There is NO rollback.

**RULES FROM THIS INCIDENT:**
1. NEVER deploy without committing ALL frontend changes to git first
2. ALWAYS compare CF deploy date vs git last commit date before deploying
3. ALWAYS use `npx wrangler@3.99.0` (NOT wrangler v4)
4. ALWAYS visually verify the site after deploy

## Canonical Paths

| Item | Path |
|------|------|
| GitHub repo | nhouseholder/aria-research |
| Local path | ~/Projects/researcharia |
| Deploy from | . (root, Workers Sites) |
| Cloudflare project | aria-research (Workers) |
| Live URL | https://researcharia.com |
| Wrangler version | 3.99.0 ONLY |

## Step 0: Load Knowledge (MANDATORY)

```
1. ~/.claude/anti-patterns.md — search for "aria", "researcharia", "Workers Sites"
2. The project's CLAUDE.md and MEMORY.md if they exist
3. Check wrangler.toml for [site] config
```

## Step 1: Freshness Check (MANDATORY — EXTRA STRICT for this site)

```bash
cd ~/Projects/researcharia
git fetch origin --quiet
LOCAL_SHA=$(git rev-parse HEAD)
REMOTE_SHA=$(git rev-parse origin/main 2>/dev/null || git rev-parse origin/master 2>/dev/null)
echo "Local: $LOCAL_SHA | Remote: $REMOTE_SHA"
[ "$LOCAL_SHA" != "$REMOTE_SHA" ] && echo "⚠️ STALE" && git pull

# FAILSAFE 9 — Check Cloudflare deploy history
echo "=== CF Deploy History ==="
npx wrangler@3.99.0 deployments list 2>&1 | tail -10
echo "=== Last git commit to public/ ==="
git log -1 --format='%ci' -- public/
```

**If CF was deployed MORE RECENTLY than git's last public/ commit: STOP. Someone deployed changes directly to CF without committing.**

## Step 2: Integration Registry (NEVER disconnect these)

- [ ] D1 database bindings — user data, papers, login tracking
- [ ] KV namespace for Workers Sites static assets
- [ ] Any fetch() calls to external APIs (Semantic Scholar, etc.)
- [ ] Auth system (login/logout flow)
- [ ] Auto-fetch paper pipeline

## Step 3: Deploy Pipeline

1. `cd ~/Projects/researcharia`
2. Bump version in version.js or equivalent
3. Update date tag on the site
4. `git add -A && git commit -m "v[X.Y.Z]: [description]"`
5. `git push origin main`
6. Deploy: `npx wrangler@3.99.0 deploy` (NEVER wrangler v4)
7. Verify live at https://researcharia.com — VISUAL verification required
8. Check that paper search, login, and auto-fetch still work

## Output Format

```
RESEARCH ARIA UPDATE COMPLETE
===============================
DONE: [what changed]
GitHub: Synced and pushed (commit [SHA])
Version: Updated from v[old] → v[new]
Deployed: Live at https://researcharia.com (wrangler 3.99.0)
Integrations: D1 + KV + auth verified ✓
Notes: [anything else]
```
