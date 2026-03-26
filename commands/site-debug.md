Debug a website/webapp systematically. Find the bug, fix it, verify the fix, log it permanently.

**Sequential pipeline. Do NOT skip phases.**

## Arguments
- `$ARGUMENTS` = bug description, URL, screenshot, or project directory
- `--phase N` = skip to Phase N

## If No Argument Provided — Auto-Investigate (do NOT just ask)
Before asking the user anything:
1. `git diff --stat HEAD~3` — what changed recently?
2. `grep -l "$(date +%Y-%m-%d)" ~/.claude/anti-patterns.md` — any bugs logged today?
3. Check for running dev servers: `ps aux | grep -E "(next|vite|express)" | grep -v grep`
4. If dev server running, check for errors: read console output or `curl -s localhost:3000 | head -20`
5. Read `~/.claude/recurring-bugs.md` for known issues in this project
6. **Then present what you found:** "I see recent changes to [files], a server on port [N], and [context]. What's the issue?" — or if the bug is obvious from the above, start fixing it.

## Phase 0: Orient (~30 seconds, main agent)

```bash
PROJECT_NAME=$(basename "$(pwd)")
[ -f package.json ] && node -e "const p=require('./package.json'); console.log('Stack:', Object.keys(p.dependencies||{}).filter(d=>/react|next|vue|svelte|express/.test(d)).join(', '))"
git log --oneline -5 2>/dev/null
git status --short 2>/dev/null
```

Read these yourself (no agent):
- `~/.claude/anti-patterns.md` — has this bug been seen before? If YES: announce it, show the prior fix, use an ESCALATED approach (the prior fix was insufficient).
- `~/.claude/recurring-bugs.md` — repeat offender?
- Project MEMORY.md

**CRITICAL: Load site-specific domain knowledge.** Match current project to its update command and READ IT:
- `ufc-predict` / `mmalogic` → `~/.claude/commands/mmalogic.md` + `~/.claude/memory/topics/ufc_website_maintenance_rules.md`
- `diamond-predictions` → `~/.claude/commands/update-diamond.md`
- `courtside-ai` → `~/.claude/commands/update-courtside.md`
- `Strain-Finder` / `mystrainai` → `~/.claude/commands/update-mystrainai.md`
- `enhanced-health` → `~/.claude/commands/update-enhancedhealth.md`
- `aria-research` → `~/.claude/commands/update-researcharia.md`
- `dad-financial` → `~/.claude/commands/update-nestwisehq.md`

The update command defines what "working correctly" looks like for this site — integration registry, domain rules, known anti-patterns. **Use it to understand the bug in context.**

**Write:** `_debug/phase0_context.md`

## Phase 1: Baseline Snapshot (~1 min, main agent)

Do this yourself:
1. If dev server is running, take screenshots or read the page via Claude Preview/Chrome
2. Record what IS working — specific values, not "looks fine"
3. Record the exact symptoms of the bug — what you see vs what's expected
4. Check browser console for errors

**Write:** `_debug/phase1_baseline.md` — working items + exact bug symptoms.

## Phase 2: Isolate (~2 min, main agent)

Do this yourself:
1. Can this bug be reproduced in a minimal test? Write a 5-10 line script if possible.
2. If screenshot provided: examine pixel-by-pixel — read every value, check every element. Do NOT glance and approve.
3. Trace the data flow: where does the displayed value come from? Read the component → the data source → the API/file.

If the bug can't be isolated: log WHY (external dependency, race condition, state-dependent) in `_debug/phase2_isolation.md` and proceed with extra caution.

**Write:** `_debug/phase2_isolation.md` — reproduction steps, data flow trace, hypothesis.

## Phase 3: Diagnose (~3 min, main agent or 1 agent for large codebases)

For small bugs (1-2 files): do this yourself.
For complex bugs (5+ files, unclear cause): spawn ONE **general-purpose agent**:
```
"DIAGNOSIS AGENT

Context: Read _debug/phase0_context.md, _debug/phase1_baseline.md, _debug/phase2_isolation.md.
Also read: ~/.claude/anti-patterns.md and ~/.claude/skills/systematic-debugging/SKILL.md.

Your task: The bug is [description]. The hypothesis is [from phase 2].
- Test the hypothesis with ONE targeted check (read a specific file, check a specific value)
- If wrong, form a new hypothesis (max 3 attempts)
- Do NOT change code — diagnosis only
- Output: Root cause with evidence, written to _debug/phase3_diagnosis.md"
```

**Write:** `_debug/phase3_diagnosis.md` — root cause, evidence, affected files.

## Phase 4: Fix (~5 min, main agent)

Do this yourself — do NOT delegate fixes to agents:
1. Read `_debug/phase3_diagnosis.md` for root cause
2. Apply the **smallest targeted fix** that addresses the root cause
3. Follow the domain rules:
   - Frontend: read `~/.claude/skills/frontend-design/SKILL.md` patterns
   - Backend: read `~/.claude/skills/senior-backend/SKILL.md` patterns
   - UFC site: read `~/.claude/skills/site-update-protocol/SKILL.md` rules
4. If the fix touches data display: verify with data-consistency-check rules (profit>0 requires wins>0, etc.)

## Phase 5: Verify (~2 min, main agent)

Do this yourself:
1. Re-check EVERY item from Phase 1 baseline — still working?
2. Verify the bug is actually fixed (don't just check the fix compiled)
3. If visual: take a new screenshot and compare against Phase 1
4. If data: spot-check at least 2 specific values end-to-end
5. Run build: `npm run build` or equivalent — must pass
6. If Phase 2 logged "can't isolate": apply EXTRA verification (multiple inputs, edge cases)

If the fix broke something else: fix THAT before proceeding. Do not declare done with regressions.

## Phase 6: Log & Commit (~1 min, main agent)

1. **Commit the fix:**
```bash
git add -A && git commit -m "fix: [short description of what was broken and why]

Root cause: [one line]
Fix: [one line]"
```

2. **Log to anti-patterns:**
```
### [BUG_TITLE] — [DATE]
- **Context**: [project/file/component]
- **Bug**: [what was broken]
- **Root cause**: [why it was broken — the real reason, not the symptom]
- **Flawed assumption**: [what the AI believed that was false]
- **Fix**: [what actually fixed it]
- **Prevention**: [one-line rule for future agents]
- **Applies when**: [when to check this before acting]
```

3. If this bug has occurred before (found in Phase 0): update `~/.claude/recurring-bugs.md` with escalated analysis.

## Deliverable

```
SITE DEBUG COMPLETE
===================
Bug: [description]
Root cause: [what was actually wrong]
Fix: [what was changed] — [files]
Verified: baseline ✓ | data-check ✓ | visual ✓ | build ✓
Logged: anti-patterns.md ✓ | recurring-bugs.md [✓/n/a]
Prevention rule: [one-line rule for future agents]

Debug files: _debug/ (phase reports)
```

## Design Principles
- **Main agent does everything except diagnosis of complex bugs.** Max 1 subagent.
- **Inter-phase data via `_debug/` files.** Each phase reads prior phases.
- **Token budget: ~15 min total.** If simple bug, skip isolation and go straight to diagnosis.
- **Never say "looks correct" without checking specific values.** State what you see.
- **Every fix gets logged.** No bug fix is complete without an anti-patterns entry.
