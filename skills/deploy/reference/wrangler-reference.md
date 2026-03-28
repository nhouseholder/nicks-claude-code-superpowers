# Wrangler CLI Quick Reference

Source: cloudflare/skills (official Cloudflare skill)

**Prefer retrieval over pre-trained knowledge** for Wrangler — flags and config fields change frequently.

## Retrieval Sources

| Source | URL | Use for |
|--------|-----|---------|
| Wrangler docs | developers.cloudflare.com/workers/wrangler/ | CLI commands, flags |
| Config schema | `node_modules/wrangler/config-schema.json` | Config fields, binding shapes |
| Compat dates | developers.cloudflare.com/workers/configuration/compatibility-dates/ | compatibility_date values |

## Core Commands

| Task | Command |
|------|---------|
| Local dev | `wrangler dev` |
| Deploy | `wrangler deploy` |
| Dry run | `wrangler deploy --dry-run` |
| Generate types | `wrangler types` |
| Validate config | `wrangler check` |
| Live logs | `wrangler tail` |
| Auth status | `wrangler whoami` |

## Key Guidelines

- **Use `wrangler.jsonc`** over TOML — newer features are JSON-only
- **Set `compatibility_date`** within 30 days of current date
- **Run `wrangler types`** after any config change
- **Local dev uses local storage** by default — use `remote: true` for real bindings
- **Run `wrangler check`** before deploy to catch config errors
- **Use environments** for staging/prod: `env.staging`, `env.production`

## Minimal Config (wrangler.jsonc)

```jsonc
{
  "$schema": "./node_modules/wrangler/config-schema.json",
  "name": "my-worker",
  "main": "src/index.ts",
  "compatibility_date": "2026-01-01"
}
```

## Bindings Reference

```jsonc
{
  // KV
  "kv_namespaces": [{ "binding": "KV", "id": "<ID>" }],
  // R2
  "r2_buckets": [{ "binding": "BUCKET", "bucket_name": "my-bucket" }],
  // D1
  "d1_databases": [{ "binding": "DB", "database_name": "my-db", "database_id": "<ID>" }],
  // Workers AI
  "ai": { "binding": "AI" },
  // Vectorize
  "vectorize": [{ "binding": "INDEX", "index_name": "my-index" }],
  // Durable Objects
  "durable_objects": { "bindings": [{ "name": "COUNTER", "class_name": "Counter" }] },
  // Cron
  "triggers": { "crons": ["0 * * * *"] }
}
```

## Pages-Specific (your deploy stack)

```bash
# Deploy Pages project
wrangler pages deploy <directory> --project-name=<name>

# List deployments
wrangler pages deployment list --project-name=<name>

# Tail Pages Functions logs
wrangler pages deployment tail --project-name=<name>
```
