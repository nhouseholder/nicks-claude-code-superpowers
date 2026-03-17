---
name: data-pipeline-guardian
description: Guard data pipelines, scrapers, cron jobs, and harvest workflows. Detects stale data, failed fetches, missing records, and schema drift. Ensures pipelines are idempotent, incremental, and self-healing. Use when working on scraping, data ingestion, ETL, cron jobs, or harvest scripts.
---

# Data Pipeline Guardian — Keep the Data Flowing

When working on data pipelines, scrapers, cron jobs, or harvest workflows, apply these standards automatically. Data pipelines fail silently — this skill makes failures loud and recovery automatic.

## When This Activates

- Editing scraper/harvest scripts
- Working on cron job configurations (GitHub Actions, Workers Cron)
- Modifying data ingestion or ETL processes
- Debugging missing or stale data
- Any task involving scheduled data fetching

## Pipeline Standards

### 1. Idempotency First
- Running the pipeline twice with the same input must produce the same result
- Use upserts, not blind inserts
- Check for existing records before creating new ones
- Timestamp all records for staleness detection

### 2. Incremental by Default
- Never re-fetch the entire dataset when only new records are needed
- Track high-water marks (last fetched ID, timestamp, page number)
- Cache responses locally — only fetch what's new
- Pipeline should get FASTER with each run, not slower

### 3. Self-Healing
- Retry transient failures (HTTP 429, 500, 503) with exponential backoff
- Skip and log permanent failures (404, invalid data) — don't block the pipeline
- If a source changes schema, detect and alert — don't silently ingest garbage
- Resume from where it left off after interruption

### 4. Observability
Every pipeline run must produce:
- **Start/end timestamps** — how long did it run?
- **Records processed** — how many new/updated/skipped/failed?
- **Errors encountered** — what went wrong and where?
- **Data freshness** — when was the newest record fetched?

### 5. Rate Limiting & Politeness
- Respect API rate limits — add delays between requests
- Use API keys when available (higher limits)
- Implement circuit breakers — if a source is down, back off
- Cache aggressively — never re-fetch data you already have

## Pre-Edit Checklist

Before modifying any pipeline code, verify:
1. **Does it have error handling?** Add try/catch with logging if not
2. **Is it idempotent?** Test: what happens if you run it twice?
3. **Does it track progress?** Can it resume after interruption?
4. **Does it have a dry-run mode?** Add one if missing (--dry-run flag)
5. **Are API keys in env vars?** Never hardcode credentials

## Pipeline Debugging Protocol

When data is missing or stale:
1. Check the last successful run timestamp
2. Check for error logs from recent runs
3. Check if the data source is reachable (curl/fetch test)
4. Check if the source schema changed (compare response to expected shape)
5. Check rate limit status (are we being throttled?)
6. Run a small test fetch manually to isolate the failure

## Common Patterns

### Deduplication
```
- Key on a stable unique identifier (URL, external ID, composite key)
- Never trust auto-increment IDs from external sources
- For dispensary/menu data: dedupe on (name + address) or (chain + location_id)
```

### Geocoding Fallbacks
```
- Primary: GPS coordinates from source API
- Fallback 1: Geocode from full address (Nominatim/Google)
- Fallback 2: City centroid with reduced confidence
- Never store (0, 0) or null coordinates without flagging
```

### Three-Tier Matching
```
- Exact match: normalize and compare (lowercase, strip whitespace)
- Fuzzy match: Levenshtein distance or token overlap with threshold
- Manual review: log unmatched records for human review
```

## Rules

1. **Loud failures** — Pipelines must log errors visibly, never fail silently
2. **Incremental always** — Fetch only what's new, cache everything
3. **Idempotent always** — Safe to re-run without duplicating data
4. **Schema awareness** — Detect when source data shape changes
5. **Rate respect** — Never hammer an API; implement backoff and caching
6. **Resume capability** — Every pipeline must survive interruption and continue
