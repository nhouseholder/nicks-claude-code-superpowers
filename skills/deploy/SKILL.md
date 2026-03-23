---
name: deploy
description: Deploy projects to Cloudflare Pages/Workers with pre-flight checks, smoke tests, and automatic rollback on failure. Handles linting, testing, building, deploying, verifying, and tagging releases. Use when asked to deploy, ship, release, push to production, or go live.
---

# Deploy Skill

Full deployment pipeline with verification and rollback for Cloudflare-hosted projects.

## Workflow

### 1. Pre-Flight Checks
```bash
# Run linter
npm run lint 2>&1 || { echo "ABORT: Lint failures"; exit 1; }

# Run tests
npm test 2>&1 || { echo "ABORT: Test failures"; exit 1; }

# Build production bundle
npm run build 2>&1 || { echo "ABORT: Build failed"; exit 1; }
```

**ABORT** if any pre-flight check fails. Do not deploy broken code.

### 2. Verify Environment
- Check that required environment variables are set (API keys, tokens)
- Verify wrangler is authenticated: `npx wrangler whoami`
- Test critical API endpoints with lightweight calls if applicable
- Confirm the target environment (production vs staging)
- For Cloudflare Pages: verify `wrangler.toml` config matches target project
- For Cloudflare Workers: check KV namespace bindings, D1 databases, and secrets are configured
- Check `functions/` directory for Pages Functions that may need separate validation

### 3. Snapshot for Rollback
```bash
# Save current deployment info for rollback
CURRENT_DEPLOY=$(npx wrangler pages deployment list --project-name <PROJECT> 2>/dev/null | head -5)
echo "$CURRENT_DEPLOY" > .last_deploy_snapshot
```

### 4. Deploy
```bash
# Deploy to Cloudflare Pages
npx wrangler pages deploy <BUILD_DIR> --project-name <PROJECT> 2>&1 | tee deploy.log
```

Or for Workers:
```bash
npx wrangler deploy 2>&1 | tee deploy.log
```

### 5. Verify Live Site
```bash
# Wait for propagation
sleep 30

# Check the live URL returns 200
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" https://<LIVE_URL>)

if [ "$HTTP_STATUS" != "200" ]; then
  echo "VERIFICATION FAILED: Got HTTP $HTTP_STATUS"
  # Trigger rollback
fi
```

Also verify:
- Key pages load correctly
- API endpoints respond (especially Pages Functions at `/api/` routes)
- No console errors on critical pages (if browser tools available)
- KV cache is accessible (if applicable)
- Workers AI endpoints respond (if applicable)

### 6. Rollback on Failure
If verification fails:
```bash
echo "Rolling back to previous deployment..."
npx wrangler pages deployment rollback --project-name <PROJECT>
echo "ROLLBACK COMPLETE — previous deployment restored"
```

Alert the user immediately about the failed deployment.

### 7. Tag Release on Success
```bash
# Get current version from package.json
VERSION=$(node -p "require('./package.json').version")

# Tag and push
git tag -a "v$VERSION" -m "Release v$VERSION"
git push origin "v$VERSION"

echo "Deployed and tagged v$VERSION"
```

## Quick Deploy Command
For simple deploys without the full pipeline:
```bash
npm run build && npx wrangler pages deploy <BUILD_DIR> --project-name <PROJECT>
```

## iCloud Projects — Build from /tmp

All user projects are in iCloud Drive. Git operations and builds MUST happen from a non-iCloud clone:
1. `git clone <repo> /tmp/<project-name>`
2. Build and deploy from `/tmp/<project-name>`
3. Never `git push` from the iCloud directory

## Known Project Deployments

| Project | Type | Deploy Command | Live URL Pattern |
|---------|------|---------------|-----------------|
| OctagonAI (UFC) | Pages | `wrangler pages deploy dist/` | octagonai.net |
| NHL | Workers/Pages | `wrangler deploy` or `wrangler pages deploy` | diamondpredictions.com |
| NBA | Pages | `wrangler pages deploy dist/` | courtside-ai |
| MyStrainAI | Workers + Pages | `wrangler deploy` (backend) + `wrangler pages deploy` (frontend) | mystrainai.com |
| Enhanced Health AI | Workers (OpenNext) | `wrangler deploy` | enhanced-health-ai |

## Cloudflare-Specific Checks

- **D1 bindings**: Verify `[[d1_databases]]` in wrangler.toml match the production database
- **KV namespaces**: Check `[[kv_namespaces]]` bindings are correct for the environment
- **Secrets**: `wrangler secret list` to verify API keys are set (never commit secrets)
- **Environment vars**: Check `[vars]` in wrangler.toml — production values, not dev defaults
- **Compatibility date**: Ensure `compatibility_date` is recent enough for features used

## Rules
- NEVER deploy without passing tests and lint
- NEVER build or deploy from iCloud Drive — clone to /tmp first
- ALWAYS snapshot current deployment before deploying
- ALWAYS verify the live site after deployment
- ALWAYS rollback on verification failure — don't leave broken production
- ALWAYS run data-consistency-check on any stats/dashboard pages post-deploy
- Use `| tee deploy.log` for all deploy commands
- Confirm with user before deploying to production (unless explicitly told to proceed)
