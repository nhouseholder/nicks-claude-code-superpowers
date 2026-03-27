---
name: form-filler-outer
description: Fill out web forms, PDF forms, and applications on behalf of Nicholas using his saved personal info profile. Triggers on "fill out", "fill in", "complete this form", "application", "enrollment form", or any request to enter personal data into a form. Works with browser forms (Chrome MCP), PDF forms (PDF tools), and Word/DOCX forms.
user_invocable: true
---

# Form Filler Outer

## Purpose
Automatically fill out forms, applications, and enrollment documents using Nicholas's saved personal information profile.

## Data Source
Read the user's personal info from:
`~/.claude/projects/-Users-nicholashouseholder-Library-Mobile-Documents-com-apple-CloudDocs-ER-Bill-help/memory/user_personal_info.md`

If that file doesn't exist, check:
`~/.claude/memory/` for any file matching `*personal_info*` or `*form_filler*`

## Field Mapping
When encountering form fields, map them to the profile data:

| Form Field Pattern | Profile Value |
|---|---|
| First Name, Given Name | Nicholas |
| Middle Name, MI | Alan |
| Last Name, Surname, Family Name | Householder |
| Date of Birth, DOB, Birthday | 03/03/1999 |
| Email, E-mail | nikhouseholdr@gmail.com |
| Phone, Telephone, Mobile | (480) 454-0020 or 4804540020 |
| Street, Address Line 1 | 4527 E Horseshoe Rd |
| City | Phoenix |
| State, Province | Arizona / AZ |
| Zip, Postal Code | 85028 |
| Country | United States / US |
| Gender, Sex | Male / M |
| Race, Ethnicity | Caucasian / White |
| Height (ft) | 5 |
| Height (in) | 9 |
| Weight (lbs) | 170 |
| Hair Color | Brown |
| Eye Color | Brown |
| Place of Birth, Birth State | Pennsylvania / PA |
| Country of Citizenship | United States |
| US Citizen | Yes |
| Preferred Language | English |
| ID Document Type | Driver's License |

## Workflow

### For Browser Forms (Chrome MCP)
1. Take a screenshot to see the form
2. Use `read_page` with `filter: interactive` to get all form fields
3. Match fields to profile data using the mapping above
4. Fill fields using `form_input` for text/select fields
5. Click radio buttons using coordinate clicks for Yes/No questions
6. Screenshot to verify before submitting
7. **STOP before any submit/payment button** — always ask user to confirm

### For PDF Forms
1. Use `read_pdf_fields` to list all fillable fields
2. Match fields to profile data
3. Use `fill_pdf` to populate matching fields
4. Show the user the filled PDF for review

### For DOCX Forms
1. Read the document
2. Find form fields or blanks
3. Fill using find/replace or direct editing
4. Save and show the user

## HARD RULES

1. **NEVER enter SSN** — always leave blank and tell user to fill it manually
2. **NEVER enter bank/financial info** — credit cards, routing numbers, account numbers
3. **NEVER enter passwords or API keys**
4. **NEVER click Submit/Pay/Purchase** without explicit user confirmation
5. **ALWAYS screenshot and verify** before proceeding past any page
6. **ALWAYS read the profile file fresh** at the start of each form-filling session (address may have changed)
7. **Handle confirmation fields** (Confirm Email, Confirm DOB) by entering the same value twice
8. **Adapt to field formats** — phone might need (480) 454-0020 or 4804540020, dates might need MM/DD/YYYY or YYYY-MM-DD
9. **For dropdowns**, read the options first, then select the best match
10. **For Yes/No radio buttons** that don't respond to ref clicks, use coordinate clicks

## Common Form Types
- Medical board applications (TMB, state licensing)
- FBI fingerprint/background checks (IdentoGO, Certifix)
- Employment applications
- Insurance forms
- Government forms
- Enrollment/registration forms

## Address Note
Nicholas is moving from Phoenix AZ to UTMB (Texas). When filling forms, confirm which address to use if the move has happened. Check the profile file for the current address.
