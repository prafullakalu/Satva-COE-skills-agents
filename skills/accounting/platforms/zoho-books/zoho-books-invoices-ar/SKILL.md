---
name: zoho-books-invoices-ar
description: >-
  Accounts receivable in Zoho Books: create and amend invoices, record customer payments against the right invoices, build an aging view, and chase overdue balances, using the Zoho Books MCP tools (list_invoices, get_invoice, create_invoice, update_invoice, create_customer_payment, list_customer_payments, list_contacts). Use when asked to "raise an invoice in Zoho", "who owes us money", "AR aging", "record this payment", "apply payment to invoice", "list overdue invoices" or "customer statement balance".
metadata:
  department: "accounting"
  domain: "accounts-receivable"
  platform: "zoho-books"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Zoho Books: invoices and receivables

Prerequisite: `zoho-books-operating-rules` (organization id, paging, write confirmation).

## A. Create an invoice

1. Resolve the customer: `list_contacts` with `contact_type=customer` and `contact_name` or `email`. Zero hits: ask before `create_contact`. Several hits: show them, do not choose.
2. Resolve each line to an `item_id` via `list_items`. `create_invoice` requires `item_id` on every line; do not invent items. If the service is not in the catalogue, propose a new item and wait.
3. Resolve tax per line: `list_taxes` and use `tax_id`. Do not hand-type `tax_percentage`; the tax object carries the account mapping. Country-specific fields are in `zoho-books-taxes-gst-vat`.
4. Duplicate check: `list_invoices` with `reference_number` (your PO or source id) and `customer_id`. If one exists, stop and report it.
5. Draft the payload: `customer_id`, `date`, `payment_terms` (or `due_date`), `reference_number`, `line_items[] {item_id, rate, quantity, tax_id, description}`, `currency_id` + `exchange_rate` if not base currency, `notes`/`terms` if the user supplied them.
6. Show a summary (customer, lines, subtotal, tax, total, due date, currency) and get a yes.
7. Call `create_invoice`. By default it creates a draft. Only pass `send=true` if the user explicitly asked to email it; sending is irreversible.
8. Read back with `get_invoice` and confirm the total equals what you quoted. A mismatch usually means tax-inclusive vs exclusive (`is_inclusive_tax`) or a discount-before-tax setting (`is_discount_before_tax`).

Conversions: from an estimate use `invoiced_estimate_id`, from a sales order use `salesorder_item_id` on lines, so the source document closes. Billable expenses attach with `expense_id`.

## B. Amend an invoice

- Draft or sent-unpaid: `get_invoice`, change what is asked, then `update_invoice` sending ALL existing lines with their `line_item_id` (omitted lines are deleted).
- Partially or fully paid: do not edit amounts. Raise a credit note or void and reissue in the UI (the connector has no credit-note tool). Explain why: editing a paid invoice breaks the payment application and any tax return already filed.
- Never `delete_invoice` a sent invoice. Delete is for mistaken drafts only.

## C. Record a customer payment

1. Identify the exact invoice(s): `list_invoices` with `customer_id` and `status=unpaid` (also `partially_paid`, `overdue`).
2. Pick the deposit account with `list_bank_accounts` (`account_id`): the bank, undeposited funds, or a clearing account. Ask if the payment came via a gateway; see `stripe-payout-fee-reconciliation` for that pattern.
3. `create_customer_payment` needs `customer_id`, `date`, `amount`, `payment_mode`, `invoice_id`, `amount_applied` and an `invoices[]` list of `{invoice_id, amount_applied}`. Rules:
   - Sum of `amount_applied` must be <= `amount`. The remainder becomes an unapplied credit on the customer, which is correct for overpayments; say so.
   - Short payment: apply what was received and leave the invoice partially paid. Bank fees go in `bank_charges`; do not shave the invoice.
   - Foreign currency: `exchange_rate` is customer currency to base; Zoho posts the realised gain or loss.
   - Put the bank reference in `reference_number` so reconciliation can find it.
4. Re-read the invoice: `balance` and `status` must have moved as expected.

Duplicates: before creating, `list_customer_payments` for the customer and date range; same amount and same reference means it already exists.

## D. Aging and collections

No aging report tool exists, so build it from `list_invoices` (`status` in unpaid, partially_paid, overdue; page to the end):

1. Use `balance`, not `total`. As-of date = today unless asked.
2. Bucket by days past `due_date`: current (not yet due), 1-30, 31-60, 61-90, 90+.
3. Group by customer; show invoice count, total balance, oldest invoice date.
4. Cross-check: the sum of balances should equal the Accounts Receivable account in `list_chart_of_accounts` with `showbalance=true`. A gap means unapplied payments, credit notes, or manual journals to AR. Report the gap and its likely source; do not plug it.
5. Rank collection effort by balance x age. Draft reminder text for the user to send; the connector cannot send reminders, and sending on the user's behalf needs their approval.

## E. Checks

- Currencies are never mixed: aging per currency, plus a base-currency total using each invoice's own rate.
- Credit balances (customers who overpaid) are listed separately, not netted silently.
- Void and draft invoices are excluded from aging.

## Do not

- Create an invoice without a source reference.
- Apply a payment to "the oldest invoice" unless the user says so; ask when the remittance is ambiguous.
- Report AR from the first page of results.

## Output

A short table: customer, invoice, due date, balance, days overdue, bucket; then totals per bucket, the reconciliation to the ledger, and the three actions you recommend.
