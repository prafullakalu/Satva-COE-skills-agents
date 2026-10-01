---
name: seo-site-architecture-internal-linking
description: >-
  Design or fix site architecture, URL structure and internal linking so authority and crawling reach the pages
  that matter. Use for "site structure", "information architecture for SEO", "orphan pages", "click depth",
  "internal linking audit", "topic cluster links", "faceted navigation", "pagination SEO", "breadcrumbs", "URL
  structure best practice" or "pillar page linking".
metadata:
  department: "seo"
  domain: "technical"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Site architecture and internal linking

Internal links are the only ranking lever fully under your control. They do three jobs: discovery (can Google
find it), context (anchor text and surrounding text say what it is), and prioritisation (more and
closer links from strong pages signal importance).

## Workflow
1. **Inventory.** Crawl the site and join with GSC (clicks, impressions) and GA4 (landing sessions, conversions)
   and, if available, backlink data per URL. Output one row per URL: depth, unique inlinks, outlinks, template,
   traffic, revenue, backlinks.
2. **Map the intended structure.** Home -> hubs (categories/services/topics) -> detail pages. Draw it. Compare to
   the crawled graph. Differences are the findings.
3. **Measure**:
   - Click depth: money pages <=3 clicks from home (blog long tail may be deeper, but check indexation there).
   - Orphans: URLs in sitemap/GSC/analytics but zero crawlable inlinks. Join the three URL sets.
   - Inlink distribution: high-value pages with few inlinks; low-value pages (tags, archives, login) with many.
   - Anchor quality: share of generic anchors ("click here", "read more", bare URL); anchors repeated for
     many different targets.
   - Link validity: links to redirected, 404, non-canonical or noindexed URLs.
   - Link implementation: real `<a href>` elements. Links created only by `onclick`, `<div>`, or hash routing
     without crawlable URLs are not followed.
4. **Prioritise targets**: pages with high conversion value and low inlink count or rank 4-20 (striking
   distance). Source pages: high-authority, topically related, already ranking/linked.
5. **Write the link plan**: source URL | target URL | anchor | placement (body, nav, related block) | status.
   Prefer contextual body links; sitewide footer/nav links carry less distinct meaning.
6. **Implement and re-crawl**; track target rankings/impressions for 4-8 weeks.

## Structure rules
- **Hub and spoke**: each hub links to every spoke; every spoke links back to the hub and to 2-4 sibling
  spokes where relevant. A flat list of unrelated "related posts" is noise.
- **Navigation**: keep primary nav to the commercial hubs; do not link every page sitewide. Mega-menus are
  fine if links are real `<a>` in the initial HTML.
- **URLs**: lowercase, hyphen-separated, short, reflect hierarchy (`/services/seo-audit/`), no session IDs,
  no tracking parameters in internal links, consistent trailing-slash policy enforced by 301. Do not change
  URLs for aesthetics; every URL change is a migration (`seo-site-migration`).
- **Breadcrumbs**: visible `Home > Category > Page` trail on all deep templates, with `BreadcrumbList`
  schema (see `seo-schema-markup`). It adds hierarchy links and clarifies structure.
- **Pagination**: each page has a crawlable `<a href>` to next/prev with its own URL (`?page=2` or
  `/page/2/`), self-referencing canonical (not canonical to page 1), unique title suffix. Google ignores
  `rel=next/prev`. "Load more" and infinite scroll need real paginated URLs behind them.
- **Faceted navigation**: decide per facet whether it has search demand. Demand -> indexable static URL with
  its own title/H1/content. No demand -> keep crawlable only as needed, canonical to the unfaceted parent,
  or block the parameter space in robots.txt if it explodes into millions of URLs (and ensure the products
  remain reachable through category pagination). Never combine robots block and canonical on the same URLs and
  expect the canonical to be seen.
- **Canonical vs internal links**: internal links must point at the canonical URL; do not rely on the canonical tag
  to clean up inconsistent linking.
- **nofollow**: use on user-generated or paid links (`rel="ugc"`, `rel="sponsored"`); do not use nofollow on
  internal links to "sculpt" PageRank; it just discards the flow.
- **Anchor text**: descriptive and varied but natural; the same target may have 3-5 anchor variants. Image
  links use the `alt` text as anchor.
- **Link count**: no hard limit; but each page's links should be useful. Hundreds of boilerplate links dilute
  prominence and bloat HTML.

## Quick diagnostics
- Orphan = (sitemap URLs + GSC URLs + analytics landing URLs) minus (crawl-discovered URLs via links).
- Depth histogram: share of indexable pages at depth 1,2,3,4,5+. A long tail beyond depth 5 correlates with
  "Discovered - not indexed".
- Internal PageRank approximation: run a link-graph calculation in the crawler or a script over the edge list;
  rank URLs and compare against business priority.

## Output
Architecture diagram (text tree is fine), findings table, link-plan spreadsheet columns above, and a
rollout list split into template-level changes (nav, breadcrumbs, related-content module) versus one-off edits.

## Do not
- Bulk-insert exact-match anchors; keep it editorial.
- Fix orphans by adding them to a footer; link them from the relevant hub and from related content.
- Noindex or delete low-traffic pages without checking whether they carry internal link equity or backlinks.
- Create a "sitemap page" of 10,000 links as an architecture fix.
