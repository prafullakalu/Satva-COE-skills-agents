---
name: ar-cash-application
description: >-
  Apply incoming customer payments to open invoices and credit notes correctly: identify the payer, match remittances, handle short pays, over-pays, deductions, discounts, bulk and batched receipts, foreign-currency receipts and processor payouts, and manage unapplied cash and unidentified receipts. Use for "apply this payment", "customer paid but invoice still shows open", "unapplied cash", "short payment", "one payment for several invoices", "remittance advice", "bank deposit does not match invoices", "payment on account", "overpayment refund or credit".
metadata:
  department: "accounting"
  domain: "payables-receivables"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# AR cash application

Cash application converts a receipt in the bank into reduced receivables. Done badly it produces false overdue balances, customers chased for money they paid, and unapplied cash that hides in the control account. Done well it is the input that makes aging and collections trustworthy (`ar-aging-analysis`, `ar-collections-dunning`).

## 1. Intake and identification
For each receipt capture: bank date and value date, amount, currency, payer name as shown by the bank, bank reference, and any remittance advice (email, portal export, EDI, cheque stub). Identify the customer from, in order: remittance advice, invoice numbers in the bank reference, a known payer bank account or name alias, an amount that matches a single open invoice, then ask the customer. Never apply on name similarity alone when two customers share a name. Keep an alias table of confirmed payer names.

## 2. Matching order
1. **Remittance lists invoices**: apply to exactly those invoices.
2. **Invoice numbers in the bank reference**: apply to those.
3. **Amount equals one open invoice, or a unique sum of invoices**: propose; confirm if more than one combination fits.
4. **No reference**: apply to the oldest open item only if the customer's terms or policy say so; otherwise hold as unapplied and ask.
5. **Batch receipts** (processor payout, lockbox, one transfer for many customers): split to customers using the payout report, with fees and refunds shown separately; the bank line equals gross less fees and refunds.

Apply open credit notes to the invoices they relate to before the cash, so the net matches the remittance.

## 3. Differences between payment and invoice

| Situation | Handling |
|---|---|
| Short pay, reason known (agreed discount, withholding tax, returns) | Apply the cash; book the difference to the proper account (discount allowed, withholding tax receivable, credit note) per policy and approval; keep the invoice balance explicit |
| Short pay, reason unknown | Apply the cash; leave the remainder open; log a query to the customer; do not write off |
| Bank charges deducted by the payer's bank | Apply the full invoice; book the charge to bank charges if policy permits, else recover from the customer |
| Early-payment discount taken | Valid only if paid within the discount period and terms allow; otherwise bill the discount back |
| Over-payment | Hold as customer credit (payment on account); refund or net against the next invoice with approval; never leave it in the control account unnamed |
| Duplicate payment | Hold, confirm with the customer, refund by the same route; do not apply to unrelated invoices |
| Payment for a disputed invoice | Apply to the undisputed items first if the customer is silent; record the dispute |
| Foreign-currency receipt | Apply in the invoice currency; the difference between booked and receipt rate is realised FX gain or loss, posted separately |
| Payer is a third party or parent | Apply only on the customer's written instruction; record the relationship |

## 4. Unapplied and unidentified cash
Post unidentified receipts to a named suspense or unapplied-cash account, never to income, and do not leave them beyond the policy period (for example identify within 5 business days, escalate at 10, report at month end). Review the unapplied listing weekly; it must tie to the ledger account at close. Return funds that cannot be identified within the policy period, with approval and documentation. Do not start credit-hold or collection action on a customer who has unapplied cash.

## 5. Controls
- Cash application is separate from invoicing, credit-note approval and write-offs; the person who applies cash does not post receipts to the bank or approve write-offs.
- Reapplication or reversal of applied cash needs a reason and approval and leaves an audit trail.
- Daily bank-to-subledger tie: receipts per bank for the day equal receipts posted. Weekly review of unapplied cash and customer credit balances.
- Statements and aging go out only after the period's cash is applied.
- Watch for lapping (one customer's cash applied to another's old invoice to hide a theft): unusual reapplications, oldest-first application that skips the customer's referenced invoice, and customers who dispute balances they have paid.

## 6. Month end
Apply all cash received up to cut-off; confirm unapplied cash and customer credits show separately in the aging and tie to the control account; list receipts after cut-off for the cut-off test; clear any suspense that has since been identified.

## Output
Application schedule per receipt (receipt, customer, invoices applied with amounts, difference and its treatment, status); unapplied and unidentified list with age and owner; queries to customers; draft entries for discounts, charges and FX. Entries are drafts until approved.

## Do not
- Apply cash to the oldest invoice by default when the remittance names another.
- Write off a short pay without authority and evidence.
- Book unidentified receipts to income.
- Net a customer credit against an invoice without saying so.
