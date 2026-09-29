# Confidence model — Linnworks → QuickBooks mapping

Four tiers. Never assign confidence arbitrarily — every tier is defined by the evidence that
produced it, and the mapping engine records which evidence fired.

| Tier | Evidence required (all must hold) |
|---|---|
| `HIGH` | An explicit existing mapping rule fires, OR an exact identifier/canonical-concept match against a QBO target whose account/item type is compatible with the source's accounting concept, AND there is no competing target of equal or greater specificity. |
| `MEDIUM` | A strong semantic/keyword match (e.g. channel name appears in the QBO account name) AND the QBO target's type is compatible with the accounting concept AND there is no explicit rule overriding it. |
| `LOW` | Only a weak similarity signal (e.g. shared account-type category with no name/keyword overlap) or accounting evidence is thin. |
| `UNRESOLVED` | Multiple plausible targets tie with no tie-breaker, OR the Linnworks source lacks the information needed to infer accounting treatment safely, OR no candidate target exists at all. |

## Ordered matching pipeline (spec §6)

The mapping engine tries these in order and stops at the first that produces a candidate;
later steps never override an earlier one's result, they only run when the earlier ones are silent:

1. **Explicit rule** — a rule in `mapping_rules.json` (human/accountant-authored) naming this exact
   source. Always `HIGH`, `review_required=false` (already reviewed once when the rule was authored).
2. **Exact identifier/code match** — source carries a code that exactly equals a QBO account/item
   number or a canonical GAAP-style slug. `HIGH`.
3. **Strong semantic/accounting-concept match** — the derived `AccountingConcept` (see
   `normalization-schema.md`) has a canonical name (e.g. "shipping income") that appears, whole-word,
   in a QBO Income/Expense account name, AND the QBO account's `AccountType` is compatible with the
   concept (Income concept → Income-type account, never Expense-type). `HIGH` if unique, `MEDIUM` if
   there are 2+ type-compatible candidates but one is clearly more specific (e.g. contains the channel
   name too).
4. **Account-type compatibility only** — same `AccountType` as required by the concept, no name overlap.
   This is **never enough on its own to confirm a mapping** (never guess): with 2+ such candidates the
   result is `AMBIGUOUS`/`LOW`; with exactly 0 or 1 candidate and no other evidence the result is
   `UNMAPPED`/`UNRESOLVED` — a single type-compatible account is not evidence it's the *right* one.
5. **Name/keyword similarity** — fuzzy token overlap between source name (channel, SKU category,
   payment method) and QBO account/item name, below the threshold needed for step 3. `LOW`.
6. **Ecommerce-specific rule** — a hardcoded domain rule (e.g. "SubSource containing 'Amazon' →
   Income account matching 'Amazon'") from `reference/ecommerce-rules.md`-equivalent embedded in
   `mapping_engine.py`. Confidence per the rule's own strength, capped at `MEDIUM` unless it reduces
   to step 2/3.
7. **Historical mapping evidence** — if a `mapping_rules.json` entry exists for a *similar* prior
   source (not this exact one), surface it as a suggestion at `LOW`, never auto-apply.
8. **LLM semantic reasoning** — last resort. The LLM proposes a target with a stated reason. This is
   **always** `review_required=true` and confidence is capped at `MEDIUM`, regardless of how confident
   the LLM's own language is. An LLM guess never becomes a `HIGH`/confirmed mapping automatically —
   spec §6 is explicit on this.

If nothing fires by step 8 (or the LLM step is skipped because the source lacks the required
accounting information), the result is `UNRESOLVED` and the record is classified per
`gap-taxonomy.md` (`UNMAPPED`, `AMBIGUOUS`, or `STRUCTURAL_DATA_GAP` depending on *why* it failed).

## Product/SKU identity pipeline (mapping_engine.match_product_identity)

Separate, simpler ordered pipeline for "does this Linnworks product exist in QBO", per user
requirement: **SKU first, then name, then price/qty**. Price/qty is corroboration only — it never
promotes a match on its own, since two unrelated products can coincidentally share a price.

1. **SKU exact match** (case-insensitive) — unique hit: `MAPPED`/`HIGH`. Two+ QBO items sharing the
   same SKU: `AMBIGUOUS`/`LOW` (a QBO data-quality issue, flagged as such).
2. **Name token overlap**, unique top candidate, **no** price corroboration: `UNVERIFIED`/`LOW` —
   a real candidate, but not confirmed. **With** price corroboration (within
   `PRICE_TOLERANCE_PCT`, default 5%): `MAPPED`/`MEDIUM`.
3. **Name overlap tied between 2+ candidates**: price corroboration breaks the tie if exactly one
   tied candidate's price matches (`MAPPED`/`MEDIUM`); otherwise `AMBIGUOUS`/`LOW`.
4. **No SKU match and no name overlap at all**: `UNMAPPED`/`UNRESOLVED`.

`HIGH` confidence is reserved for SKU exact matches only — name+price corroboration caps at
`MEDIUM` because two signals of moderate strength are still weaker than one near-unique identifier.

## `review_required`

`review_required = true` whenever confidence is `MEDIUM`, `LOW`, or `UNRESOLVED`, or whenever an
`AMBIGUOUS`/`INVALID`/`ORPHANED`/`INACTIVE` status is assigned — regardless of confidence. Only
`HIGH`-confidence `MAPPED` results from an explicit rule or exact/unique semantic match skip review.
