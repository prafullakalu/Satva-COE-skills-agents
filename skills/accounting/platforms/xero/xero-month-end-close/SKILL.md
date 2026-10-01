---
name: xero-month-end-close
description: >-
  Runs a month-end close checklist inside Xero via the Satva Xero MCP: bank reconciliation status, unapproved
  invoices and bills, AR/AP tie-out, suspense and clearing balances, accrual and prepayment journals, tax review,
  trial balance and P&L flux, then the period lock. Use for "month end in Xero", "close the books", "close
  checklist", "lock the period", "are we ready to close", "pre-close review", "year-end Xero".
metadata:
  department: "accounting"
  domain: "close"
  platform: "xero"
  owner: "satva-coe"
  status: "stable"
  license: "Satva-original"
  source: "original"
---

# Xero month-end close

Follow `xero-mcp-operating-rules`. This skill orchestrates others: `xero-bank-reconciliation-review`,
`xero-invoices-and-collections`, `xero-bills-and-supplier-payments`, `xero-manual-journals`, `xero-reports-pack`,
`xero-tax-rates-and-sales-tax`.

## Important limits

- The MCP cannot set the period lock date, post bank statement matches, approve draft invoices or credit notes, or file
  tax returns. The close ends with a human setting the lock date in Xero (Settings > Financial settings) after the
  user signs off. Say so at the start.
- Everything below is a review and proposal; writes need confirmation.

## Workflow (in order; stop and report on a blocker)

**0. Scope.** Org (`list-organisation-details`), period start/end, base currency, tax basis, current lock date.
Confirm the period end date with the user. Close is for a completed period; refuse a period still running.

**1. Cut-off sanity.** Anything dated after period end must not be in the period; anything for the period must be
dated in it. Look at `list-invoices`, `list-bank-transactions`, `list-manual-journals` near the cut-off dates.

**2. Bank.** Per bank account: bank summary closing balance (`list-report-bank-summary`) vs statement balance
(supplied by user). Unreconciled items at period end, stale items, duplicates, transfers. Statement-line matching
is a user task in Xero.

**3. Unapproved documents.** From `list-invoices`: DRAFT and SUBMITTED sales invoices and bills dated in the
period. Each is either missing revenue/expense or junk. List with amount and age; the user approves or deletes
(`void-invoice` targetStatus DELETED works only on DRAFT/SUBMITTED). Also draft credit notes
(`list-credit-notes`), draft manual journals (`list-manual-journals`), draft/authorised purchase orders that are
received but unbilled (`list-purchase-orders`).

**4. Sub-ledger tie-out.** Compute AR and AP from `list-invoices` (AUTHORISED, Amount Due) as at period end and
compare to Accounts Receivable and Accounts Payable on the balance sheet at the same date
(`list-report-balance-sheet date`). Differences = credits, overpayments/prepayments, or back-dated payments.
Explain to zero or document why not.

**5. Suspense and clearing.** `list-trial-balance date` for accounts named Suspense, Uncategorised, Clearing,
Ask my accountant, Unallocated: balance must be zero. Unknown items block the close.

**6. Accruals and prepayments.** Check recurring journals from last period (`list-manual-journals modifiedAfter`):
reverse last month's accruals, post this month's accruals, release prepayments, depreciation. Prepare through
`xero-manual-journals` (DRAFT first). Check recurring bills (`list-repeating-invoices`) are not due to generate
inside the closed period.

**7. Inter-company / loans / payroll / tax control accounts.** Balance sheet lines for sales tax (GST/VAT),
payroll liabilities, loans: compare to returns, payroll reports (NZ/UK org only: `list-payroll-*`), loan
statements. Variance explained or flagged. See `xero-tax-rates-and-sales-tax`.

**8. FX.** For foreign-currency bank accounts, receivables, payables: confirm rates and revaluation
(`xero-multi-currency`).

**9. Reasonableness (flux).** `list-profit-and-loss fromDate toDate periods=3 timeframe=MONTH` compare
this month vs prior months and vs same month last year; list lines moving more than 10% and a materiality floor
(e.g. 500 in base currency); give a cause or a question. Check gross margin %, payroll % revenue, and unusual
zero/doubled lines (a missing or doubled recurring bill).

**10. Trial balance proof.** `list-trial-balance date`: debits = credits; no accounts with the wrong sign (assets
credit, liabilities debit) without explanation; negative AR/AP flagged.

**11. Sign-off pack.** Produce the report pack (`xero-reports-pack`): P&L, balance sheet, TB, aged lists.

**12. Lock.** After sign-off, a user sets the period lock date in Xero. Re-read `list-organisation-details` to
confirm the date. Record who/when.

## Pitfalls

- Reporting on a cash basis hides AR/AP problems; the balance sheet is always accrual-based in effect, so compare.
- A back-dated payment or invoice entered after review changes closed numbers: ask the user to set the lock date
  immediately after sign-off, and re-run the TB if any activity is dated in the closed period afterwards (check
  `list-invoices` Last Updated, `list-bank-transactions`).
- Do not "fix" a failed tie-out with a plug journal.
- Year-end: retained earnings and current-year earnings roll automatically; do not journal them. Confirm the
  financial year end in org details.
- Rate limit: a close touches many pages. Plan about 30-80 calls per org; do not run multiple orgs in parallel.

## Output format

```
Org | period | lock date (before -> after) | prepared as-at
Checklist table: # | step | status (done/blocked/not applicable) | evidence | owner
Blockers (must fix) / Adjustments proposed (journal drafts) / Questions for client
Key figures: revenue, gross margin %, net profit, cash, AR, AP vs prior period
Sign-off: statement of what was NOT verified (e.g. statement balances, payroll, tax filing)
```
