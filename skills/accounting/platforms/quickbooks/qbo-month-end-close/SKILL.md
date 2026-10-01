---
name: qbo-month-end-close
description: >-
  Run a month-end close inside QuickBooks Online using the Satva MCP: pre-close checks, cut-off, A/R and A/P tie-out, bank and card status, catch-all accounts, accruals, trial balance and variance review, and close-package output. Use when asked to "close the month in QuickBooks", "QBO month-end checklist", "is June ready to close", "prepare the close package", "tie out AR and AP", or "what is still open before we lock the books".
metadata:
  department: "accounting"
  domain: "period-close"
  platform: "quickbooks"
  owner: "satva-coe"
  status: "stable"
  license: "Satva-original"
  source: "original"
---

# QuickBooks month-end close

Platform-neutral close design is in `month-end-close`; this skill is the QuickBooks execution: which tool proves each step. Read-only until the user approves each fix (`qbo-mcp-operating-rules`). The server cannot set the closing date or password: locking the period is a manual step for an authorised user in QuickBooks.

## Inputs
Company (`list_companies`), period start and end (`YYYY-MM-DD`), report basis to close on (accrual unless the user says cash), prior-month close package if any.

## Close checklist with proof
Run in order. For each step record PASS, FAIL (with amount) or N/A, and the evidence.

1. **Setup.** `get_company_overview`: basis, tracking features, multicurrency. Confirm period dates against the fiscal year start.
2. **Nothing new will arrive.** Confirm with the user that sales, bills, payroll and expense claims for the period are all entered. `get_changes` (`changedSince` = a few days back) lists late edits after you start; re-run it before sign-off.
3. **Bank and card status.** Per account: `get_balance_sheet` at period end versus statement balance (see `qbo-bank-reconciliation-review`). The server cannot see Banking-tab feed items; ask the user to clear the "For review" queue and finish each reconciliation in QuickBooks. Record the date of the last reconciliation for each account.
4. **Undeposited Funds** at period end: `get_general_ledger` with `account` = its Id. Expected: only items banked after period end. Anything older must be deposited or corrected.
5. **A/R tie-out.** `get_aged_receivables` with `report_date` = period end versus the Accounts Receivable line on `get_balance_sheet`. Must match exactly (home currency). Open credits and unapplied payments: `ar_collections_worklist` plus `get_customer_balance`. Bad-debt review: invoices 90+ days (`ar_collections_worklist` buckets).
6. **A/P tie-out.** `get_aged_payables` with `report_date` = period end versus the Accounts Payable line. Review unpaid bills dated before period end that belong in the period (cut-off), and bills dated in the period for goods or services received after.
7. **Catch-all accounts.** `uncategorized_transactions` for the month. Target zero in `Uncategorized Expense`, `Uncategorized Income`, `Uncategorized Asset`, `Ask My Accountant`. Also check `Opening Balance Equity` has not moved.
8. **Accruals and prepayments.** Walk the user's schedule: accrued expenses (bills not yet received), accrued income, prepaid amortisation, deferred revenue, depreciation, payroll accrual, loan interest. Post missing ones with `qbo-journal-entries` and reverse accruals on day one of next month.
9. **Inventory** (if on): `get_inventory_valuation_summary` with `report_date` = period end versus the Inventory Asset balance on the balance sheet. Negative quantities, zero-cost items and large gaps are findings (`qbo-items-and-inventory`).
10. **Sales tax** (if on): `get_tax_summary` for the month versus the Sales Tax Payable balance (`qbo-sales-tax`).
11. **Multicurrency** (if on): exchange rates updated for period end; unrealised gain/loss entry posted if the policy requires (`qbo-multi-currency`).
12. **Trial balance.** `get_trial_balance` at period end. Debits equal credits; no unexpected balances in suspense or clearing accounts (Payroll Clearing, Undeposited Funds, Opening Balance Equity, Uncategorized *, Ask My Accountant). Negative balances on accounts that should not (A/R, A/P, inventory, bank) are findings.
13. **P&L review.** `period_comparison` (`start_date`, `end_date`, `compare: "prior_period"`, `accounting_method`) for top increases and decreases, with `compare: "prior_year"` for seasonality. Every movement above the user's threshold (suggest the larger of 10% and an absolute amount) needs a one-line explanation or a correction. Same `accounting_method` for both periods or the comparison is meaningless.
14. **Balance sheet review.** `get_balance_sheet` current month versus prior month (`summarize_column_by: "Month"` over two months). Every account with a movement has a supporting document or schedule; every loan, accrual and prepaid rolls forward.
15. **Class/location review** (if on): `get_profit_and_loss` with `summarize_column_by: "Classes"` or `"Departments"`; the "Not specified" column should be near zero.
16. **Lock (manual).** After sign-off, an authorised user sets the closing date (and password) in QuickBooks under Account and settings, Advanced. Say this is not done by the tool. Afterwards, any change must be a current-period correcting entry.

## Close package (output)
1. Status table: every step above with PASS/FAIL/N/A, owner, evidence.
2. Reports as at period end: `get_profit_and_loss`, `get_balance_sheet`, `get_cash_flow` (state the basis), `get_aged_receivables`, `get_aged_payables`, `get_trial_balance`. See `qbo-financial-reports` for reading them.
3. Variance commentary (3-8 bullets, each with the number and the cause).
4. Open items list: item, amount, owner, due date, whether it blocks lock.
5. Entries proposed or posted, with ids.
6. Not verified: bank feed queue, payroll provider reports, anything outside the QuickBooks scope the server was granted.

## Pitfalls
- Running reports on the wrong basis: the QuickBooks default can be cash even when the accountant works accrual. Pass `accounting_method` explicitly and quote it.
- Using `CurrentBalance` on an account as the period-end balance: it is today's balance. Use the balance sheet with `end_date`.
- Backdated entries after the package is issued change prior-period numbers silently unless a closing date is set.
- Reports in QuickBooks are live: save or export the package immediately, because the same report next week may differ.
- A balanced trial balance does not prove correctness; it proves only that debits equal credits.
