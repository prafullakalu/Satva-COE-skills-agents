---
name: qbo-bills-and-vendor-payments
description: >-
  Run accounts payable in QuickBooks Online: enter and correct bills, vendor credits and expenses, build a payment run from the due-bills worklist, record bill payments (check, bank transfer, credit card), spot duplicate bills, and handle 1099 vendors. Use when asked to "enter this bill in QuickBooks", "what do we owe this week", "pay these vendors", "payment run", "duplicate bill check", "vendor credit", "bill vs expense in QBO", or "vendor balance is wrong".
metadata:
  department: "accounting"
  domain: "accounts-payable"
  platform: "quickbooks"
  owner: "satva-coe"
  status: "stable"
  license: "Satva-original"
  source: "original"
---

# QuickBooks bills and vendor payments

Follow `qbo-mcp-operating-rules`. Paying a vendor moves real money in the user's bank only if they release it elsewhere; the MCP records the payment in the books. Say that plainly: recording a bill payment does not send funds.

## Bill, expense, or check? (pick before you post)
| Situation | Record as | Entity |
|---|---|---|
| Vendor invoice received, paid later | Bill, then Bill Payment | `Bill`, `BillPayment` |
| Paid immediately by card, cash or debit | Expense | `Purchase` with `PaymentType` Cash or CreditCard |
| Paid immediately by cheque | Cheque | `Purchase` with `PaymentType: "Check"` |
| Vendor refunds or credits you | Vendor credit | `VendorCredit` |
| Goods ordered, not yet received or billed | Purchase order | `PurchaseOrder` (non-posting) |
Bills credit Accounts Payable on the bill date; expenses and cheques do not touch A/P at all. Entering the same invoice as both a bill and an expense is the most common duplicate.

## A. Payment run (read-only prep)
1. `ap_due_bills_worklist` (`asOf`, `limit`): open bills ordered by due date, bucketed overdue, 0-7, 8-14, 15-30, later, with per-vendor totals (reads up to 1000 open bills; honour the `truncated` flag).
2. Cross-check total with `get_aged_payables` at the same `report_date`. A difference points to unapplied vendor credits, bill payments not linked to bills, or journal entries posted to Accounts Payable.
3. `cash_position` to see bank and card balances against payables due within the horizon (`horizonDays`). It shows net position = cash - card debt + AR due - AP due. Flag if AP due exceeds cash.
4. For each vendor to pay, `vendor_360` (by `vendorId` or `name`): open and overdue bills, recent payments, 12-month spend (Bills only), vendor credits. Apply credits before paying.
5. Propose the run: vendor, bills, amounts, pay-by date, source bank account. Prioritise: statutory (tax, payroll), late fees and supplier holds, early-payment discounts (if terms give 2/10 net 30 and cash allows), then oldest first. Get the user's approval of the list.

## B. Enter a bill
1. Vendor: `query_quickbooks` `SELECT Id, DisplayName, Vendor1099, Active FROM Vendor WHERE DisplayName LIKE '%name%'`. Create only if none and `find_duplicates` `kind: "vendors"` shows no look-alike. Set `Vendor1099: true` for US contractors paid for services.
2. Duplicate check: `find_duplicates` `kind: "bills"` (same vendor and amount within `windowDays`, or repeated DocNumber per vendor) and `query_quickbooks` `SELECT Id, TxnDate, TotalAmt FROM Bill WHERE VendorRef = '<id>' AND DocNumber = '<invoice no>'`.
3. Show the draft: vendor, invoice number (put the vendor's invoice number in `DocNumber`), bill date, due date (from terms), each line with account (or item), amount, class/location, tax code, memo.
4. `create_entity` `Bill` (`VendorRef`, `Line[]` of `AccountBasedExpenseLineDetail` with `AccountRef` and `Amount`, or `ItemBasedExpenseLineDetail` for inventory items) or `create-bill` (`bill.VendorRef`, `bill.DueDate`, lines; note the hyphen). Do not send `TotalAmt` or `Balance`: QBO calculates them. A duplicate `DocNumber` for the same vendor is rejected unless `include=allowduplicatedocnum`; treat that error as a possible duplicate and investigate, not as something to force.
5. Attach the source document: `upload_attachment` (`contentBase64`, `contentType` pdf/png/jpeg/..., `attachTo: [{type:"Bill", id}]`, max 10 MB).
6. Read back with `get_entity` and report id, total, due date, `qboLink`.

Coding rules: expense account from the vendor's usual history (last 3 bills via query); prepaids (insurance, annual software) go to a prepaid asset, not expense; capital items above the capitalisation threshold go to fixed assets; sales tax or VAT on purchases per `qbo-sales-tax`.

## C. Correct or remove a bill
- Not paid, wrong coding or amount: `update_entity` `Bill` (full-update entity: the tool merges your patch into the whole object). Send the complete `Line` array if you change lines.
- Paid: reverse via the bill payment first, or leave the bill and book a `VendorCredit` for the difference.
- Wrong vendor: do not change `VendorRef` on a paid bill. Void the payment flow, or journal the correction with the correct vendor on the A/P line (an A/P journal line must name a vendor).
- `delete_entity` removes a bill permanently. Use only for an unpaid duplicate. Bills already included in a filed 1099 or tax return are never deleted.

## D. Record a payment
1. Confirm bill Ids and open balances (`query_quickbooks` `SELECT Id, Balance, VendorRef FROM Bill WHERE Id IN (...)`).
2. Build the `BillPayment` body: `VendorRef`, `PayType` (`Check` with `CheckPayment.BankAccountRef`, or `CreditCard` with `CreditCardPayment.CCAccountRef`), `TotalAmt`, and `Line[]` each with `Amount` and `LinkedTxn: [{TxnId, TxnType: "Bill"}]`. Include applied vendor credits as `LinkedTxn` with `TxnType: "VendorCredit"` so the total is net.
3. Show it with the bank account, date and reference number. Get approval. `create_entity` `BillPayment` (or `create_bill_payment`).
4. Read back the bill: `Balance` should be 0 or the expected remainder.
5. A payment sent by online banking is recorded here, then matched to the bank-feed line later (see `qbo-bank-reconciliation-review`); if the feed line was already added as an expense, you will create a duplicate. Check the feed first with the user.
6. Mistaken payment: reverse the payment (delete it if unreconciled; otherwise reverse via journal or vendor credit). `void_bill_payment` is not provided by this server.

## E. Vendor credits and refunds
`create_entity` `VendorCredit` (`VendorRef`, lines). Apply it by including it in a `BillPayment` as above. If the vendor refunds cash instead, record a `Deposit` with a line to the vendor account (`DepositLineDetail` with `Entity` = the vendor and the `AccountRef` of the original expense or Accounts Payable per the user's accountant), not income.

## Pitfalls
- Foreign currency vendors: the bill is in the vendor's currency; bank payment in another currency produces a realised gain or loss. See `qbo-multi-currency`.
- Billable expenses: lines with `CustomerRef` and `BillableStatus: "Billable"` flow to the customer's next invoice; check before deleting.
- Vendors and customers share one name space: a vendor and a customer with the same DisplayName must be named differently.
- 1099 reporting depends on the `Vendor1099` flag and the payment method (card payments are excluded from 1099-NEC); confirm before year end rather than at filing.
- `vendor_360` spend counts Bills only; direct expenses and cheques are not in it.

## Output
Payment run: table of vendors and bills with amounts, due, proposed pay date, net of credits, total, and cash available. Entry: before/after, ids, links, remaining balance.
