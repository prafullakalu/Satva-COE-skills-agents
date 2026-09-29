# Gap taxonomy — Linnworks → QuickBooks mapping

Every Linnworks source item and every QBO target object ends up in exactly one bucket.
Never call something "unmapped" when the underlying data required to map it doesn't exist
in Linnworks at all — that is a STRUCTURAL_DATA_GAP, a different and more serious problem.

| Status | Meaning | Example |
|---|---|---|
| `MAPPED` | A Linnworks source has a valid, confirmed QBO destination (explicit rule or HIGH-confidence match against an active, type-compatible target). | Channel `AMAZON` → QBO Income account "Amazon Sales" (active, type=Income). |
| `UNMAPPED` | The Linnworks source exists and carries enough information to be mapped, but no QBO destination could be found at all. | Channel `TIKTOK` has orders; no QBO account name/keyword corresponds. |
| `AMBIGUOUS` | Two or more QBO targets are plausible and nothing (explicit rule, exact code, type constraint) breaks the tie. | Sub-source "coinsofamerica" (eBay) could map to "Sales" or "Sales of Product Income" — both Income type, neither channel-specific. |
| `INVALID` | A mapping exists (explicit rule or prior config) but the target is structurally wrong for the source. | A refund source mapped to an Expense-type account instead of a contra-Income/Income account. |
| `ORPHANED` | A QBO account/item/class has no corresponding Linnworks source at all. | QBO income account "Commission Income" with no Linnworks channel or fee dimension that would ever post to it. |
| `INACTIVE` | A mapping (explicit or matched) points at a QBO target that is not active/usable. | Target account `Active: false` in QBO chart of accounts. |
| `UNVERIFIED` | Exactly one plausible candidate target exists, but the evidence supporting it is too weak to confirm without human review — distinct from `AMBIGUOUS` (2+ tied candidates) and `UNMAPPED` (no candidate at all). Used by the product/SKU-identity pipeline: a name-only match with no SKU or price corroboration. | Linnworks SKU "0051" ("Two Cent Coin") has no QBO item with a matching SKU; a QBO item named "Two Cent Coin Set" overlaps by name but its price doesn't corroborate — reported `UNVERIFIED`, not `MAPPED`. |
| `STRUCTURAL_DATA_GAP` | The Linnworks side does not carry the information needed for correct accounting treatment — no amount of matching logic fixes this; it's a missing source field/entity, not a missing mapping. | Marketplace/payment-processor fees and settlement adjustments are not present in Linnworks order data — they live in the marketplace/PSP settlement feed, not Linnworks. |

## Two distinct matching pipelines

This skill runs **two separate matching problems**, both feeding the same taxonomy above:

1. **Accounting-concept mapping** (`mapping_engine.propose_mapping`) — Linnworks *dimensions*
   (channel, refund, tax, shipping) → QBO *accounts* (Income/Expense/COGS/Liability). Answers
   "which account does this revenue/cost stream post to?"
2. **Product/SKU identity mapping** (`mapping_engine.match_product_identity`) — Linnworks
   *products* → QBO *items*. Answers "does this specific product exist, correctly, in QBO?" Matched
   in priority order: **SKU first** (near-zero false positives), **then product name**, **then
   price/qty as corroboration only** — price/qty alone never confirms a match; it only corroborates
   or breaks a tie on a name match that already exists. See `confidence-model.md` for the full
   ordered pipeline.

## Source-availability grading (per spec §5)

For every accounting concept in scope (sales, refunds, returns, discounts, shipping income/expense,
tax, marketplace fees, processing fees, settlements, chargebacks, COGS, inventory, inventory
adjustments, purchase orders, supplier costs, currency conversion/FX, warehouse/location, channel,
payment method), grade Linnworks source availability as one of:

- `SOURCE_AVAILABLE` — the field/entity exists and is populated for the sampled period.
- `SOURCE_PARTIALLY_AVAILABLE` — present but incomplete (e.g. populated for some channels/orders, not others).
- `SOURCE_NOT_AVAILABLE` — no Linnworks table/field carries this at all.
- `SOURCE_AVAILABLE_BUT_INSUFFICIENT` — the field exists but doesn't carry enough precision/detail for
  correct accounting treatment (e.g. a lump `fTotalCharge` without a tax/shipping/discount breakdown
  would be this; Linnworks' `Order` table actually does break these out, so this grade is for cases
  like per-fee-type marketplace charges being absent even though a lump deduction shows up elsewhere).

This grading is a factual statement about what a live `describeTable`/tool call returned, never a guess.

## Rule: never silently degrade a status

Once a status is assigned, the report must carry the evidence that produced it (spec §6 "Evidence").
`AMBIGUOUS` and `UNRESOLVED` findings always route to the "Unresolved Items" report section for
human/accountant review — the mapping engine never auto-picks a winner to make the coverage number
look better.
