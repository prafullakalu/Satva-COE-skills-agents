---
name: seo-ga4-reporting
description: >-
  Measure and diagnose organic search performance in Google Analytics 4: channel grouping, landing page reports,
  key events/conversions, Search Console integration, attribution, and data-quality checks. Use for "GA4 organic
  traffic report", "organic conversions", "GA4 vs Search Console mismatch", "set up GA4 for SEO", "organic landing
  pages", "direct traffic jumped", "GA4 BigQuery" or "SEO KPI dashboard".
metadata:
  department: "seo"
  domain: "analytics"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# GA4 reporting for SEO

GA4 tells you what organic visitors do after the click; Search Console tells you what happens before it. They will
never match exactly (clicks vs sessions). Report them side by side, never merge them as one number.

## Setup checklist (verify before reporting)
1. **Property/stream**: one web data stream, enhanced measurement on, internal traffic and developer traffic
   filtered (Admin > Data filters; set to Active after testing), unwanted referrals excluded (payment gateways, own
   domains, e.g. cross-domain list).
2. **Key events** (formerly conversions): mark only business outcomes (`generate_lead`, `purchase`,
   `form_submit`, `phone_click`); ecommerce events with `value` and `currency`. Verify with DebugView.
3. **Search Console link** (Admin > Product links) to get the Search Console reports (queries and landing pages
   with GSC metrics) inside GA4.
4. **BigQuery link** for raw export when sampling/thresholds or custom joins matter (daily export is free; streaming costs).
5. **Data retention**: set event data retention to 14 months (default 2 months limits Explorations).
6. **Consent**: with Consent Mode, unconsented traffic is modelled or missing; note this in reports. Different CMPs
   shift organic vs direct counts.
7. **UTM discipline**: never tag organic links; keep paid/email tagging consistent. Untagged campaigns land in
   Direct or Organic.

## Reports to build
- **Acquisition > Traffic acquisition**: filter `Session default channel group = Organic Search`; metrics: sessions,
  engaged sessions, engagement rate, key events, revenue. Use "Session source / medium" for engines (google /
  organic, bing / organic).
- **Landing pages** (Reports > Engagement > Landing page, or Exploration): dimension `Landing page + query string`,
  secondary dimension `Session default channel group`; rank by sessions and key events. Landing page is the
  SEO unit of analysis.
- **Exploration (free form)**: rows = landing page group (use content grouping or regex by directory), columns =
  month, values = organic sessions, engagement rate, key event rate, revenue; compare with the prior year.
- **Search Console reports** (if linked): Queries, Google organic search traffic by landing page.
- **Assisted/organic role**: Advertising > Attribution > Conversion paths; model comparison. Organic is often an
  assisting channel; last-click undercounts it.
- **Looker Studio**: blend GA4 (by landing page) and GSC (by page) on normalised URL path for the exec dashboard.

## Definitions that matter
- Session default channel group is **Organic Search** when source is a known search engine and medium is
  `organic`. AI assistants may appear as referrals (e.g. chatgpt.com / referral) unless you build a custom
  channel group; create one for AI referrals if relevant.
- **Engaged session**: >=10 s, or >=1 key event, or >=2 page/screen views. Engagement rate = engaged sessions /
  sessions. Bounce rate = 1 - engagement rate; not comparable to Universal Analytics.
- **Data thresholds / sampling**: Google Signals and small cohorts can hide rows; explorations may sample above
  the quota (10M events for standard properties); BigQuery avoids this.
- Attribution: default reporting attribution model is data-driven (last click for organic channel in some
  reports); the model in use is shown at Admin > Attribution settings.

## GA4 vs Search Console mismatch diagnostic
Expect GSC clicks > GA4 organic sessions by 5-30%. Larger gaps imply: blocked tag (consent, ad blockers), slow tag
load, redirects dropping the referrer, landing page without the tag (checkout/subdomain/PDF), bot clicks, or
traffic categorised as Direct. Check: tag coverage crawl, Direct landing-page spikes on deep URLs, Tag Assistant,
consent rates, referrer policy.

## Diagnosing organic changes
1. Check whether the drop appears in GSC clicks too (real) or only in GA4 (tracking/consent/tagging).
2. Check Direct/(not set) for the opposite spike (misclassified organic).
3. Segment by landing page group, device, country; compare to the same weekdays.
4. Check key-event definitions changed (a conversion change looks like a traffic problem).

## Output
KPI table (organic sessions, engagement rate, key events, revenue, YoY), landing-page winners/losers, data-quality
caveats, and recommended actions. State the date range, attribution model, and filters used.

## Do not
- Present GA4 organic sessions as "clicks" or compare them 1:1 to GSC.
- Mark every interaction as a key event.
- Report from a property with internal traffic unfiltered or the tag missing on some templates.
- Use UA-era benchmarks (bounce rate, session definition) for GA4 numbers.
