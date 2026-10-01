---
name: xero-invoices-and-collections
description: >-
  Accounts receivable in Xero via the Satva Xero MCP: building an overdue and ageing list, drafting sales invoices
  and credit notes, recording customer payments, applying prepayments/overpayments, emailing invoices, and collection
  follow-up lists. Use for "overdue invoices in Xero", "who owes us money", "create an invoice in Xero", "record
  this customer payment", "apply a credit note", "send the invoice", "chase list", "aged receivables".
metadata:
  department: "accounting"
  domain: "accounts-receivable"
  platform: "xero"
  owner: "satva-coe"
  status: "stable"
  license: "Satva-original"
  source: "original"
---

# Xero invoices and collections (AR)

Follow `xero-mcp-operating-rules`. Sales invoices are `type=ACCREC`.

## Tools used

Read: `list-invoices`, `get-invoice`, `list-contacts`, `list-aged-receivables-by-contact`, `list-payments`,
`list-credit-notes`, `list-overpayments`, `list-prepayments`, `list-repeating-invoices`, `get-invoice-reminders-settings`,
`list-history`, `list-items`, `list-accounts`, `list-tax-rates`, `list-tracking-categories`, `list-quotes`.
Write: `create-invoice`, `update-invoice`, `create-credit-note`, `update-credit-note`, `create-payment`,
`allocate-overpayment`, `allocate-prepayment`, `email-invoice`, `void-invoice`, `void-credit-note`, `create-quote`.

## A. Overdue and ageing analysis

1. `list-invoices page=1..n` (pageSize 100). There is no status or date filter, so page the full set and filter
   yourself: `Type=ACCREC`, `Status=AUTHORISED`, `Amount Due > 0`.
2. Compute days overdue from `Due Date` to the as-at date (state the as-at date). Buckets: current, 1-30, 31-60,
   61-90, 90+. Sum `Amount Due` per bucket and per contact. Totals in the invoice's currency; do not add different
   currencies without a conversion rule (`xero-multi-currency`).
3. For a single customer's authoritative ageing use `list-aged-receivables-by-contact contactId reportDate`. It is
   per contact only; there is no organisation-wide aged receivables tool, so reconcile your computed total to the
   Accounts Receivable line of the balance sheet (`list-report-balance-sheet`). A gap means credit notes, unallocated
   overpayments/prepayments or a date mismatch; investigate before presenting.
4. Check for credits that offset: `list-credit-notes contactId`, `list-overpayments`, `list-prepayments` with
   remaining balances for the same contact. Present net exposure, not just gross.
5. Rank by risk: amount x age, repeat late payers, no recent payment (`list-payments`).

## B. Create a sales invoice

1. Confirm customer exists: `list-contacts searchTerm=<name>`; handle duplicates (`xero-contacts-cleanup`).
2. Gather per line: description, quantity, unitAmount, `accountCode` (revenue account from `list-accounts`),
   `taxType` (from `list-tax-rates`; use the customer's `AR Tax Type` as a hint, not a rule), optional `itemCode`,
   tracking (max 2 categories, only when asked; see `xero-tracking-categories`).
3. Present the invoice for approval: customer, date, reference, each line, subtotal, tax, total.
4. `create-invoice contactId type=ACCREC lineItems date reference`. Result is a **DRAFT**. The tool has no
   currency, due-date, or status parameter: the due date follows the contact's payment terms, the currency follows
   the contact default. If either is wrong, tell the user; do not guess a workaround.
5. The MCP cannot authorise a draft. Hand back the deep link and ask a user to Approve in Xero. Only then can
   `email-invoice` and `create-payment` work.
6. `update-invoice` only changes drafts and replaces all lines. Re-send every line, with tracking, or they are lost.

## C. Record a customer payment

1. Confirm invoice status is AUTHORISED and `Amount Due` (`get-invoice`).
2. Pay to a bank account marked "enable payments"; `accountId` is that account's ID.
3. Amount must be positive and <= amount due. Overpaid cash: record the invoice amount via `create-payment`, and
   put the excess in Xero as an overpayment (not possible through `create-payment`; needs a bank RECEIVE or UI).
4. After writing, check the invoice shows the new `Amount Paid` and the right status.
5. Wrong payment: `delete-payment` (irreversible; reopens the balance). Confirm by payment ID first.
6. Check the money is not also already entered as a RECEIVE bank transaction (double-count risk; see
   `xero-bank-reconciliation-review`).

## D. Credit notes and allocations

- `create-credit-note contactId lineItems reference` makes a DRAFT; a user authorises it in Xero.
- Apply credit to an invoice: authorised credit notes are allocated in Xero; for overpayments and prepayments use
  `allocate-overpayment` / `allocate-prepayment` with `allocations[{invoiceID, amount}]`. Total <= remaining credit,
  each <= invoice amount due.
- Wrong credit note: `void-credit-note` (VOIDED only from AUTHORISED; DELETED from DRAFT/SUBMITTED). Irreversible.

## E. Chasing

1. `email-invoice invoiceId` re-sends Xero's standard invoice email only; no custom text, no cc. Confirm the contact's
   email address on the contact record first (`list-contacts`).
2. Xero's automatic reminders are configured in Xero; read with `get-invoice-reminders-settings`.
3. Produce a chase list rather than sending in bulk: customer, invoices, amount, days overdue, last payment, last
   contact (`list-history entityType=invoices entityId`), proposed action. Let a human send messages.
4. Recurring bills to customers: `list-repeating-invoices` shows templates, `create-repeating-invoice` creates one
   (status DRAFT or AUTHORISED for generated invoices; AUTHORISED generates live invoices automatically, so
   confirm explicitly).

## Pitfalls

- `list-invoices` includes ACCPAY bills in the same list; always filter `Type`.
- `Amount Due` may be omitted when zero; treat missing as 0, not unknown.
- A DRAFT or SUBMITTED invoice is not a receivable. Exclude from ageing, list separately as "unapproved".
- Dates are from Xero (UTC-based); report as-at date explicitly.
- A voided or deleted invoice is irreversible; prefer a credit note if the invoice was already sent.
- Locked period: invoices dated on/before the lock date are rejected. Do not shift the date silently.
- Do not email an invoice that has not been approved or whose contact has no valid email.

## Output format

```
Org | as-at | scope (all customers / <name>)
Ageing table: bucket | # invoices | amount | % of total   (base currency, or per currency)
Reconciliation: computed AR <x> vs balance sheet AR <y> difference <d> (explained: ...)
Top exposures: customer | amount | oldest days | credits available | action
Proposed writes (none executed): ...
```
