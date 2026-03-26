---
name: senior-backend
description: Backend audit and development skill. When invoked, performs a systematic audit of ALL backend code — API routes, middleware, auth, database, storage, error handling. Finds security vulnerabilities, performance issues, and architecture problems. Also guides backend feature development with production-grade patterns. Use when asked to audit backend, review APIs, fix server issues, or build backend features.
weight: heavy
---

# Senior Backend — Audit & Build Protocol

## When This Fires
- User says "audit the backend", "review the API", "check server code"
- User says "build an API", "add an endpoint", "fix the server"
- Hook routes to this skill for backend-related work

## Backend Audit Protocol (When Auditing)

### Step 1: Map the Backend
Read the project structure and identify:
- API routes directory (e.g., `functions/api/`, `src/routes/`, `pages/api/`)
- Middleware files (auth, CORS, rate limiting)
- Database/storage layer (ORM, raw queries, KV, Firestore)
- Configuration files (env vars, secrets management)
- Count: total endpoints, auth-protected vs. open

### Step 2: Security Scan (P0)
For EACH endpoint, check:
- [ ] **Authentication**: Is it behind auth middleware? Should it be?
- [ ] **Input validation**: Are params validated and sanitized?
- [ ] **Injection**: Are queries parameterized? No string concatenation in SQL?
- [ ] **Secrets**: Any hardcoded API keys, tokens, passwords?
- [ ] **CORS**: Properly configured? Not `*` in production?
- [ ] **Rate limiting**: On sensitive endpoints?
- [ ] **File system**: Using `node:fs` on serverless? (crashes on Cloudflare/Vercel)

### Step 3: Performance Scan (P1)
- [ ] **N+1 queries**: Loops with DB calls per iteration
- [ ] **Missing indexes**: Queries on unindexed columns
- [ ] **No caching**: Expensive repeated queries
- [ ] **Unbounded queries**: SELECT * without LIMIT
- [ ] **Connection pooling**: New connections per request?

### Step 4: Architecture Scan (P2)
- [ ] **Error handling**: Try/catch with proper HTTP error responses?
- [ ] **Response format**: Consistent across all endpoints?
- [ ] **Logging**: Errors logged or silently swallowed?
- [ ] **Dead code**: Unused routes, commented-out endpoints?
- [ ] **God files**: Files > 300 lines that should be split?

### Step 5: Output ranked issue list with file:line and fix.
### Step 6: Fix P0 and P1 issues directly. Log via error-memory.

## Backend Development Protocol (When Building)
- Input validation and sanitization on all inputs
- Error responses with appropriate HTTP status codes
- Auth/permission checks where needed
- Database queries efficient (no N+1)
- Response format matches frontend expectations
- Rate limiting on write endpoints
- Don't leak stack traces in production errors
