---
name: UFC Canonical Paths
description: Canonical directory paths for UFC/MMALogic project. Prevents wrong-directory deploys and stale file edits. Updated after reorganization.
type: reference
---

## UFC/MMALogic Project Canonical Paths [2026-03-25]

### CRITICAL — Deploying from wrong directory reverts production

**POST-REORGANIZATION (run /reorganize-ufc first):**

| What | Canonical Path | NEVER Use |
|------|---------------|-----------|
| **Project root** | `~/Projects/ufc-predict/` | Any iCloud path (stale, iCloud sync unreliable for git) |
| **Webapp source** | `~/Projects/ufc-predict/webapp/frontend/` | `webapp/` (root — frozen at v10.68) |
| **Build/deploy** | `cd ~/Projects/ufc-predict/webapp/frontend && npm run build` | Any iCloud path |
| **Data files** | `~/Projects/ufc-predict/webapp/frontend/public/data/` | Stale copies anywhere else |
| **Version file** | `~/Projects/ufc-predict/webapp/frontend/src/version.js` | Any other version.js |
| **Algorithm code** | `~/Projects/ufc-predict/` | Loose .py files in iCloud root |
| **GitHub CI deploys from** | `ufc-predict/webapp/frontend/` (on push to main) | — |
| **GitHub repo** | `nhouseholder/ufc-predict` | — |

**PRE-REORGANIZATION (if /reorganize-ufc hasn't been run yet):**

| What | Canonical Path | NEVER Use |
|------|---------------|-----------|
| **Project root** | `iCloud/UFC Algs/ufc-predict/` | `~/Projects/ufc-predict-local/` (v10.71), `iCloud/octagonai/`, `iCloud/UFC App 3.0/` |
| **Webapp source** | `iCloud/UFC Algs/ufc-predict/webapp/frontend/` | `iCloud/UFC Algs/webapp/` (root — frozen at v10.68) |

### Before ANY deploy, verify:
```bash
cat ~/Projects/ufc-predict/webapp/frontend/src/version.js 2>/dev/null || \
cat ufc-predict/webapp/frontend/src/version.js 2>/dev/null
# Must show v11.x+
```

### Stale directories to avoid (will be archived by /reorganize-ufc):
- `iCloud/UFC Algs/ufc-predict/` — 101 commits behind as of 2026-03-25
- `~/Projects/ufc-predict-local/` — hundreds of commits behind (v10.71)
- `iCloud/octagonai/` — loose files, no git
- `iCloud/UFC App 3.0/` — ancient prototype
- `iCloud/A UFC *.py`, `iCloud/__UFC*.py` — legacy standalone scripts

### Incident History
- **2026-03-25**: AI deployed from root `webapp/` (v10.68) instead of `ufc-predict/webapp/` (v11.9.3), overwriting production with months-old stale code.
- **Root cause**: 5 different UFC directories existed. AI picked the nearest `webapp/` without checking version.
- **Prevention**: Single canonical location (`~/Projects/ufc-predict/`), freshness checks, `/mmalogic` agent.
