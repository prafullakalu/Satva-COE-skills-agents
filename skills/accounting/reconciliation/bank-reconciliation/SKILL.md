---
name: bank-reconciliation
description: >-
  Reconcile a bank or cash account to the statement: matching hierarchy, outstanding items, deposits in transit, unrecorded bank items, unexplained differences, and sign-off. Use for "reconcile the bank", "bank rec", "statement does not match the ledger", "outstanding cheques", "reconciling items", "stale uncleared items", or "bank reconciliation review".
metadata:
  department: "accounting"
  domain: "reconciliation"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Bank reconciliation

A bank reconciliation is a statement of timing differences, not a plug. The ledger cash balance, adjusted, must equal the bank balance, adjusted, with every difference named, dated and supported.

## 1. Inputs

Signed or system-generated statement for the exact period, the ledger account for the same period, prior period's reconciliation (to carry forward open items), and the list of unreconciled ledger items. Confirm the statement's opening balance equals the prior reconciled closing balance; if not, stop (missing statement, or a change after the last reconciliation).

## 2. Standard form

```
Balance per bank statement at <date>                       X
  Add: deposits in transit (in ledger, not yet on bank)    +
  Less: outstanding payments (in ledger, not yet cleared)  -
  +/- Bank errors (to be reported to bank)                 +/-
Adjusted bank balance                                      A

Balance per ledger at <date>                               Y
  Add: bank credits not yet in ledger (interest, receipts) +
  Less: bank debits not yet in ledger (fees, charges)      -
  +/- Ledger errors (to be corrected by entry)             +/-
Adjusted ledger balance                                    B

Difference (A - B) must be exactly zero.
```

## 3. Matching hierarchy

Match in this order and stop at the first strong match:

1. **Exact**: same amount, date within a few days, reference or counterparty agrees.
2. **One-to-one on amount and date window**: unique candidate only.
3. **Grouped**: one bank line to several ledger items (a batched deposit of several customer payments, a payment run) or the reverse. The grouped total must equal the bank amount.
4. **Net of fees**: processor or merchant payouts, where bank equals gross less fees and refunds.
5. **Manual with evidence**: anything left, matched by a person with a note.

Never match two items merely because they net to zero across unrelated payees.

Confidence tiers, normalisation rules, a table of what may be auto-matched versus what needs approval, tests for stubborn differences (divisible by 9, double entries) and catch-up scenarios are in `references/matching-tiers-and-scenarios.md`.

## 4. Classify every unmatched item

| Class | Action |
|---|---|
| Deposit in transit (recorded, not yet banked) | Carry forward; clears within a few days |
| Outstanding payment (issued, not cleared) | Carry forward; chase if older than the normal clearing time (cheques commonly 30 to 90 days; stale-dated per policy) |
| Bank item not in ledger (fees, interest, direct debits, returned items) | Prepare entry; do not leave as reconciling item beyond close |
| Ledger error (duplicate, wrong amount, wrong date, wrong account) | Correct in the ledger via `journal-entry-controls` or the source document |
| Bank error | Query with the bank; keep as reconciling item with correspondence reference |
| Unidentified receipt or payment | Suspense, with an investigation owner and age |

## 5. Procedure

1. Confirm opening balance continuity.
2. Auto-match, then work through the remainder by value, largest first.
3. Check dates at the edges: items in the last days of the period and the first days of the next.
4. Check for transposition errors when the difference is divisible by 9, and for a single item equal to the difference or half of it (a sign error doubles).
5. Check foreign-currency accounts: compare in the account's currency; revaluation is separate.
6. Prepare entries for bank items not in ledger; post only after approval, then rematch.
7. Complete the statement above and confirm the difference is zero.
8. Review ageing: list all reconciling items over 30 days, 60 days, 90 days with owner and action.

## 6. Review and sign-off

- Preparer signs and dates; a different person reviews (or the owner for a one-person shop).
- Reviewer verifies: statement balance agrees to the bank source (not only to what the preparer typed), ledger balance agrees to the system at the same date, reconciling items agree to subsequent clearing in the next statement (subsequent clearing test), no net unexplained difference, no old items without action.
- Retain statement, reconciliation, listing of outstanding items and the review evidence.
- After sign-off, lock reconciled transactions; changes then require reversal and a note.

## 7. Red flags

Round-number reconciling items, items repeatedly rolled forward, a "difference" line, payments cleared to someone not in the vendor master, unusual cash withdrawals, deposits from unrecognised sources, many manual matches by the same person, reconciliation completed long after period end.

## Output

Reconciliation statement in the form above, list of reconciling items with class, age and owner, proposed entries (draft), exception list for the reviewer.

## Do not

- Use a plug, suspense or "bank adjustment" to reach zero.
- Reconcile to a balance without the statement.
- Auto-clear items on amount alone when several candidates exist.
- Net old uncleared items away without investigating them.
