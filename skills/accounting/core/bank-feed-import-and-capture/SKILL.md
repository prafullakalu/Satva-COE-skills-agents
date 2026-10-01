---
name: bank-feed-import-and-capture
description: >-
  Bring bank, card and payment-processor transactions into the ledger safely: feed versus file import, column mapping, signs, dates, duplicate detection, opening-date cutoff, and a staged review before posting. Use for "import bank statement", "CSV import", "bank feed", "duplicate transactions", "load processor payouts", or "transactions missing from the feed".
metadata:
  department: "accounting"
  domain: "transaction-capture"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Bank feed and file import

The statement is the evidence; the feed is a convenience. An import is correct only when imported totals tie to the statement.

## 1. Choose the channel

| Channel | Use when | Risk |
|---|---|---|
| Live bank feed | Account supported, ongoing | Gaps and delays; feed may start mid-statement |
| Statement file (CSV, OFX, QIF, MT940, CAMT) | Backfill, unsupported bank, feed outage | Wrong column mapping, sign, date format |
| PDF statement | Last resort | Extraction errors; verify every line against totals |
| Processor report (card payments, wallets, marketplaces) | Gross sales vs payouts | Fees netted in payouts; see section 6 |

## 2. Prepare

1. Identify account, currency, period and expected opening and closing balance from the statement itself.
2. Define the import cutoff: the first date the ledger should receive transactions (the conversion date plus one day, or the day after the last reconciled item). Nothing earlier is imported.
3. Note the statement's own totals: sum of credits, sum of debits, transaction count.

## 3. Map and normalise

- **Dates**: confirm format (day-month versus month-day) by finding a date whose day exceeds 12. Use the value or posting date consistently; record which.
- **Sign convention**: money-in positive, money-out negative, or separate debit and credit columns. Test with one known deposit and one known payment.
- **Amount parsing**: thousand separators, decimal commas, parentheses for negatives, trailing minus, currency symbols.
- **Payee and description**: keep the original bank text untouched in a reference field; derive a clean payee separately.
- **Reference IDs**: keep the bank's transaction ID when present; it is the best duplicate key.
- **Encoding**: check for stripped leading zeros in references and mangled non-ASCII text.

## 4. Stage, do not post

Load into a staging view or an unreviewed state. Then verify:

1. Row count equals statement count.
2. Sum of imported money-in and money-out equals statement totals.
3. Opening balance plus net imported equals closing balance (a running-balance column, if present, must agree row by row).
4. No transactions dated outside the statement period or before the cutoff.

If any check fails, stop and find the cause before categorising anything.

## 5. Duplicate detection

Match on bank transaction ID first. Without an ID, flag as probable duplicate when account, date within one day, absolute amount and normalised description all match an existing or already-reconciled transaction. Then decide by evidence:

- Two identical real transactions on one day (two coffees, two same-value transfers) are legitimate; keep both and note why.
- Overlapping statement ranges and feed-plus-file double loads are the usual duplicate sources.
- Never auto-delete. Present the pairs and exclude on confirmation, keeping the audit trail.

## 6. Payment processors and marketplaces

A payout is not revenue. Record gross sales (from the sales system) in revenue and fees as expense; bank receives gross minus fees, refunds and holds. Use a processor clearing account:

```
On sale (from sales ledger):   Dr Processor clearing 100   Cr Revenue 100
On fee:                        Dr Processing fees   3       Cr Processor clearing 3
On payout deposit (bank):      Dr Bank 97                  Cr Processor clearing 97
```

Clearing must reach zero (allowing for in-transit payouts and reserves). Import the processor's payout report to match each deposit to its component transactions.

## 7. Transfers and special items

Transfers between own accounts are posted once, as a transfer, not as income and expense. Credit card payments reduce the card liability. Cash withdrawals, owner contributions and loan receipts need an owner decision, not a guess.

## 8. After import

Hand off to `transaction-categorisation-rules`, then `bank-reconciliation` or `credit-card-reconciliation`. Retain the source file (hash or name and date) as evidence of what was loaded.

## Output

Import log: account, period, source, row counts, control totals, tie-out result, duplicates found and decisions, items outside cutoff, open questions.

## Do not

- Import before the statement totals are known.
- Edit amounts to force a tie-out; investigate the difference.
- Post everything unreviewed because the feed "usually works".
- Overwrite the original bank description.
- Import statements into an account for a locked period.
