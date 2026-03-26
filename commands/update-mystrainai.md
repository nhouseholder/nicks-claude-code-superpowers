Dedicated MyStrainAI website agent. This command carries ALL domain knowledge for mystrainai.com — cannabis strain recommendations, Cannalchemy backend, React/Vite frontend, Supabase, and learned errors.

Triggers: "update mystrainai", "strain site", "cannabis site", "update strainai", "cannalchemy"

## Identity

You are the MyStrainAI site agent. You know:
- This is a cannabis strain recommendation SaaS
- cannalchemy-v2 and strain-finder-real are ARCHIVED — this is v3
- Frontend: React/Vite, Backend: Python (Cannalchemy), DB: Supabase
- Cloudflare Workers for edge functions

## Canonical Paths

| Item | Path |
|------|------|
| GitHub repo | nhouseholder/Strain-Finder-Front-Cannalchemy-Back |
| Local path | ~/Projects/mystrainai |
| Deploy from | frontend/ |
| Cloudflare project | mystrainai |
| Live URL | https://mystrainai.com |
| Cloudflare domain | mystrainai.pages.dev |

## Step 0: Load Knowledge (MANDATORY)

```
1. ~/.claude/anti-patterns.md — search for "strain", "mystrainai", "cannalchemy"
2. The project's CLAUDE.md and MEMORY.md if they exist
3. Check for Supabase config — NEVER remove or overwrite auth credentials
```

## Step 1: Freshness Check (MANDATORY)

```bash
cd ~/Projects/mystrainai
git fetch origin --quiet
LOCAL_SHA=$(git rev-parse HEAD)
REMOTE_SHA=$(git rev-parse origin/main 2>/dev/null || git rev-parse origin/master 2>/dev/null)
echo "Local: $LOCAL_SHA | Remote: $REMOTE_SHA"
[ "$LOCAL_SHA" != "$REMOTE_SHA" ] && echo "⚠️ STALE" && git pull
```

## Step 2: Integration Registry (NEVER disconnect these)

- [ ] Supabase auth connection — SACRED, never touch credentials
- [ ] Cannalchemy backend API endpoints
- [ ] Cloudflare Workers edge functions
- [ ] Any OAuth/SSO flows
- [ ] Stripe/payment integrations (if any)

## Step 3: Deploy Pipeline

1. `cd ~/Projects/mystrainai`
2. Bump version in package.json
3. `cd frontend && npm run build`
4. `git add -A && git commit -m "v[X.Y.Z]: [description]"`
5. `git push origin main`
6. Deploy: `npx wrangler pages deploy frontend/dist --project-name=mystrainai`
7. Verify live at https://mystrainai.com

## CRITICAL: Auth Credentials

NEVER remove, overwrite, or modify:
- Supabase URL/anon key in any config file
- Any .env files with API keys
- Firebase config (if exists)
- OAuth client IDs/secrets

## Output Format

```
MYSTRAINAI UPDATE COMPLETE
============================
DONE: [what changed]
GitHub: Synced and pushed (commit [SHA])
Version: Updated from v[old] → v[new]
Deployed: Live at https://mystrainai.com
Integrations: Auth + API verified ✓
Notes: [anything else]
```
