---
name: intercompany-tie-out
description: >-
  Reconcile intercompany balances and transactions between related entities: matching due-to and due-from, currency differences, timing items, netting and settlement, and elimination readiness. Use for "intercompany reconciliation", "due to due from do not match", "IC mismatch", "related party balances", "intercompany loan", or "prepare for consolidation".
metadata:
  department: "accounting"
  domain: "reconciliation"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Intercompany tie-out

Every intercompany receivable in one entity must have a mirror payable in the counterparty, in the same amount and currency after documented timing items. This skill ties out the books; consolidation and elimination entries themselves belong to the multi-entity reporting work.

## 1. Setup

- One intercompany account pair per counterparty (due from X, due to X), not one pooled account. Separate trading balances (recharges, goods) from financing balances (loans, interest) and from equity-like contributions.
- A written intercompany agreement or policy: what is charged, basis (cost plus, fixed fee, allocation key), currency, payment terms, who records first, cut-off day each month.
- Intercompany transactions raised as documents (invoice or journal with an agreed reference), not informal bank transfers.

## 2. Procedure each period

1. Extract each entity's intercompany account, by counterparty, as of the cut-off. Include currency and transaction-level detail.
2. Lay out a matrix: rows are entities, columns counterparties, receivable positive and payable negative. Matrix transpose should net to zero.
3. For each pair compute the difference and decompose:

| Cause | Handling |
|---|---|
| Timing: one side booked after cut-off, cash in transit | Accrue the missing side in the period with approval from the counterparty, or list as documented in-transit item |
| Different recording date or reference | Align to the agreed document date |
| Amount difference: tax, rounding, unagreed allocation | Agree with counterparty; correct the party in error |
| Currency: each side translates at a different rate | Compare in the transaction currency first; remaining difference is revaluation, booked per policy to FX |
| One side missing | Obtain the document; raise the booking |
| Disputed or unagreed charge | Hold in a dispute list with owner, do not eliminate |
| Misposted to a third-party account | Reclass |

4. Agree the corrected balances in writing with both entity owners (confirmation by email or system confirmation).
5. After correction the pair's difference must be zero in the transaction currency.
6. Record settlements: cash settlement reduces both sides on the same date; netting arrangements documented and approved.

## 3. Things to check

- Intercompany loans: principal, interest accrued both sides, withholding tax if any, arm's-length rate documented where required.
- Management fees and recharges: supportable allocation, tax treatment (VAT/GST, transfer pricing), recognised in the same period both sides.
- Profit in stock transferred between entities: flag for the consolidation preparer.
- Dormant balances: intercompany balances sitting for long periods suggest an unsettled or forgotten arrangement; escalate.
- Related-party disclosure: balances and transactions with owners, directors and affiliates are listed for disclosure.

Mismatch resolution order (timing, then FX, then missing booking, then pricing dispute), a transaction lifecycle standard, worked consolidation eliminations (balances, unrealised profit in inventory and fixed assets, loans, fees, dividends) and a settlement netting cycle are in `references/framework-and-eliminations.md`.

## 4. Approval

Entity controllers agree each pair. A balance disagreement at close is escalated to the group controller; manual elimination or write-off needs documented approval. Segregate: the person who books the entry in one entity does not also approve the counterparty confirmation alone.

## Output

Matrix of balances before and after, per-pair difference analysis with owner and action, agreed confirmation record, proposed adjusting entries (draft), and elimination-readiness statement (clean, or list of exceptions).

## Do not

- Eliminate or write off a difference you cannot explain.
- Pool all intercompany into a single account.
- Revalue one side only.
- Settle in cash without a matching document on both sides.

See also: `multi-entity-intercompany-consolidation` (overlapping topic; this skill covers its own scope, that one covers the other side).
