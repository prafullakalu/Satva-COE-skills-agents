---
name: marketing-positioning-messaging
description: >-
  Build a B2B positioning statement and messaging framework: category, alternatives, unique attributes, value, best-fit customer, proof, message hierarchy and pillars. Use when someone says "write our positioning", "messaging framework", "value proposition", "why do we win", "our homepage says nothing", "how do we describe what we do", or before any copy, deck or campaign is written for a product or service line.
metadata:
  department: "marketing"
  domain: "strategy"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Positioning and messaging framework

Positioning is a decision about how a buyer should file you in their head. Messaging is the language that carries that decision. Do positioning first; copy written without it is decoration.

## Inputs to collect (ask, do not invent)
- What it is, in plain words, and who pays for it.
- 3-5 real customers (anonymised is fine) and why they bought, in their words. Won/lost notes, call transcripts, reviews.
- What the buyer does today instead (spreadsheets, an in-house hire, a competitor, nothing).
- Proof that exists: metrics, case studies, certifications, integrations, years of practice.
If proof or customer language is missing, say so and mark the output `[Unvalidated]`. Do not fabricate numbers or logos.

## Workflow

### 1. Name the competitive alternatives
List what a best-fit buyer would use if you did not exist. Include "do nothing" and "hire in-house". Positioning is relative to these, not to your feature list.

### 2. Extract unique attributes
For each alternative, list what you have that they lack (capability, method, integration depth, team, speed, price model). Keep only attributes that are true, provable and that some buyers care about. Cut generic ones ("quality", "support", "innovative").

### 3. Translate attributes into value
Chain each attribute: **attribute -> what it enables -> outcome the buyer cares about**. Example: "pre-built Shopify-to-QuickBooks sync -> orders post to the ledger without re-keying -> month-end close in days, not weeks". Quantify only with sourced numbers.

### 4. Pick the best-fit customer
Who cares most about that value and buys fastest? Describe by situation and trigger (e.g. "multichannel seller outgrowing manual journal entries"), not just industry. Route detailed work to `marketing-icp-personas`.

### 5. Choose the market category frame
Decide the frame of reference that makes the value obvious: an existing category (easiest), a sub-category ("accounting automation for multichannel retailers") or a new one (expensive; only with budget and proof). Test: would a buyer search for this phrase?

### 6. Write the positioning statement (internal, never published as is)
```
For [best-fit customer in their situation]
who [problem or trigger],
[Product/Service] is a [category frame]
that [primary value / outcome].
Unlike [main alternative], we [key differentiator + proof].
```
One sentence per slot. If a slot needs "and" twice, you have two positionings; pick one.

### 7. Build the message hierarchy
| Layer | Content | Length |
|---|---|---|
| Headline claim | The single outcome, in buyer words | <= 12 words |
| Elevator pitch | Problem, solution, proof | 2-3 sentences |
| Pillars | 3 supporting claims (never more than 4) | each: claim + proof + example |
| Proof bank | Metrics, quotes, case studies mapped to each pillar | list |
| Objection answers | Top 5 objections with honest answers | 1-2 sentences each |

### 8. Stress-test (all must pass)
- **Falsifiable:** could a competitor credibly say the same? If yes, rewrite.
- **Buyer language:** does a phrase come from customer transcripts rather than internal jargon?
- **Provable:** every claim maps to a proof item; otherwise tag `[Needs proof]`.
- **Narrow enough:** does it exclude someone? Positioning for everyone persuades no one.
- **Consistent:** headline, pitch and pillars say the same thing at three zoom levels.

## Output format
A single markdown doc: Alternatives table, Attribute->value chains, Positioning statement, Message hierarchy table, Proof bank with gaps flagged, Open questions. Add a "Where to use" list (site hero, deck slide 2, LinkedIn banner, sales opener) with a one-line adaptation for each.

## Failure modes
- Listing features and calling it positioning.
- Positioning against a straw man competitor or against nobody.
- Three pillars that are really one pillar restated.
- Claims like "best-in-class", "end-to-end", "seamless": replace with the observable fact.
- Rewriting the statement to please internal stakeholders instead of testing it on five buyers; recommend a 5-call validation before a rebrand-scale rollout.
