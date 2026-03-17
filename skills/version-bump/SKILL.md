---
name: version-bump
description: Automated semantic versioning for commits. Determines major/minor/patch from the nature of changes, bumps package.json version, and formats commit messages with version prefix. Use when committing changes that warrant a version bump, or when the user asks to bump/tag/release a version.
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

### 2. Read Current Version
```bash
node -p "require('./package.json').version"
```

### 3. Bump Version
```bash
# For the determined bump type:
npm version patch --no-git-tag-version  # or minor, or major
```

If no package.json exists, track version in the most appropriate config file.

### 4. Commit with Version Prefix
```bash
git add package.json
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

## Rules

1. **Always bump** — Every meaningful commit gets a version number
2. **Semver strictly** — PATCH for fixes, MINOR for features, MAJOR for breaking
3. **Version in commit message** — Always prefix with `vX.Y.Z:`
4. **package.json sync** — Version in commit message must match package.json
5. **No skipping** — Don't jump from v5.64.0 to v5.70.0; increment sequentially
6. **Ask on ambiguity** — If unsure between MINOR and MAJOR, ask the user
