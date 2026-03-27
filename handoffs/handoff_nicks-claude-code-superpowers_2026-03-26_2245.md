# Handoff — superpowers — 2026-03-26 22:45
## Model: Claude Opus 4.6 (1M context)
## Previous handoff: handoff_nicks-claude-code-superpowers_2026-03-26_1955.md
## GitHub repo: nhouseholder/nicks-claude-code-superpowers
## Local path: ~/Library/Mobile Documents/com~apple~CloudDocs/superpowers
## Last commit date: 2026-03-26 21:37:45 -0700

---

## 1. Session Summary
Massive infrastructure hardening. Built 11 enforcement hooks to replace documentation-only rules, cleaned skill bloat (71→51, -29%), trimmed CLAUDE.md (622→167 lines, -73%), fixed the agent router forcing unnecessary subagent spawns, created /whats-next command, and upgraded /mmalogic with ground truth validator spec. Theme: hooks > rules.

## 2. What Was Done
- **Created /whats-next command**: Strategic advisor reviewing all handoffs/memory/project state
- **Upgraded /mmalogic**: Ground truth validator spec, clean rebuild protocol, mandatory knowledge recording + GitHub sync
- **Created UFC ground truth spec**: Full Python spec for validate_registry.py (12 scoring rules + learned bug checks)
- **CLAUDE.md rules #31 (triple-write) + #32 (max 2 agents)**: Added and enforced by hooks
- **Post-change report upgraded**: ✅/❌ truthful confirmation format
- **Fixed /site-redesign**: Restored 8-phase skill pipeline, Opus required, framework preservation rule
- **Added skill pipelines to 6 commands**: site-audit, site-update, site-debug, site-recover, deploy, audit
- **Built 11 enforcement hooks**: protect-skills, agent-limit, version-bump-check, surgical-scope (upgraded), correction-detector (upgraded), impossible-stats-detector, missing-odds-detector, no-narration-stops, ufc-context-loader + upgrades to block-dangerous-commands, version-bump-check
- **Protected 11 aitmpl.com skills**: READ-ONLY via protect-skills.py hook
- **Major skill cleanup**: 17 zombie dirs deleted, 20 overlapping skills archived (71→51)
- **CLAUDE.md trimmed**: 622→167 lines, all rules preserved but condensed with hook references
- **Fixed improve-prompt.py**: Removed 7 stale skill refs, stopped "spawn agent" ENFORCEMENT instruction
- **Added /whats-next routing** in improve-prompt.py

## 3. What Failed (And Why)
No failures — meta-infrastructure session with no production code changes.

## 4. What Worked Well
- Hook-first architecture: mechanical enforcement beats documentation
- Skill cleanup freed ~3,000 lines of context
- improve-prompt.py "spawn agent" fix was likely the single biggest quality improvement
- Systematic audit: scan → categorize → prioritize → fix

## 5. What The User Wants
- "I am so tired of the latest event table being wrong" — led to ground truth validator spec
- "I still feel like claude has gotten dumber" — led to skill bloat audit + cleanup
- "lets take our rules and make them hooks" — the core insight driving this session
- Wants ✅/❌ confirmation on every website change: version, GitHub, deploy, live

## 6. In Progress (Unfinished)
- **validate_registry.py**: Spec written, actual script needs building in mmalogic project
- **observe.py + parry-guard overhead**: 3 parry-guard calls/turn not yet investigated
- **`dippy` in settings.json**: Unknown command, may cause errors
- **NFL Draft redesign revert**: Tailwind→inline styles needs redo

## 7. Blocked / Waiting On
- validate_registry.py build needs mmalogic session
- courtside-ai admin recovery needs courtside session
- diamondpredictions 422 error needs diamond session

## 8. Next Steps (Prioritized)
1. **Build validate_registry.py** in mmalogic — ground truth validator
2. **Clean rebuild UFC site** — fresh backtest + validated data + rebuilt frontend
3. **Fix NFL Draft** — revert inline styles, redo with corrected /site-redesign
4. **Fix courtside-ai admin page** — destroyed during algorithm update
5. **Fix diamondpredictions Generate Picks** — 422 workflow_dispatch
6. **Investigate parry-guard overhead** — 3x per turn
7. **Remove `dippy` from settings.json**

## 9. Agent Observations
### Recommendations
- Hook-based enforcement is the right architecture. Every new rule should be a hook first.
- improve-prompt.py needs maintenance when skills are archived — stale references accumulate.
- Extend ufc-context-loader.py pattern to diamond/courtside for project-specific rule injection.

### Where I Fell Short
- Should have identified the "spawn agent" ENFORCEMENT issue earlier — likely the biggest cause of degraded performance.

## 10. Miscommunications
- User corrected that Sonnet should not be used for site-redesign (creative work needs Opus)
- User corrected that /site-redesign should use the original 8-phase skill pipeline, not the simplified version

## 11. Files Changed
| File | Action | Why |
|------|--------|-----|
| commands/whats-next.md | Created | Strategic advisor command |
| commands/mmalogic.md | Modified | Validator + knowledge recording |
| commands/site-redesign.md | Modified | 8-phase pipeline, Opus, framework preservation |
| commands/site-audit.md | Modified | Skill pipeline table |
| commands/site-update.md | Modified | Skill pipeline table |
| commands/site-debug.md | Modified | Skill pipeline table |
| commands/site-recover.md | Modified | Skill pipeline table |
| commands/deploy.md | Modified | Skill pipeline table |
| commands/audit.md | Modified | Skill pipeline table |
| CLAUDE.md | Modified | 622→167 lines |
| hooks/ (11 files) | Created/Modified | Enforcement hooks |
| settings.json | Modified | Wired all hooks |
| memory/topics/ufc_ground_truth_spec.md | Created | Validator spec |
| anti-patterns.md | Modified | 2 new entries |
| 17 zombie skill dirs | Deleted | Empty dirs |
| 20 skills | Archived | SKILL.md→SKILL.md.ARCHIVED |

## 12. Current State
- **Branch**: main
- **Last commit**: 837e362 (2026-03-26 21:37:45 -0700)
- **Build**: N/A — skills/config repo
- **Deploy**: N/A — not a website
- **Uncommitted changes**: none
- **Local SHA matches remote**: yes

## 13. Environment
- **Node.js**: v25.6.1
- **Python**: 3.14.3
- **Dev servers**: wrangler (all-things-ai:8799), next (nestwisehq)

## 14. Session Metrics
- **Duration**: ~180 minutes
- **Tasks**: 15 / 15
- **User corrections**: 3
- **Commits**: 14 to superpowers GitHub
- **Skills used**: error-memory, Explore agents (2 audits)

## 15. Memory Updates
- memory/topics/ufc_ground_truth_spec.md — created
- anti-patterns.md — 2 new entries
- CLAUDE.md — rules #31-32 added, then trimmed to 167 lines
- 20 skills archived, 17 zombie dirs deleted

## 16. Skills Used
| Skill | Purpose | Helpful? |
|-------|---------|----------|
| error-memory | Logged incidents | Yes |
| Explore agent x2 | Skill/rule audits | Yes |

## 17. For The Next Agent
Read these files first:
1. This handoff
2. handoff_nicks-claude-code-superpowers_2026-03-26_1955.md
3. ~/.claude/anti-patterns.md
4. ~/.claude/CLAUDE.md (167 lines)
5. ~/.claude/hooks/ (11 enforcement hooks)

**Canonical local path: ~/Library/Mobile Documents/com~apple~CloudDocs/superpowers**

---
## NEXT AGENT: MANDATORY STARTUP SEQUENCE
1. GATE 1: Verify you're in the superpowers repo
2. GATE 2: git clone to /tmp/, compare SHA
3. GATE 3: Read this handoff + MEMORY.md + anti-patterns.md
ALL 3 GATES MUST PASS before touching any code.

**Last verified commit: 837e362 on 2026-03-26 21:37:45 -0700**
