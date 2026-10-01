---
name: seo-keyword-research
description: >-
  Run keyword research that ends in a prioritised, business-aligned keyword list rather than a data dump. Covers seed generation, expansion from Search Console and competitors, volume and difficulty interpretation, business-value scoring and prioritisation. Use when asked for "keyword research", "find keywords for", "what should we rank for", "keyword list for a new site", "which keywords are worth targeting", or "prioritise these keywords".
metadata:
  department: "seo"
  domain: "keywords"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# SEO keyword research

Goal: a ranked list of queries where ranking produces revenue or pipeline, each mapped to one page and one intent. Volume is an input, never the objective.

## Inputs to collect first
1. Business model and what a conversion is (demo, trial, quote, purchase, call).
2. Products/services, ideal customer, geographies, languages.
3. Existing assets: domain, Search Console access, analytics, current rankings, competitor list (3-5 true search competitors, not just business rivals).
4. Constraints: brand terms to avoid, regulated claims, capacity (pages per month).

If Search Console is available, start there. Real impressions beat any tool estimate.

## Workflow
1. **Seed list (30-60 terms).** Sources: product and feature names, the problem in the customer's own words (sales calls, support tickets, reviews, forums), jobs-to-be-done phrasing ("how to reconcile ...", "alternative to ..."), competitor navigation and H1s. Do not start from tool suggestions.
2. **Expand.** Use every source you have access to: Search Console queries (filter impressions > 0; positions 8-40 are the quick wins), autocomplete and "People also ask", related searches, competitor ranking keywords from whichever third-party tool the team licenses, community threads. Record the source for each term.
3. **Normalise.** Merge singular/plural, word-order and typo variants into one row. Keep a `parent` term and `variants`. Never count volume twice for variants that return the same SERP.
4. **Classify intent** per term (informational, commercial investigation, transactional, navigational, local). Use `seo-search-intent-analysis` for anything ambiguous. Check the live SERP for the top terms of each group.
5. **Measure difficulty honestly.** Tool difficulty scores are rough. For each shortlisted term open the SERP and ask: do the top 10 results come from sites with comparable authority? Is the top result an exact-match, high-quality page? Are SERP features (AI Overview, shopping, maps, video) pushing organic below the fold? Record `winnable: yes / stretch / no`.
6. **Score business value** 0-3: 3 = buyer-ready and a direct product fit, 2 = evaluating, 1 = problem aware, 0 = irrelevant to anything we sell.
7. **Prioritise** with a simple score: `priority = value x winnability x volume tier`, where winnability is 1 (no), 2 (stretch), 3 (yes) and volume tier is 1 (<100/mo), 2 (100-1k), 3 (>1k). Sort descending. Low volume with value 3 and winnable 3 beats high volume with value 1.
8. **Map to pages.** One primary keyword per page; list secondary terms that share the same SERP. If two terms need different pages, their SERPs will look different. If a page already exists, flag it as optimise or merge, not create.
9. **Plan the roadmap.** Group into quick wins (existing pages in positions 8-30), new money pages, and supporting content. Hand clusters to `seo-topic-clustering`.

## Output
A table with columns: keyword | variants | source | intent | volume (number or tier, with tool and month) | winnable | value | priority | target URL | action (create / optimise / merge). Followed by 5-10 lines: top opportunities, terms deliberately rejected and why, and data gaps.

## Failure modes
- Targeting terms because volume is high when the audience is not buyers.
- Treating tool difficulty as truth; check the SERP.
- Counting the same demand under ten variants.
- Ignoring "zero-volume" tool terms that Search Console or sales calls prove people use. Long, specific, bottom-funnel queries often show 0 and convert.
- Cannibalisation: two pages for one intent.
- Reporting volumes without tool and month. Volumes are estimates; say so.

## Do not
Fabricate volume or difficulty numbers. If no tool data is available, say so, rank by value and winnability from SERP inspection, and mark volume as unknown.
