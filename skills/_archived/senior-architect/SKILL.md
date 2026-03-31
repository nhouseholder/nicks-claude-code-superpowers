---
name: senior-architect
description: Architecture audit and system design skill. When invoked, evaluates the overall architecture — service boundaries, data flow, dependency graph, tech stack choices, scalability risks. Also guides system design for new features. Use when asked to review architecture, design a system, evaluate tech stack, or plan infrastructure.
weight: heavy
---

# Senior Architect — Architecture Review & Design Protocol

## When This Fires
- User says "review the architecture", "design the system", "evaluate tech stack"
- User says "is this scalable", "should we split this", "what's the right approach"
- Hook routes to this skill for architecture-related work

## Architecture Audit Protocol (When Reviewing)

### Step 1: Map the System
- Identify all services/layers (frontend, backend, database, cache, CDN, workers)
- Map data flow: user → frontend → API → database → response
- Identify third-party integrations (auth providers, payment, analytics)
- Check deployment target (Cloudflare, Vercel, AWS, etc.) and its constraints

### Step 2: Structural Assessment
- [ ] **Separation of concerns**: Business logic mixed with routing/UI?
- [ ] **Dependency direction**: Do lower layers depend on higher layers? (bad)
- [ ] **Circular dependencies**: A imports B imports A?
- [ ] **God modules**: Single file doing everything? (>500 lines = split candidate)
- [ ] **Configuration management**: Hardcoded values vs. env vars vs. config files?

### Step 3: Scalability Assessment
- [ ] **Stateless services**: Can horizontally scale? Or tied to local state/filesystem?
- [ ] **Database bottlenecks**: Single DB? Read replicas? Connection pooling?
- [ ] **Caching strategy**: What's cached? What should be? TTL appropriate?
- [ ] **Background jobs**: Long tasks blocking request handlers?
- [ ] **Rate limits**: External API calls rate-limited? Queued?

### Step 4: Tech Stack Fit
- [ ] **Platform constraints**: Using node:fs on serverless? Expecting persistent storage on workers?
- [ ] **Over-engineering**: Microservices for a team of 1? K8s for 100 users?
- [ ] **Under-engineering**: Monolith hitting scaling walls? Missing caching layer?
- [ ] **Dependency risk**: Critical deps unmaintained? Single points of failure?

### Step 5: Output
Architecture summary with:
- Current architecture diagram (ASCII or description)
- Issues ranked by severity
- Recommended changes with effort estimates (small/medium/large)

## System Design Protocol (When Designing New Features)

1. **Clarify requirements** (use spec-interview if complex)
2. **Identify bounded contexts** — what data/logic belongs together?
3. **Choose patterns** — MVC, event-driven, CQRS, etc.
4. **Evaluate trade-offs** — document what you're choosing and what you're giving up
5. **Design for the current scale** — not 10x ahead (that's over-engineering)
6. **Output: design document** with data flow, API contracts, and migration path
