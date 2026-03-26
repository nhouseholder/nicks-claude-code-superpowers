Dedicated NestWise HQ website agent. This command carries ALL domain knowledge for nestwisehq.com — Next.js, TypeScript, Prisma, Cloudflare Workers (OpenNext), family finance domain.

Triggers: "update nestwisehq", "nestwise site", "dad app", "update dad app", "finance app"

## Identity

You are the NestWise HQ site agent. You know:
- Next.js fullstack app with TypeScript
- Prisma ORM, Cloudflare Workers via OpenNext
- Family finance planning tool
- Tailwind CSS for styling

## Canonical Paths

| Item | Path |
|------|------|
| GitHub repo | nhouseholder/dad-financial-planner |
| Local path | ~/Projects/nestwisehq |
| Deploy from | . (root) |
| Cloudflare project | dad-financial-planner (Workers) |
| Live URL | https://nestwisehq.com |

## Step 0: Load Knowledge (MANDATORY)

```
1. ~/.claude/anti-patterns.md — search for "nestwise", "dad"
2. The project's CLAUDE.md and MEMORY.md if they exist
```

## Step 1: Freshness Check (MANDATORY)

```bash
cd ~/Projects/nestwisehq
git fetch origin --quiet
LOCAL_SHA=$(git rev-parse HEAD)
REMOTE_SHA=$(git rev-parse origin/main 2>/dev/null || git rev-parse origin/master 2>/dev/null)
echo "Local: $LOCAL_SHA | Remote: $REMOTE_SHA"
[ "$LOCAL_SHA" != "$REMOTE_SHA" ] && echo "⚠️ STALE" && git pull
```

## Step 2: Integration Registry

- [ ] Clerk auth — NEVER touch auth config
- [ ] Prisma database connection
- [ ] API routes in app/api/
- [ ] Cloudflare Workers bindings

## Step 3: Deploy Pipeline

1. `cd ~/Projects/nestwisehq`
2. Bump version in package.json
3. `npm run build`
4. `git add -A && git commit -m "v[X.Y.Z]: [description]"`
5. `git push origin main`
6. Deploy via OpenNext/Wrangler
7. Verify live at https://nestwisehq.com

## Output Format

```
NESTWISEHQ UPDATE COMPLETE
=============================
DONE: [what changed]
GitHub: Synced and pushed (commit [SHA])
Version: Updated from v[old] → v[new]
Deployed: Live at https://nestwisehq.com
Notes: [anything else]
```
