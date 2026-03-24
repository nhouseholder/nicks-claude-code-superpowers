---
name: version-bump
description: Automated semantic versioning for commits. Determines major/minor/patch from the nature of changes, bumps package.json version, and formats commit messages with version prefix. Use when committing changes that warrant a version bump, or when the user asks to bump/tag/release a version.
weight: light
---

# Version Bump — Semantic Versioning on Autopilot

Automatically determine and apply the correct version bump based on what changed. No manual version tracking needed.

## When This Activates

- After completing a feature, fix, or significant change that should be versioned
- When the user says "commit", "version", "bump", "release", or "tag"
- When git-sorcery is creating a commit for meaningful work

## Version Rules (semver)

### PATCH (x.x.X) — Bug fixes, minor tweaks
- Bug fixes that don't change behavior
- Typo fixes, copy changes
- Dependency updates (non-breaking)
- Performance improvements (same API)
- CSS/styling fixes

### MINOR (x.X.0) — New features, enhancements
- New feature or component added
- New API endpoint
- New page or route
- Enhancement to existing feature (new option, better UX)
- New data added (new strains, new cities, new effects)
- Non-breaking config changes

### MAJOR (X.0.0) — Breaking changes
- Breaking API changes
- Database schema migration required
- Removed features or endpoints
- Changed authentication flow
- Major architecture refactor

## Workflow

### 1. Determine Bump Type
Analyze the staged changes:
```bash
git diff --cached --stat
git diff --cached
```

Map changes to PATCH/MINOR/MAJOR using the rules above.

### 2. Detect and Read Current Version

Detect the project's version file: package.json (Node.js), pyproject.toml (Python), Cargo.toml (Rust), or similar. If no standard version file exists, track version in the most prominent config file or skip version bumping for that project.

```bash
# Node.js
node -p "require('./package.json').version"

# Python (pyproject.toml)
grep 'version' pyproject.toml

# Rust (Cargo.toml)
grep '^version' Cargo.toml
```

### 3. Bump Version

Use the appropriate tool for the detected version file:

```bash
# Node.js (package.json):
npm version patch --no-git-tag-version  # or minor, or major

# Python (pyproject.toml): edit the version field directly
# Rust (Cargo.toml): edit the version field directly or use cargo-bump
```

### 4. Commit with Version Prefix
```bash
git add package.json  # or pyproject.toml, Cargo.toml, etc.
git add <other-changed-files>
git commit -m "vX.Y.Z: Short description of what changed"
```

Format: `vMAJOR.MINOR.PATCH: Description`

Examples:
- `v5.64.1: Fix dispensary geocoding fallback for THC-A markets`
- `v5.65.0: Add flavor scoring to recommendation engine`
- `v6.0.0: Migrate auth from Firebase to Clerk`

### 5. Multi-Change Commits
When a commit includes multiple changes:
- Use the HIGHEST bump type among all changes
- List all changes in the commit body
- Example: if you fixed a bug (PATCH) and added a feature (MINOR), it's MINOR

## Post-Commit Checklist — Ship It Completely

After bumping and committing, complete the full release cycle. Don't stop at the commit.

### 6. Update Displayed Version (if applicable)
If the project displays a version number to users (website footer, about page, header subtitle, repo description):
- Find and update ALL places the version is displayed
- Common locations: footer component, about page, site title, meta tags
- Use grep to find the old version string and replace with the new one
- Include the date: `v5.65.0 (2026-03-16)` or whatever format the project uses

### 7. Push and Follow CI/CD
```bash
git push
```
- If CI/CD is configured (GitHub Actions, Cloudflare Pages, etc.), verify the pipeline kicks off
- Don't walk away until the deploy succeeds or you've confirmed it's running

### 8. Update GitHub Repo Description (when warranted)
For MINOR+ bumps on primary projects, update the GitHub repo description/name if it includes the version:
```bash
gh repo edit --description "Project Name vX.Y.Z — description"
```

### 9. Update Project Memory
If the project has a memory system (MEMORY.md or project memory), update with the version:
- Record: version number, date, what changed

## Rules

1. **Always bump** — Every meaningful commit gets a version number
2. **Semver strictly** — PATCH for fixes, MINOR for features, MAJOR for breaking
3. **Version in commit message** — Always prefix with `vX.Y.Z:`
4. **Version file sync** — Version in commit message must match the project's version file (package.json, pyproject.toml, Cargo.toml, etc.)
5. **No skipping** — Don't jump from v5.64.0 to v5.70.0; increment sequentially
6. **Ask on ambiguity** — If unsure between MINOR and MAJOR, ask the user
7. **Update displayed versions** — If users can see the version, update it everywhere
8. **Push after commit** — A version bump isn't done until it's deployed. Never push from iCloud-synced directories — use a non-iCloud clone first (see CLAUDE.md git workflow).
9. **Update shared memory** — Keep AGENT-MEMORY.md current with the latest version and date
