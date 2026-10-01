---
name: seo-on-page-optimization
description: >-
  Audit and optimise a single page's on-page SEO: title, meta description, headings, intro, body coverage, internal links, images, schema and snippet eligibility, with concrete before/after rewrites. Use when asked to "optimise this page for SEO", "on-page SEO review", "fix the title tag and meta", "why does this page not rank", "improve CTR", or "SEO check before publishing".
metadata:
  department: "seo"
  domain: "content"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# On-page optimisation

Scope: one URL at a time. Site-wide crawl, speed and indexation problems belong to technical SEO; here assume the page is crawlable and indexable, and verify that first.

## Preflight (2 minutes)
- Is the URL indexed (site: query or Search Console URL Inspection)? Canonical self-referencing? No noindex? If not, stop and fix that.
- Pull Search Console data for the URL: top queries, impressions, average position, CTR. Optimise for the queries it already earns impressions for.
- Run `seo-search-intent-analysis` on the primary query. Intent mismatch outweighs every tweak below.

## Workflow
1. **Title tag.** Primary keyword near the start, a distinct benefit or qualifier, brand last, roughly 50-60 characters (pixel width is the real limit). Unique per page. Do not stuff. If CTR is low for the position, test a title that matches the dominant query phrasing plus a differentiator.
2. **Meta description.** 120-155 characters, written as ad copy: what the reader gets, a proof point, a soft call to action. It does not rank directly; it earns clicks. Google may rewrite it; that is fine.
3. **H1 and heading structure.** One H1 that matches the page promise. H2s mirror the questions searchers ask, in the order they ask them; H3s only for real sub-points. Headings must read as an outline of the page on their own.
4. **Intro.** Within the first 100 words state the answer or promise and who it is for. Remove throat-clearing.
5. **Body coverage.** Compare with the top ranking pages: which sub-topics, definitions, examples, tables or tools do they include that you lack? Add those only where they help the reader. Add original value (data, process, screenshots, worked example).
6. **Keyword use.** Primary term in title, H1, first paragraph and naturally elsewhere with variants and related entities. No density target.
7. **Internal links.** 3-8 contextual links to relevant pages with descriptive anchors; ensure at least 2-3 relevant pages link to this one. Replace generic anchors ("click here").
8. **External links.** Cite primary sources; no links to low-quality sites. Default behaviour needs no nofollow except sponsored (rel="sponsored") and user-generated (rel="ugc").
9. **Images and media.** Descriptive file names, alt text that describes the image for a screen-reader user (not keyword lists), dimensions set, modern format, lazy loading below the fold. Add a diagram or table where a paragraph is explaining structure.
10. **URL.** Short, readable, hyphenated. Do not change an indexed URL without a 301 and a strong reason.
11. **Structured data.** Add the schema type that matches visible content (Article, FAQPage only if eligible and visible, Product, BreadcrumbList, Organization). Validate with the Rich Results Test. Never mark up content that is not on the page.
12. **Snippet eligibility.** For question queries add a concise definition or numbered steps or a small table directly under the relevant H2.
13. **UX and conversion.** Clear CTA, readable layout on mobile, no intrusive interstitials, table of contents on long pages.

## Output
A changelog with before and after for title, meta, H1, intro and each material edit, plus a prioritised list (high / medium / low) of remaining actions, and the query set and date to re-measure (allow 4-8 weeks).

## Failure modes
- Rewriting a title that already ranks well and losing position. Change one variable at a time on high-traffic pages and annotate the date.
- Chasing every competitor subtopic and bloating the page.
- Keyword in every heading.
- Optimising a page whose real problem is intent mismatch or lack of authority.

## Do not
Promise rankings. State expected effect as a hypothesis with a measurement plan.
