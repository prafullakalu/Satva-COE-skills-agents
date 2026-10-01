---
name: accruals-deferrals-prepaids
description: >-
  Calculate and book month-end accruals, deferrals, prepaid expense amortisation and accrued revenue under accrual accounting, with schedules, reversal logic and a completeness search. Use for "month-end accruals", "unrecorded liabilities", "prepaid schedule", "amortise insurance or software", "accrue bonus or utilities", "deferred expense", or "search for unrecorded liabilities".
metadata:
  department: "accounting"
  domain: "journal-entries"
  owner: "satva-coe"
  status: "beta"
  license: "Apache-2.0"
  source: "https://github.com/anthropics/knowledge-work-plugins/tree/main/finance/skills/journal-entry-prep"
---

<!-- Satva original, extended with references adapted from anthropics/knowledge-work-plugins finance/skills/journal-entry-prep (Apache-2.0). Modified by Satva: condensed into references/standard-entry-patterns.md. -->

# Accruals, deferrals and prepaids

Matching principle: expense belongs to the period that received the benefit, revenue to the period it was earned, regardless of when cash moves. Four patterns:

| Pattern | Cash vs recognition | Balance sheet account | Entry at recognition |
|---|---|---|---|
| Accrued expense | Expense first, cash later | Accrued liability | Dr Expense, Cr Accrued liability |
| Prepaid expense | Cash first, expense later | Prepaid asset | Dr Expense, Cr Prepaid asset |
| Accrued revenue | Earned first, billed later | Contract or accrued asset | Dr Accrued revenue, Cr Revenue |
| Deferred revenue | Cash first, earned later | Contract liability | Dr Deferred revenue, Cr Revenue |

(Revenue recognition judgements for contracts belong to a separate revenue skill; this covers routine mechanics.)

## 1. Set materiality for the exercise

Agree a threshold below which items are expensed as paid (for example any prepaid under a stated amount, or an accrual under a stated amount), applied consistently and recorded in the client file. Below it, do not create schedules.

## 2. Accruals: find unrecorded liabilities

Cut-off test. For the period just ended:

1. Review all payments and bills dated in the first weeks after period end; for each, ask what period the goods or services belong to.
2. Review goods-received-not-invoiced and open purchase orders (see `ap-three-way-match`).
3. Recurring items billed in arrears: utilities, rent escalations, telecoms, payroll and related taxes, bonuses and commissions, holiday pay, interest on loans, professional fees (ask for work-in-progress), contractor hours.
4. Compare to the same month in prior periods: a recurring expense with no posting this month is a candidate.
5. Ask budget owners for committed-but-unbilled spend above the threshold.

Measure at best estimate: quote, contract rate times units, or last actual with the change explained. Show the calculation.

```
Dr Utilities expense   1,850
  Cr Accrued liabilities     1,850     (dated period end, auto-reverse day 1 next period)
```

## 3. Prepaids: schedule

For each prepaid above threshold keep a schedule row: vendor, description, payment date, service start, service end, total, months, monthly amount, balance. Straight-line by default, daily proration if the start date is mid-month and material.

```
Annual software 6,000 paid 1 Mar, term 1 Mar to 28 Feb.   Monthly 500.
On payment:      Dr Prepaid software 6,000  Cr Bank 6,000
Each month end:  Dr Software expense 500    Cr Prepaid software 500
```

Control: sum of schedule balances must equal the prepaid account balance at every close (a reconciliation, see `subledger-to-gl-reconciliation`). Terminate or write off the remainder if a contract is cancelled.

## 4. Accrued and deferred revenue (routine cases)

- Billed in advance (subscriptions, retainers, deposits): credit deferred revenue; release monthly over the service term.
- Work done not yet invoiced (time and materials, milestones achieved): accrue revenue at billable value with support (timesheets, signed milestone); reverse when the invoice is issued.
- Customer deposits for goods not yet delivered are liabilities, not revenue.

## 5. Reversal logic

- Accruals for expected invoices: auto-reverse on day one of next period; the real bill then posts to expense normally. Check after reversal that nothing is left behind (a reversed accrual with no bill means the bill is still missing; a bill with no reversal means double expense).
- Prepaid and deferral releases are permanent, not reversing.

## 6. Quality checks

1. Prior-month accruals: for each, was a bill received and at what variance? Large persistent variances show poor estimating.
2. Accrued liabilities listing: age each line; anything older than the normal billing cycle needs resolution or release.
3. Expense run-rate by account versus prior months and budget after accruals: a drop with no business reason signals a missing accrual.
4. Tax: accrued items may carry tax recoverable only on invoice; follow the jurisdiction's rule.

## Output

The accrual and prepaid schedules, the journal entries (with reversal dates), a short cut-off test log (items reviewed, period assigned, decision), and the net effect on profit.

## Do not

- Accrue without a basis; "estimate" must show how it was derived.
- Create schedules for trivial amounts below the agreed threshold.
- Release deferred revenue by guess; tie to the service term or milestone.
- Leave stale accruals on the balance sheet quarter after quarter.
- Book accruals in a locked period.

## References

- [references/standard-entry-patterns.md](references/standard-entry-patterns.md): entry patterns for AP, payroll, depreciation, prepaid and revenue accruals with documentation requirements.
- Roll-forward schedule formats (prepaid, fixed assets, deferred revenue, standing accruals, loans) are in `adjusting-entries-register`, which runs these mechanics for the whole period and builds the approved entry file.
