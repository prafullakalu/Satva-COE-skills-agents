---
name: zoho-books-month-end
description: >-
  A month-end close checklist for a Zoho Books organization that an agent can run read-only and report on: bank balances, AR and unapplied payments, uncategorised and duplicate entries, tax checks, draft documents, currency and chart-of-accounts sanity, and a sign-off summary. Use when asked to "close the month in Zoho Books", "month-end checks", "is the books ready to close", "pre-close review" or "what is still open for March".
metadata:
  department: "accounting"
  domain: "period-close"
  platform: "zoho-books"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Zoho Books: month-end close

Prerequisite: `zoho-books-operating-rules`. The connector cannot lock periods, post journals, or run reports, so this skill is a read-only pre-close review that produces a clear go/no-go and a fix list. Locking the period and any journals are done by the accountant in the UI.

Define the period first: `period_start`, `period_end` (yyyy-mm-dd) and the as-of date for balances. Confirm the org with `get_organization`.

## Steps (run in order, record pass/fail for each)

1. **Drafts and stale documents.** `list_invoices` with `status=draft` and date in the period; same for `list_estimates`, `list_sales_orders`, `list_purchase_orders`. Drafts are not in the ledger. Each draft is either to be sent (revenue missing) or deleted. Also `status=sent` with a date in the period that are really still quotes.
2. **Revenue completeness.** Compare invoices dated in the period against the source of truth the client uses (shop orders, timesheets, subscription list). Count and total must agree; list gaps. Beware invoices dated one day outside the period due to timezone.
3. **AR.** Build aging per `zoho-books-invoices-ar` D. Check: AR subledger total equals the AR control account (`list_chart_of_accounts`, `showbalance=true`); unapplied customer payments (`list_customer_payments`, look for amounts not fully applied) have a reason; debtors over 90 days have a bad-debt decision recorded by the owner.
4. **Cash and banks.** For each account in `list_bank_accounts`: the book balance versus the statement balance at period end (needs the user's statements). Uncleared items older than 30 days get queried. Run `zoho-books-bank-reconciliation` where a difference exists. A close with an unreconciled bank account is not a close.
5. **Expenses.** `list_expenses` for the period: missing receipts (no attachment is not visible; ask), expenses on suspense or "uncategorized" accounts, duplicates (same vendor, amount, date), personal items, items dated outside the period. Capitalisation candidates (large one-off purchases booked to expense) go to the owner.
6. **Payables.** The MCP cannot list bills. Ask the user for the AP aging from Reports > Payables and check it against the AP control balance from the chart of accounts. If unavailable, mark this step "not verifiable via connector".
7. **Tax.** Run the pre-return pass in `zoho-books-taxes-gst-vat` section 6. Tax control accounts should be near the amount the return will show.
8. **Foreign currency.** `list_currencies`: confirm exchange rates were updated for the period end. Open foreign-currency balances (AR, AP, bank) need period-end revaluation, which is a UI/journal action; flag it.
9. **Chart of accounts hygiene.** `list_chart_of_accounts` with balances: unexpected balances (negative AR, negative inventory, equity or suspense accounts with movement), inactive accounts with balance, accounts created this month.
10. **Accruals and prepayments.** Ask for or review known items: payroll, rent, subscriptions, deferred revenue, depreciation. These need manual journals the connector cannot post; give the proposed entries (debit, credit, amount, reason) for approval.
11. **Cut-off tests.** Last five invoices of the period and first five of the next: dated in the right period? Same for large expenses.
12. **Roll-forward sanity.** Compare key balances and P&L lines with the previous month and the same month last year (the user supplies the P&L if not extractable). Investigate lines moving more than 20 percent or 1,000 in base currency, whichever the user prefers; state the threshold you used.

## Decision

- **Go**: every step pass, or fails are only documented and accepted by the owner.
- **Conditional**: only non-material items open; list them with owner and date.
- **No-go**: any unreconciled bank account, AR control mismatch, unexplained tax difference, or missing revenue.

## Do not

- Declare "closed". You can recommend; the accountant locks the period.
- Post catch-up entries dated in a closed period.
- Make quiet corrections during the review. Every proposed change is listed and confirmed.

## Output

A one-page close memo: period, org, go/no-go; a table of steps with status (pass, fail, not verifiable) and evidence (counts, totals, ids); an exceptions list with suggested owner; proposed journals; what the accountant must do in the UI to lock the period.
