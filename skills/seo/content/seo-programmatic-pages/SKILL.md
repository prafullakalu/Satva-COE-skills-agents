---
name: seo-programmatic-pages
description: >-
  Plan and quality-control programmatic SEO: templated pages generated from structured data (locations, integrations, comparisons, use cases, glossaries) at scale without triggering thin-content or scaled-content-abuse problems. Use when asked for "programmatic SEO", "template pages at scale", "integration pages", "city pages", "[X] vs [Y] pages", "generate hundreds of landing pages", or "pSEO".
metadata:
  department: "seo"
  domain: "content"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Programmatic SEO

Programmatic SEO works when each generated page answers a real query with unique, useful data. It fails when it is the same paragraph with a word swapped. Google's spam policy on scaled content abuse applies to pages produced at scale primarily to rank, however they are made.

## 1. Decide whether it fits
Pass all four or do not proceed:
1. **Repeatable pattern:** a head term plus a modifier (`[service] in [city]`, `[tool] integration with [tool]`, `[A] vs [B]`, `[template] for [industry]`) with demand across many modifiers. Validate demand on a sample of 20 modifiers.
2. **Unique data per page:** you own or can license data that differs per page (real specs, pricing, stats, reviews, inventory, setup steps). Without it, stop.
3. **Intent match:** the SERP shows pages of this type ranking. Check with `seo-search-intent-analysis`.
4. **Business value:** each page can convert or support a conversion.

## 2. Design the template
- Data model first: a table with one row per page and the fields that vary. Mark which fields are required; a page with missing required fields is not published.
- Page sections: unique intro driven by data, the data presentation (table, chart, map), expert or editorial section that differs by page, FAQ drawn from real questions about that modifier, related pages, clear CTA.
- Target at least 40-50 percent of the visible body being page-specific. If you cannot show two pages that differ meaningfully, the template is too thin.
- Title, H1, meta description and URL generated from rules with length limits and uniqueness checks.
- Schema appropriate to the content, validated.

## 3. Information architecture and links
- Hub pages (category, city index, integration directory) that list and link to children; breadcrumbs.
- Every page reachable within 3 clicks; no orphan pages.
- Related-page modules based on real relationships, not random.
- XML sitemaps split by template (max 50,000 URLs each) so indexation can be monitored per template.
- Use canonical tags for parameter variants; block faceted or search result pages that create near-infinite URLs.

## 4. Pilot before scale
1. Publish 20-50 pages in one template. Wait 4-6 weeks.
2. Measure indexation rate (Search Console page indexing report), impressions, clicks, and conversion.
3. Healthy: most pages indexed and earning impressions. Warning: "Crawled - currently not indexed" or "Discovered - not indexed" on a large share means quality or demand is missing; improve the template, data or internal links before adding more.
4. Scale in tranches, keep monitoring per sitemap.

## 5. Quality gate (automated where possible)
- Minimum data completeness per page.
- Near-duplicate detection between sibling pages; set a similarity ceiling and fail pages above it.
- No placeholder text, broken variables or empty modules.
- Human review of a random sample (at least 5 percent) per release.
- Factual and compliance review for regulated topics.

## 6. Maintain
Refresh data on a schedule; remove or noindex pages whose data goes stale or whose modifier lost demand; fold low-performers into hubs.

## Output
Opportunity assessment (go / no-go with evidence), data model, template spec with required fields, URL and metadata rules, link architecture, pilot plan with success thresholds, and QA checklist.

## Do not
Use AI to spin near-identical text per page. Do not publish pages without unique data. Do not generate city pages for places you do not serve. Do not launch thousands of pages before a pilot.
