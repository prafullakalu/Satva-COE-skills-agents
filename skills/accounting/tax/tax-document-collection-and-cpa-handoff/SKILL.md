---
name: tax-document-collection-and-cpa-handoff
description: >-
  Guide a US taxpayer through organising tax documents for a CPA: situation interview, account-to-document mapping, document collection with confirmed extraction, reconciliation of gaps (K-1s, estimated payments, rentals, investments), and a structured accountant package with cover letter, checklist, open questions and a directional estimate. Covers W-2, 1099s, 1098, K-1, Schedule E, and NJ/NY/CA/CT state items. Use for 'organize my taxes', 'CPA handoff', 'tax package', 'what documents am I missing', 'tax document checklist'. Not tax advice.
metadata:
  department: "accounting"
  domain: "tax"
  owner: "satva-coe"
  status: "beta"
  license: "MIT"
  source: "https://github.com/ajaysurie/tax-prep"
---
<!-- Adapted from ajaysurie/tax-prep (MIT, Copyright (c) 2026 Ajay Surie). Modified by Satva: rewritten SKILL.md source-agnostic (no update-check network call, no MCP detection, no fixed home-directory state, no TurboTax export); references kept except schemas, TurboTax mapping, prior-return import and tax-data-sources. -->

> **Tax year.** Upstream reference tables target US tax year 2025 (federal plus NJ, NY, CA, CT state guides). Rates, limits and state rules change yearly: verify against current IRS and state sources before quoting. Organises documents and data; never gives tax advice and never files.

# Tax document collection and accountant handoff

Walk a US taxpayer (individual, landlord, K-1 holder, self-employed owner) from "I don't know what I need" to a structured package their CPA can work from. Works across weeks as documents arrive, or in one sitting.

Boundary: organise, reconcile and flag; never give tax advice, never file. Open questions go to the CPA, not into a guess.

## Working state (keep it simple)

Keep a small working folder per tax year containing: a profile note (filing status, states, income sources, life changes), an accounts list (every institution or entity and the documents it should send), a document log (expected vs received, with status pending / received / not applicable), a session-notes log (corrections, CPA notes, decisions), and the package output. Any spreadsheet or markdown files will do. Treat the folder as sensitive financial data: do not commit it to version control or share it by chat. Resume work by reading the profile, the document log and the session notes, then report: "Profile complete. 9 of 12 documents received. Waiting on: K-1 (Fund A), 1099-B (Broker B)."

## The five phases (a guide, not a gate)

Any action can happen at any time: a document uploaded mid-interview is processed immediately; a new account is added whenever it surfaces; asked for the package early, produce it with gaps flagged.

### 1. Situation interview
Goal: a complete profile for the year. If a prior-year return exists, start from it (filing status, income sources, deductions, rentals, K-1 entities, state filings), present what you extracted for confirmation, and ask only what changed. Ask **one question at a time**, each informed by the previous answer, and say briefly why it matters. Question bank and order: `references/situation-questions.md` (filing status, dependents, employment, self-employment, rentals, investments, K-1s, bank interest, healthcare/HSA, life changes, estimated payments, charitable, education, state items). Never dump a form.

### 2. Account discovery
Map every account to the documents it should produce, using `references/document-matrix.md`. Cross-check against the profile: every employer produces a W-2; every rental a mortgage statement (1098) and property-tax record; every brokerage a 1099-B and perhaps 1099-DIV; every K-1 source a K-1; every bank may produce a 1099-INT above the reporting threshold; an HSA a 1099-SA and 5498-SA. Flag gaps specifically ("a rental at 123 Main Street but no insurance expense recorded"). Report "Expecting N documents from M accounts."

### 3. Document collection
Accept PDFs, images or manual entry and extract the key fields per form type (W-2 boxes 1, 2, 17; 1099-INT box 1 and 4; 1099-DIV 1a, 1b, 2a, 7; 1099-B proceeds, basis, wash sales, term; 1098 boxes 1 and 6; 1099-NEC box 1; K-1 per `references/k1-guide.md`). **Always show extracted values to the user for confirmation before recording them.** For a multi-form PDF, list the forms found and their pages first, then process each separately. Match each document to an expected item and update its status; for an unexpected document, ask whether to add the account. Prompt for rental expenses by property type (`references/schedule-e-guide.md`). K-1s arrive late: say so. Track estimated payments as first-class items, per quarter, federal and each state.

### 4. Reconciliation
Compare received vs expected and classify the missing: delayed (K-1s), possibly forgotten, not applicable. Where transaction data exists, compare 1099 amounts with actual interest, dividends and gains and flag differences over about $50. Compare year over year and flag swings over about 20% for confirmation. Use `references/common-gaps.md` to ask about commonly missed items by profile (estimated payments and safe harbour, child care, charitable, HSA, student-loan interest, home office, vehicle) and the state guides in `references/state-guides/` for state-specific items. Validate each rental has rent, mortgage interest, property tax, insurance, repairs and depreciation; flag wash sales, missing basis and capital-loss carryforwards.

### 5. Accountant package
Produce one structured document with a short cover letter (filing status, states, two or three notable items, count of open questions, document completeness) and the 11 sections in `references/cpa-handoff-format.md` (summary, document checklist, W-2s, investment income, rentals, business income, K-1s, deductions and credits, state items, year-over-year, open questions). Optionally the same sections as CSV or spreadsheet tabs. Include a rough directional estimate using `references/estimate-template.md` with its disclaimer; where a line has no source document show "TBD: [document] not yet received", never $0. Fold unresolved CPA notes into Open Questions.

## Behaviour rules
- One question at a time; explain why it matters.
- Be specific about gaps, not "you might be missing something".
- Report progress after every document or phase.
- Never give tax advice; organise and defer.
- Log corrections and decisions to the session notes and read them on resume ("Last time you corrected the Q4 estimated payment to $4,000").
- Protect personal data; never reproduce full SSNs or account numbers in the package.

## Done when
Profile captured; all accounts mapped to expected documents; all available documents collected and user-confirmed; reconciliation shows no unresolved gap; package generated; the user knows exactly what to hand the CPA.

## Reference files
`situation-questions.md`, `document-matrix.md`, `common-gaps.md`, `k1-guide.md`, `schedule-e-guide.md`, `s-corp-home-office.md`, `estimate-template.md`, `cpa-handoff-format.md`, `state-guides/NJ.md`, `NY.md`, `CA.md`, `CT.md`. The upstream's TurboTax import mapping, JSON schemas and state-file bootstrap scripts were left out (vendor-specific or tied to local state files).
