# Web Performance Audit Reference

Source: cloudflare/skills (official Cloudflare web-perf skill)

## Core Web Vitals Thresholds

| Metric | Good | Needs Work | Poor |
|--------|------|------------|------|
| TTFB | < 800ms | < 1.8s | > 1.8s |
| FCP | < 1.8s | < 3s | > 3s |
| LCP | < 2.5s | < 4s | > 4s |
| INP | < 200ms | < 500ms | > 500ms |
| TBT | < 200ms | < 600ms | > 600ms |
| CLS | < 0.1 | < 0.25 | > 0.25 |
| Speed Index | < 3.4s | < 5.8s | > 5.8s |

## Audit Checklist

```
- [ ] Phase 1: Performance trace (navigate + record)
- [ ] Phase 2: Core Web Vitals analysis (LCP, CLS, render blocking)
- [ ] Phase 3: Network analysis (blocking resources, chains, caching)
- [ ] Phase 4: Accessibility snapshot
- [ ] Phase 5: Codebase analysis (framework, bundler, tree-shaking)
```

## Key Guidelines

- **Be assertive** — verify claims by checking network/DOM, then state findings definitively
- **Quantify impact** — use estimated savings. Don't prioritize 0ms-impact changes
- **Skip non-issues** — a site with 200ms LCP and 0 CLS is already excellent
- **Be specific** — "compress hero.png (450KB) to WebP" not "optimize images"
- **Prioritize ruthlessly** — biggest impact first

## Network Analysis Checklist

1. **Render-blocking resources** — JS/CSS in `<head>` without `async`/`defer`/`media`
2. **Network chains** — resources discovered late (CSS imports, JS-loaded fonts)
3. **Missing preloads** — critical fonts, hero images, key scripts
4. **Caching issues** — missing/weak `Cache-Control`, `ETag`, `Last-Modified`
5. **Large payloads** — uncompressed JS/CSS bundles
6. **Unused preconnects** — verify zero requests went to that origin before removing

## Codebase Analysis

### Framework Detection

| Tool | Config Files |
|------|-------------|
| Vite | `vite.config.js/ts` |
| Next.js | `next.config.js/mjs` |
| Webpack | `webpack.config.js` |
| Astro | `astro.config.mjs` |

### Common Optimization Targets

- **Barrel files** — `index.js` re-exports defeat tree-shaking
- **Wholesale imports** — `import lodash` vs `import get from 'lodash/get'`
- **PurgeCSS/Tailwind** — check `content` config covers all template files
- **Polyfills** — check `browserslist` isn't overly broad
- **Source maps** — should be external or disabled in production
- **Compression** — verify gzip/brotli on build output or server config
