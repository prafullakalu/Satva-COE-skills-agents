---
name: seo-technical-audit
description: >-
  Run a full technical SEO audit of a website and produce a prioritised fix list. Use when asked for a
  "technical SEO audit", "site audit", "why is our site not ranking", "SEO health check", "pre-launch SEO
  review" or "audit this domain". Orchestrates crawlability, indexation, architecture, rendering, speed, schema,
  international and security checks, and routes each deep-dive to the specialist skill.
metadata:
  department: "seo"
  domain: "technical"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Technical SEO audit

A technical audit answers one question: is anything stopping Google from discovering, rendering, indexing and
trusting the pages that should earn traffic? It is not a list of every Lighthouse warning. Rank findings by
revenue-page impact, not by count.

## Inputs to collect first
- Canonical domain, all hostnames/subdomains in scope, CMS/framework, hosting/CDN.
- Read access to Google Search Console (Domain property preferred) and GA4. Without GSC, say so: every
  indexation conclusion drops from "confirmed" to "inferred".
- The 10-30 URLs that make money (templates: home, category, product/service, article, location, contact).
- Recent changes: migration, redesign, CMS swap, robots/CDN change, release dates. Correlate to traffic drops.

## Workflow
1. **Scope and baseline.** Pull 16 months of GSC clicks/impressions and GA4 organic sessions. Note drops and
   the date. Segment by template/directory, not just sitewide.
2. **Crawl the site** with a crawler configured as Googlebot Smartphone (Screaming Frog, Sitebulb or similar;
   respect robots only when asked to mimic Google). Run twice if the site is JS-heavy: raw HTML and rendered.
   Export: URL, status, indexability, canonical, robots meta/X-Robots-Tag, title, H1, depth, inlinks, word count,
   hreflang, response time.
3. **Check the gates in this order** (a failure at gate N makes later gates moot for that URL):
   1. Reachable: DNS, TLS, 200 status, no 5xx or timeouts (see `seo-crawl-indexation-diagnosis`).
   2. Allowed: robots.txt, meta robots, X-Robots-Tag, auth walls.
   3. Renderable: content and links present after rendering (see `seo-javascript-rendering`).
   4. Canonical: self-referencing, consistent with sitemap and internal links.
   5. Discoverable: in the XML sitemap, linked within 3-4 clicks, not orphaned (see `seo-site-architecture-internal-linking`).
   6. Indexed: GSC "Page indexing" status and `site:` sanity check; compare indexed count to sitemap count.
4. **Layer the page-level checks**: speed (`seo-core-web-vitals`), structured data (`seo-schema-markup`),
   international (`seo-hreflang-international`), mobile parity, HTTPS/mixed content, redirects, duplicate titles.
5. **Triage** every finding with the matrix below and write the report.

## Check list (pass/fail evidence required)
| Area | Check | Threshold / rule |
|---|---|---|
| Protocol | One canonical host: http->https and www/non-www 301 to a single version in one hop | no redirect chains > 1 hop |
| Status | Money pages return 200; deleted pages 404/410 (not soft-404 200) | 0 5xx on templates |
| robots.txt | Returns 200, <500 KiB, no `Disallow` on CSS/JS/images/key paths, sitemap declared | 5xx = Google treats as disallow-all |
| Meta robots | No stray `noindex`/`nofollow` on indexable templates; none left over from staging | check X-Robots-Tag too |
| Canonicals | Present, absolute, self-referencing on indexables, point to 200 indexable URL | no canonical to redirect/noindex/404 |
| Sitemap | Only canonical 200 indexable URLs; <=50,000 URLs and <=50 MB uncompressed per file; accurate `lastmod` | `priority`/`changefreq` are ignored by Google |
| Titles / H1 | Unique, present, not truncated templates, one clear H1 | duplicates grouped by template |
| Architecture | Key pages <=3 clicks from home; no orphans; descriptive anchors | depth distribution table |
| Redirects | No chains/loops; 301/308 for permanent | fix internal links to final URL |
| Speed | CrUX p75 passes LCP <=2.5 s, INP <=200 ms, CLS <=0.1 | field data beats lab |
| Mobile | Same content, links, structured data and meta on mobile as desktop (mobile-first indexing) | viewport meta present |
| Structured data | Valid JSON-LD matching visible content | no rich-result spam |
| International | Hreflang reciprocal, valid codes | see hreflang skill |
| Security | Valid TLS, HSTS, no mixed content, no hacked/injected pages | spot-check `site:` for pharma/casino spam |
| Page weight | Critical content and JSON-LD inside the first 2 MB of HTML | Googlebot truncates beyond 2 MB per file |

## Severity matrix
- **Critical**: blocks indexing or sends traffic to wrong URLs on revenue templates (sitewide noindex, robots
  `Disallow: /`, canonical to wrong host, 5xx, redirect loop).
- **High**: suppresses many pages (orphaned category pages, duplicate parameter URLs in the index, failed CWV on a
  top template, broken hreflang on all alternates).
- **Medium**: efficiency/quality (redirect chains, thin duplicates, missing alt text, oversized images).
- **Low**: hygiene (title length, missing optional schema).
Score impact = pages affected x traffic/revenue per page x confidence. Put the top 10 on page one.

## Output format
1. Executive summary (5 lines): overall verdict, top 3 issues, expected effect, effort.
2. Findings table: ID | issue | evidence (URL + screenshot/export row) | affected count | severity | fix | owner.
3. Quick wins (<1 day) versus projects (>1 sprint).
4. Verification plan: how to confirm each fix (re-crawl, URL Inspection "Test live URL", GSC validate-fix).
5. Open questions / data not available.

## Do not
- Report "score out of 100" from a tool as the finding; report the cause and the URLs.
- Recommend "add more keywords", `meta keywords`, or a crawl-delay for Googlebot (ignored).
- Treat lab-only Lighthouse numbers as CWV pass/fail; CWV is assessed on field data at the 75th percentile.
- Ask for `noindex` in robots.txt (unsupported since 2019) or advise blocking pages in robots.txt to deindex them.
- Declare causation from a single correlated date without checking algorithm updates and seasonality.
