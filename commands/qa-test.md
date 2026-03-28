Structured QA testing with bug fixing. Tests the live site like a real user using Claude in Chrome, finds bugs, fixes them with atomic commits, and re-verifies. Produces a before/after health report.

## Arguments
- `$ARGUMENTS` = URL to test (optional — auto-detects from project context)
- `--quick` = Critical + high severity only
- `--exhaustive` = Include low/cosmetic issues
- `--report-only` = Find bugs but don't fix them

---

## Phase 1: Setup

1. Determine the live URL:
   - If URL provided in arguments, use it
   - Otherwise, identify project from `pwd` + `git remote get-url origin`
   - Look up URL from `~/Projects/site-to-repo-map.json`
   - If no URL found, ask the user

2. Check for clean working tree:
```bash
git status --porcelain
```
If dirty, ask user to commit or stash first. QA needs a clean tree for atomic fix commits.

3. Create report directory:
```bash
mkdir -p _qa/screenshots
```

4. Determine tier:
   - **Quick:** Fix P0 + P1 only
   - **Standard** (default): + P2
   - **Exhaustive:** + P3

---

## Phase 2: Page Discovery

1. Navigate to URL with `mcp__Claude_in_Chrome__navigate`
2. Build a page map — extract all internal links:
```javascript
Array.from(document.querySelectorAll('a[href]'))
  .map(a => { try { return new URL(a.href, window.location.origin); } catch(e) { return null; } })
  .filter(u => u && u.origin === window.location.origin)
  .map(u => u.pathname)
  .filter((v, i, a) => a.indexOf(v) === i)
```
3. Always include `/`. Prioritize pages with forms, auth, and dynamic content.

---

## Phase 3: Test Each Page

For each discovered page, run these checks:

### 3a. Console Errors
- Navigate to page with `mcp__Claude_in_Chrome__navigate`
- Wait 3 seconds for full load
- Check `mcp__Claude_in_Chrome__read_console_messages` for errors
- Classify: P0 if blocking (uncaught exceptions), P2 if warnings

### 3b. Visual Check
- Take screenshot with `mcp__Claude_in_Chrome__computer` (screenshot)
- Look for: broken layouts, overlapping elements, missing images, text overflow
- Check at default viewport

### 3c. Mobile Responsiveness
- Resize to 375px width with `mcp__Claude_in_Chrome__resize_window`
- Take screenshot
- Check for: horizontal scroll, unreadable text, broken nav, overlapping elements
- Resize to 768px, check again
- Restore original size

### 3d. Broken Links
- Use `mcp__Claude_in_Chrome__javascript_tool` to check all links on page:
```javascript
JSON.stringify(
  Array.from(document.querySelectorAll('a[href]'))
    .map(a => ({ href: a.href, text: a.textContent.trim().substring(0, 50) }))
    .filter(l => !l.href.startsWith('javascript:') && !l.href.startsWith('mailto:'))
)
```
- Navigate to each internal link, check for 404s

### 3e. Form Validation
- Find forms on page with `mcp__Claude_in_Chrome__javascript_tool`:
```javascript
JSON.stringify(Array.from(document.querySelectorAll('form')).map(f => ({
  action: f.action, method: f.method,
  fields: Array.from(f.querySelectorAll('input, select, textarea')).map(i => ({
    type: i.type, name: i.name, required: i.required
  }))
})))
```
- Try submitting empty required fields
- Try invalid email/phone formats
- Check error messages display correctly

### 3f. Accessibility Basics
- Check with `mcp__Claude_in_Chrome__javascript_tool`:
```javascript
JSON.stringify({
  images_without_alt: document.querySelectorAll('img:not([alt])').length,
  buttons_without_text: Array.from(document.querySelectorAll('button')).filter(b => !b.textContent.trim() && !b.getAttribute('aria-label')).length,
  inputs_without_label: Array.from(document.querySelectorAll('input:not([type=hidden])')).filter(i => !i.getAttribute('aria-label') && !document.querySelector(`label[for="${i.id}"]`)).length
})
```

---

## Phase 4: Classify Bugs

Classify each finding:
- **P0** — Broken, users are blocked (page crash, form doesn't submit, auth broken)
- **P1** — Significant quality issue (broken layout on mobile, console errors, broken links)
- **P2** — Medium issue (missing alt text, minor visual glitch, slow load)
- **P3** — Cosmetic (spacing inconsistency, color mismatch, minor text issues)

Create bug report in `_qa/bugs.md`:
```
# QA Bug Report — [project] — [date]

## P0 — Critical
| # | Page | Issue | Evidence |
|---|------|-------|----------|

## P1 — High
...

## P2 — Medium
...

## P3 — Low
...
```

---

## Phase 5: Fix Loop (unless --report-only)

For each bug, highest severity first:

1. **Identify the source file** — trace from the rendered page to the source code
2. **Fix in source code** — make the minimal change needed
3. **Commit atomically:**
```
fix: [brief description of what was fixed]

QA: [page] — [issue description]
```
4. **Re-verify in browser** — navigate back to the page, confirm the fix
5. **If fix breaks something else** — revert the commit immediately, try a different approach
6. **Move to next bug**

**Important:**
- NEVER touch files outside the scope of the bug (surgical-scope rule)
- NEVER disconnect working integrations
- Commit between each fix (rate limit protection)
- If a bug requires a large refactor, skip it and note in the report

---

## Phase 6: Health Report

After all fixes:

```
QA REPORT — [project] — [date]
═══════════════════════════════
URL:          [live URL]
Pages tested: [N]
Tier:         [Quick/Standard/Exhaustive]

BEFORE                          AFTER
──────                          ─────
P0: 2 critical                  P0: 0 (all fixed)
P1: 3 high                     P1: 1 (2 fixed, 1 deferred)
P2: 5 medium                   P2: 3 (2 fixed)
P3: 4 low                      P3: 4 (not in scope)

Health Score: 45/100 → 82/100

FIXES APPLIED:
1. [commit SHA] — [description]
2. [commit SHA] — [description]
...

DEFERRED:
- [issue] — Reason: [why it was skipped]

SCREENSHOTS: _qa/screenshots/
```

Save to `_qa/{date}-qa-report.md`.

---

## Rules

1. **Commit between each fix.** Rate limits kill multi-task sessions.
2. **Surgical scope.** Only modify files related to the specific bug.
3. **Re-verify every fix.** Don't trust that code changes work — check in browser.
4. **Revert on regression.** If a fix breaks something else, revert immediately.
5. **Never disconnect integrations.** API calls, webhooks, auth — leave them alone.
6. **Skip vs force.** If a bug requires 200+ LOC change, skip it and note in report.
7. **Evidence everything.** Screenshots for visual bugs, console output for JS errors.
