# Handoff — Superpowers — 2026-03-25 19:15
## Model: Claude Opus 4.6 (1M context)
## Previous handoff: HANDOFF.md (cross-project loss-analyst session, 2026-03-25 03:30 AM)
## GitHub repo: nhouseholder/nicks-claude-code-superpowers
## Local path: ~/Library/Mobile Documents/com~apple~CloudDocs/superpowers/
## Last commit date: 2026-03-25 19:08:34 -0700

---

## 1. Session Summary
User requested a complete reorganization of all project directories across the filesystem. We flattened the `~/Projects/` structure from 3-level (Projects/category/repo) to 2-level (Projects/repo), renamed all project folders to match their website names, moved everything to iCloud Drive, created a symlink at `~/Projects/`, and updated every reference across CLAUDE.md, commands, memory files, site-to-repo-map.json, and project-manifest.json. Full audit confirmed zero stale references remain.

## 2. What Was Done
- **Renamed 6 project folders to website names**: ufc-predict->mmalogic, diamond-predictions->diamondpredictions, enhanced-health-ai->enhancedhealthai, strain-finder->mystrainai, dad-financial-planner->nestwisehq, aria-research->researcharia
- **Flattened folder structure**: Removed category subdirs (sports/, health/, cannabis/, apps/, tools/) -- all projects now at ~/Projects/<name>/
- **Moved to iCloud**: All projects moved from ~/Projects/ (local) to iCloud Drive/Projects/, with ~/Projects symlink pointing there
- **Updated all references**: CLAUDE.md (canonical structure, site-to-repo table, 3-gate verification), 6 command files, 3 memory files, site-to-repo-map.json, project-manifest.json
- **Cleaned stale dirs**: Moved ~/ufc-predict.ARCHIVED to iCloud _archived_projects/
- **Pulled 2 stale repos**: diamondpredictions and icebreaker-ai were 1 commit behind
- **Full audit**: 12-point verification -- all passing
- **Synced to GitHub**: 4 commits pushed (dcf4fb3 -> f81b853)
- **Saved memory**: feedback_flat_project_structure.md -- flat 2-level, no categories, on iCloud

## 3. What Failed (And Why)
- **SSH clone failed**: git clone git@github.com:... failed -- SSH key not configured for this session. Switched to HTTPS which worked fine.
- **First rsync had stale /tmp dir**: Initial /tmp/superpowers-sync didn't exist (from prior session cleanup). Re-cloned via HTTPS.

## 4. What Worked Well
- Batch sed updates across all command files and memory files -- efficient pattern propagation
- Symlink approach (~/Projects/ -> iCloud/Projects/) means all existing ~/Projects/ references work without changes
- 12-point audit at the end caught 1 remaining <category>/<repo> pattern in CLAUDE.md Gate 1

## 5. What The User Wants
- **Simple, flat folder structure**: "No categories folders, just a projects folder" -- strong preference for 2 levels max
- **iCloud storage**: "which i want on ICLOUD, not locally" -- wants projects accessible via iCloud sync
- **Website names as folder names**: "name them after the websites, rename all them" -- folder should immediately tell you what site it serves
- **Foolproof for AI agents**: "ensure everything is perfect for claude to never be confused again"

## 6. In Progress (Unfinished)
All tasks completed.

## 7. Blocked / Waiting On
- **GitHub PAT rotation**: User was advised to revoke exposed token found in recipes-app remote URL. Status unknown -- the remote URL has been cleaned locally but the token itself needs manual revocation at github.com/settings/tokens.

## 8. Next Steps (Prioritized)
1. **Revoke the exposed GitHub PAT** -- security risk, found in prior session, user was notified
2. **Test /full-handoff from a project dir** -- verify the command works correctly when run from e.g. ~/Projects/mmalogic/
3. **Consider archiving /reorganize-all and /reorganize-ufc commands** -- one-time-use, reorg is complete
4. **Consider a session-start hook** that automatically runs 3-Gate Verification

## 9. Agent Observations
### Recommendations
- The ~/Projects symlink approach is clean but fragile -- if the symlink breaks (iCloud update, macOS upgrade), all paths break. Consider adding a check in the 3-Gate system: readlink ~/Projects must resolve to iCloud.
- The 85+ skills in the ecosystem are heavy. Consider a pruning session.
- The /reorganize-all and /reorganize-ufc commands are now one-time-use artifacts.

### Where I Fell Short
- Initially created the 3-level category structure before the user corrected it -- should have asked about structure preference upfront.
- Had to be reminded to check dates on repos -- the date-checking rule exists in CLAUDE.md but wasn't followed proactively.

## 10. Miscommunications
- Built category-based structure (sports/, health/, apps/) -- user rejected it as unnecessary complexity. Fixed immediately to flat structure.

## 11. Files Changed
4 commits in this session. Key changes:

| File | Action | Why |
|------|--------|-----|
| ~/.claude/CLAUDE.md | Modified | Flattened canonical structure, updated site-to-repo table, fixed 3-Gate paths |
| ~/.claude/commands/*.md | Modified (6 files) | Updated paths from 3-level to 2-level |
| ~/.claude/memory/topics/*.md | Modified (3 files) | Updated paths |
| ~/Projects/site-to-repo-map.json | Modified | Removed category subdirs from all local_path values |
| ~/Projects/project-manifest.json | Modified | Removed category references |

## 12. Current State
- **Branch**: main
- **Last commit**: f81b853 Fix remaining category path reference in 3-Gate verification (2026-03-25 19:08:34 -0700)
- **Build**: N/A (config/skills repo, no build step)
- **Deploy**: N/A (synced to GitHub via /tmp clone)
- **Uncommitted changes**: none
- **Local SHA matches remote**: yes

## 13. Environment
- **Node.js**: v25.6.1
- **Python**: 3.14.3
- **Dev servers**: none

## 14. Session Metrics
- **Duration**: ~45 minutes
- **Tasks**: 5/5 completed (rename, flatten, move to iCloud, update refs, audit)
- **User corrections**: 2 (flat not categorized, iCloud not local)
- **Commits**: 4 to superpowers repo
- **Skills used**: pattern-propagation, adaptive-voice

## 15. Memory Updates
- **feedback_flat_project_structure.md**: New -- all projects flat at ~/Projects/<name>/, no categories, on iCloud, folder names match website names
- **CLAUDE.md**: Major rewrite of Canonical Project Structure section and Live Site -> Repo Mapping table

## 16. Skills Used
| Skill | Purpose | Helpful? |
|-------|---------|----------|
| pattern-propagation | Batch-updated all path references across 12+ files | Yes |
| adaptive-voice | Matched user's direct communication style | Yes |

## 17. For The Next Agent
Read these files first (in order):
1. This handoff (HANDOFF.md in superpowers root)
2. ~/.claude/CLAUDE.md -- especially "Canonical Project Structure" and "Live Site -> Repo Mapping"
3. ~/.claude/anti-patterns.md
4. ~/Projects/site-to-repo-map.json
5. ~/Projects/project-manifest.json

**Canonical local path for this project: ~/Library/Mobile Documents/com~apple~CloudDocs/superpowers/**
**Do NOT open this project from /tmp/. The iCloud path above is canonical.**

---
## NEXT AGENT: MANDATORY STARTUP SEQUENCE
Before doing ANY work, run the 3-Gate Verification from ~/.claude/CLAUDE.md:
1. GATE 1: Check ~/Projects/site-to-repo-map.json -- verify you're in the correct repo
2. GATE 2: git fetch && compare local SHA to remote -- git pull if behind
3. GATE 3: Read this handoff + MEMORY.md + anti-patterns.md + recurring-bugs.md
ALL 3 GATES MUST PASS before touching any code.

**Canonical path for this project: ~/Library/Mobile Documents/com~apple~CloudDocs/superpowers/**
**Last verified commit: f81b853 on 2026-03-25 19:08:34 -0700**
