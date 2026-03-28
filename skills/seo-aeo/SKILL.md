---
name: seo-aeo
description: SEO and Answer Engine Optimization for portfolio sites. Covers metadata, Open Graph, JSON-LD structured data, sitemaps, robots.txt, EEAT signals, and AI-answer readiness. Use during site builds, redesigns, or audits.
weight: light
---

# SEO & AEO — Be Findable by Search Engines and AI

Source: sanity-io/agent-toolkit seo-aeo-best-practices (cherry-picked, Sanity-specific code removed)

## When to Apply

- During `/site-redesign` or `/site-update` — check SEO after visual changes
- During `/site-audit` or `/site-review` — include SEO checklist
- When building any new page or site
- When user asks about SEO, metadata, or structured data

## Technical SEO Checklist

### Metadata (every page)
- [ ] Title tag: unique, 50-60 chars, primary keyword near start
- [ ] Meta description: unique, 150-160 chars, includes CTA
- [ ] Open Graph: `og:title`, `og:description`, `og:image` (1200x630), `og:url`, `og:type`
- [ ] Canonical URL set (prevents duplicate content)

### Infrastructure
- [ ] Sitemap at `/sitemap.xml` — dynamic from content, includes `lastModified`
- [ ] `robots.txt` — allow `/`, disallow `/api/`, `/studio/`, etc.
- [ ] HTTPS enforced
- [ ] No broken internal links

### Performance (SEO impact)
- [ ] LCP < 2.5s, INP < 200ms, CLS < 0.1
- [ ] Images: WebP/AVIF, explicit dimensions, lazy loading below fold
- [ ] Fonts: `display: swap`, preloaded

## JSON-LD Structured Data

Add to every page. Use `@graph` to combine multiple schemas:

```tsx
function JsonLd({ data }) {
  return (
    <script
      type="application/ld+json"
      dangerouslySetInnerHTML={{ __html: JSON.stringify(data) }}
    />
  )
}
```

### Common Schema Types

**Article/Blog Post:**
```json
{
  "@type": "Article",
  "headline": "...",
  "datePublished": "...",
  "dateModified": "...",
  "author": { "@type": "Person", "name": "..." },
  "publisher": { "@type": "Organization", "name": "...", "logo": { "@type": "ImageObject", "url": "..." } }
}
```

**FAQ Page:**
```json
{
  "@type": "FAQPage",
  "mainEntity": [{ "@type": "Question", "name": "...", "acceptedAnswer": { "@type": "Answer", "text": "..." } }]
}
```

**Organization:**
```json
{
  "@type": "Organization",
  "name": "...", "url": "...", "logo": "...",
  "sameAs": ["https://twitter.com/...", "https://linkedin.com/..."]
}
```

**Breadcrumb:**
```json
{
  "@type": "BreadcrumbList",
  "itemListElement": [{ "@type": "ListItem", "position": 1, "name": "...", "item": "..." }]
}
```

### Combining Schemas
```json
{
  "@context": "https://schema.org",
  "@graph": [articleSchema, breadcrumbSchema, orgSchema]
}
```

### Testing
- Google Rich Results Test: search.google.com/test/rich-results
- Schema.org Validator: validator.schema.org

## EEAT Signals

Experience, Expertise, Authoritativeness, Trustworthiness — Google's content quality framework.

**Implement on every site:**
- Author bios with credentials and relevant experience
- Publication and update dates displayed prominently
- `dateModified` in structured data
- Contact information visible
- HTTPS + privacy policy
- Citations to primary sources

## Answer Engine Optimization (AEO)

Optimize content for AI assistants (ChatGPT, Perplexity, Google AI Overviews):

### Content Structure
1. **Lead with the answer** — direct answer first, then explanation
2. **Heading = question** — "What is X?" > "Overview"
3. **Use lists and tables** — AI extracts structured data more easily
4. **FAQ format** — question-answer pairs are ideal for AI extraction
5. **Cover follow-up questions** — anticipate related queries

### AI Crawler Management (robots.txt)
```
# Decide per-site whether to allow AI crawlers
# Allowing = more AI citations. Blocking = no AI training use.
# User-agent: GPTBot
# User-agent: ClaudeBot
# User-agent: PerplexityBot
# User-agent: Google-Extended
```

`Google-Extended` blocks AI training while keeping Google Search indexing.

## Next.js Implementation

```tsx
// app/layout.tsx or page.tsx
export async function generateMetadata({ params }): Promise<Metadata> {
  return {
    title: "...",
    description: "...",
    openGraph: {
      images: [{ url: "...", width: 1200, height: 630 }],
    },
    alternates: {
      canonical: `https://example.com/${params.slug}`,
    },
  }
}
```

```tsx
// app/sitemap.ts
export default async function sitemap(): Promise<MetadataRoute.Sitemap> {
  const pages = await getPages()
  return pages.map(page => ({
    url: `https://example.com${page.path}`,
    lastModified: new Date(page.updatedAt),
  }))
}
```

## Rules

1. **Every page needs metadata** — title, description, OG tags, canonical
2. **Every site needs infrastructure** — sitemap, robots.txt, HTTPS
3. **Add structured data** — JSON-LD for the content type (Article, FAQ, Organization, Product)
4. **Lead with answers** — AI and featured snippets prefer direct answers
5. **Show EEAT signals** — author, dates, credentials, sources
6. **Test structured data** — use Google Rich Results Test before deploying
7. **Decide on AI crawlers** — explicit allow/block in robots.txt per site
