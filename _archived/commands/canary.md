Post-deploy canary monitoring. Watches the live site for console errors, performance regressions, and page failures after a deploy. Uses Claude in Chrome MCP for real browser verification.

## Arguments
- `$ARGUMENTS` = URL to monitor (optional — auto-detects from project context)
- `--baseline` = Capture baseline screenshots before deploying
- `--quick` = Single-pass health check (no continuous monitoring)
- `--duration Nm` = Custom monitoring duration (default: 10m, max: 30m)

---

## Phase 1: Setup

1. Determine the live URL:
   - If URL provided in arguments, use it
   - Otherwise, identify project from `pwd` + `git remote get-url origin`
   - Look up URL from `~/Projects/site-to-repo-map.json`
   - If no URL found, ask the user

2. Create report directory:
```bash
mkdir -p _canary/baselines _canary/screenshots
```

3. Parse arguments for mode (baseline vs monitor vs quick) and duration.

---

## Phase 2: Page Discovery

Navigate to the live URL using Claude in Chrome:

1. Use `mcp__Claude_in_Chrome__navigate` to load the site
2. Use `mcp__Claude_in_Chrome__get_page_text` to read the page
3. Use `mcp__Claude_in_Chrome__javascript_tool` to extract internal navigation links:
```javascript
Array.from(document.querySelectorAll('a[href]'))
  .map(a => new URL(a.href, window.location.origin))
  .filter(u => u.origin === window.location.origin)
  .map(u => u.pathname)
  .filter((v, i, a) => a.indexOf(v) === i)
  .slice(0, 5)
```

4. Always include the homepage `/`. Present the discovered pages to the user and confirm.

---

## Phase 3: Baseline Capture (--baseline mode)

For each page:

1. Navigate to the page with `mcp__Claude_in_Chrome__navigate`
2. Wait 2 seconds for full load
3. Take screenshot with `mcp__Claude_in_Chrome__computer` (screenshot action)
4. Check console errors with `mcp__Claude_in_Chrome__read_console_messages`
5. Measure load timing with `mcp__Claude_in_Chrome__javascript_tool`:
```javascript
JSON.stringify((() => {
  const nav = performance.getEntriesByType('navigation')[0];
  return {
    ttfb: Math.round(nav.responseStart - nav.requestStart),
    dom_interactive: Math.round(nav.domInteractive),
    dom_complete: Math.round(nav.domComplete),
    full_load: Math.round(nav.loadEventEnd)
  };
})())
```

6. Save baseline manifest to `_canary/baselines/baseline.json`:
```json
{
  "url": "<url>",
  "timestamp": "<ISO>",
  "pages": {
    "/": {
      "console_errors": 0,
      "load_time_ms": 450
    }
  }
}
```

Then STOP: "Baseline captured. Deploy your changes, then run `/canary` to monitor."

---

## Phase 4: Quick Health Check (--quick mode)

Single pass through all pages. For each page:
1. Navigate, screenshot, check console, measure timing
2. Compare against baseline if one exists
3. Report immediately — no continuous monitoring

---

## Phase 5: Continuous Monitoring Loop

Monitor for the specified duration (default 10 minutes). Every 60 seconds, check each page:

1. Navigate with `mcp__Claude_in_Chrome__navigate`
2. Check console errors with `mcp__Claude_in_Chrome__read_console_messages`
3. Measure load timing with `mcp__Claude_in_Chrome__javascript_tool`
4. Take screenshot with `mcp__Claude_in_Chrome__computer`

After each check, compare against baseline (or first-check snapshot):

- **Page load failure** — navigate returns error or timeout → CRITICAL
- **New console errors** — errors not in baseline → HIGH
- **Performance regression** — load time >2x baseline → MEDIUM
- **Broken links** — new 404s not in baseline → LOW

**Alert rules:**
- Alert on CHANGES vs baseline, not absolutes
- Require 2+ consecutive failures before alerting (transient tolerance)
- If CRITICAL or HIGH persists, immediately notify user with evidence

**Alert format:**
```
CANARY ALERT
════════════
Time:     Check #N at Ns
Page:     /path
Type:     CRITICAL / HIGH / MEDIUM
Finding:  [what changed]
Baseline: [baseline value]
Current:  [current value]
```

Ask user: A) Investigate now B) Continue monitoring C) Dismiss

---

## Phase 6: Health Report

After monitoring completes:

```
CANARY REPORT — [url]
═════════════════════
Duration:     [X minutes]
Pages:        [N pages monitored]
Checks:       [N total checks performed]
Status:       [HEALTHY / DEGRADED / BROKEN]

Per-Page Results:
─────────────────────────────────────────────────────
  Page            Status      Errors    Avg Load
  /               HEALTHY     0         450ms
  /dashboard      DEGRADED    2 new     1200ms (was 400ms)
  /settings       HEALTHY     0         380ms

Alerts Fired:  [N] (X critical, Y high, Z medium)
Screenshots:   _canary/screenshots/

VERDICT: [DEPLOY IS HEALTHY / DEPLOY HAS ISSUES — details above]
```

Save report to `_canary/{date}-canary.md`.

---

## Phase 7: Baseline Update

If deploy is healthy, offer to update baseline:
- A) Update baseline with current data
- B) Keep old baseline

---

## Rules

1. **READ-ONLY.** Observe and report. Do NOT modify code unless explicitly asked.
2. **Alert on changes, not absolutes.** Compare against baseline, not industry standards.
3. **Screenshots are evidence.** Every alert includes a screenshot path.
4. **Transient tolerance.** Only alert on patterns that persist across 2+ consecutive checks.
5. **Speed matters.** Start monitoring within 30 seconds of invocation.
6. **Baseline is king.** Without a baseline, this is a health check. Encourage `--baseline` before deploying.
