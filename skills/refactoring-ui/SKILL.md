---
name: refactoring-ui
description: Audit and fix visual design issues using the Refactoring UI system — hierarchy, spacing, shadows, color, typography. Use when the UI looks "off" but you can't explain why, when asked to fix the design, improve visual hierarchy, or refine a color palette.
weight: light
---

# Refactoring UI — Visual Design Audit

When the UI looks "off," run this audit. It checks the 7 pillars of visual design and tells you exactly what to fix.

## When This Fires

- "my UI looks off"
- "fix the design"
- "improve visual hierarchy"
- "color palette"
- "spacing feels wrong"
- Any design review or site-redesign phase

## The 7-Pillar Audit

Run each check in order. Score pass/fail. Fix failures before moving on.

### 1. Visual Hierarchy
- [ ] Is there ONE dominant element per section? (not everything competing for attention)
- [ ] Are font sizes limited to 3-4 distinct sizes? (more = visual noise)
- [ ] Is font weight used to create emphasis, not just size?
- [ ] Are labels smaller/lighter than values? ("Price:" should be quieter than "$49")

**Common fix:** Make primary content larger/bolder, make labels and metadata smaller/lighter. Use color weight (dark vs gray) instead of size differences.

### 2. Spacing & Layout
- [ ] Consistent spacing scale? (4, 8, 12, 16, 24, 32, 48, 64 — not arbitrary)
- [ ] More space between groups than within groups? (proximity = relationship)
- [ ] Padding inside cards/sections is generous, not cramped?
- [ ] No trapped whitespace? (awkward gaps that aren't intentional)

**Common fix:** Double the padding. Seriously. Then use spacing to group related items and separate unrelated ones.

### 3. Color
- [ ] Using 1 primary color + 1 accent + neutrals? (not a rainbow)
- [ ] Grays have slight color tint? (pure gray looks dead — add blue or warm undertone)
- [ ] Sufficient contrast for text? (4.5:1 minimum for body, 3:1 for large text)
- [ ] Color conveys meaning, not just decoration? (green=success, red=error)

**Common fix:** Pick ONE saturated color for CTAs. Everything else should be neutral tones. Add a slight blue/warm tint to all grays.

### 4. Typography
- [ ] Max 2 font families? (1 is often better)
- [ ] Line height: 1.5 for body, 1.2-1.3 for headings?
- [ ] Line length: 45-75 characters for readability?
- [ ] Letter-spacing: slightly positive for uppercase, default for lowercase?

**Common fix:** Increase line-height on body text. Reduce line-length by adding max-width to content containers.

### 5. Shadows & Depth
- [ ] Shadows are subtle and consistent? (not 5 different shadow styles)
- [ ] Shadow color matches the surface? (blue-tinted for cool themes, warm for warm)
- [ ] Elevation correlates with interactivity? (buttons raised, backgrounds flat)
- [ ] No harsh black shadows? (use rgba with low opacity)

**Common fix:** Use 2-3 shadow levels max. Make shadow color semi-transparent and slightly tinted.

### 6. Borders & Separation
- [ ] Using spacing/color to separate, not just borders?
- [ ] Borders are light (gray-200 or lighter), not heavy?
- [ ] Not every element has a border? (too many borders = visual clutter)

**Common fix:** Remove half your borders. Use background color differences and spacing instead.

### 7. Icons & Images
- [ ] Icons are consistent style? (all outline OR all filled, not mixed)
- [ ] Icons have enough padding/space around them?
- [ ] Images have consistent treatment? (all rounded OR all square)

## Output Format

After auditing, present:
```
REFACTORING UI AUDIT
Hierarchy:  PASS / FAIL — [specific issue]
Spacing:    PASS / FAIL — [specific issue]
Color:      PASS / FAIL — [specific issue]
Typography: PASS / FAIL — [specific issue]
Shadows:    PASS / FAIL — [specific issue]
Borders:    PASS / FAIL — [specific issue]
Icons:      PASS / FAIL — [specific issue]

Top 3 fixes (highest impact):
1. [specific change with exact values]
2. [specific change with exact values]
3. [specific change with exact values]
```

Then implement the top 3 fixes.
