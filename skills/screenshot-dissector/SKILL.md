---
name: screenshot-dissector
description: Maximizes Claude's visual bug analysis when screenshots are provided during troubleshooting. Enforces a methodical, pixel-level examination instead of a quick glance — catches layout bugs, state issues, console errors, and UI regressions that surface only visually.
weight: light
---

# Screenshot Dissector — See Every Bug in the Frame

## The Problem This Solves

When users share screenshots during troubleshooting, Claude tends to glance at the obvious issue and respond immediately. This misses:
- Subtle layout shifts or overflow issues in other parts of the UI
- State inconsistencies visible in the UI but not mentioned by the user
- Console errors or network failures visible in DevTools panels
- Missing elements that SHOULD be there but aren't
- Incorrect data rendering (wrong numbers, truncated text, stale values)
- Mobile/responsive breakpoint issues
- Z-index stacking problems (elements hidden behind others)

## When This Fires

Automatically when a screenshot is provided during a troubleshooting or debugging context.

**Does NOT fire for:**
- Design review or aesthetic feedback (that's subjective, not bug-hunting)
- Screenshots of documentation or reference material
- Screenshots shared for context but not for debugging

## The Analysis Protocol

### Pass 1 — User's Reported Issue (5 seconds)
Identify what the user is pointing at. Confirm you see it. Don't stop here.

### Pass 2 — Full Visual Scan (systematic, thorough)

Scan the screenshot in this order:

1. **Layout & Structure**
   - Is everything aligned correctly? Any unexpected gaps, overlaps, or shifts?
   - Are containers properly sized? Any overflow or clipping?
   - Is the responsive layout correct for the viewport width?
   - Any elements that appear to be missing or duplicated?

2. **Data & Content**
   - Are all visible values plausible? (e.g., "$NaN", "undefined", empty where data should be)
   - Is text truncated, overlapping, or unreadable?
   - Are images loaded or showing broken placeholders?
   - Do numbers/dates/labels match expected formats?

3. **State & Interactivity**
   - Are buttons/inputs in the correct state? (enabled/disabled, active/inactive)
   - Does the UI reflect the expected state? (loading spinner still showing, empty state when there should be data)
   - Are conditional elements (modals, tooltips, dropdowns) rendering correctly?
   - Any visual indication of errors (red borders, warning icons)?

4. **DevTools (if visible)**
   - Console tab: Any errors or warnings?
   - Network tab: Any failed requests (red entries)?
   - Elements tab: Any relevant computed styles visible?
   - React DevTools: Component state/props if visible?

5. **Cross-reference with Code Knowledge**
   - Based on the visible URL/route, which component renders this page?
   - What data source feeds the visible elements?
   - What state management controls the visible UI state?
   - Are there known issues with this page/component?

### Pass 3 — Report Findings

**Format:**
```
**Primary issue** (what you reported): [description + likely cause]

**Also spotted:**
- [Additional issue 1] — [likely cause]
- [Additional issue 2] — [likely cause]

**Root cause hypothesis:** [What code path likely produced this visual state]
```

Only include "Also spotted" if there ARE additional issues. Don't invent problems.

## What Makes This Different From "Just Looking"

| Quick Glance | Screenshot Dissector |
|-------------|---------------------|
| Sees the obvious error | Systematically scans every region |
| Responds to what user said | Finds what user DIDN'T notice |
| Guesses at the cause | Cross-references visible state with code knowledge |
| Misses DevTools info | Reads console errors, network failures, component state |
| Ignores surrounding UI | Checks adjacent elements for collateral damage |

## Integration

- **systematic-debugging**: Dissector provides the visual evidence; systematic-debugging drives the root-cause investigation
- **codebase-cartographer**: After identifying the likely component from the screenshot, read that file before proposing fixes
- **pre-debug-check**: Check if the visual bug matches a known anti-pattern before investigating
- **proactive-qa**: Dissector catches visual bugs; proactive-qa catches them before they happen
- **qa-gate**: qa-gate covers functional testing; screenshot-dissector covers VISUAL bug detection that QA checklists miss. If identified component isn't already in context, flag it: "Likely caused by [Component] — loading that file for a fix proposal."

## Rules

1. **Always do Pass 2** — Never skip the full scan just because the obvious issue is clear
2. **Name the component** — Always identify which code file/component renders what's shown
3. **Don't invent problems** — Only report issues you actually see, not hypothetical ones
4. **Prioritize actionable findings** — "The submit button is disabled when it shouldn't be" > "The font looks slightly different"
5. **Read DevTools first** — If console/network panels are visible, read them BEFORE theorizing about the code
6. **Cross-reference** — Connect visual symptoms to code paths using your codebase knowledge
7. **One response** — Report all findings in a single structured response, not a back-and-forth
