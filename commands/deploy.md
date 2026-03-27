Full deployment pipeline: pre-flight checks, build, deploy to Cloudflare Pages/Workers, post-deploy verification, automatic rollback on failure.

## Skill Pipeline (load at each phase — read SKILL.md, don't "apply mentally")

| Phase | Skills to Load |
|-------|---------------|
| Phase 0 | `website-guardian` (directory verification, version check) |
| Phase 1-2 | `code-reviewer` (pre-flight quality check) |
| Phase 3 | `deploy` skill protocol |
| Phase 4 | `qa-gate` + `screenshot-dissector` (post-deploy verification) |
| Phase 5 | `error-memory` (log any failures) |

## Arguments
- `$ARGUMENTS` = project directory, environment (prod/staging), or specific flags

## Phase 0: Directory Verification (MANDATORY — prevents catastrophic deploys)

**Before ANYTHING else**, verify you're deploying from the correct directory:
```bash
# Check version in current directory
cat version.js 2>/dev/null || cat src/version.js 2>/dev/null || node -e "console.log(require('./package.json').version)" 2>/dev/null
echo "Deploy directory: $(pwd)"
```

**STOP if ANY of these are true:**
- Version number is unexpectedly old (e.g., v10.x when you expect v11.x)
- You're in a root `webapp/` when a `ufc-predict/webapp/` exists (UFC project: canonical source is ALWAYS `ufc-predict/webapp/frontend/`)
- The directory has no recent git commits (check `git log --oneline -3`)
- `package.json` version doesn't match what's expected

**This check exists because deploying from the wrong directory OVERWROTE v11.9.3 with v10.68, reverting months of production work.**

## Phase 1: Pre-flight Checks
```bash
# Verify clean git state
UNCOMMITTED=$(git status --porcelain 2>/dev/null | wc -l | tr -d ' ')
if [ "$UNCOMMITTED" != "0" ]; then
  echo "WARNING: $UNCOMMITTED uncommitted changes"
  git status --short
fi

# Current branch
BRANCH=$(git branch --show-current 2>/dev/null)
echo "Branch: $BRANCH"

# Node.js version
node --version 2>/dev/null || echo "ERROR: Node.js not found"

# Detect deploy target
[ -f wrangler.toml ] && echo "Cloudflare Workers (TOML)"
[ -f wrangler.json ] && echo "Cloudflare Workers (JSON)"
grep -q "pages" wrangler.toml 2>/dev/null && echo "Cloudflare Pages"
```

Checklist (fail = STOP):
- [ ] Tests pass
- [ ] Lint passes
- [ ] Build succeeds
- [ ] No uncommitted changes (or explicitly approved)
- [ ] On correct branch

## Phase 2: Build & Test
1. Run linter: `npm run lint` or equivalent
2. Run tests: `npm test` or equivalent
3. Run build: `npm run build` or equivalent
4. If ANY step fails → STOP. Do NOT deploy broken code.

## Phase 3: Deploy
Follow the deploy SKILL.md protocol (`~/.claude/skills/deploy/SKILL.md`):

1. **Snapshot current state** (for rollback)
2. Deploy using project-appropriate method:
   - Cloudflare Pages: `npx wrangler pages deploy`
   - Cloudflare Workers: `npx wrangler deploy`
   - Other: project-specific deploy script
3. Capture deploy output and URL

## Phase 4: Post-deploy Verification
1. **Hit the deployed URL** — verify it loads (curl or Claude in Chrome)
2. **Check for console errors**
3. **Verify critical functionality** — does the main feature work?
4. **Compare against pre-deploy** — anything broken?

If verification fails → **rollback immediately**, report what failed.

## Phase 5: Report
```
DEPLOY COMPLETE
===============
Project: [name]
Branch: [branch] → [environment]
URL: [deployed URL]

Pre-flight: lint ✓ | tests ✓ | build ✓
Deploy: [success/failed/rolled back]
Verification: [all checks passed / issues found]
```

If successful, tag the release: `git tag -a v[version] -m "Deploy [date]"`
