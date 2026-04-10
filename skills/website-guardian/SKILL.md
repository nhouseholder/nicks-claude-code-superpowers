---
name: website-guardian
description: "MANDATORY enforcement for web app changes. Snapshot baseline before edits, verify after, and run root-cause analysis with permanent logging on any bug. Fires on every file change in a webapp directory."
weight: light
triggers:
  - "update the website", "deploy", "fix the site", "the site is broken"
  - after ANY deploy or build (post-deploy verification)
  - when a user reports a visual bug or broken feature
  - when a screenshot shows something wrong
  - NOTE: Does NOT fire on every file edit — only on deploy, explicit site work, or user-reported bugs
---

# Website Guardian — Stop Breaking Things

## RULE ZERO: Surgical Scope (MANDATORY — READ FIRST)

**Only touch files directly related to the task you were given. NOTHING ELSE.**

- Algorithm update? Touch algorithm files ONLY. Do NOT touch HTML, CSS, admin pages, dashboards, or frontend components.
- Data fix? Touch data files ONLY. Do NOT restructure the UI that displays them.
- Config change? Touch config ONLY. Do NOT "improve" nearby code.
- If you notice other issues while working, **NOTE them for the user in your response.** Do NOT fix them.
- The blast radius of your changes MUST match the scope of the request.

**This rule exists because Claude has repeatedly destroyed admin pages, lost entire frontend redesigns, and broken working UIs by making unsolicited "improvements" during focused backend tasks (courtside-ai NCAA admin page destroyed during algorithm update, researcharia.com redesign lost during backend deploy). These incidents caused hours of lost work.**

**Violation of this rule is a CRITICAL failure — worse than not completing the task at all. A working site with an incomplete backend update is infinitely better than a broken site with a "complete" update.**

## Why This Exists

Claude has a pattern of breaking websites during updates:
1. Fixes one thing, breaks two others
2. Never checks what was working BEFORE making changes
3. Claims "fixed" without verifying the actual rendered output
4. Doesn't learn — the same bugs recur across sessions
5. Doesn't follow its own maintenance instructions
6. **Makes unsolicited changes to files outside the task scope**

**This skill makes it impossible to skip verification.** It is not optional. It is not "nice to have." Every website change goes through this gate.

## BEFORE Touching Any Web Code (Mandatory)

### Step 1: Read the Maintenance Instructions

Before ANY edit to any webapp:

```
REQUIRED READS (stop and read these NOW):
1. ~/.claude/recurring-bugs.md — know what keeps breaking
2. ~/.claude/anti-patterns.md — know what mistakes were made before
3. Project-specific MEMORY.md or site-update-protocol
4. The ACTUAL current state of the page you're about to change
```

**If you skip this step and cause a bug that was already documented, that's a CRITICAL failure.**

### Step 2: Snapshot the Baseline

Before making ANY change, record what currently works:

```
BASELINE SNAPSHOT — [date] [time]
Page: [URL or route]
Working features:
  - [ ] Feature A: [current state, specific values]
  - [ ] Feature B: [current state, specific values]
  - [ ] Feature C: [current state, specific values]
Working integrations (CRITICAL — these break silently):
  - [ ] GitHub Actions buttons (workflow_dispatch triggers)
  - [ ] API endpoints called by UI buttons
  - [ ] Cron/scheduled job triggers
  - [ ] OAuth/auth service connections
  - [ ] External service webhooks
  - [ ] "Generate Picks" / "Refresh Data" / any action buttons
Screenshots taken: [yes/no — take them if you have Claude in Chrome]
```

**Integration preservation rule:** Any code that calls external APIs, triggers GitHub Actions, connects to webhooks, or wires UI buttons to backend services is SACRED. If you don't understand what it does, DON'T TOUCH IT. If you're editing a file that contains integration code, preserve it character-for-character unless explicitly told to change it. After every edit, verify ALL integration buttons still work.

**The baseline is your safety net.** If you can't describe what's working NOW, you can't tell if you broke it.

### Step 3: Identify Blast Radius

Before editing, answer:
1. What components/pages use the code I'm about to change?
2. What data flows through this code?
3. What OTHER features depend on the same data/functions?
4. Could my change affect anything I'm NOT trying to fix?

**If the blast radius is more than 1 page, check ALL affected pages after.**

## AFTER Every Web Code Change — Tiered Verification

### Step 4: Classify Change Risk

Before verifying, classify what you changed:

| Tier | Change Type | Examples | Verification |
|------|------------|----------|-------------|
| **LOW** | Data/content only | New picks JSON, updated stats, text copy, version bump | Deploy CLI success = done. No visual check needed. |
| **MEDIUM** | Style/layout tweak | Color change, spacing fix, font swap, single component edit | One screenshot of the changed page at one breakpoint. 30 seconds. |
| **HIGH** | New feature, redesign, multi-file change | New page, component rewrite, redesign phase, algorithm change affecting display | Full verification: all affected pages, all breakpoints, data spot-check. |

**Default to MEDIUM if unsure.** Only go HIGH for multi-page or structural changes.

### Step 5: Verify Per Tier

**LOW risk (data/content):**
```
✅ Deploy command succeeded
✅ No build errors
Done. Move on.
```

**MEDIUM risk (style/layout):**
- One screenshot of the changed page (desktop width)
- Quick scan: does the change look right? Any obvious breakage?
- If it looks fine → done

**HIGH risk (feature/redesign/algorithm):**
- Screenshot every affected page at 375px, 768px, 1280px
- Check: layout intact? Data correct? All elements present?
- Spot-check one data row end-to-end
- Check console for new errors
- Full baseline comparison:
```
POST-CHANGE VERIFICATION — [date] [time]
Page: [URL or route]
Baseline check:
  - [x] Feature A: STILL WORKING [same values]
  - [x] Feature B: STILL WORKING [same values]
  - [ ] Feature C: BROKEN — [what changed]
    → FIX BEFORE CONTINUING
```

### Step 6: The "Did I Break Anything?" Checklist (HIGH tier only)

```
[ ] All features from baseline snapshot still work
[ ] No new console errors or warnings
[ ] No visual regressions (layout, colors, text)
[ ] Data values are correct (not placeholder, not zero, not null)
[ ] The thing I was trying to fix actually IS fixed
[ ] No other pages/components affected by my change are broken
```

**If ANY checkbox fails, fix it NOW.** Do not declare the task done.

## WHEN A BUG IS FOUND (Root Cause Protocol)

When ANY bug is discovered on a website — whether found by you, the user, or a screenshot:

### Step A: Acknowledge and Document

```
BUG REPORT — [date]
What's broken: [specific symptom]
Where: [page, component, element]
Expected: [what it should look like/do]
Actual: [what it actually looks like/does]
```

### Step B: Root Cause Analysis (5 Whys)

Don't just fix the symptom. Trace the cause:

```
1. WHY is the data wrong?
   → Because the calculation uses flat +1u instead of odds-based payout
2. WHY does the calculation use flat +1u?
   → Because I wrote the payout function without reading how bets actually settle
3. WHY didn't I read how bets settle?
   → Because I assumed I knew (confident ignorance)
4. WHY wasn't this caught before deploy?
   → Because I didn't verify the actual numbers, only that the UI rendered
5. WHY didn't I verify the numbers?
   → Because there's no automated check and I skipped manual verification

ROOT CAUSE: Skipped domain research + skipped output verification
```

### Step C: Identify the Carelessness

Be brutally honest. Which of these caused this bug?

| Carelessness Type | Description |
|-------------------|-------------|
| **Didn't read first** | Changed code without reading the existing implementation |
| **Didn't verify after** | Claimed "fixed" without checking the actual output |
| **Didn't check blast radius** | Fixed one thing, broke another because I didn't check related components |
| **Assumed domain knowledge** | Wrote logic for a domain I don't fully understand |
| **Ignored maintenance docs** | The fix was documented in recurring-bugs.md but I didn't read it |
| **Copied without understanding** | Duplicated code or patterns without understanding why they work |
| **Didn't snapshot baseline** | Can't tell what I broke because I don't know what was working |
| **Rushed** | Took shortcuts to finish faster, introduced bugs |

### Step D: Permanent Learning (Write to Memory)

**EVERY bug gets logged.** No exceptions. Append to `~/.claude/anti-patterns.md`:

```markdown
### [WEBSITE_BUG] [SHORT_TITLE] — [DATE]
- **Project**: [project name]
- **Page/Component**: [specific location]
- **Bug**: [what was broken]
- **Root cause**: [from 5 Whys analysis]
- **Carelessness type**: [from table above]
- **Fix**: [what actually fixed it]
- **Prevention rule**: [one imperative sentence for future agents]
- **Verification**: [how to confirm this specific bug isn't present]
```

### Step E: Update Maintenance Instructions

If the bug reveals a gap in existing maintenance docs:

1. **Update site-update-protocol** — add the bug to the checklist
2. **Update recurring-bugs.md** — if this is a repeat, increment the counter and escalate
3. **Add a verification check** — a specific test or check that would catch this bug automatically
4. **Update CLAUDE.md** — if the bug pattern is general enough to be a project rule

### Step F: Instruct Future Agents

Write a clear instruction that prevents this bug from ever happening again. Add it to the project's MEMORY.md or CLAUDE.md:

```markdown
## [BUG PREVENTION] [Title]
BEFORE: [what to check before making this type of change]
NEVER: [what to never do]
ALWAYS: [what to always do]
VERIFY: [how to confirm this bug isn't present]
```

## The Non-Negotiable Rules

1. **Snapshot baseline BEFORE every change** — if you can't say what was working, you can't tell what you broke
2. **Verify EVERY baseline item after EVERY change** — not some, ALL
3. **Never claim "fixed" without checking the actual output** — rendered page, real data, not just "I edited the code"
4. **Every bug gets a root cause analysis** — not "it was broken, I fixed it" but WHY it was broken and what carelessness caused it
5. **Every bug gets logged permanently** — anti-patterns.md, recurring-bugs.md, project memory
6. **Every bug updates the instructions** — if the instructions didn't prevent this bug, the instructions are incomplete
7. **Read maintenance docs BEFORE touching code** — recurring-bugs.md exists for a reason
8. **Check blast radius** — if your change touches shared code, verify ALL consumers
9. **Regressions are treated as CRITICAL** — fixing X and breaking Y is worse than not fixing X
10. **The user should NEVER have to report the same bug twice** — if they do, the learning system failed

### User Evidence Primacy
When the user reports a visual bug or provides a screenshot:
1. BELIEVE THEM — their browser is showing the real state
2. Verify via Claude in Chrome, NEVER via curl (CDN caching lies)
3. Never argue "it looks fine to me" based on CLI output when user has visual proof
4. The user's screenshot IS the ground truth — your job is to figure out WHY it looks wrong, not WHETHER it's wrong

## Universal Deploy Verification (All 7 Sites)

These patterns are promoted from site-update-protocol (UFC-specific) to apply universally.

### Every Deploy Must Include (scaled to tier)

**ALL tiers (mandatory):**
1. Deploy command must exit successfully — if it fails, stop.

**MEDIUM + HIGH tiers only:**
2. Visual verification of changed pages (MEDIUM: one page, one breakpoint. HIGH: all affected pages, all breakpoints).

**HIGH tier only:**
3. Spot-check one data row end-to-end — pick one piece of data, trace it from source through code to rendered page.
4. Check action buttons still work — any button calling APIs, triggering workflows, or submitting data.
5. Version/data regression check — compare deployed version and data counts against baseline.
6. Console error scan — load affected pages and check for new errors.

### Per-Page Verification Template

```
POST-DEPLOY CHECK — [site] [date]
Page: [URL]
  [ ] Renders without errors
  [ ] All data present (not empty, not placeholder)
  [ ] All interactive elements respond (buttons, links, forms)
  [ ] No visual regressions (layout, colors, spacing)
  [ ] No console errors
  [ ] Data matches source (spot-checked 1 row)
```

### Data Consistency Invariants (Universal)

These apply to ANY site displaying computed data:

| Invariant | Violation Example |
|-----------|-------------------|
| Positive metric requires positive count | "Revenue: $500" with "Sales: 0" |
| Percentages must be 0-100 | "260% confidence" |
| Totals must equal sum of parts | "Combined: $100" but parts sum to $85 |
| Win/loss records must match detail | "5W-3L" but table shows 4 wins |
| Dates must be chronological | Future dates in historical data |
| No null/undefined in rendered output | "undefined" or "NaN" visible on page |

## Integration with Other Skills

- **error-memory**: Website Guardian handles the investigation; error-memory handles the persistence format
- **site-update-protocol**: Specific to UFC/mmalogic.com; Website Guardian is universal for ALL webapps
- **proactive-qa**: Should catch bugs before the user sees them; Website Guardian catches what proactive-qa missed
- **pre-debug-check**: Reads anti-patterns before fixing; Website Guardian WRITES the anti-patterns after finding bugs
