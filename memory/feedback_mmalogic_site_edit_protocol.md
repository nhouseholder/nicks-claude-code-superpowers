---
name: MMALogic 6-Step Site Edit Protocol
description: Mandatory 6-step checklist for all MMALogic site edits — pipeline, universal fix, agent update, version bump, GitHub sync, deploy
type: feedback
---

Every MMALogic site edit must complete ALL 6 steps:
1. Proactive pipeline — automate prevention of the recurring error
2. Universal application — fix ALL components (grep every occurrence)
3. Update mmalogic agent knowledge (maintenance rules, anti-patterns, memory)
4. Version bump in version.js
5. Commit + push to GitHub (specific files, never git add -A)
6. Deploy via CI and verify live

**Why:** User set this 2026-04-01 after repeated stale data and partial fixes across sessions.
**How to apply:** Before closing any site edit task, verify all 6 complete. Missing any = incomplete.
