---
name: seo-core-web-vitals
description: >-
  Diagnose and fix Core Web Vitals and page speed (LCP, INP, CLS, TTFB) using field data first. Use for "Core Web
  Vitals failing", "poor LCP", "INP problem", "CLS layout shift", "PageSpeed Insights score", "slow site",
  "Lighthouse says", "CrUX", "page experience report" or "improve site speed for SEO".
metadata:
  department: "seo"
  domain: "technical"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Core Web Vitals and page speed

## Current metrics and thresholds (assessed at the 75th percentile of real-user field data, mobile and desktop separately)
| Metric | Good | Needs improvement | Poor |
|---|---|---|---|
| LCP Largest Contentful Paint | <= 2.5 s | 2.5-4.0 s | > 4.0 s |
| INP Interaction to Next Paint | <= 200 ms | 200-500 ms | > 500 ms |
| CLS Cumulative Layout Shift | <= 0.1 | 0.1-0.25 | > 0.25 |
Supporting: TTFB <= 800 ms (good), FCP <= 1.8 s. INP replaced FID in March 2024; do not cite FID. A URL group
passes only if all three metrics are Good. Core Web Vitals are a (modest) ranking signal; relevance dominates,
but poor CWV loses ties and hurts conversion.

## Data hierarchy
1. **Field (real users)**: CrUX via PageSpeed Insights "Discover what your real users experience", CrUX API /
   BigQuery, Search Console Core Web Vitals report (groups URLs by template), or your own RUM using the
   `web-vitals` library. Field data is the verdict. CrUX is a 28-day rolling window, so fixes take about a month
   to show fully; low-traffic URLs have no CrUX data (use origin-level data or RUM).
2. **Lab (Lighthouse, WebPageTest, DevTools)**: for diagnosis and regression testing only. Lab cannot measure INP
   without interaction (it reports TBT as a proxy). A Lighthouse score of 100 does not mean CWV pass.

## Workflow
1. Identify failing **templates** in GSC (Poor/Needs improvement groups) and confirm with CrUX at origin and URL
   level by device. Fix templates, not individual URLs.
2. Reproduce in lab on the representative URL with mobile throttling (Moto G class CPU slowdown 4x, slow 4G) and
   in DevTools Performance panel; capture a trace. For INP use the "Interactions" track or the Web Vitals
   extension / RUM attribution (`web-vitals/attribution`) to find the offending element and interaction.
3. Diagnose by metric (below). Change one thing, re-measure in lab, ship, then watch field data for 28 days.
4. Add a performance budget (e.g. LCP image <= 200 KB, JS <= 300 KB compressed on key templates) to CI.

## LCP (loading)
Break LCP into four parts and find the biggest: TTFB, resource load delay, resource load duration, element render delay.
- Slow TTFB: CDN/edge caching, full-page cache, DB/query tuning, avoid redirect chains, HTTP/2 or 3, `Cache-Control`.
- LCP resource discovered late: do not lazy-load the LCP image; add `fetchpriority="high"` to it; preload when
  it is only discoverable via CSS/JS (`<link rel="preload" as="image" href="..." fetchpriority="high">`); keep
  the `<img>` in server HTML, not client-rendered.
- Heavy resource: modern formats (AVIF/WebP), responsive `srcset`/`sizes`, correct dimensions, compression.
- Render delay: remove render-blocking CSS/JS in head, inline critical CSS, `defer` scripts, fix web-font blocking
  (`font-display: swap`, preload the key WOFF2, subset fonts).

## INP (responsiveness: worst interaction latency across the page visit)
Split into input delay, processing time, presentation delay.
- Long tasks (>50 ms) on the main thread: split work, `scheduler.yield()` / `setTimeout` chunking, move to a Web
  Worker, debounce handlers.
- Third-party scripts (tag managers, chat, A/B testing, ads): audit each; load after interaction or on consent;
  remove unused tags. This is the most common cause.
- Expensive re-renders (React/Vue): memoise, virtualise long lists, avoid layout thrash, reduce DOM size (keep
  well under ~1,500 nodes where possible).
- Presentation delay: avoid large style/layout recalculation after the click; use `content-visibility: auto`.

## CLS (visual stability)
- Always set `width`/`height` (or `aspect-ratio`) on images, video, iframes, embeds, ad slots; reserve space.
- Inject no content above existing content after load (banners, consent bars, late fonts: use `size-adjust`/
  fallback metrics to limit font-swap shift).
- Animate with `transform`/`opacity`, not `top/left/height`.
- bfcache-eligible pages (avoid `unload` handlers, `Cache-Control: no-store`) improve back/forward behaviour.

## Delivery checklist
Brotli/gzip enabled, long-lived immutable caching for hashed static assets, preconnect to critical third-party
origins, HTTP/2+, image CDN, no render-blocking third-party in `<head>`, prioritise above-the-fold, lazy-load below the fold only.

## Output
Per template: metric | field p75 | main cause (with trace evidence) | fix | owner | expected effect | validation
date. Include a before/after table from CrUX/RUM at 28 days.

## Do not
- Optimise to the Lighthouse score or to desktop only; mobile field data decides.
- Lazy-load everything including the hero image.
- Add a speed plugin stack without measuring; plugins often add JS and hurt INP.
- Declare success from a one-day lab improvement; wait for the CrUX window.
