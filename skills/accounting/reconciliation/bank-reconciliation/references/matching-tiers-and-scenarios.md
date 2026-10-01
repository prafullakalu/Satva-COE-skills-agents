<!-- Adapted from Receiptor-AI/bookkeeping-skills skills/bank-reconciliation (MIT, Copyright (c) 2026 Receiptor AI). Modified by Satva: jurisdiction-specific tax line references removed, reorganised, added approval boundaries. -->
# Matching tiers, normalisation and catch-up scenarios

Supplements the matching hierarchy in `SKILL.md`. Use when working a large statement or deciding what may be auto-matched.

## Normalise both sides first

| Field | Format | Note |
|---|---|---|
| date | YYYY-MM-DD | Transaction date, not posting date, when they differ (cards: swipe date, not statement date) |
| description | cleaned string | Collapse whitespace, standardise merchants; keep a lookup of cryptic bank strings ("POS DEBIT 4829 AMZN MKTP US" is Amazon) |
| amount | signed decimal | Negative = money out, positive = money in |
| reference | string | Cheque number, transaction id or confirmation number when present |

Dates commonly differ by 1 to 3 days between books and bank. Amounts can differ by pennies through rounding, conversion or bank fees; set a tolerance (for example 0.02 domestic, 1.00 for foreign-currency) and record it.

## Tiers, in decreasing confidence

| Tier | Rule | Handling |
|---|---|---|
| 1 Exact | Same amount and same date; also same reference when both sides have one | Auto-match |
| 2 Near | Same amount, date within 2 business days (weekends, holidays, posting delay) | Auto-match with a brief glance |
| 3 Fuzzy | Same amount within 5 days, or same vendor pattern, amount within 2 percent, within 5 days | Present for confirmation |
| 4 Batch | Several book entries sum exactly (within tolerance) to one bank line, or one book entry equals several bank lines; dates within 3 days | Present for confirmation |
| 5 Suggested | Similar vendor and amount within 10 percent, dates do not align | Flag only, never auto-match |

Safe to auto-match: tiers 1 and 2, or an explicit shared reference number. Review required: date drift beyond 2 business days, batch matches, near-equal amounts that depend on fee, FX or rounding assumptions, possible duplicates or sign reversals.

Never auto-resolve without approval: deleting a book entry; reclassifying owner draws, payroll, loan or tax payments; forcing a match just to make the balance agree; changing entries in a closed period.

## Finding a stubborn difference

- Pennies (0.01 to 0.05): rounding; find the item recorded a penny off.
- Difference divisible by 9: transposed digits (46 recorded for 64 gives 18).
- Difference equals one transaction: that transaction was omitted.
- Difference equals twice a transaction: a double entry or a sign error (debit booked as credit).
- Same difference every month: a systematic recording error, not noise.

## Scenarios

**Catching up on months of unreconciled books.** Start with the oldest unreconciled month and work forward; each month's outstanding items carry into the next. Never reconcile six months at once, and never skip a month (errors cascade).

**Several accounts and cards.** Reconcile each account separately. A transfer between your own accounts is a withdrawal on one statement and a deposit on the other, never income or expense. The monthly card payment from the bank account is a liability payment; the individual card charges are the expenses.

**Credit-card statements.** Same process, but the reconciled balance is a liability. Interest is interest expense; rewards or cash-back reduce expense or are other income according to the accountant's policy. See `credit-card-reconciliation`.

**Foreign currency.** Match in the transaction currency. Bank and books may convert at different rates; the difference is a separate exchange gain or loss line, not a correction to the original item. Use the transaction-date rate.

**Petty cash.** Count the cash, add receipts since the last replenishment, and compare with the fund amount; investigate any shortfall.

## Extra red flags

Same vendor with round amounts and no receipts; cheques out of sequence (voided, lost or stolen); frequent insufficient-funds charges (a cash-flow problem to alert the owner to); unrecognised payees; consistent small discrepancies every month.

## Critical rules

Never silently discard an unmatched item, even 0.50; small errors can mark a systematic problem. Never force a reconciliation with a "reconciliation adjustment" entry whose cause is not understood. Reconcile in chronological order.
