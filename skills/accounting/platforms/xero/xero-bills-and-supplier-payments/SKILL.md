---
name: xero-bills-and-supplier-payments
description: >-
  Accounts payable in Xero via the Satva Xero MCP: reviewing unpaid bills, drafting supplier bills, purchase orders,
  recording supplier payments and batch payments, supplier credit notes, duplicate-bill detection and a payment-run
  proposal. Use for "bills due in Xero", "create a bill", "supplier payment run", "batch payment", "purchase order",
  "duplicate supplier invoice", "what do we owe", "aged payables".
metadata:
  department: "accounting"
  domain: "accounts-payable"
  platform: "xero"
  owner: "satva-coe"
  status: "stable"
  license: "Satva-original"
  source: "original"
---

# Xero bills and supplier payments (AP)

Follow `xero-mcp-operating-rules`. Bills are invoices with `type=ACCPAY`.

## Tools used

Read: `list-invoices`, `get-invoice`, `list-contacts`, `list-aged-payables-by-contact`, `list-payments`,
`list-batch-payments`, `list-credit-notes`, `list-purchase-orders`, `get-purchase-order`, `list-history`,
`list-attachments`, `list-accounts`, `list-tax-rates`.
Write: `create-invoice` (type ACCPAY), `update-invoice`, `create-purchase-order`, `update-purchase-order`,
`create-credit-note`, `create-payment`, `create-batch-payment`, `delete-batch-payment`, `delete-payment`,
`upload-attachment`, `void-invoice`.

## A. What do we owe (payables position)

1. `list-invoices` all pages; filter `Type=ACCPAY`, `Status=AUTHORISED`, `Amount Due > 0`. (No server-side filter.)
2. Bucket by due date: overdue, due 0-7, 8-14, 15-30, later. Show per supplier and in total.
3. Per-supplier authority: `list-aged-payables-by-contact contactId reportDate`. There is no organisation-wide aged
   payables tool; tie your computed total to Accounts Payable on the balance sheet (`list-report-balance-sheet`) and
   explain any gap (supplier credits, prepayments, draft/awaiting approval bills excluded).
4. Separate "Awaiting approval" (DRAFT/SUBMITTED) from "approved to pay" so nothing unapproved enters a payment run.

## B. Duplicate bill detection (do this before every payment run)

Candidate duplicates: same supplier + same total (or within 1%) + dates within 30 days; or same supplier +
same `Reference`/invoice number after stripping spaces, dashes and leading zeros; or same total + near dates across two
supplier records that look alike (`xero-contacts-cleanup`). List them as pairs with IDs and statuses; the user decides.
Never void a bill because it "looks" duplicated: check `list-history` and attachments first.

## C. Enter a supplier bill

1. Supplier from `list-contacts searchTerm`; if absent, ask before `create-contact`.
2. Lines: description, quantity, unitAmount, expense `accountCode`, `taxType` (input tax type from
   `list-tax-rates`; check the contact's `AP Tax Type`), tracking if the business uses it.
3. Verify the arithmetic against the supplier document: subtotal + tax = total. Xero computes tax from the tax type
   on the line; a mismatch of a few cents means the wrong tax rate or `INCLUSIVE/EXCLUSIVE` assumption. The
   `create-invoice` tool does not expose `lineAmountTypes`, so amounts are tax-exclusive; convert tax-inclusive
   documents before sending.
4. Show the bill for approval, then `create-invoice type=ACCPAY contactId lineItems date reference`. Use the supplier's
   own invoice number as `reference` so duplicate checks work later. Result is DRAFT: a user approves it in Xero.
5. Attach the source document with `upload-attachment entityType=invoices entityId fileName base64Content`
   (max 1 MB; needs the attachments scope). Same file name replaces the existing attachment.

## D. Purchase orders

`create-purchase-order contactId lineItems date deliveryDate reference status` (DRAFT by default). Status can move
DRAFT -> SUBMITTED -> AUTHORISED (or DELETED to cancel a draft) via `update-purchase-order`; fields other than
status only change while DRAFT. `list-purchase-orders status dateFrom dateTo page` finds open (AUTHORISED) orders;
BILLED means converted. Match PO to bill (quantity/price/tax) before approving a bill.

## E. Pay suppliers

1. Choose only approved bills: AUTHORISED, `Amount Due > 0`. Confirm the paying bank account (`list-accounts`,
   Type=BANK, "payments enabled").
2. Check available cash with `list-report-bank-summary` (closing balance) before proposing a run; propose a run
   total and a deferred list.
3. Single payment: `create-payment invoiceId accountId amount date reference`.
4. One bank debit covering several bills: `create-batch-payment accountId date payments[{invoiceID, amount,
   reference}]`. Each bill must be AUTHORISED and not fully paid. Total = sum of amounts. Recheck the sum with the
   user before sending.
5. Supplier credit notes: `list-credit-notes contactId` first; apply credits in Xero before paying, or the supplier is
   overpaid.
6. Reversal: `delete-batch-payment` / `delete-payment` are irreversible and reopen the bills; confirm by ID.
7. This MCP records payments; it does not move money. Actual bank payment happens in the bank or via a payment file
   outside this server.

## Pitfalls

- A paid-looking bill with an unreconciled payment is common; reconcile before declaring it settled
  (`xero-bank-reconciliation-review`).
- Foreign-currency bills: amount due is in the bill currency; payment must be in that currency account or Xero
  books an FX difference (`xero-multi-currency`).
- Approving then paying a bill with no attachment/PO is a control gap: list bills over a threshold with no
  attachment (`list-attachments`) for review.
- Bill dates on/before the period lock date are rejected.
- `update-invoice` replaces all lines; re-send them all.
- Statuses: only AUTHORISED bills can be paid. DRAFT/SUBMITTED cannot.

## Output format

```
Org | as-at | scope
Payables: bucket | # bills | amount ; reconciled to AP <x> vs <y> diff <d>
Possible duplicates: pair | supplier | amount | dates | evidence
Proposed payment run: supplier | bill ref | due | amount | account ; run total vs available cash
Not yet approved (excluded): ...
Writes executed: ID/link per record
```
