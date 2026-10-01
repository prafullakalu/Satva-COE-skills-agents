---
name: credit-card-reconciliation
description: >-
  Reconcile company credit card and charge-card accounts to the statement: liability roll-forward, payments, interest and fees, refunds and chargebacks, employee cards, and missing receipts. Use for "reconcile the credit card", "card statement does not match", "card payments and rewards", "employee card expenses", "unrecognised card charge", or "card balance on the balance sheet".
metadata:
  department: "accounting"
  domain: "reconciliation"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Credit card reconciliation

A card is a liability account. The reconciliation proves the ledger liability equals what the issuer says is owed, and that every charge has a business purpose and a document.

## 1. Roll-forward test

```
Prior statement closing balance (owed)             P
+ Purchases and cash advances this period          +
+ Interest, fees, annual fee                       +
- Payments made                                    -
- Refunds, credits, rewards credited               -
= Closing balance per statement                    S
```

Check that P equals last period's reconciled ledger balance and that the arithmetic reproduces S. Then compare S to the ledger balance at statement date.

Remember the statement date usually differs from month end. At month end, the ledger holds charges from the statement cutoff to month end that are not on any statement yet; that is a normal reconciling item (charges since statement date) or is reconciled to the issuer's online pending-transactions view.

## 2. Procedure

1. Import or enter the statement transactions (see `bank-feed-import-and-capture`); control totals to the statement.
2. Match each line to a ledger entry or to a receipt and bill.
3. Payments to the card from the bank: the bank side is a transfer to the card liability, not an expense. Verify both ledgers show the payment once, on matching dates.
4. Record interest, annual fees, late fees and foreign transaction fees as expense (interest and bank charges). Late fees often are not deductible; code separately.
5. Refunds and chargebacks: credit the original expense account (or the vendor), not income. A chargeback in dispute stays visible as a receivable from the issuer or vendor until resolved.
6. Rewards, cashback and points: record when credited or redeemable, not when accrued by the issuer, unless the amounts are material and the policy says otherwise; credit to the relevant expense or other income per policy.
7. Foreign-currency charges: record in the card currency at the issuer's converted amount to keep the statement tie; do not re-translate.
8. Compare adjusted ledger to statement; difference must be zero.

## 3. Employee and shared cards

- Each cardholder's spend is reviewed monthly against receipts and a purpose; unexplained or personal charges become employee receivables or payroll deductions per policy, never silent expense.
- Matching the cardholder, merchant and amount to the expense report prevents double reimbursement (a claim for something already paid by the company card).
- Limits and cancellations: confirm leavers' cards are cancelled.

## 4. Fraud and anomaly checks

Charges from unknown merchants, repeated small test amounts followed by a large one, charges after a card was reissued, duplicates on the same day, weekend or foreign charges outside the usual profile, subscription creep. Escalate unrecognised charges to the cardholder and the issuer promptly; disputes have time limits.

## 5. Missing receipts

List charges over the client's threshold without a document, request in one batch, and track age. Persistent missing receipts for the same cardholder are a control finding, not a bookkeeping nuisance.

## 6. Sign-off

Preparer and reviewer as for `bank-reconciliation`. Retain statement, reconciliation, unmatched list, receipt exceptions. Review ageing of disputes and unidentified charges.

## Output

Roll-forward, reconciliation to ledger, unmatched and disputed items with owners, receipt exception list, proposed entries (fees, interest, reclasses) in draft.

## Do not

- Record card payments as expenses.
- Net refunds against a different vendor's expense.
- Write off unexplained charges to miscellaneous.
- Reconcile a card to a "current balance" screenshot instead of the statement.
