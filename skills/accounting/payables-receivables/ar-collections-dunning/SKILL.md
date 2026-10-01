---
name: ar-collections-dunning
description: >-
  Run accounts receivable collections: prioritise overdue customers, sequence reminder and escalation messages, handle disputes, promises to pay, payment plans and write-offs, with drafts approved before anything is sent. Use for "chase overdue invoices", "dunning", "payment reminders", "collections plan", "customer is not paying", "write off a bad debt", or "credit hold".
metadata:
  department: "accounting"
  domain: "ap-ar"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# AR collections and dunning

Collections is cash acceleration with the customer relationship intact. Work from the aging (`ar-aging-analysis`), spend effort where value and risk are highest, and keep every contact on record. All outbound messages are drafts until the owner approves them.

## 1. Before contacting anyone

1. Confirm the invoice is correct and delivered: right customer, amount, tax, PO number, due date, terms, and proof of delivery or service completion.
2. Check for unapplied payments, credits and disputes. Chasing a customer who already paid, or who holds an open credit note, damages the relationship and costs time.
3. Confirm the customer's contact for payables (not the project sponsor), and the preferred remittance method.
4. Check promises already made (promise-to-pay dates) and prior communications.

## 2. Prioritise

Rank by expected recovery value: amount overdue times collection risk, weighted by age and customer history. Typical order: large and moderately overdue first; very old small balances batch; disputed items by owner of the dispute; customers near credit limit or on stop-supply watch; chronic late payers by pattern.

## 3. Sequence (adjust to terms and relationship)

| Stage | Timing | Channel and tone |
|---|---|---|
| Pre-due courtesy | 3 to 5 days before due (large or new customers) | Email: invoice attached, due date, remit details |
| Day 1 to 7 overdue | Light | Email: "may have been missed", invoice copy, payment link |
| Day 8 to 21 | Firm | Email plus phone to the payables contact; ask for a payment date |
| Day 22 to 45 | Escalation | Named senior contact, statement of account, state the consequence (late fee per contract, credit hold) |
| Day 46 to 90 | Formal | Formal demand letter, hold new orders per credit policy, discuss a payment plan |
| 90 plus | Recovery decision | Collection agency, legal, or provision and write-off, per policy and amount |

Never threaten an action the business will not or cannot take, and keep language consistent with consumer or commercial debt rules in the jurisdiction (contact hours, frequency and conduct rules are stricter for consumers).

## 4. Drafting a message

Include: customer name, invoice number(s), amounts, due dates, days overdue, one clear ask (pay by a date, or tell us why not), how to pay, a copy of the invoice, and a named contact. Short, factual, courteous. Do not include other customers' data. Do not say "final notice" until it is.

## 5. Outcomes

- **Promise to pay**: record date, amount and who promised. If missed, escalate at once; a broken promise moves one stage up.
- **Dispute**: log reason (price, quantity, quality, not received, duplicate, no PO), owner and target date. Resolve with the right team, then issue a credit note or confirm the invoice. Collect the undisputed portion meanwhile.
- **Payment plan**: written, with dates and amounts; the first instalment is a test of intent. Missed instalment accelerates the balance.
- **Cannot pay**: assess solvency signals (late payments across vendors, returned payments); consider credit hold, partial prepayment or security.
- **Wrong payee or unidentified payment**: apply cash only when identified; otherwise hold in unapplied cash and ask.

## 6. Bad debt

Allowance (provision) for expected losses: an aging-based percentage method or specific identification. Example (policy percentages are illustrative, set per client):

```
Provision entry:    Dr Bad debt expense  X    Cr Allowance for doubtful accounts  X
Write-off:          Dr Allowance         Y    Cr Accounts receivable (customer)   Y
Recovery later:     Dr Accounts receivable   Cr Allowance  (reinstate), then Dr Bank  Cr Accounts receivable
```

Tax relief on bad debts and VAT/GST bad-debt relief have conditions and time limits that vary by jurisdiction; confirm them before writing off. Write-offs above a threshold need approval by someone other than the collector, and the write-off is recorded with evidence of collection effort.

## 7. Controls

Collectors cannot post cash receipts or credit notes alone; the person who approves write-offs is not the person who chases. Log every contact (date, who, outcome). Review disputed and promised items weekly.

## Output

Prioritised call list (customer, overdue amount, oldest item, stage, next action, owner), draft messages, a dispute and promise-to-pay log, write-off and provision proposals for approval. Nothing is sent or posted until approved.

## Do not

- Send reminders without checking cash application and credits.
- Contact anyone other than the agreed payables contact without cause.
- Offer discounts or write-offs without authority.
- Disclose another customer's balance.
- Treat a disputed invoice as collectable on the normal timeline.
