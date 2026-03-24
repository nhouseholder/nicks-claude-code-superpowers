---
name: audit
description: Audit codebases for security issues, code quality problems, and hardcoded secrets. Scans Python and JavaScript files for API keys, credentials, and anti-patterns. Fixes issues and commits with structured messages. Use when asked to audit, scan for secrets, check security, or review code quality.
---

# Audit Skill

Systematic codebase audit for security, quality, and hygiene issues.

## Workflow

### 1. Security Audit — Hardcoded Secrets
Scan for hardcoded API keys, tokens, passwords, and credentials:

```bash
# Search for common secret patterns
grep -rn --include="*.py" --include="*.js" --include="*.jsx" --include="*.ts" --include="*.tsx" --include="*.env" \
  -E "(api_key|apikey|api-key|secret|password|token|credential|auth)[\s]*[=:][\s]*['\"][^'\"]{8,}" . \
  | grep -v node_modules | grep -v .git | grep -v __pycache__
```

Also check for:
- Hardcoded URLs with credentials (`https://user:pass@...`)
- AWS keys (`AKIA...`)
- Private keys (`-----BEGIN`)
- `.env` files committed to git

### 2. Fix Found Issues
For each secret found:
1. Move the value to an environment variable
2. Update the code to read from `os.environ` (Python) or `process.env` (JS)
3. Add the variable name to `.env.example` with a placeholder
4. Ensure `.env` is in `.gitignore`

### 3. Code Quality Check
Scan for common anti-patterns:
- `console.log` debugging statements left in production code
- `print()` statements that should be `logging`
- Unused imports
- TODO/FIXME comments that have been there too long
- Commented-out code blocks (>5 lines)

### 4. Commit Fixes
```bash
git add <fixed_files>
git commit -m "security: remove hardcoded keys, move to env vars"
```

Or for quality fixes:
```bash
git commit -m "cleanup: remove debug statements and unused imports"
```

### 5. Report
Output a summary:
```
AUDIT REPORT
============
Files scanned: X
Secrets found: Y (Z fixed)
Quality issues: N
Commits made: M

Remaining items requiring manual review:
- [list any that couldn't be auto-fixed]
```

## Headless Mode
This skill works well in headless mode for batch processing:
```bash
claude -p "Audit all Python files for hardcoded API keys, fix any found, and commit with message 'security: remove hardcoded keys'" \
  --allowedTools "Read,Edit,Bash,Grep" > audit_results.log 2>&1
```

## Rules
- Never commit files containing real secrets — always replace first
- Always verify .gitignore includes .env before committing
- Report what was found even if auto-fix isn't possible
- Keep audit logs for compliance trail
