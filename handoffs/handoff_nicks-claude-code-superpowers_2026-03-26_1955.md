# Handoff — superpowers — 2026-03-26 19:55
## Model: Claude Opus 4.6 (1M context)
## Previous handoff: handoff_nicks-claude-code-superpowers_2026-03-25_1915.md
## GitHub repo: nhouseholder/nicks-claude-code-superpowers
## Local path: ~/Library/Mobile Documents/com~apple~CloudDocs/superpowers
## Last commit date: 2026-03-26 12:54:55 -0700

---

## 1. Session Summary
User had a catastrophic day — multiple Claude sessions destroyed websites (researcharia.com redesign lost, courtside-ai admin page destroyed, diamondpredictions GitHub Actions broken) and a directory rename killed 7 active sessions. This session was a massive hardening effort: built site-specific update agents for all 7 websites, added surgical scope rules, integration preservation rules, mandatory post-change reports, and learning loops so Claude never repeats these failures.

## 2. What Was Done
- **Surgical scope rule (CLAUDE.md #27)**: Only touch files directly related to the task. Algorithm update = algorithm files only.
- **Integration preservation rule (CLAUDE.md #29)**: Never disconnect GitHub Actions buttons, webhooks, API endpoints.
- **Post-change report (CLAUDE.md)**: Mandatory DONE/GitHub/Version/Deployed/Notes block after every code change.
- **Superpowers repo sync rule**: After any skills/rules/hooks change, sync to GitHub via /tmp/ clone.
- **6 site-specific update commands**: `/update-diamond`, `/update-courtside`, `/update-mystrainai`, `/update-enhancedhealth`, `/update-researcharia`, `/update-nestwisehq`
- **Auto-invocation rule (CLAUDE.md #9)**: Claude must self-invoke site-specific command when updating any website.
- **site-audit + site-debug upgraded**: Auto-detect site and load domain knowledge before auditing/debugging.
- **Learning & Growth sections**: All 7 update commands now have mandatory learning loops.
- **Website Guardian upgraded**: Rule Zero (surgical scope) + integration preservation checklist.
- **Anti-patterns**: 3 new entries — admin destruction, GitHub Actions disconnect, directory rename session kill.
- **Memory**: feedback_surgical_scope.md, feedback_preserve_integrations.md, feedback_post_change_report.md.
- **Directory rename rule (CLAUDE.md #30)**: Never rename directories with active sessions.

## 3. What Failed (And Why)
- **Directory rename killed 7 sessions**: Renaming `***Projects***` to `ProjectsHQ` destroyed all active sessions. Sessions store absolute paths. In-progress context was lost.
- **NFL Draft created wrong folder**: New session created `Projects` at iCloud root instead of using `ProjectsHQ`.

## 4. What Worked Well
- Post-change report format validated by user immediately
- Site-specific agent architecture approved enthusiastically
- mmalogic command served as proven template for other 6 agents

## 5. What The User Wants
- "No more breaking things on the website, reverting things, removing features randomly"
- "the most important thing will be for the agents to learn as they go and remember all the bugs they fix"
- Mandatory confirmation: "github synced, pushed, deployed, updated version number from ____ to ____" every time

## 6. In Progress (Unfinished)
- **Chrome focus-stealing**: Claude in Chrome brings Chrome to front, interrupting user. No fix found.
- **courtside-ai admin page recovery**: Destroyed during algorithm update. Needs recovery.
- **diamondpredictions workflow_dispatch fix**: Generate Picks button returns 422.

## 7. Blocked / Waiting On
- Chrome focus-stealing: unknown cause, extension behavior
- courtside-ai and diamond fixes need their own project sessions

## 8. Next Steps (Prioritized)
1. **Fix courtside-ai admin page** — destroyed by unsolicited frontend changes
2. **Fix diamondpredictions Generate Picks button** — 422 workflow_dispatch error
3. **Fix Chrome focus-stealing** — investigate what changed today vs yesterday
4. **Test new update commands** — invoke each on its project to verify
5. **Consolidate icebreaker-ai into diamondpredictions** — NHL should be in diamond only

## 9. Agent Observations
### Recommendations
- Update commands are starting templates. They become valuable after 5-10 sessions of accumulated learning.
- Run `/site-audit` on each site to populate integration registries with real data.

### Where I Fell Short
- Should have warned about directory rename killing sessions BEFORE doing it.
- Chrome focus investigation was inconclusive.

## 10. Miscommunications
- Another session misinterpreted "review handoff" as /full-handoff instead of reading existing handoff.

## 11. Files Changed
| File | Action | Why |
|------|--------|-----|
| CLAUDE.md | Modified | Rules #27-30, post-change report, repo sync, auto-invocation |
| anti-patterns.md | Modified | 3 new incident entries |
| skills/website-guardian/SKILL.md | Modified | Rule Zero + integration checklist |
| commands/update-diamond.md | Created | Diamond Predictions site agent |
| commands/update-courtside.md | Created | Courtside AI site agent |
| commands/update-mystrainai.md | Created | MyStrainAI site agent |
| commands/update-enhancedhealth.md | Created | Enhanced Health AI site agent |
| commands/update-researcharia.md | Created | Research Aria site agent |
| commands/update-nestwisehq.md | Created | NestWise HQ site agent |
| commands/site-audit.md | Modified | Auto-loads site-specific domain knowledge |
| commands/site-debug.md | Modified | Auto-loads site-specific domain knowledge |

## 12. Current State
- **Branch**: main
- **Last commit**: a451c20 (2026-03-26 12:54:55 -0700)
- **Build**: N/A — skills/config repo
- **Deploy**: N/A — not a website
- **Uncommitted changes**: none
- **Local SHA matches remote**: yes

## 13. Environment
- **Node.js**: v25.6.1
- **Python**: 3.14.3
- **Dev servers**: wrangler (all-things-ai:8799), vite (nfl-draft:5176), next (nestwisehq), vite (mystrainai)

## 14. Session Metrics
- **Duration**: ~120 minutes
- **Tasks**: 12 / 13 (Chrome focus unresolved)
- **User corrections**: 3
- **Commits**: 5 to superpowers GitHub
- **Skills used**: error-memory, unified-learning, claude-code-guide

## 15. Memory Updates
- feedback_surgical_scope.md, feedback_preserve_integrations.md, feedback_post_change_report.md
- anti-patterns.md — 3 new entries
- website-guardian SKILL.md — Rule Zero + integration checklist

## 16. Skills Used
| Skill | Purpose | Helpful? |
|-------|---------|----------|
| error-memory | Logged incidents to anti-patterns | Yes |
| unified-learning | Captured user corrections as rules | Yes |
| claude-code-guide | Chrome focus research | Partial |

## 17. For The Next Agent
Read these files first:
1. This handoff
2. handoff_nicks-claude-code-superpowers_2026-03-25_1915.md
3. ~/.claude/anti-patterns.md
4. ~/.claude/CLAUDE.md (rules #27-30 + post-change report)
5. ~/.claude/commands/update-*.md

**Canonical local path: ~/Library/Mobile Documents/com~apple~CloudDocs/superpowers**

---
## NEXT AGENT: MANDATORY STARTUP SEQUENCE
1. GATE 1: Verify you're in the superpowers repo
2. GATE 2: git fetch && compare local SHA to remote
3. GATE 3: Read this handoff + MEMORY.md + anti-patterns.md
ALL 3 GATES MUST PASS before touching any code.

**Last verified commit: a451c20 on 2026-03-26 12:54:55 -0700**
