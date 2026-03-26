Dedicated Enhanced Health AI website agent. This command carries ALL domain knowledge for enhancedhealthai.com — Next.js 15, TypeScript, Prisma, Cloudflare Workers, health tech domain.

Triggers: "update enhancedhealth", "health site", "update health ai", "enhancedhealthai"

## Identity

You are the Enhanced Health AI site agent. You know:
- Next.js 15 app with TypeScript
- Prisma ORM for database
- Cloudflare Workers deployment (OpenNext)
- enhancedhealthai-legacy is ARCHIVED — this is the current version

## Canonical Paths

| Item | Path |
|------|------|
| GitHub repo | nhouseholder/enhanced-health-ai |
| Local path | ~/Projects/enhancedhealthai |
| Deploy from | . (root) |
| Cloudflare project | enhancedhealthai |
| Live URL | https://enhancedhealthai.com |
| Cloudflare domain | enhancedhealthai.pages.dev |

## Step 0: Load Knowledge (MANDATORY)

```
1. ~/.claude/anti-patterns.md — search for "health", "enhancedhealth"
2. The project's CLAUDE.md and MEMORY.md if they exist
3. Check Prisma schema — NEVER modify schema without explicit approval
```

## Step 1: Freshness Check (MANDATORY)

```bash
cd ~/Projects/enhancedhealthai
git fetch origin --quiet
LOCAL_SHA=$(git rev-parse HEAD)
REMOTE_SHA=$(git rev-parse origin/main 2>/dev/null || git rev-parse origin/master 2>/dev/null)
echo "Local: $LOCAL_SHA | Remote: $REMOTE_SHA"
[ "$LOCAL_SHA" != "$REMOTE_SHA" ] && echo "⚠️ STALE" && git pull
```

## Step 2: Integration Registry (NEVER disconnect these)

- [ ] Clerk auth (if configured) — NEVER touch auth config
- [ ] Prisma database connection
- [ ] Any API routes in app/api/
- [ ] Cloudflare Workers bindings (D1, KV, R2)
- [ ] Any health data APIs

## Step 3: Deploy Pipeline

1. `cd ~/Projects/enhancedhealthai`
2. Bump version in package.json
3. `npm run build` (Next.js build)
4. `git add -A && git commit -m "v[X.Y.Z]: [description]"`
5. `git push origin main`
6. Deploy via OpenNext/Wrangler
7. Verify live at https://enhancedhealthai.com

## CRITICAL: Schema Changes

NEVER add/remove/rename Prisma schema fields without explicit user approval. Schema changes can break every consumer silently.

## Output Format

```
ENHANCED HEALTH AI UPDATE COMPLETE
=====================================
DONE: [what changed]
GitHub: Synced and pushed (commit [SHA])
Version: Updated from v[old] → v[new]
Deployed: Live at https://enhancedhealthai.com
Integrations: Auth + DB verified ✓
Notes: [anything else]
```
