---
name: month-end-close
description: >-
  Run a monthly close end to end: close calendar (WD-1 to WD+10), sub-ledger cut-off, accruals and prepaids, reconciliations, review sign-offs, lock date and close package. Use when asked to "run the month-end close", "build a close checklist", "close calendar", "what must be done before we lock the period", or "why does close take 15 days".
metadata:
  department: "accounting"
  domain: "period-close"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Month-end close

Goal: a locked, reviewed set of books and a close package, within a fixed number of working days, with every balance sheet account supported. Platform-neutral: map each step to your ledger's equivalent report or screen.

## Inputs to confirm first
- Period end date, entity, base currency, reporting basis (cash, accrual, IFRS, US GAAP).
- Prior period close package and open-items list (carry-forwards).
- Materiality: default for review = the lower of 0.5% of revenue or 5% of pre-tax income for the month; for SMEs also set an absolute floor (e.g. 250 in base currency) below which items are not investigated.
- Who prepares, who reviews. Preparer and reviewer must be different people; record both.

## Close calendar (target 5-8 working days; WD = working day after period end)
| Day | Work | Owner |
|---|---|---|
| WD-3 to WD-1 | Send cut-off reminders (expenses, timesheets, PO receipts); confirm payroll dates; pre-book recurring entries | Controller |
| WD0 (period end) | Stop-ship/cut-off note for inventory and billing; export bank statements | AR/AP |
| WD1 | Sub-ledger cut-off: AR invoices, AP bills (incl. goods received not invoiced), expense reports, payroll posted | AR/AP/Payroll |
| WD2 | Bank, card, payment-processor and wallet reconciliations (use the reconciliation skills) | Bookkeeper |
| WD2-3 | Accruals, prepaids, deferred revenue, depreciation, FX revaluation, inventory/COGS adjustments | Accountant |
| WD3-4 | Balance sheet account reconciliations with supporting schedule; intercompany matched and eliminated | Accountant |
| WD4 | Preliminary trial balance; flux review (see flux-variance-analysis) | Controller |
| WD5 | Adjustments from flux; reviewer sign-off; tax and payroll liability tie-outs | Controller |
| WD5-6 | Lock the period (soft lock first); close package issued | Controller |
| WD+10 | Late-adjustment window closes; hard lock | Finance lead |

## Procedure
1. **Cut-off.** Confirm no transactions are dated after period end in the period and vice versa. Test: last 5 invoices and bills before, first 5 after; goods received/shipped around the date; credit notes issued in the next month that relate to this one.
2. **Sub-ledger to GL tie-out.** AR sub-ledger total = AR control account; AP sub-ledger = AP control; inventory valuation report = inventory account; fixed asset register = FA cost and accumulated depreciation. Any difference is unposted manual journals into control accounts: find and fix, never plug.
3. **Bank and clearing accounts.** Reconcile every bank, card, PayPal/Stripe-type clearing and payout account. Unreconciled items older than 30 days must have an owner and a reason.
4. **Accruals.** Expenses incurred not invoiced (GRNI, utilities, contractors, bonuses, audit fees). Method: PO/receipt report, contracts, run-rate for recurring items. Reverse on day 1 of next period (auto-reversing journals). Keep a schedule with basis and amount.
5. **Prepaids and deferrals.** Amortise per schedule: monthly amount = total / months of benefit. Deferred revenue released per revenue-recognition-606.
6. **Fixed assets.** Post depreciation (see fixed-assets-depreciation), additions, disposals; capitalisation threshold respected.
7. **Payroll.** Payroll expense and liabilities reconciled to the payroll register (see payroll-accounting).
8. **FX.** Revalue open foreign-currency monetary balances at the closing rate; post unrealised gain/loss; reverse next month if policy requires.
9. **Inventory and COGS** for product businesses (see ecommerce-inventory-cogs).
10. **Taxes.** Sales tax/VAT control account agrees to the return working; income tax provision if required monthly.
11. **Intercompany.** Both sides agree before elimination (see multi-entity-intercompany-consolidation).
12. **Suspense and clearing accounts to zero.** Uncategorised, ask-my-accountant, undeposited funds, and suspense must be zero or itemised.
13. **Trial balance review.** Run the flux analysis, post adjustments, re-run.
14. **Sign-off and lock.** Preparer and reviewer sign the checklist; set the lock date; any later change goes through a documented reopen.

## Balance sheet reconciliation standard
For every balance sheet account: GL balance, supporting balance (statement, sub-ledger, schedule), difference, explanation of each reconciling item with age, preparer, reviewer, date. Tolerance: zero for cash and control accounts; judgement elsewhere but any unexplained difference over materiality escalates.

## Evidence to keep
Bank statements, reconciliation reports, accrual and prepaid schedules, depreciation run, payroll register, tax return working, flux commentary, signed checklist, lock-date screenshot or audit-log entry.

## Red flags
- Same person prepares and approves their own manual journals.
- Large round-number journals at period end without support.
- Reversals that do not reverse; recurring entries that stopped.
- Suspense balances carried more than one close.
- Close takes longer each month: usually unreconciled bank feeds or late AP.

## Do not
- Do not lock the period before the flux review is done.
- Do not plug differences to suspense or to retained earnings.
- Do not post into a locked period; reopen with approval and log it.

## Output
A close package: (1) completed checklist with names and dates, (2) trial balance, P&L and balance sheet, (3) flux commentary, (4) open-items list with owner and due date, (5) summary of adjustments posted after the first TB.
