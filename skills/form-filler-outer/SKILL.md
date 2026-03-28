---
name: form-filler-outer
description: Fill out web forms, PDF forms, and applications on behalf of Nicholas using his saved personal info profile. Triggers on "fill out", "fill in", "complete this form", "application", "enrollment form", or any request to enter personal data into a form. Works with browser forms (Chrome MCP), PDF forms (PDF tools), and Word/DOCX forms.
weight: light
user_invocable: true
---

# Form Filler Outer

## Purpose
Automatically fill out forms, applications, and enrollment documents using stored personal information profiles.

## Data Source (Canonical Location)
```
~/Projects/Form Filler/profiles/nicholas.json   ← PRIMARY (structured JSON with format variants)
~/Projects/Form Filler/profiles/               ← additional profiles (future)
~/Projects/Form Filler/templates/              ← saved PDF form templates
~/Projects/Form Filler/filled/                 ← completed form outputs
```

Fallback (legacy): `~/.claude/projects/-Users-nicholashouseholder-Library-Mobile-Documents-com-apple-CloudDocs-ER-Bill-help/memory/user_personal_info.md`

**ALWAYS read the profile JSON fresh at session start** — address or details may have changed.

## Profile Structure
The JSON profile contains:
- `legal_name` — first, middle, last, suffix, full
- `dob` — raw ISO date + pre-formatted variants (MM/DD/YYYY, YYYY-MM-DD, etc.)
- `contact` — email, phone with format variants (parenthesized, dashed, raw digits, +1)
- `address` — street, city, state (full + abbrev), zip, county, country (full + abbrev + ISO)
- `citizenship` — US citizen flag, place of birth
- `physical` — gender, race, height (ft/in/cm), weight (lbs/kg), hair, eyes
- `field_map` — maps common form field labels to profile keys
- `never_fill` — fields that must ALWAYS be left blank (SSN, bank, credit card, passwords)

## Field Matching Strategy
1. Read the form field name/label
2. Check `field_map` for a matching pattern (case-insensitive)
3. If matched, pull the value from the corresponding profile section
4. For fields with format variants (phone, DOB, address), detect the expected format from:
   - Placeholder text (e.g., "MM/DD/YYYY")
   - Input mask or maxlength
   - Other filled examples on the page
5. If `__NEVER_FILL__`, skip and warn user

## Workflow

### For Browser Forms (Chrome MCP)
1. Screenshot to see the form layout
2. `read_page` with `filter: interactive` to get all form fields
3. Match fields to profile using `field_map`
4. Fill using `form_input` for text/select fields
5. For radio buttons on custom-styled sites: use `computer` with `left_click` at coordinates
6. For masked date fields: use `computer` with `type` action, not `form_input`
7. Screenshot to verify before advancing
8. **STOP before any Submit/Pay/Purchase button** — ask user to confirm

### For PDF Forms
1. `read_pdf_fields` to list all fillable fields
2. Match fields to profile using `field_map`
3. Build field_data dict with matched values
4. `fill_pdf` with input path, output path (`~/Projects/Form Filler/filled/`), and field_data
5. Show user the filled PDF for review

### For DOCX Forms
1. Read the document structure
2. Find form fields, blanks, or placeholder text
3. Fill using find/replace or direct editing
4. Save to `~/Projects/Form Filler/filled/`

## HARD RULES

1. **NEVER enter SSN** — leave blank, tell user to fill manually
2. **NEVER enter bank/financial info** — credit cards, routing numbers, account numbers
3. **NEVER enter passwords or API keys**
4. **NEVER click Submit/Pay/Purchase** without explicit user confirmation
5. **ALWAYS screenshot and verify** before proceeding past any page
6. **ALWAYS read the profile JSON fresh** at start (address may have changed)
7. **Handle confirmation fields** (Confirm Email, Confirm DOB) with same value twice
8. **Adapt to field formats** — use the pre-computed format variants from the profile
9. **For dropdowns**, read options first, select best match
10. **For Yes/No radio buttons** that don't respond to ref clicks, use coordinate clicks
11. **Save filled PDFs** to `~/Projects/Form Filler/filled/` with descriptive names

## Common Form Types
- Medical board applications (TMB, state licensing)
- FBI fingerprint/background checks (IdentoGO, Certifix)
- Employment applications
- Insurance forms
- Government forms
- Enrollment/registration forms
- Financial assistance applications

## Address Note
Nicholas is moving from Phoenix AZ to UTMB (Texas). When filling forms, confirm which address to use if the move has happened. The profile JSON has the current address.
