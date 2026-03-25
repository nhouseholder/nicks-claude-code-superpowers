Update a website/webapp safely using the composite agent pipeline. Follows website-guardian protocol: baseline → changes → verify → deploy.

**This command calls agents in order. Do NOT skip phases.**

## Arguments
- `$ARGUMENTS` = project directory or specific update description
- If no argument, ask what needs updating

## Phase 1: Baseline Snapshot (Website Guardian)
Follow website-guardian SKILL.md:
- Screenshot or read current state of every affected page
- Record what's currently working (specific values, not "looks fine")
- Note the current build/deploy status

## Phase 2: Plan the Update (Planner Agent — Priority 1 skills)
- Read brainstorming SKILL.md — is this a simple update or complex change?
- If complex (3+ files): use writing-plans to write PLAN.md first
- If simple: proceed directly

## Phase 3: Make Changes (Frontend Agent or Backend Agent)
Based on what's being updated:
- **Frontend changes** → Use Frontend Agent profile: follow frontend-design, ui-ux-pro-max, react-best-practices, senior-frontend, senior-dev-mindset protocols
- **Backend changes** → Use Backend Agent profile: follow senior-backend audit checklist, senior-dev-mindset Backend section
- **Both** → Frontend first, then Backend

## Phase 4: Verify (Debugger Agent — Priority 1 skills)
- Check EVERY item from the Phase 1 baseline — is it still working?
- Run data-consistency-check on any displayed numbers
- If webapp-testing Playwright is available, run automated checks
- If anything from baseline is broken, FIX IT before proceeding

## Phase 5: Deploy (Deploy Agent)
- Invoke /deploy via Skill tool
- Follow website-guardian post-deploy verification
- Follow site-update-protocol if UFC/mmalogic project
- Visual verification of every affected page

## Phase 6: Log (Error Memory)
- If any bugs were found/fixed, log to anti-patterns.md via error-memory
- Update project memory with what changed

## Output
```
SITE UPDATE COMPLETE
====================
Changed: [list of files]
Baseline: [all items verified ✓ or ✗]
Deployed: [yes/no]
Bugs found: [N] | Fixed: [N]
```
