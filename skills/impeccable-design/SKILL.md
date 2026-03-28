---
name: impeccable-design
description: "Expert design enhancement layer. Provides deep reference library (typography, color/OKLCH, motion, spatial, interaction, responsive, UX writing), AI slop detection checklist, and design normalization. Use alongside frontend-design for any site build, redesign, or visual work. Automatically loaded by site-redesign, design-options, and site-review."
weight: light
---

# Impeccable Design — Expert Enhancement Layer

Enhancement layer for `frontend-design`. Provides deep design references, AI slop detection, and design system normalization. Adapted from [pbakaus/impeccable](https://github.com/pbakaus/impeccable) (Apache 2.0).

## When This Fires

This skill is loaded automatically when:
- Building or redesigning any website/webapp
- Running `/site-redesign`, `/design-options`, `/site-review`
- Any task where `frontend-design` is active

## Deep Reference Library

Before making design decisions, **read the relevant reference files**. They contain expert-level specifics — exact cubic-bezier values, OKLCH formulas, font alternatives, interaction patterns — that produce measurably better output than generic rules.

| Reference | When to Read | Key Insight |
|-----------|-------------|-------------|
| `reference/typography.md` | Font selection, pairing, hierarchy | Modular scales, fluid type via clamp(), OpenType features, font-display swap with metric overrides |
| `reference/color-and-contrast.md` | Palette creation, theming | OKLCH > HSL (perceptually uniform), tinted neutrals (chroma 0.01), 60-30-10 rule, dark mode ≠ inverted |
| `reference/motion-design.md` | Any animation work | 100/300/500ms rule, quart-out as default easing, only animate transform+opacity, reduced motion mandatory |
| `reference/spatial-design.md` | Layout, spacing, grids | 4pt base (not 8pt), squint test for hierarchy, cards-in-cards = anti-pattern, container queries > viewport |
| `reference/interaction-design.md` | Interactive elements | 8 states per element, :focus-visible (not :focus), native dialog/popover API, anchor positioning, roving tabindex |
| `reference/responsive-design.md` | Responsive work | Content-driven breakpoints, pointer/hover media queries, safe-area-inset, srcset + sizes |
| `reference/ux-writing.md` | Microcopy, labels, errors | Verb+object buttons (not "OK/Submit"), error formula (what+why+fix), empty states = onboarding moments |

**Read the reference before implementing.** Don't apply from memory — the specifics matter.

## AI Slop Detection — Mandatory Pre-Delivery Check

After implementation, scan your output for these AI-generated design fingerprints. **If 3+ are present, you've produced slop — redesign before delivering.**

| # | Fingerprint | What It Looks Like | Fix |
|---|---|---|---|
| 1 | **The Inter/Roboto default** | Body or headings in Inter, Roboto, Open Sans, Lato, Montserrat, Space Grotesk | See `reference/typography.md` for alternatives |
| 2 | **Purple gradient hero** | Purple-to-blue gradient on white background | Choose palette specific to brand/context |
| 3 | **Cards-in-cards** | Nested card containers with rounded corners | Use spacing + typography for hierarchy |
| 4 | **Gray text on color** | Gray (#6B7280) on colored backgrounds | Use tinted neutrals or bg-color transparency |
| 5 | **Glassmorphism everywhere** | backdrop-filter blur on every surface | Reserve for 1-2 elements max |
| 6 | **Hero metrics row** | 3-4 stats (Users: 10K+, Downloads: 50K+) | Only with real data; use meaningful proof |
| 7 | **Generic gradient buttons** | bg-gradient-to-r from-purple-500 to-blue-500 | Solid color, intentional hover state |
| 8 | **Identical section rhythm** | Every section: heading → subtitle → 3-col grid | Vary layout, break the grid, use asymmetry |
| 9 | **Stock testimonials** | "Changed my life" — Sarah J., CEO | Real quotes or skip entirely |
| 10 | **The blob background** | SVG blobs/circles as decoration | Purposeful, brand-aligned visual texture |

**Slop score**: Count matches. 0-1 = clean. 2 = borderline (fix the matches). 3+ = slop (redesign).

## Design Normalization Protocol

When reviewing or updating an existing site (not a fresh build), normalize against the project's own design tokens before adding anything new:

1. **Audit existing tokens**: Extract current colors, fonts, spacing from CSS/config
2. **Identify drift**: Find elements that deviate from the project's own system (not some ideal — the project's actual tokens)
3. **Normalize first**: Bring drifted elements back to existing tokens before proposing new ones
4. **Propose additions**: If existing tokens are insufficient, propose new ones that extend (not replace) the system
5. **Never mix systems**: If the project uses Tailwind custom colors, add to tailwind.config — don't add inline OKLCH

## Integration Points

This skill enhances but never replaces:
- `frontend-design` — still provides the core aesthetic direction and creative philosophy
- `ui-ux-pro-max` — still provides the searchable design system database
- `ui-design-system` — still provides token generation scripts

This skill adds what those lack: expert-depth reference material, a concrete slop detection checklist, and normalization discipline.
