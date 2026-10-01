---
name: seo-content-refresh
description: >-
  Find decaying or underperforming pages and decide per URL whether to refresh, rewrite, consolidate, redirect or prune, then execute the refresh and measure recovery. Use when asked about "content decay", "traffic dropped on blog posts", "refresh old content", "content audit", "which articles should we update", "recover lost rankings", or "prune thin content".
metadata:
  department: "seo"
  domain: "content"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Content refresh and decay recovery

Updating existing pages that already have links and history is usually higher return than new content. The skill is deciding which action each URL needs.

## 1. Detect decay
Data needed: Search Console performance by page (compare last 3 months vs previous 3 and vs same period last year for seasonality), analytics sessions and conversions, a crawl or sitemap URL list, backlink counts per URL if available.

Flag a page when any of these hold:
- Clicks down 25 percent or more period over period, not explained by seasonality.
- Average position slipped by 3 or more places on its main queries.
- Impressions stable but CTR falling (SERP change, AI Overview, stronger titles).
- Position 4-20 with meaningful impressions (striking distance).
- No clicks in 12 months and no assisted conversions.

## 2. Diagnose the cause (do this before editing)
| Symptom | Likely cause | Action |
|---|---|---|
| Rankings fell after a competitor published | Content gap or staleness | Refresh with the new coverage |
| New SERP features or AI Overview | CTR loss, not ranking loss | Retitle, win the feature, target deeper queries |
| Intent shifted (SERP is now tools or listicles) | Format mismatch | Rewrite to the new format |
| Date-sensitive facts, screenshots, product names out of date | Staleness | Update facts, visuals, dates |
| Two of your pages rank alternately | Cannibalisation | Merge and 301 the weaker |
| Sitewide drop on many pages | Technical or algorithmic | Escalate to a technical audit, do not refresh page by page |
| Lost backlinks or broken internal links | Authority erosion | Fix links, reclaim |

## 3. Decide the action per URL
- **Refresh:** good topic, still matches intent, content aging. Keep URL.
- **Rewrite:** right keyword, wrong depth or format. Keep URL.
- **Consolidate:** overlapping pages; merge the best parts into the strongest URL, 301 the rest.
- **Redirect:** topic dead but page has links; 301 to the closest relevant page.
- **Prune (410/404):** no traffic, no links, no value, thin.
- **Leave:** evergreen and performing.
Never mass-delete; check links and conversions first.

## 4. Execute a refresh
1. Re-run the SERP and intent check.
2. Verify every fact, statistic, price, screenshot, link and product reference; replace stale ones with current primary sources.
3. Add what top results now have and you lack; add first-hand experience, a named author and a real review date.
4. Improve the intro and headings for the current query set; update the title and meta for CTR.
5. Add internal links from newer pages and fix broken ones.
6. Keep the URL. Update the visible "last updated" date only for substantive changes; keep the structured data dateModified consistent with it. Do not fake freshness by changing dates alone.
7. Request indexing in Search Console after publishing, and note the change on an annotation log.

## 5. Measure
Re-check at 4 and 8 weeks: position and clicks on target queries, CTR, conversions. Compare against a control group of similar unrefreshed pages. Log wins and losses to learn which kinds of refresh work for this site.

## Output
A prioritised table: URL | issue | diagnosis | action | effort | expected upside (clicks, from striking-distance impressions) | owner | re-check date.

## Do not
Refresh pages that are not decaying. Do not delete pages with referring domains without a redirect. Do not change URLs.
