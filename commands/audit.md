Scan the current project for hardcoded secrets, API keys, credentials, and code quality issues. Fix found issues by moving secrets to env vars.

## Arguments
- `$ARGUMENTS` = project directory or specific files to scan (default: current directory)

## Phase 1: Pre-checks
```bash
# Verify we're in a project directory
ls package.json requirements.txt pyproject.toml Cargo.toml go.mod 2>/dev/null || echo "WARNING: No project manifest found — scanning anyway"

# Check for .env files that should NOT be committed
git ls-files --cached .env .env.* 2>/dev/null | head -5

# Check .gitignore covers sensitive patterns
grep -q "\.env" .gitignore 2>/dev/null || echo "WARNING: .gitignore missing .env pattern"
```

## Phase 2: Execute Scan
Follow the audit SKILL.md protocol (`~/.claude/skills/audit/SKILL.md`):

1. **Secrets scan**: Grep all Python and JavaScript/TypeScript files for:
   - API keys, tokens, passwords (hardcoded strings matching key patterns)
   - Connection strings with embedded credentials
   - Private keys or certificates
2. **Code quality**: Check for common anti-patterns:
   - `eval()`, `exec()` usage
   - Unvalidated user input in queries
   - Missing error handling on external calls
3. **Dependency check**: Look for known vulnerable patterns

Classify severity:
- **P0 Critical**: Hardcoded secrets, exposed credentials
- **P1 High**: SQL injection, command injection vectors
- **P2 Medium**: Missing input validation, weak error handling
- **P3 Low**: Code style, unused imports

## Phase 3: Fix & Verify
For P0/P1 issues:
1. Move secrets to environment variables
2. Add missing `.env` entries to `.env.example` (without values)
3. Ensure `.gitignore` covers sensitive files
4. Verify the fix doesn't break imports/references

For P2/P3: fix if quick (<5 lines), otherwise list for manual attention.

## Phase 4: Report
```
AUDIT COMPLETE
==============
Project: [name]
Files scanned: [N]
Issues found: P0: [N] | P1: [N] | P2: [N] | P3: [N]
Issues fixed: [N]
Remaining: [N] (need manual attention)

Fixed:
- [file]: [what was fixed]

Manual attention needed:
- [file:line]: [issue description]
```
