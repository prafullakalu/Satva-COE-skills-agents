---
name: seo-search-console-diagnostics
description: >-
  Use Google Search Console data to report on and diagnose organic performance: traffic drops, query and page
  analysis, CTR opportunities, indexing and enhancement reports, Search Analytics API pulls. Use for "Search
  Console report", "why did clicks drop", "GSC analysis", "low CTR pages", "striking distance keywords", "GSC API",
  "performance report", "cannibalisation", "branded vs non-branded" or "monthly SEO report".
metadata:
  department: "seo"
  domain: "analytics"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Search Console reporting and diagnostics

## Know the data
- **Metrics**: clicks, impressions, CTR (clicks/impressions), position (average of the top position of the site in
  each impression; an average, so inspect by query/page, never sitewide only).
- **Retention**: 16 months. Export monthly to BigQuery (bulk data export) or Sheets so history survives.
- **Property type**: Domain property (DNS verified) covers all protocols and subdomains: prefer it. URL-prefix
  properties for per-folder views.
- **Anonymised queries**: a share of queries is hidden, so query-level sums are lower than page/total sums. UI exports
  cap at 1,000 rows; the API returns up to 25,000 rows per request (page with `startRow`), and a per-day-per-property
  cap exists on the underlying data (~50k rows per search type per day), so very long-tail data is incomplete.
- **Freshness**: ~2 day lag; today and yesterday are partial. Comparisons need equal days-of-week.
- Google has changed how impressions are counted over time (e.g. results-per-page behaviour). Annotate known
  data-collection changes on charts before reading a step change as a ranking change.

## Standard report (monthly)
1. Totals vs previous period and vs same period last year (seasonality): clicks, impressions, CTR, position.
2. Split: branded vs non-branded queries (regex of brand terms and misspellings in the Query filter);
   Device; Country; Search appearance; Search type (Web/Image/Video/News/Discover separately).
3. Top gaining and losing pages and queries (delta table) with reasons.
4. Index health: Indexing > Pages, count of valid vs not indexed by reason, sitemap indexed vs submitted.
5. Experience/enhancements: Core Web Vitals groups, HTTPS, Breadcrumbs/Products/etc. errors.
6. Manual actions and Security issues (must be empty; if not, escalate immediately).
7. Actions list with owner and expected impact.

## Traffic drop diagnosis (follow in order)
1. **Is it real?** Compare clicks and impressions. Check GA4 organic and other sources, and tracking breakage.
2. **When?** Daily chart; match to deploys, migrations, robots/CDN changes, Google core/spam updates (Search Status
   Dashboard), seasonality, outages.
3. **Where?** Segment by page group/directory, device, country, query type (branded/non-branded), search appearance.
   Sitewide drop = technical or penalty; one section = template/content/competition; one device = mobile issue.
4. **Impressions down vs CTR down vs position down**:
   - Impressions down, position stable: demand fell or fewer queries indexed -> check indexing and seasonality.
   - Position down, impressions down: lost rankings -> content/links/relevance/algorithm; compare to winners in SERP.
   - Impressions flat, CTR down: SERP features (AI Overviews, snippets), title/meta change, competitor rich results.
5. **Index and crawl**: Pages report deltas; Crawl stats (Settings) for 5xx/host status; robots.txt report; URL
   Inspection of top losers (canonical choice flipped? noindex? soft 404?).
6. **Confirm**: reproduce in SERP from the target country/device; fix; log the hypothesis and date.

## Opportunity finders
- **Low CTR, high impressions**: pages at positions 1-10 with CTR below the curve for their position; rewrite
  title/meta to match intent, add rich result eligibility.
- **Striking distance**: queries at average position 8-20 with meaningful impressions: improve content depth,
  internal links, anchor text.
- **Cannibalisation**: Query filter, then Pages; multiple URLs alternating for one query with split clicks:
  consolidate (merge+301), differentiate intent, or adjust internal links.
- **Decaying content**: pages losing impressions YoY; refresh.
- **Zero-click queries and new queries**: content gaps from impressions with no dedicated page.

## Search Analytics API essentials
Request body: `startDate`, `endDate`, `dimensions` (`date, query, page, country, device, searchAppearance`),
`dimensionFilterGroups`, `rowLimit` (<=25000), `startRow`, `dataState` (`final` or `all`), `type`
(`web`...). Auth: OAuth/service account added as a user on the property; never commit credentials. URL Inspection
API: ~2,000 queries/day and 600/min per property, use for sampling top templates, not mass checking.

## Output
A dated report: summary (3 bullets), charts/tables listed above, causes with evidence, prioritised actions, and
"what I could not determine" (data gaps, anonymised queries, no GA4 access).

## Do not
- Quote "average position" sitewide as a KPI without segmentation.
- Compare a partial last week to a full week, or ignore day-of-week.
- Blame the algorithm before ruling out tracking, indexing and your own deploys.
- Pass service account keys or tokens in chat; keep them in a secret manager.
