---
name: zoho-books-operating-rules
description: >-
  Ground rules for any agent working inside Zoho Books through an MCP connector: always resolve the organization_id first, know which Zoho data centre the org lives in, respect API limits, understand which operations the connector can and cannot do, and confirm before any write or delete. Use before touching Zoho Books at all, when a user says "check our Zoho Books", "post this in Zoho", "why did the Zoho call fail", or when a Zoho tool returns 401, 404, 429 or an empty list.
metadata:
  department: "accounting"
  domain: "platform-operations"
  platform: "zoho-books"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Zoho Books operating rules

Read this first; the other `zoho-books-*` skills assume it. Tool names below are those of the Zoho Books MCP connector (`list_invoices`, `create_invoice`, ...). Different connectors expose different subsets: verify the tool list you actually have before promising a capability.

## 1. Always start with the organization

1. Call `list_organizations`. One Zoho login can hold several independent organizations (separate books, currencies, tax set-ups).
2. If more than one comes back, ask which one. Never guess, never default to the first.
3. Call `get_organization` for the chosen id and note: base currency, fiscal year start, tax regime/country (India GST, UK/EU/GCC VAT, US sales tax), multi-currency on/off, and the plan edition. Everything later depends on these.
4. Pass that `organization_id` on every call. A missing or wrong id gives empty lists that look like "no data". An empty result on the first call of a session is a reason to re-check the org id, not to report zero activity.

## 2. Data centre and auth failures

- Zoho is hosted per data centre (`.com`, `.eu`, `.in`, `.com.au`, `.jp`, ...). A token from one DC does not work against another. A 401 or "invalid OAuth token" right after a successful login usually means the connector points at the wrong DC.
- Access tokens last one hour; the connector refreshes them. Repeated 401 after refresh means the grant was revoked or the scope is too narrow (scopes look like `ZohoBooks.invoices.CREATE`). Report which operation failed; do not retry blindly.

## 3. Limits

- About 100 requests per minute per organization; daily caps depend on plan (low thousands on small plans). HTTP 429 means stop and back off, not retry in a tight loop.
- `list_*` tools return 10 rows per page by default (max 200 on `list_invoices`). Always set `per_page` high and walk `page` until `page_context.has_more_page` is false. Reporting from page 1 only is the most common wrong answer.
- Prefer filtered lists (`status`, `date_start`/`date_end`, `customer_id`, `last_modified_time`) over pulling everything and filtering in your head.

## 4. What the connector can and cannot do

Typically covered: organizations, users, contacts (customers and vendors), items, taxes, currencies, chart of accounts, bank account list, estimates, sales orders, invoices, customer payments, expenses, purchase orders, custom modules and fields.

Typically NOT covered (check your tool list): bills and vendor payments, vendor credits, credit notes, manual journals, bank statement lines and matching, reconciliation, period locks, reports (P&L, balance sheet, aging, GST returns). When a task needs one of these:

- Say plainly that the connector cannot do it and name the UI path (e.g. Banking > account > Uncategorized / Reconcile, Accountant > Manual Journals, Reports > Receivables).
- Produce the evidence the user needs to do it themselves (a worklist, the figures, the proposed entry). Never fake the step with a workaround such as an expense that mimics a bill: it posts to the wrong ledger and breaks AP.

## 5. Write discipline

1. **Read before write.** Before `create_*`, search for the same record (`list_invoices` by `reference_number`/`customer_id`, `list_contacts` by name/email). Duplicates are the main source of damage.
2. **Show, then confirm.** For every create/update/delete, present customer, amounts, tax, currency and date, and wait for an explicit yes. Batch confirmation is fine for a clearly described batch.
3. **Delete is not void.** `delete_invoice`, `delete_expense`, `delete_customer_payment` remove history; refused for invoices with payments, and wrong for anything already reported to a tax authority. For a posted invoice the right action is a void or credit note in the UI. Offer that, do not delete.
4. **update_invoice replaces line items.** Always `get_invoice` first, resend every existing line with its `line_item_id`; a line sent without its id, or omitted, is removed. Same care for other `update_*` tools with arrays.
5. **Idempotency.** Zoho does not dedupe for you. Use a stable `reference_number` (source system id) on every record you create and search for it before creating. Custom invoice numbers need `ignore_auto_number_generation=true` and must be unique.
6. **Dates are yyyy-mm-dd; money is in the document currency.** If the document currency differs from the base currency supply `currency_id` and `exchange_rate`; check the org's exchange-rate policy first.
7. **Locked periods.** If the org has a transaction lock date, writes dated before it fail. Surface the error; do not backdate around it.
8. Use a trial or sandbox organization for any test. Never experiment in a live client organization.

## 6. Output habits

- State organization name, currency and the date range you queried at the top of every answer.
- Totals must reconcile: when you sum invoices, state the count and say whether you paged to the end.
- Never include customer secrets, tokens or full bank numbers in output.

## Failure modes

| Symptom | Likely cause | Action |
|---|---|---|
| Empty list, no error | Wrong organization_id, or filter too tight | Re-check org, drop filters |
| 401 after login | Wrong data centre, or scope missing | Check DC; ask admin to re-grant scope |
| 429 | Rate or daily cap | Stop, wait, narrow the query |
| "Invoice number already exists" | Custom number reused | Search by number; do not append hacks |
| Update removed lines | Omitted `line_item_id` | Restore from `get_invoice` and resend |
