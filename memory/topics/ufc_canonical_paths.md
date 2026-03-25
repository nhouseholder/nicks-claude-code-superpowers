## UFC/MMALogic Project Canonical Paths [2026-03-25]

### CRITICAL — Deploying from wrong directory reverts production

| What | Canonical Path | NEVER Use |
|------|---------------|-----------|
| **Webapp source** | `ufc-predict/webapp/frontend/` | `webapp/` (root — frozen at v10.68) |
| **Build/deploy** | `cd ufc-predict/webapp/frontend && npm run build` | `cd webapp && npm run build` |
| **Data files** | `ufc-predict/webapp/frontend/public/data/` | `webapp/frontend/public/data/` (stale copy) |
| **Version file** | `ufc-predict/webapp/frontend/src/version.js` | `webapp/frontend/src/version.js` (shows v10.68) |
| **Algorithm code** | `ufc-predict/` | — |
| **GitHub CI deploys from** | `ufc-predict/webapp/frontend/` (on push to main) | — |

### Before ANY deploy, verify:
```bash
cat ufc-predict/webapp/frontend/src/version.js
# Must show v11.x+
```

### Why root webapp/ exists
It was a copy made during an earlier sync. It was never kept current with v11.x changes. It must be archived or deleted.

### Incident: 2026-03-25
AI deployed from root `webapp/` (v10.68) instead of `ufc-predict/webapp/` (v11.9.3), overwriting production with months-old stale code. Lost all v11.x improvements on the live site.
