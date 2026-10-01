---
name: marketing-web-copywriting
description: >-
  Write and rewrite B2B web copy: homepage, service and product pages, landing pages, and long-form sales pages, with a clear structure, specific claims and one CTA. Use when someone says "write the homepage", "landing page copy", "rewrite this page", "service page", "hero headline", "our copy is vague", or "make this convert". Not for emails (see email skills) or blog posts (see marketing-blog-production).
metadata:
  department: "marketing"
  domain: "content"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Web copywriting (B2B)

Good copy is clarity plus proof for one reader with one decision. Gather the inputs first; write second; edit hardest.

## Inputs (do not start without 1-4)
1. Page goal and single primary action (book a call, download, start trial).
2. Reader: persona, awareness level, what they just clicked from.
3. Positioning and proof (use `marketing-positioning-messaging` output if it exists).
4. Voice rules (use `marketing-brand-voice-guide` output if it exists).
5. Constraints: word count, compliance claims, existing URL and SEO target.
Missing proof? Write the copy with `[PROOF NEEDED: ...]` placeholders. Never invent statistics, customer names or quotes.

## Workflow

### 1. Choose the page pattern
- **Landing page (one action):** hero, problem, solution, how it works, proof, objections, CTA. No site nav competing.
- **Service/solution page:** hero, who it is for, outcomes, what is included, process, proof, FAQ, CTA.
- **Homepage:** what you do and for whom in 5 seconds, 3 paths by audience, proof strip, one CTA.
- **Long-form sales page:** problem story, agitation with real cost, mechanism, proof ladder, offer, risk reversal, FAQ, repeated CTA.

### 2. Write the hero first (most of the value)
- **Headline:** the outcome for the reader, concrete, <= 12 words. Formula options: outcome + timeframe ("Close the month in 5 days, not 15"); outcome without pain; "For [who]: [outcome]".
- **Subhead:** how, for whom, 1-2 lines. Must contain the category words a buyer would search.
- **CTA:** a verb plus the thing ("Book a 20-minute integration review"), never "Submit" or "Learn more". Add a friction reducer under it (no card, reply within a day).
- Draft 5 headline variants in different angles (outcome, pain, proof, contrast, specificity) and recommend one with a reason.

### 3. Body rules
- One idea per section; heading states the claim, body proves it.
- **Specific over superlative:** "Orders from Shopify, Amazon and eBay post to QuickBooks every 15 minutes" beats "seamless integration".
- **Feature -> benefit -> proof** triplets; benefits are what changes in the reader's week.
- Use the reader's words from transcripts and reviews; cut internal jargon and acronyms the reader does not use.
- Short sentences, active verbs, you-focus: count "you" against "we"; aim for you >= we.
- Proof near every claim: number, named (permissioned) customer, logo, certification, process screenshot. Place the strongest proof near the CTA.
- Handle objections explicitly (price, risk, switching effort, security, "we already have someone") in FAQ or inline.
- Skimmable: descriptive subheads, bullets for parallel items only, no walls of text.

### 4. CTA architecture
One primary CTA repeated at hero, mid-page and end; one low-commitment secondary (resource) for not-ready visitors. Align button, microcopy and the next page (what happens after click, how long it takes).

### 5. Edit pass (checklist)
- Every sentence passes "so what?" and "says who?"
- Remove: "leading", "robust", "cutting-edge", "world-class", "solutions" as a noun, "synergy", "unlock", "leverage".
- No claims you cannot document. Regulated claims (tax, compliance, financial outcomes) need review by the owner.
- Read headline-only: do the headings alone tell the story?
- Read aloud for rhythm; one thought per breath.
- Meta title (<= 60 chars) and description (<= 155) written for the click, with primary keyword.

## Output
Page copy in sections with labels (HERO, PROBLEM, ...), alt headline variants, meta tags, proof placeholders list, and 3 notes on what to A/B test first (headline, CTA wording, proof placement). Offer a hand-off to a conversion-review skill if available.

## Failure modes
- Writing about the company instead of the reader's problem.
- Multiple competing CTAs.
- Copy that fits any competitor if the logo is swapped.
- Fake urgency, fake scarcity, fake testimonials. Never.
- Hiding price/process vagueness behind "contact us" when buyers need orientation; at least give a range or what drives cost.
