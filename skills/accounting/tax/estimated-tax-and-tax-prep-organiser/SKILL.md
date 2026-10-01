---
name: estimated-tax-and-tax-prep-organiser
description: >-
  Calculate and schedule US quarterly estimated tax (Form 1040-ES) for self-employed owners and pass-through businesses: annualised income, self-employment tax (15.3% on 92.35%), income-tax estimate, safe harbours (90% current / 100% or 110% prior year), due dates, missed-quarter catch-up, underpayment penalty, state estimates, plus the tax-prep organiser checklist for the preparer. Use for 'quarterly estimated taxes', '1040-ES', 'how much should I set aside', 'avoid underpayment penalty', 'get ready for tax season'. Not tax advice.
metadata:
  department: "accounting"
  domain: "tax"
  owner: "satva-coe"
  status: "beta"
  license: "MIT"
  source: "https://github.com/Receiptor-AI/bookkeeping-skills/tree/main/skills/estimated-taxes"
---
<!-- Adapted from Receiptor-AI/bookkeeping-skills skills/estimated-taxes (MIT, Copyright (c) 2026 Receiptor AI), anthropics/knowledge-work-plugins small-business/skills/tax-season-organizer (Apache-2.0) and openaccountant/skills (MIT, Copyright (c) 2026 Open Accountant). Modified by Satva: merged three sources, removed vendor promotion and connector-specific steps, kept Satva's organiser checklist and posting rules. -->

> **Currency of figures.** The workflow is stable; the numbers are not. Receiptor's figures in the body are 2024 values; the reference file uses 2025 values. For any other tax year, fetch the current figures from IRS.gov (Form 1040-ES, Pub. 505, annual revenue procedures) or ask the owner; never reuse an old table silently.

# Estimated Tax Payments

Calculate and schedule quarterly estimated tax payments to avoid underpayment penalties. Essential for self-employed individuals, freelancers, and small business owners who don't have taxes withheld from a paycheck.

## Why you need to pay quarterly

Employees have taxes withheld every paycheck. Self-employed people don't. The IRS expects to receive tax payments throughout the year, not one lump sum in April. If you wait until filing to pay everything, you'll owe an underpayment penalty.

**You must make estimated payments if** you expect to owe **$1,000 or more** in tax for the year after subtracting withholding and credits.

**You're exempt if:** You had zero tax liability last year (100% of prior-year tax is $0), or your withholding from other sources (W-2 job, pension, etc.) covers your expected tax.

## Payment schedule

| Quarter | Covers income from | Payment due |
|---------|-------------------|-------------|
| Q1 | January 1 – March 31 | **April 15** |
| Q2 | April 1 – May 31 | **June 15** |
| Q3 | June 1 – August 31 | **September 15** |
| Q4 | September 1 – December 31 | **January 15** (next year) |

Note: Q2 covers only 2 months and Q3 covers 3 months — the periods are uneven. If a due date falls on a weekend or holiday, the deadline moves to the next business day.

**How to pay:** IRS Direct Pay (irs.gov/payments), EFTPS (Electronic Federal Tax Payment System), credit/debit card (processors charge a fee), or mail a check with a 1040-ES payment voucher. Direct Pay or EFTPS are free and instant-confirmation.

## The two things you're paying

### 1. Self-employment tax (Social Security + Medicare)

This is the self-employed equivalent of FICA. Employees pay 7.65% and their employer pays 7.65%. As a self-employed person, you pay both halves.

**Calculation:**

```
Net Schedule C profit                               $100,000
× 92.35% (adjustment factor)                        × 0.9235
= Self-employment tax base                          $92,350
× 15.3% (12.4% Social Security + 2.9% Medicare)     × 0.153
= Self-employment tax                               $14,130
```

**Social Security cap:** The 12.4% Social Security portion applies only to the first **$168,600** of net self-employment income (2024; $176,100 for 2025; it adjusts annually). Income above this cap is taxed only at the 2.9% Medicare rate.

**Additional Medicare tax:** If net self-employment income exceeds **$200,000** ($250,000 married filing jointly), an additional **0.9% Medicare surtax** applies on the excess.

**Half is deductible:** 50% of your self-employment tax ($7,065 in the example above) is deducted on Form 1040 Line 15. This is an "above the line" deduction — you get it even if you don't itemize. This reduces your income tax (but not your SE tax).

### 2. Income tax (federal)

Your Schedule C net profit (minus the above-the-line SE tax deduction, plus any other income, minus other deductions) is taxed at your marginal income tax rate.

**2024 tax brackets (single), illustration only; the 2025 table is in `references/calculation-assumptions.md`:**

| Taxable income | Rate |
|---|---|
| $0 – $11,600 | 10% |
| $11,601 – $47,150 | 12% |
| $47,151 – $100,525 | 22% |
| $100,526 – $191,950 | 24% |
| $191,951 – $243,725 | 32% |
| $243,726 – $609,350 | 35% |
| $609,351+ | 37% |

Don't forget: your self-employed health insurance deduction (Form 1040 Line 17), retirement contributions (Form 1040 Line 20), and the 50% SE tax deduction all reduce taxable income before applying these brackets.

## Quick estimation method

For a back-of-the-envelope quarterly payment:

```
Estimated annual net profit          $100,000
Self-employment tax:                  $14,130
Deductible half of SE tax:           −$7,065
Adjusted profit for income tax:       $92,935
Federal income tax (approx):          $15,000  (depends on filing status, other income, deductions)
Total estimated tax:                  $29,130
÷ 4 quarters:                         $7,283 per quarter
```

This is a rough estimate. For precision, use IRS Form 1040-ES worksheet or tax software.

## Safe harbor rules — how to avoid penalties

Even if your estimate is wrong, you avoid the underpayment penalty if you meet either safe harbor:

### Safe harbor 1: 90% of current-year tax

Pay at least 90% of what you'll actually owe for the current year. This requires accurately predicting your income — hard if your income fluctuates.

### Safe harbor 2: 100% of prior-year tax (the easy one)

Pay at least **100% of last year's total tax liability**, divided into four equal quarterly payments. If your prior-year AGI exceeded **$150,000** ($75,000 married filing separately), the threshold is **110%** of prior-year tax.

**This is the safe harbor most self-employed people use** because it's predictable. You know exactly what last year's tax was. It doesn't matter if you earn more this year — as long as your quarterly payments total 100% (or 110%) of last year's tax, no penalty.

**Where to find prior-year tax:** Form 1040 Line 24 (total tax) minus Line 33 (total payments and credits from withholding, etc.). Or your tax software will calculate it.

### Which safe harbor to use?

| Situation | Best safe harbor |
|---|---|
| Income is stable year to year | Either works, but prior-year is simpler |
| Income is growing | Prior-year — pay based on last year, even if this year is higher |
| Income is dropping | Current-year 90% — why overpay based on a higher prior year? |
| First year of self-employment | Current-year 90% — there's no prior-year SE tax to use |
| Prior-year AGI >$150K | 110% of prior-year tax |

## Annualized income installment method

If your income is highly seasonal (e.g., 70% of revenue in Q4), you can use the **annualized income installment method** (Form 2210 Schedule AI). This calculates each quarter's required payment based on income actually earned through that quarter, rather than dividing the annual estimate by 4.

This is more work but avoids overpaying early in the year when income hasn't arrived yet. Useful for: holiday-season businesses, accountants/CPAs (busy Jan–Apr), real estate agents (spring/summer heavy), consultants with uneven project timing.

## State estimated taxes

Most states with income tax also require quarterly estimated payments, often on the same schedule. Common states with self-employment-relevant taxes:

- **California:** Franchise Tax Board, same quarterly dates. Uses 30/40/0/30% allocation instead of equal quarters.
- **New York:** Same quarterly dates. NYC residents also owe city estimated tax.
- **Texas, Florida, Nevada, Wyoming, Washington, South Dakota, Alaska, New Hampshire (wages only):** No state income tax — no state estimated payments needed.

Check your state's requirements separately. Some states have different safe harbor rules.

## What happens if you underpay

The penalty is essentially interest on the underpayment. The IRS charges the federal short-term rate + 3% (currently around 8% annually, but it fluctuates). The penalty is calculated per quarter, so paying late for Q1 accumulates more penalty than paying late for Q4.

**The penalty is NOT a flat fee** — it's computed as interest. If you underpaid by $5,000 for one quarter, the penalty might be $100–$150 for that quarter. Annoying but not catastrophic.

**When the penalty is waived:** If you owe less than $1,000 at filing. If your withholding + estimated payments cover at least 90% or the 100%/110% safe harbor. If you had a casualty, disaster, or other unusual circumstance. If you retired or became disabled during the year.

## Adjusting payments mid-year

If your income changes significantly during the year, adjust your remaining quarterly payments. The IRS doesn't require equal payments — you can pay $2,000 in Q1 and $10,000 in Q3 if that reflects your income pattern. Just ensure the total meets the safe harbor by year-end.

**If you realize you've underpaid:** Make a larger Q4 payment by January 15 to reduce the penalty. You can also increase Q4 to cover earlier shortfalls.

**If your income spiked late in the year:** Consider making an extra payment before December 31 to cover the spike. This doesn't have a special form — just make an additional estimated payment via Direct Pay or EFTPS marked for the current tax year.

## Annualise before you estimate

Tax math runs on a full year of income, so project YTD net profit before computing SE tax and income tax. Keep the two numbers separate and labelled:

```
YTD net profit (Jan 1 - Jun 30):  64,000   actual, from reconciled books
Annualised net profit:           128,000   projected = YTD / months elapsed x 12
```

Straight-line annualising is wrong for a seasonal business. Ask once whether income is even through the year; if not, use the owner's own full-year estimate and label it "owner estimate, not projected from YTD". Use reconciled books only: an estimate built on unreconciled books is a number someone will send to the IRS.

## A quarter already missed

If today is past a due date with nothing paid against it: (1) name it ("Q2 was due June 15 and no payment is on file"), (2) show the catch-up amount on its own line, separate from the next scheduled payment, (3) route the penalty question to the preparer. Penalty runs from each quarter's own due date (see `references/underpayment-penalty.md`); never fold the shortfall silently into later quarters. With no quarters left, the balance is due with the return.

## What every estimate leaves out (list these in the output)

State and local income tax; the QBI deduction (Section 199A, up to 20% of qualified business income); home-office and vehicle deductions (`home-office-deduction`, `vehicle-expense-deduction`); depreciation and Section 179 (`us-tax-depreciation-179-macrs`); retirement contributions (SEP-IRA, Solo 401(k)); self-employed health insurance; prior-year loss carryforwards. Each can move the number materially: list them so the preparer can apply them.

## Entity differences

| Structure | Income tax route | SE tax |
|---|---|---|
| Sole proprietor / single-member LLC | Schedule C into the 1040 | Yes |
| Partnership / multi-member LLC | K-1 into the 1040 | Yes, on earned income |
| S corporation | W-2 wages plus K-1 distributions | On wages only (owner must take reasonable salary through payroll) |
| C corporation | Separate corporate return, flat corporate rate | No; payroll taxes instead |

Default to sole-proprietor math only when the entity is unknown, and say so as an assumption.

## Posting the payments

For pass-through owners, estimated income-tax payments are owner draws (equity) and are not a business expense; for a corporation they reduce income tax payable. Do not expense owner income-tax payments in the business P&L.

## Integration with bookkeeping

During the monthly close, calculate year-to-date net profit. Before each quarterly deadline, estimate the quarter's tax liability and compare against your safe harbor target. This prevents the "surprise" of a large underpayment at filing.

Your monthly P&L from the monthly-close skill gives you the numbers you need. Multiply YTD net profit by your combined tax rate (SE tax + income tax marginal rate) and compare to payments made.

## Output format

Open every deliverable with: "Prepared for review by your accountant. Not tax advice." Put the **tax year** in the header. Sections, in order:

1. Header: estimate for the quarter, tax year, prepared date, the year the rate tables came from.
2. YTD snapshot: YTD net profit with its date range, annualised net profit, assumed entity type (flag as assumed).
3. Self-employment tax on annualised net profit, with the deductible half.
4. Income tax estimate: adjusted net income, assumed bracket (default 22% only if the owner gives nothing better, with a note to confirm), result.
5. Total estimated annual liability.
6. Quarterly payment: (annual liability - payments already made) / quarters still ahead, with the due date; any missed quarter on its own catch-up line.
7. Safe-harbour test result: 100% of prior-year tax (110% if prior-year AGI exceeded 150,000), or 90% of current-year tax.
8. Assumptions: bracket, entity, state tax excluded, deductible SE half included, every deduction not applied.

Worked example: `references/worked-example-quarterly.md`. Common failure patterns: `references/gotchas.md`.

## Part B: tax-prep organiser (workpapers for the preparer)

Prepare a package the preparer can work from without email ping-pong. The full package specification and Schedule C mapping are in `tax-prep-package` and `schedule-c-expense-categories`; this section is the checklist.

**Books:** reconciled trial balance and year-end P&L/BS with prior-year comparatives (`quarter-and-year-end-close`); all accounts reconciled; no uncategorised or suspense balances; owner draws, contributions and personal items cleaned out of business expenses; fixed-asset register with additions and disposals (`fixed-assets-depreciation`); loan statements and interest; vehicle mileage logs; contractor payments and forms (`contractor-1099-reporting`); payroll year-end forms (`payroll-accounting`); sales tax returns (`sales-tax-vat-gst-compliance`).

**Document checklist:** income (sales reports, 1099-K/1099-NEC received, bank and processor statements); expenses (categorised ledger, receipts above the substantiation threshold); assets (purchase invoices, closing statements); financing (loan statements, interest forms); prior year (filed return and carryforwards: losses, credits, depreciation, charitable); elections and tax-authority notices; for owner-level returns: W-2s, interest and dividends, retirement contributions, health coverage forms, estimated payments made (dates and amounts).

**Deduction guardrails:** ordinary and necessary expenses with documentation; capitalise above the policy threshold; split partly personal items on a documented basis; fines, penalties, personal expenses and entertainment are not deductible; meals are limited (`business-meals-deduction`). Flag grey areas, do not decide them.

**Organiser output:** (1) estimate worksheet with assumptions, safe-harbour result and instalment schedule; (2) document index with status (have / missing / not applicable); (3) list of judgement items for the preparer.

## Do not

- Do not file, pay or elect anything, and do not present an estimate as a tax liability.
- Do not apply a rate to gross revenue; apply it to net profit after the deductible half of SE tax.
- Do not quote a bracket, wage base or due date from memory for a year you have not verified: cite IRS.gov or a revenue procedure, or ask the owner.
- Do not hide an assumption; do not put full tax IDs or account numbers in shared documents.

## References

- `references/calculation-assumptions.md`: SE tax and income-tax math, 2025 figures, YTD vs annualised, missed quarters.
- `references/worked-example-quarterly.md`: a full worked quarterly estimate.
- `references/underpayment-penalty.md`: Form 2210 style penalty arithmetic and waiver conditions.
- `references/state-estimated-taxes.md`: state income-tax planning, no-tax states, multi-state notes.
- `references/gotchas.md`: good and bad patterns.
