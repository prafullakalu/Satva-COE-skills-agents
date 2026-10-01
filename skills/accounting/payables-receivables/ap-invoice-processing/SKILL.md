---
name: ap-invoice-processing
description: >-
  Process supplier invoices through accounts payable: intake, validation, duplicate and fraud checks, coding, approval routing, scheduling and payment-run preparation with segregation of duties. Use for "enter this bill", "process vendor invoices", "AP workflow", "what bills are due", "prepare a payment run", "duplicate invoice", or "bill approval".
metadata:
  department: "accounting"
  domain: "ap-ar"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# AP invoice processing

Accounts payable converts a supplier's claim into a validated liability and then into a controlled payment. The two failure modes are paying something wrong (duplicate, fictitious, overpriced) and not recording something owed (cut-off).

## 1. Intake

Single channel preferred (a dedicated AP mailbox or intake queue). Log each document on receipt: date received, supplier, document number, amount. Date received matters for payment terms and cut-off. Extract fields per `receipt-ocr-intake`.

## 2. Validation checklist (reject or hold on failure)

1. **Is it a valid invoice?** Supplier name, tax ID where required, document number, date, itemised lines, tax shown, remit-to details. Statements and reminders are not invoices.
2. **Known vendor?** Match to the vendor master (see `vendor-setup-and-1099-data`). New vendor: stop, run vendor setup first.
3. **Bank details match master?** A change in bank account on an invoice is a classic fraud pattern: confirm by calling a known number on file, never a number on the invoice or email.
4. **Duplicate?** Test vendor plus invoice number (normalised: strip spaces, zeros, case), vendor plus amount plus date, and amount plus date across vendors for repeated billing under different names.
5. **Authorised?** There is a PO, contract, or named budget owner who confirms the goods or services were received. See `ap-three-way-match` when POs are used.
6. **Arithmetic and tax right?** Lines sum, tax rate correct for the supply, reverse-charge or withholding tax applied where required.
7. **Period and cut-off**: service period determines expense period; invoices for next period go to prepaid, see `accruals-deferrals-prepaids`.
8. **Currency and terms** agree with the contract; early-payment discounts noted.

## 3. Coding

Expense account by nature, department or project dimension, tax code from the tax rates configured in the ledger (do not invent). Capital items go to fixed assets. Related-party or unusual supplier flags noted.

Entry on approval:

```
Dr Expense or Asset (net)      1,000
Dr Input tax recoverable         200
  Cr Accounts payable                1,200
```

## 4. Approval matrix

Define limits by amount and category: budget owner approves the business need, finance approves coding and tax, a higher authority approves above threshold. The person who enters a bill does not approve it, and neither of them releases payment. Approval evidence (who, when) is retained with the bill. Where the team is small, the owner approves everything above a stated amount and reviews the payment list.

## 5. Payment scheduling

- Pay on due date, not on receipt, unless an early-payment discount exceeds the cost of capital (a 2 percent discount for 20 days earlier is roughly 36 percent annualised: take it).
- Build the payment run from approved, unpaid bills due within the run window; exclude bills on hold, in dispute, or with unresolved vendor details.
- Review before release: total, count, largest items, new or changed bank details since last run, vendors with debit balances or unapplied credits (apply credits first), duplicate check across the run.
- Release requires a second person (or bank dual authorisation). Prepare the run as a draft and wait for approval; never release payments in the same step as preparing them.
- After payment: record payment against each bill, send remittance advice, retain bank confirmation.

## 6. Exceptions

Disputed items: hold the disputed amount, pay the undisputed part, log the dispute with owner and date. Credit notes: apply against open bills or request refund; do not leave unapplied. Missing invoices for received goods: accrue (`accruals-deferrals-prepaids`).

## 7. Monthly reviews

AP aging tied to the ledger control account (`subledger-to-gl-reconciliation`); unusual vendors (new, one-off, round amounts, just under approval limits); payments after period end for cut-off; vendors paid but not in the master; Benford or round-sum scan for splits just under limits.

## Output

For an invoice batch: validated table (vendor, number, date, amount, tax, coding, approval route, issues). For a payment run: draft schedule (vendor, bill, amount, due, discount, bank change flag) with totals and the exception list.

## Do not

- Pay from a statement or an emailed copy without checking the original in the system.
- Change vendor bank details on the strength of an email.
- Let one person create the vendor, enter the bill and release payment.
- Pay duplicates "to keep the supplier happy"; recover them via credit.
