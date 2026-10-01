---
name: automated-reconciliation
description: >-
  Match two large financial data sources (bank statement against ledger, payments against invoices, processor payouts against deposits) with a staged engine: data cleaning and vendor-name normalisation, exact matching on ids, tolerance matching, fuzzy description matching, and subset-sum matching for batched settlements, with confidence scores, an exceptions list and suggested entries for unrecorded fees and interest. Use for "reconcile thousands of transactions", "match payments to invoices", "bank rec at scale", "fuzzy matching in finance", "one deposit covers several invoices", "AWS versus Amazon Web Services in the ledger". Pair with bank-reconciliation for the statement, balance proof and sign-off.
metadata:
  department: "accounting"
  domain: "reconciliation"
  owner: "satva-coe"
  status: "beta"
  license: "MIT"
  source: "https://github.com/GAJETOso/financeskills/tree/main/skills/automated-reconciliation"
---
<!-- Adapted from GAJETOso/financeskills skills/automated-reconciliation (MIT, Copyright (c) 2026 KOMVIA). Modified by Satva: persona framing removed, evals and example fixtures left out, limits, money-precision and approval rules added; script renamed matching_engine.py. -->

# Automated reconciliation

Eliminate manual matching of high-volume data by running deterministic passes first and probabilistic matching second, then spending human attention only on the exceptions. This skill is the matching engine; the reconciliation statement, balance proof and sign-off belong to `bank-reconciliation` (cash) or `subledger-to-gl-reconciliation` (control accounts).

## Initial assessment
1. Data sources: source A (for example bank statement CSV or OFX) and source B (ledger or ERP export). What is the period, the currency, and the opening balance agreed on both sides?
2. What common identifiers exist (reference numbers, cheque numbers, invoice numbers, batch ids)?
3. What counts as a match: exact (same id, amount and date) or fuzzy (similar name, same amount, within a few days)? What tolerance is acceptable and who approved it?

## Limits of the model
Language models are poor at matching tens of thousands of rows. For large sets run the engine (or a dataframe and string-similarity library) and use the model only to resolve ambiguous cases, typically the last few percent. Never claim a match rate that was not computed by code.

## Priority order
1. **Clean**: standardise dates, signs, currency and descriptions; normalise vendor names ("AWS" and "Amazon Web Svcs" are one counterparty) through an alias table that persists confirmed matches.
2. **Deterministic**: exact match on id, amount and date. Lock matched items after each pass so they cannot be reused.
3. **Tolerance**: amount within a stated tolerance (for example plus or minus 0.5 percent, or a fixed amount for bank fees), date within 3 business days, reference agreeing.
4. **Fuzzy**: amount within tolerance plus string similarity on description or reference at or above a threshold (see `references/fuzzy-logic.md`).
5. **One-to-many and many-to-many**: subset-sum, such as one deposit covering several invoices; cap the combination size at 5 to hold false positives down.
6. **Exceptions**: whatever remains, with a reason and a suggested action.

## Engine
`scripts/matching_engine.py` provides `exact_match`, `tolerance_match` and `one_to_many_match` over a small `Txn` dataclass; running it self-tests. Standard library only. Two cautions before using it on real money:
- It uses floats and a first-found combination search. For ledgers, convert to integer minor units or `Decimal` first, and treat a subset-sum result as a candidate to confirm, because several combinations can sum to the same target.
- It does not look at dates or currencies. Filter by currency and window before calling it, and never match across currencies without conversion at the transaction-date rate.

## Steps
1. Normalise vendor names and descriptions; build or load the alias table.
2. Run the passes in order, logging the tier and score on every pairing (an auditor will ask).
3. Many-to-one: find cases where one bank deposit represents several ledger invoices (or the reverse) and record the group.
4. Compute the match rate and reconciled value from code output.
5. Detect bank fees and interest present on the statement but missing from the ledger and draft the entries.
6. Sample 25 auto-matches per month; more than 2 errors means raise the thresholds.

## Guardrails
- Auto-clear only below the materiality threshold; any fuzzy match at or above it goes to a person.
- Never delete or alter a ledger entry from this step; propose corrections for approval.
- Never plug a difference. An unmatched residual is listed, with an owner.
- Reconciliation controls (separate preparer and reviewer, aged and owned reconciling items, source independence) are in `references/rec-controls.md`.

## Output
**Results**: match rate by tier (for example 94 percent matched automatically), total reconciled value, tolerance and thresholds used.
**Exceptions**: unmatched items from both sides, and ambiguous matches with confidence scores awaiting sign-off.
**Suggested entries**: ready-to-copy journal entries for bank fees or interest missing from the ledger, marked draft.
**Statement**: `assets/reconciliation-statement-template.md` for the cash proof with outstanding-item detail.

## Related
`bank-reconciliation`, `credit-card-reconciliation`, `intercompany-tie-out`, `month-end-close`, `internal-controls-matrix`.
