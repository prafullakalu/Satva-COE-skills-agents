---
name: seo-content-brief
description: >-
  Produce an SEO content brief a writer can execute without guessing: target query and intent, audience, outline with headings, entities and questions to cover, internal links, sources, E-E-A-T inputs and success metric. Use when asked to "write a content brief", "SEO brief for", "outline an article for this keyword", "brief a freelancer", or "what should this page cover to rank".
metadata:
  department: "seo"
  domain: "content"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# SEO content brief

A brief converts SERP evidence into writing instructions. It should remove ambiguity, not dictate prose. Aim for one to two pages.

## Workflow
1. **Confirm the target.** Primary keyword, 3-8 secondary keywords (from the same SERP cluster, see `seo-topic-clustering`), target URL (new or existing), market and language.
2. **Read the SERP** with `seo-search-intent-analysis`: intent, dominant format, SERP features, freshness expectations. Capture top 5-8 competing pages with their angle and what they miss.
3. **Define the reader and the job.** Who they are, what they know, what decision or task the page helps with, and the single next step we want them to take.
4. **Choose the angle.** One sentence stating why ours is better: original data, a worked example, a template, practitioner experience, a clearer decision framework. If there is no angle, do not commission the page.
5. **Build the outline.** H1 (primary keyword, human-readable), H2s ordered by reader need, with a one-line purpose each and the questions each must answer. Pull sub-questions from People Also Ask, Search Console, sales/support questions. Put the direct answer first for question-style queries (40-60 words), then depth.
6. **List coverage requirements:** entities, terms and concepts the page must mention naturally; definitions; data points needing a cited source; tables, checklists, calculators, screenshots or diagrams to include.
7. **Add experience inputs.** Name the subject-matter expert, the first-hand examples, numbers or client-safe stories to include. Writers cannot invent these; flag what must be supplied.
8. **Specify on-page elements:** title tag draft (<= 60 characters, keyword early), meta description (<= 155, includes a reason to click), URL slug, schema type if relevant, image needs with alt text intent.
9. **Internal links:** which pages to link to (with anchor guidance) and which pages should link to this one once published.
10. **Constraints:** tone, banned claims, compliance review needs, word range as a guide (length follows coverage, not the reverse), sources to prefer and avoid.
11. **Success metric:** the query set, target position range, and the conversion or engagement signal, with a review date (typically 8-12 weeks post-publish).

## Output template
```
Title (working): 
Primary keyword / secondary keywords:
Intent and format:
Audience and job to be done:
Angle / why we win:
Competitor gaps (3 bullets):
Outline:
  H1:
  H2 - purpose - questions to answer
  ...
Must include: data, examples, visuals, definitions
Experience inputs needed (owner, due date):
Title tag / meta / slug:
Internal links in / out:
Sources and compliance notes:
Success metric and review date:
```

## Quality checks before handing over
- Could a writer who knows nothing about the topic still produce a page that fits the intent?
- Does the outline answer each People Also Ask question that is genuinely relevant?
- Is there at least one element a competitor lacks?
- Does the page have a clear next step?

## Do not
Pad the brief with keyword counts or density targets. Do not copy competitor headings wholesale. Do not set a word count as a goal.
