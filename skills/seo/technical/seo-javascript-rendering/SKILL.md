---
name: seo-javascript-rendering
description: >-
  Diagnose and fix SEO problems on JavaScript-driven sites (React, Vue, Angular, Next.js, Nuxt, SPAs): content or
  links missing from indexed HTML, rendering strategy, hydration, lazy loading. Use for "JavaScript SEO",
  "Googlebot can't see my content", "SPA indexing", "client-side rendering SEO", "SSR vs CSR for SEO", "React
  site not indexed", "view source is empty" or "rendered HTML differs".
metadata:
  department: "seo"
  domain: "technical"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# JavaScript rendering SEO

Googlebot crawls the raw HTML, queues the page for rendering with an evergreen headless Chromium, then indexes
the rendered DOM. Rendering is deferred and resource-limited; other search engines and most AI/LLM crawlers run
little or no JavaScript. So: anything important should be in the initial HTML.

## What must be in the raw HTML response
Title, meta robots, canonical, hreflang, primary content (headings, body text), internal links as `<a href>`,
structured data for time-sensitive data (price, stock), `<img>` for the LCP element.
Rules from Google's guidance:
- If raw HTML and rendered DOM disagree on canonical, Google may use either: make them identical.
- A `noindex` in raw HTML may be honoured even if JS removes it later. Never rely on JS to relax a noindex.
- Pages returning non-200 are generally not rendered; content/meta injected by JS on error pages is lost.
- Soft-404 SPA: client router shows "not found" but server returns 200. Return a real 404 status server-side
  (or a `noindex` plus redirect to a genuine 404 URL).

## Workflow
1. **Raw vs rendered diff** on representative URLs per template.
   - Raw: `curl -s -A "Googlebot" URL` or "View source".
   - Rendered: URL Inspection > View crawled page / Test live URL > HTML and screenshot; or crawler JS-rendering
     mode; or headless Chromium `page.content()`.
   Compare: title, canonical, H1, body word count, link count, structured data, images.
2. **Check what Google actually indexed**: URL Inspection (rendered HTML as indexed), and a quoted-phrase search
   `site:example.com "unique sentence from JS-loaded content"`.
3. **Find blockers**: JS/CSS/API endpoints disallowed in robots.txt; API calls requiring cookies/auth; content only
   after scroll/click/hover; timeouts (rendering is not guaranteed to wait for slow API calls); errors in the
   console of the Test live URL (JavaScript console messages panel); service worker dependencies; fragments
   (`#!`, `#/route`) instead of History API paths.
4. **Choose rendering strategy** per template:
   | Strategy | Use for | Note |
   |---|---|---|
   | SSG (build-time HTML) | docs, blog, marketing, stable catalogs | fastest, safest |
   | SSR (per-request HTML, hydrate) | dynamic public pages | watch TTFB and hydration cost |
   | ISR / stale-while-revalidate | large catalogs | set sensible revalidate |
   | CSR only | logged-in apps | not for pages that need to rank |
   | Dynamic rendering (bot-only prerender) | legacy stopgap | Google calls it a workaround; accept as debt, plan removal |
5. **Fix and re-test**: deploy SSR/SSG for ranked templates; verify via curl that raw HTML contains content,
   then URL Inspection live test; then monitor indexation for the template.

## Implementation rules
- **Links**: `<a href="/real/path">` with the History API. Not `<span onClick>`, not `href="#"`/`javascript:void(0)`.
- **URLs**: unique, clean path per view; no hash routing. Each route has its own title, meta description, canonical,
  and H1 updated on navigation and present in server output.
- **Lazy loading**: native `loading="lazy"` for below-the-fold images is fine (Googlebot handles it);
  never lazy-load the LCP image. For infinite scroll provide paginated URLs. Content loaded only on user
  interaction (click tabs/"show more") may not be indexed; keep important copy in the DOM on load.
- **Hydration**: ensure server output equals client first render (hydration mismatch removes/duplicates content).
- **Metadata** via framework head manager (Next.js `generateMetadata`, Nuxt `useHead`, Angular Meta service) on the server.
- **Structured data**: render JSON-LD server-side.
- **Performance**: JS bundle splitting and deferring; heavy bundles hurt INP and delay rendering. See `seo-core-web-vitals`.
- **Bot access**: do not block Googlebot behind a JS challenge, geo wall or consent wall that hides content;
  serve consent as an overlay over real content.
- **AI/other crawlers**: they mostly read raw HTML; SSR also protects visibility there.

## Common failure signatures
| Symptom | Likely cause |
|---|---|
| Indexed page shows empty body/"Loading..." | API failed or timed out during render; blocked endpoint |
| Only the homepage indexed | Router uses hash/JS-only links; sitemap missing |
| Wrong canonical or title in index | Head changed client-side only |
| Product price stale in SERP | Price injected late by JS |
| "Crawled - not indexed" at scale | Rendered content thin/duplicate, or soft 404s |

## Output
Template table: raw-HTML completeness (title/canonical/content/links/schema: yes/no), rendered result,
recommended strategy, effort, and a test script/curl assertions to put into CI.

## Do not
- Trust "Google renders JS so it is fine"; verify per template with the live test.
- Introduce user-agent-based cloaking that serves different content to bots than to users beyond equivalent prerender.
- Block `/static/` or `/api/` that rendering needs.
- Fix with meta tags added by client-side JS only.
