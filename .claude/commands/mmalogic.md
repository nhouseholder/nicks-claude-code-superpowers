Dedicated MMALogic/OctagonAI website agent. This command carries ALL domain knowledge for mmalogic.com — betting rules, canonical paths, anti-patterns, verification checklists, and learned errors. Use this for ANY task involving the UFC website.

Triggers: "mmalogic", "octagonai", "ufc website", "ufc site", "update the site", "deploy the site", "fix the site", any mention of mmalogic.com

## Step 0: Load Knowledge Base (MANDATORY — read before doing ANYTHING)

Read ALL of these files. Do NOT skip any. Do NOT "apply mentally" — actually read them:

```
1. ~/.claude/memory/topics/ufc_website_maintenance_rules.md    — 15-item verification checklist
2. ~/.claude/memory/topics/ufc_canonical_paths.md              — canonical directory paths
3. ~/.claude/memory/topics/ufc_betting_model_spec.md           — 4-bet model specification
4. ~/.claude/skills/site-update-protocol/SKILL.md              — full update protocol with 19 display rules
5. ~/.claude/anti-patterns.md                                  — search for "UFC" entries
6. ~/.claude/recurring-bugs.md                                 — search for "UFC" entries
```

After reading, summarize in one line what you loaded: "Loaded: 15-item checklist, canonical paths (ufc-predict/webapp/frontend/), 4-bet model, 19 display rules, N anti-patterns, N recurring bugs."

## Step 1: Freshness Check (MANDATORY — prevents stale file disasters)

```bash
# Where am I?
echo "Working directory: $(pwd)"

# Is this iCloud? (iCloud folders diverge from GitHub)
[[ "$(pwd)" == *"Mobile Documents"* ]] && echo "⚠️ iCLOUD DIRECTORY — must verify freshness against GitHub"

# Clone fresh from GitHub for comparison
cd /tmp && rm -rf mmalogic-fresh
git clone https://github.com/nhouseholder/ufc-predict.git mmalogic-fresh --depth 1 2>&1 | tail -1

# Compare version
LOCAL_VER=$(cat ufc-predict/webapp/frontend/src/version.js 2>/dev/null || echo "NOT FOUND")
REMOTE_VER=$(cat /tmp/mmalogic-fresh/webapp/frontend/src/version.js 2>/dev/null || echo "NOT FOUND")
echo "Local version: $LOCAL_VER"
echo "GitHub version: $REMOTE_VER"

# If versions differ, ALWAYS use GitHub version
if [ "$LOCAL_VER" != "$REMOTE_VER" ]; then
  echo "⚠️ VERSION MISMATCH — local is stale. Work from /tmp/mmalogic-fresh/ or pull latest."
fi
```

**RULE: If local is stale, work from the fresh GitHub clone in /tmp/. Never edit stale files.**

## Step 2: Determine Task Type

Based on what the user asked, route to the appropriate workflow:

| User says | Task type | Workflow |
|-----------|-----------|---------|
| "update the site" / "push changes" / "deploy" | **Update & Deploy** | → Step 3A |
| "fix [bug]" / "something's broken" / screenshot | **Debug** | → Step 3B |
| "audit the site" / "check everything" | **Audit** | → Step 3C |
| "redesign" / "rebuild the look" | **Redesign** | → Step 3D |
| "add [feature]" / "change [component]" | **Feature Work** | → Step 3E |
| "check the site" / "how does it look" | **Visual Verification** | → Step 3F |

## Step 3A: Update & Deploy

1. **Data sync** — copy all 7 data files from `ufc-predict/webapp/frontend/public/data/` (see site-update-protocol Step 0)
2. **Source sync** — check for divergence: `diff -rq ufc-predict/webapp/frontend/src/ webapp/frontend/src/`
3. **Registry verification** — all 5 bet types present with wins/losses/pnl
4. **Build** — `cd ufc-predict/webapp/frontend && npm run build` (NEVER from root webapp/)
5. **Deploy** — push to `ufc-predict` main branch to trigger GitHub CI auto-deploy
6. **Post-deploy verification** — run the 15-item checklist on the live site

## Step 3B: Debug

1. Read anti-patterns for matching bugs
2. Baseline snapshot (specific values, not "looks fine")
3. Isolate → diagnose → fix
4. Verify against 15-item checklist
5. Log to anti-patterns with root cause
6. Commit and push to trigger CI redeploy

## Step 3C: Audit

1. Run `/site-audit` from `ufc-predict/webapp/frontend/`
2. Additionally run the UFC-specific 15-item checklist
3. Check all 19 display rules from site-update-protocol
4. Spot-check 2 events end-to-end

## Step 3D: Redesign

1. Run `/site-redesign` from `ufc-predict/webapp/frontend/`
2. Preserve all betting display logic — redesign is VISUAL only
3. After redesign, re-verify all 19 display rules still pass

## Step 3E: Feature Work

1. Plan the feature
2. Implement in `ufc-predict/webapp/frontend/`
3. Verify 15-item checklist (features often break existing displays)
4. Build and test before committing

## Step 3F: Visual Verification

Run the full 15-item checklist from ufc_website_maintenance_rules.md:
- Use Claude in Chrome or Claude Preview to view the live site
- Check EACH item with specific values
- Report pass/fail per item

## Domain Rules (Quick Reference — full spec in the knowledge base files)

### The 4+1 Bet Model
- **ML** (moneyline): fighter wins = payout at odds, fighter loses = -1u
- **Method** (ML + exact method): requires ML win + correct method. KO/TKO grouped.
- **Round** (ML + exact round): requires ML win + correct round. ONLY for R1 KO predictions.
- **Combo** (ML + method + round): requires ALL three correct. ONLY for R1 KO predictions.
- **Parlay** (per event): 2 parlays per event — High Confidence + High ROI
- Fighter loss = ALL bets on that fighter lose (-1u each, up to -4u)
- Method and Round are scored INDEPENDENTLY

### Display Rules (Most Violated)
- Confidence = raw differential (0.14–3.0+), NOT a percentage. "2.23 diff" not "223% conf"
- Losses show -1u (not blank, not "—")
- Wins show payout at odds (not +1u flat, not blank)
- All 5 bet types on every page
- Both parlays per event
- Event count = 71+ (current backtest window)

### Canonical Paths
- Webapp: `ufc-predict/webapp/frontend/` (NEVER root `webapp/`)
- Data: `ufc-predict/webapp/frontend/public/data/`
- Algorithm: `ufc-predict/`
- GitHub repo: `nhouseholder/ufc-predict`
- GitHub CI deploys on push to main

## Learning & Growth

After EVERY task, this agent updates its knowledge:

1. **New bug found?** → append to `~/.claude/anti-patterns.md` with UFC prefix
2. **New display rule learned?** → append to `~/.claude/skills/site-update-protocol/SKILL.md`
3. **New verification item?** → append to `~/.claude/memory/topics/ufc_website_maintenance_rules.md`
4. **Canonical path changed?** → update `~/.claude/memory/topics/ufc_canonical_paths.md`
5. **Commit all knowledge updates** to GitHub via the superpowers sync workflow

This ensures the NEXT session has everything THIS session learned.

## Output Format

Every task ends with:
```
MMALOGIC TASK COMPLETE
======================
Task: [what was done]
Directory: [confirmed canonical path]
Version: [version.js value]
Freshness: [verified against GitHub ✓]
15-item checklist: [N/15 passed]
Display rules: [N/19 verified]
Knowledge updated: [list of files updated, or "none"]
Deployed: [yes/no — if yes, via GitHub CI]
```
