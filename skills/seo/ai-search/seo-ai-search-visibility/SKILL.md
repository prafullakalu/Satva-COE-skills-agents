---
name: seo-ai-search-visibility
description: >-
  Measure and improve how often and how accurately a brand is mentioned and cited by AI search and assistants (Google AI Overviews and AI Mode, ChatGPT search, Perplexity, Copilot, Gemini, Claude): prompt-set testing, citation analysis, content and entity changes, and crawler access. Use when asked for "GEO", "AEO", "AI SEO", "get cited by ChatGPT", "show up in AI Overviews", "AI visibility audit", "llms.txt", or "why does AI not mention us".
metadata:
  department: "seo"
  domain: "ai-search"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# AI search visibility (GEO / AEO)

AI answer engines retrieve web pages, extract passages and synthesise an answer, sometimes with citations. Visibility means two things: being **cited** (your URL is a source) and being **mentioned** (your brand appears in the answer text). The platforms differ, change often, and are not fully transparent; treat all claims as hypotheses and test.

## What is established
- Google states that its AI features in Search rely on the same ranking and quality systems, require no special markup, and that pages must be indexable and eligible for snippets. Strong organic SEO remains the base layer.
- Other engines retrieve through their own search backends (for example Bing-based or proprietary indexes) and their own crawlers. A page blocked to the relevant crawler cannot be cited.
- Brand mentions across third-party sources (reviews, comparison articles, forums, Wikipedia-type references, press) strongly shape what models say about a brand.
- `llms.txt` is a proposed convention, not a standard that major engines are confirmed to honour. Optional, low cost, no guaranteed effect.

## Workflow
1. **Define the prompt set (30-100 prompts).** Cover: category discovery ("best X for Y"), comparisons ("A vs B", "alternatives to A"), problem questions, how-to, brand queries, and pricing or integration questions. Include buyer personas and geographies. Freeze the list for repeatable measurement.
2. **Baseline.** For each prompt on each target engine, run it (logged out where possible, multiple runs because answers vary) and record: brand mentioned (yes/no, position, sentiment, accuracy), brand cited (URL), competitors mentioned, and top cited domains. Calculate mention rate and citation rate per engine, and share of voice against competitors. Note date, engine, mode and location.
3. **Diagnose sources.** List the domains and page types the engines cite for your prompts. If they cite third-party listicles, review sites and forums, those are your real targets, more than your own blog.
4. **Check access and eligibility.** robots.txt and CDN rules for search and user-agent crawlers of each engine (distinguish training crawlers from search/answer crawlers; blocking is a business decision, state tradeoffs); indexable, not noindexed; main content rendered in HTML, not only by client-side JavaScript; no heavy paywall or login on key pages; fast server response.
5. **Improve content for extraction.** Answer the question directly in the first sentences under each heading; use clear headings that mirror real questions; self-contained passages that make sense out of context; definitions, steps, comparison tables with explicit criteria; precise, verifiable facts with sources and dates; consistent naming of product, features and entities; pricing, integrations, limits and specs stated plainly; a visible update date. Do not write separate content for bots, and do not chunk unnaturally.
6. **Strengthen entity and third-party presence.** Consistent brand description across the site, Organization schema with sameAs links, profiles on relevant directories and review platforms (G2, Capterra, marketplace listings for your category), accurate Wikipedia or Wikidata entries only if notable, genuine participation in communities, digital PR for inclusion in comparison and "best of" pages (see `seo-link-building-digital-pr`).
7. **Fix misinformation.** If an engine states wrong facts, update the primary source pages first, correct third-party sources, and re-test. Keep an inaccuracy log.
8. **Track and iterate.** Re-run the frozen prompt set monthly. Segment by engine. Pair with referral traffic from AI engines in analytics (referrer and UTM patterns), branded search trend and demo or signup attribution (self-reported "how did you hear" often reveals AI).

## Output
Visibility baseline table (prompt cluster x engine: mention rate, citation rate, accuracy), competitor share of voice, top cited sources, prioritised actions (content, entity, third-party, technical), and a monthly tracking template.

## Do not
Promise citations or guarantee placement. Do not publish fake reviews or manipulate prompts, hidden text or injection attempts; these violate policies and can backfire. Do not cite statistics about "AI SEO lift" unless the source is named and recent. Do not abandon classic SEO.
