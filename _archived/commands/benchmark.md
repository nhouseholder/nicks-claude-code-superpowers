Performance benchmarking and regression detection. Measures Core Web Vitals, bundle sizes, and load times using real browser data. Tracks trends over time.

## Arguments
- `$ARGUMENTS` = URL to benchmark (optional — auto-detects from project context)
- `--baseline` = Capture baseline (run before making changes)
- `--quick` = Single-pass timing check (no baseline needed)
- `--trend` = Show performance trends from historical data
- `--pages /,/dashboard,/about` = Specify pages to benchmark

---

## Phase 1: Setup

1. Determine the live URL:
   - If URL provided in arguments, use it
   - Otherwise, identify project from `pwd` + `git remote get-url origin`
   - Look up URL from `~/Projects/site-to-repo-map.json`
   - If no URL found, ask the user

2. Create report directory:
```bash
mkdir -p _benchmark/baselines
```

---

## Phase 2: Page Discovery

If no `--pages` specified:
1. Navigate to URL with `mcp__Claude_in_Chrome__navigate`
2. Extract internal nav links with `mcp__Claude_in_Chrome__javascript_tool`:
```javascript
Array.from(document.querySelectorAll('a[href]'))
  .map(a => new URL(a.href, window.location.origin))
  .filter(u => u.origin === window.location.origin)
  .map(u => u.pathname)
  .filter((v, i, a) => a.indexOf(v) === i)
  .slice(0, 5)
```
3. Always include `/`. Confirm page list with user.

---

## Phase 3: Performance Data Collection

For each page, navigate and collect metrics using `mcp__Claude_in_Chrome__javascript_tool`:

**Navigation timing:**
```javascript
JSON.stringify((() => {
  const nav = performance.getEntriesByType('navigation')[0];
  const paint = performance.getEntriesByType('paint');
  return {
    ttfb: Math.round(nav.responseStart - nav.requestStart),
    fcp: Math.round((paint.find(p => p.name === 'first-contentful-paint') || {}).startTime || 0),
    dom_interactive: Math.round(nav.domInteractive),
    dom_complete: Math.round(nav.domComplete),
    full_load: Math.round(nav.loadEventEnd)
  };
})())
```

**Resource analysis:**
```javascript
JSON.stringify((() => {
  const res = performance.getEntriesByType('resource');
  return {
    total_requests: res.length,
    total_transfer: res.reduce((s, e) => s + (e.transferSize || 0), 0),
    js_bundle: res.filter(r => r.initiatorType === 'script').reduce((s, e) => s + (e.transferSize || 0), 0),
    css_bundle: res.filter(r => r.initiatorType === 'css').reduce((s, e) => s + (e.transferSize || 0), 0),
    top_slow: res.sort((a, b) => b.duration - a.duration).slice(0, 10).map(r => ({
      name: r.name.split('/').pop().split('?')[0],
      type: r.initiatorType,
      size: r.transferSize,
      duration: Math.round(r.duration)
    }))
  };
})())
```

---

## Phase 4: Baseline Capture (--baseline mode)

Save all metrics to `_benchmark/baselines/baseline.json`:
```json
{
  "url": "<url>",
  "timestamp": "<ISO>",
  "pages": {
    "/": {
      "ttfb_ms": 120,
      "fcp_ms": 450,
      "dom_interactive_ms": 600,
      "dom_complete_ms": 1200,
      "full_load_ms": 1400,
      "total_requests": 42,
      "total_transfer_bytes": 1250000,
      "js_bundle_bytes": 450000,
      "css_bundle_bytes": 85000
    }
  }
}
```

Also copy to `_benchmark/baselines/{date}-baseline.json` for historical tracking.

---

## Phase 5: Comparison

If baseline exists, compare current vs baseline:

```
PERFORMANCE REPORT — [url]
══════════════════════════
Baseline: [baseline date]

Page: /
─────────────────────────────────────────────────────
Metric              Baseline    Current     Delta    Status
────────            ────────    ───────     ─────    ──────
TTFB                120ms       135ms       +15ms    OK
FCP                 450ms       480ms       +30ms    OK
DOM Interactive     600ms       650ms       +50ms    OK
DOM Complete        1200ms      1350ms      +150ms   WARNING
Full Load           1400ms      2100ms      +700ms   REGRESSION
Total Requests      42          58          +16      WARNING
Transfer Size       1.2MB       1.8MB       +0.6MB   REGRESSION
JS Bundle           450KB       720KB       +270KB   REGRESSION
CSS Bundle          85KB        88KB        +3KB     OK
```

**Regression thresholds:**
- Timing: >50% increase OR >500ms absolute increase = REGRESSION
- Timing: >20% increase = WARNING
- Bundle size: >25% increase = REGRESSION
- Bundle size: >10% increase = WARNING
- Request count: >30% increase = WARNING

---

## Phase 6: Performance Budget

Check against industry budgets:

```
PERFORMANCE BUDGET CHECK
════════════════════════
Metric              Budget      Actual      Status
────────            ──────      ──────      ──────
FCP                 < 1.8s      0.48s       PASS
LCP                 < 2.5s      1.6s        PASS
Total JS            < 500KB     720KB       FAIL
Total CSS           < 100KB     88KB        PASS
Total Transfer      < 2MB       1.8MB       WARNING (90%)
HTTP Requests       < 50        58          FAIL

Grade: [A-F] ([N]/6 passing)
```

**Grading:** A = 6/6, B = 4-5/6, C = 3/6, D = 2/6, F = 0-1/6

---

## Phase 7: Slowest Resources

```
TOP 10 SLOWEST RESOURCES
═════════════════════════
#   Resource                  Type      Size      Duration
1   vendor.chunk.js          script    320KB     480ms
2   main.js                  script    250KB     320ms
...

RECOMMENDATIONS:
- [specific, actionable suggestions for each slow resource]
```

---

## Phase 8: Trend Analysis (--trend mode)

Load all historical baselines from `_benchmark/baselines/*-baseline.json`:

```
PERFORMANCE TRENDS
══════════════════
Date        FCP     Full Load  JS Bundle  Requests  Grade
2026-03-10  420ms   1200ms     380KB      38        A
2026-03-14  450ms   1400ms     450KB      42        A
2026-03-18  480ms   2100ms     720KB      58        B

TREND: [growing/stable/improving] — [specific observation]
```

---

## Phase 9: Save Report

Write full report to `_benchmark/{date}-benchmark.md` and `_benchmark/{date}-benchmark.json`.

---

## Rules

1. **READ-ONLY.** Produce the report. Don't modify code unless explicitly asked.
2. **Measure, don't guess.** Use actual performance API data, not estimates.
3. **Relative thresholds.** Compare against YOUR baseline, not generic standards.
4. **Bundle size is the leading indicator.** Track it consistently.
5. **Third-party scripts are context.** Flag them, but focus on first-party resources.
