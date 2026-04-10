---
name: senior-backend
description: "Backend audit, architecture, and development — APIs, middleware, auth, DB, error handling, service boundaries, scalability, tech stack. Use for backend audits, API/architecture review, system design, or backend features."
weight: heavy
---

# Senior Backend & Architecture — Audit & Build Protocol

## When This Fires
- User says "audit the backend", "review the API", "check server code"
- User says "build an API", "add an endpoint", "fix the server"
- User says "review the architecture", "design the system", "evaluate tech stack", "is this scalable"
- Hook routes to this skill for backend or architecture work

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

## Architecture Review Protocol (When Reviewing Architecture)

### Structural Assessment
- [ ] **Separation of concerns**: Business logic mixed with routing/UI?
- [ ] **Dependency direction**: Do lower layers depend on higher layers? (bad)
- [ ] **Circular dependencies**: A imports B imports A?
- [ ] **God modules**: Single file >500 lines = split candidate
- [ ] **Configuration management**: Hardcoded values vs. env vars vs. config files?

### Scalability Assessment
- [ ] **Stateless services**: Can horizontally scale? Or tied to local state?
- [ ] **Database bottlenecks**: Single DB? Read replicas? Connection pooling?
- [ ] **Caching strategy**: What's cached? What should be? TTL appropriate?
- [ ] **Background jobs**: Long tasks blocking request handlers?
- [ ] **Rate limits**: External API calls rate-limited? Queued?

### Tech Stack Fit
- [ ] **Platform constraints**: Using node:fs on serverless? Persistent storage on workers?
- [ ] **Over-engineering**: Microservices for a team of 1? K8s for 100 users?
- [ ] **Under-engineering**: Monolith hitting scaling walls? Missing caching layer?
- [ ] **Dependency risk**: Critical deps unmaintained? Single points of failure?

### Output
Architecture summary with issues ranked by severity + effort estimates (small/medium/large).

## System Design Protocol (When Designing New Features)
1. **Clarify requirements** (use spec-interview if complex)
2. **Identify bounded contexts** — what data/logic belongs together?
3. **Choose patterns** — MVC, event-driven, CQRS, etc.
4. **Evaluate trade-offs** — document choices and what you're giving up
5. **Design for current scale** — not 10x ahead
6. **Output: design document** with data flow, API contracts, migration path
