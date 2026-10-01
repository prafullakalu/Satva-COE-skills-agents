---
name: qbo-invoicing-and-collections
description: >-
  Run accounts receivable in QuickBooks Online: create, correct, void and send invoices, convert estimates, record and apply customer payments and credit memos, and work an overdue collections list. Use when asked to "invoice this customer in QuickBooks", "who owes us money", "chase overdue invoices", "apply this payment", "convert the estimate to an invoice", "void that invoice", "customer credit memo", or "why is the customer balance wrong".
metadata:
  department: "accounting"
  domain: "accounts-receivable"
  platform: "quickbooks"
  owner: "satva-coe"
  status: "stable"
  license: "Satva-original"
  source: "original"
---

# QuickBooks invoicing and collections

Follow `qbo-mcp-operating-rules` for every write. All amounts in cents internally; QBO rounds per line.

## A. Collections review (read-only)
1. `ar_collections_worklist` (`asOf` optional, `minDaysOverdue: 1` to hide not-yet-due, `limit`). It returns open invoices (Balance > 0) grouped by customer, with buckets current / 1-30 / 31-60 / 61-90 / 90+, oldest due date, email and invoices. It reads at most 1000 open invoices; if `truncated` is true, say totals are partial. Invoices without terms are aged from the invoice date.
2. Cross-check the total against `get_aged_receivables` at the same `report_date`. They should agree; a difference is usually (a) unapplied payments or credit memos (aging report nets them, a list of invoices does not), or (b) a journal entry posted to Accounts Receivable.
3. For each customer to chase, `customer_360` (by `customerId` or `name`): profile, open and overdue amounts, last invoices and payments, outstanding credit memos, average days to pay (sampled). Ambiguous names return a list instead of a guess; pick by Id.
4. Draft the chase: tone by bucket, the invoice numbers and amounts, payment instructions, and any credits the customer holds. Do not send; show the draft. Sending an invoice reminder is a human decision.

Rank by (amount x days overdue), not by days alone. A 95-day $40 balance rarely beats a 35-day $18,000 one.

## B. Create an invoice
1. Find the customer: `query_quickbooks` `SELECT Id, DisplayName, Balance, Active FROM Customer WHERE DisplayName LIKE '%Acme%'`. If none, `create_entity` `Customer` (`DisplayName` must be unique across customers, vendors and employees; no colon, tab or newline). Run `find_duplicates` `kind: "customers"` before creating a new one.
2. Find items: `query_quickbooks` `SELECT Id, Name, Type, UnitPrice FROM Item WHERE Active = true`. Every sales line needs `SalesItemLineDetail.ItemRef`.
3. Currency, tax and class: read `get_company_overview`. For a foreign-currency customer see `qbo-multi-currency`; for tax codes see `qbo-sales-tax`; if class or location tracking is on, include `ClassRef`/`DepartmentRef` per the company's convention.
4. Show the draft (customer, date, terms, each line item/qty/rate/tax, total) and get approval.
5. `create_invoice` (`customer_ref`, `line_items[{item_ref, qty, unit_price, description}]`, optional `doc_number`, `txn_date`) or `create_entity` `Invoice` for full control (terms, tax detail, class, `BillEmail`, `CustomerMemo`).
6. Read back with `read_invoice` or `get_entity`. Report invoice number, total, due date and the `qboLink`.

## C. Fix an invoice
- Unpaid, unsent, wrong detail: `update_entity` `Invoice` with a sparse patch. If you patch `Line`, send ALL lines (arrays are replaced).
- Already emailed or paid, amount wrong: do not edit history. Issue a `CreditMemo` for the difference or `void_invoice` and reissue, per the customer's wishes and your accountant's policy. `void_invoice` zeroes the invoice and is irreversible.
- Never `delete_entity` an invoice that has a payment applied: reverse the payment first, or void.
- Duplicate invoice found by `find_duplicates` `kind: "invoices"` (same customer, same amount, within `windowDays`, or repeated DocNumber): confirm with the customer's history, then void the duplicate rather than delete if it was emailed.

## D. Send
`send_invoice` emails the invoice to the `BillEmail` already on it and sets EmailStatus. The recipient cannot be passed. Check the address first; to change it, `update_entity` `Invoice` `{BillEmail:{Address:"..."}}`. Needs explicit approval every time. `get_invoice_pdf` returns the PDF without emailing.

## E. Estimate to invoice
`convert_estimate_to_invoice` with `dryRun: true` first and show the `invoiceBody`. It refuses estimates that are Closed, Rejected, Converted or already linked to an invoice unless `force: true` (do not force without asking why). Check the warnings it returns (totals can differ after tax recalculation).

## F. Record a customer payment
1. Identify the invoices and amounts. Check each is open: `query_quickbooks` `SELECT Id, DocNumber, Balance, CustomerRef FROM Invoice WHERE Id IN ('..')`.
2. `apply_payment_to_invoices` with `dryRun: true`: it validates in integer cents (positive, 2 decimals, sum <= total, invoices belong to the customer, each amount <= open balance). Show the result, including `unapplied`.
3. Run it for real. Without `depositToAccountId` the money lands in Undeposited Funds, which is correct when a bank deposit will batch several receipts; pass the bank account Id when the payment is deposited alone (cash, direct bank transfer).
4. If a payment is overpaid, the unapplied remainder stays as a customer credit. Do not leave it floating: apply it to another invoice or refund it.
5. Payment recorded against the wrong invoice or customer: `void_payment` and re-record. Do not edit Payment lines in place.

## G. Credits and refunds
- Credit for returned goods or price error: `create_entity` `CreditMemo` (`CustomerRef`, lines). Apply it to the invoice by creating a `Payment` whose line links both the Invoice and the CreditMemo (`LinkedTxn`), total zero or net; verify with `get_entity` `Invoice` that `Balance` fell.
- Cash refund of a paid sale: `RefundReceipt` (`create_entity`), `DepositToAccountRef` = the bank or card account it was paid from.
- Immediate sale paid at once: `create_sales_receipt`, not an invoice plus payment.

## Pitfalls
- An invoice without terms has no due date, so it never ages as overdue in tools that use `DueDate`; check terms on the customer.
- `DocNumber` is a free text field; auto-numbering may be on. Do not set a number that skips the sequence without a reason.
- Voided invoices stay in the books at zero. If the user expects them to disappear from lists, tell them.
- Sales tax is applied by QBO from the customer and item tax codes; sending your own tax amount in `TxnTaxDetail` can be overridden. Verify the total after create.
- Multicurrency: `Balance` is in the invoice currency, `HomeBalance` in home currency. The worklists use `HomeBalance` so totals add up.
- Statement balances differ from invoice-only lists when there are unapplied payments and credit memos.

## Output
Collections: table of customers (total due, oldest due, bucket split, proposed action). Writes: before/after, ids, links, and the open balance after.
