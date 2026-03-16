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
- API endpoints respond
- No console errors on critical pages (if browser tools available)

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

## Rules
- NEVER deploy without passing tests and lint
- ALWAYS snapshot current deployment before deploying
- ALWAYS verify the live site after deployment
- ALWAYS rollback on verification failure — don't leave broken production
- Use `| tee deploy.log` for all deploy commands
- Confirm with user before deploying to production (unless explicitly told to proceed)
