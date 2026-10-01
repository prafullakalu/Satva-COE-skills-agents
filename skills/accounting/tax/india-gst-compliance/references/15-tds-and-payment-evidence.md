# Payment evidence: income-tax TDS, and who actually paid

LAST_VERIFIED: 2026-07-29

Two things that come up constantly when reconciling a small business's GST against
its bank statement, and that neither the portal nor a purely GST-focused workflow
will tell you about.

## Contents

- [TDS on your receipts](#tds-on-your-receipts)
- [GST TDS is a different thing](#gst-tds-is-a-different-thing)
- [Expenses paid from a personal account](#expenses-paid-from-a-personal-account)
- [Reconciling the bank statement](#reconciling-the-bank-statement)

## TDS on your receipts

A B2B customer paying an invoice for services will usually withhold income-tax TDS
— commonly 10% under §194J for professional or technical services, 2% under §194C
for contract work, 5% under §194H for commission. The bank receipt is therefore
**smaller than the invoice**, and it is easy to reconcile the wrong figure.

**GST is payable on the full taxable value regardless.** TDS is the customer's
income-tax obligation on your income; it has nothing to do with your GST liability.
A receipt short by 10% does not reduce output tax by anything.

The identity to reconcile against:

```
  Invoice taxable value
+ GST (IGST, or CGST + SGST)
= Invoice gross
− income-tax TDS  (computed on the TAXABLE VALUE, not on the gross)
± rounding
= amount actually credited to the bank
```

**TDS is deducted on the taxable value, excluding GST**, provided the GST is shown
separately on the invoice (CBDT Circular 23/2017). If a customer has deducted on
the gross including GST, they have over-deducted — worth telling them, since it is
their compliance issue and your cash.

### Worked example

Invoice for ₹1,00,000 plus 18% IGST, customer deducts 10% under §194J:

| | ₹ |
|---|---|
| Taxable value | 1,00,000 |
| IGST @ 18% | 18,000 |
| Invoice gross | 1,18,000 |
| Less TDS @ 10% of 1,00,000 | (10,000) |
| **Bank receipt** | **1,08,000** |

GSTR-1 and GSTR-3B report **1,00,000** taxable and **18,000** IGST. The ₹10,000 is
an asset — TDS receivable — not a discount, not a bad debt, and not a reason to
issue a credit note.

### What to track

For every receipt short of the invoice gross:

- **TDS receivable** in the books, by customer and section.
- **Form 16A** expected from the customer, quarterly.
- **Form 26AS / AIS** — verify the credit actually appears. A customer who deducted
  but did not deposit or did not file their TDS return leaves you unable to claim
  it, and you only find out by checking.
- Any residual difference after TDS, which is usually rounding or a bank charge and
  occasionally a short payment worth chasing.

If the deducted amount does not reconcile to a standard rate on the taxable value,
say so rather than plugging the difference — an unexplained shortfall is more often
a short payment than an unusual TDS rate.

## GST TDS is a different thing

Do not confuse the above with **GST TDS under §51**: 2% deducted by government
departments, local authorities and certain notified bodies on contracts above
₹2.5 lakh, reported by them in **GSTR-7**, and appearing in your electronic cash
ledger once they file. There is also the 2% deduction on metal scrap supplies
between registered persons.

GST TDS credits your **cash ledger** and can be used to pay GST. Income-tax TDS
credits your **income-tax** account and cannot. Both can appear on the same
transaction. Keep them in separate columns in the working paper, because
accidentally treating income-tax TDS as available cash is a real way to be short
at the payment step.

## Expenses paid from a personal account

Small businesses, especially partnerships and LLPs early on, routinely pay vendors
from a partner's personal account. The instinct to disallow these is wrong.

**The bank account the money came from does not determine ITC eligibility.** What
matters is:

1. **The tax invoice is addressed to the registered business**, with its correct
   GSTIN. If the invoice is in the partner's personal name, there is no ITC — the
   supply was not made to the registered person. This is the actual test, and it is
   the one to check first.
2. **The supply is for business use**, and not blocked under §17(5).
3. **It appears in GSTR-2B** and the other §16(2) conditions are met.
4. **The supplier is paid within 180 days** — Rule 37 runs from the invoice date and
   is indifferent to which account paid. Payment by a partner on the business's
   behalf still counts as payment to the supplier.

So the accounting treatment, not the eligibility, is what changes:

- Record the expense and the ITC in the business books as normal.
- Record a corresponding **payable to the partner** (partner's current account, or
  a reimbursement liability). The business owes them the money.
- If it is not going to be reimbursed, it is a **capital contribution** — say so
  explicitly rather than leaving it as a floating credit balance nobody understands
  a year later.
- Keep the personal bank evidence with the invoice. It is the proof of payment for
  Rule 37 and the first thing an officer asks about when the business account shows
  no corresponding debit.

`scripts/ims_triage.py` carries a `paid_from` column through from the payments CSV
for exactly this reason: the payment is *traced*, and the source is recorded, but a
personal source never downgrades the recommendation on its own.

What genuinely does disqualify it: an invoice in the individual's name, a personal
expense run through the business, or anything blocked under §17(5). Those are
substance problems, not account-number problems.

## Reconciling the bank statement

When the bank statement is the starting point — common when the books are thin —
work outward from it rather than treating it as the answer.

**Receipts.** For each credit: which invoice, and does the difference equal TDS at
a standard rate on the taxable value? Advances received for services are taxable on
receipt even with no invoice yet. A receipt with no invoice at all is either an
advance, a loan, a capital introduction or an unbilled supply — and only the last
one is a GST problem, so identify which.

**Payments.** For each debit: which purchase invoice? Feed these into
`ims_triage.py --payments` so IMS records without a local invoice can be separated
into "paid, so it is probably genuine and the document is just missing" and "no
trace at all, verify before accepting".

**What the bank cannot tell you.** Non-cash supplies leave no bank trace at all and
are still taxable: barter, related-party supplies without consideration under
Schedule I, branch transfers across states, free samples, recoveries adjusted
against payables. A bank-led reconciliation will silently miss every one of them,
so it is a cross-check on the registers, never a substitute for them.
