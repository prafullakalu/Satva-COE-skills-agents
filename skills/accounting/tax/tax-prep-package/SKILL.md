---
name: tax-prep-package
description: >-
  Compile a tax-ready package from reconciled books for a US small business: P&L mapped to Schedule C lines, quarterly breakdown, 1099 contractor summary, flagged special-treatment items (meals, home office, vehicle, depreciation, startup costs, NOL, health insurance and retirement off Schedule C), carryforwards, and the delivery checklist for the accountant. Use for 'prepare for taxes', 'tax prep', 'Schedule C', 'get ready for my accountant', 'tax package'. Organises data only; does not file or give tax advice.
metadata:
  department: "accounting"
  domain: "tax"
  owner: "satva-coe"
  status: "beta"
  license: "MIT"
  source: "https://github.com/Receiptor-AI/bookkeeping-skills/tree/main/skills/tax-prep"
---
<!-- Adapted from Receiptor-AI/bookkeeping-skills skills/tax-prep (MIT, Copyright (c) 2026 Receiptor AI). Modified by Satva: tool frontmatter and helper script removed, renamed, cross-references repointed, currency caveat added. -->

> **Currency of figures.** Rates, limits and thresholds in this skill are the upstream's (written March 2026, mostly 2024 values with 2026 law changes noted). They change every year: verify against current IRS publications and instructions before relying on a number. Organises data; not tax advice.

# Tax Preparation Support

Organize financial records into tax-ready reports that an accountant can use directly or that the business owner can use to file accurately.

## Read these when needed

- Read [references/tax-package.md](references/tax-package.md) before delivering a package to an accountant or tax preparer.
- Track package completeness as a simple table (artifact | status: ready / missing / needs-review / draft); the upstream's helper script that counted these was left out.

> **Disclaimer:** This skill organizes financial data for tax purposes. It does not constitute tax advice. Tax rules vary by jurisdiction and change frequently. Always consult a qualified tax professional for advice specific to your situation.

## When to use

Use this when: tax season is approaching (Jan–Apr for calendar-year filers), the user's accountant requests organized records, quarterly estimated payments are due, or the user is catching up on prior-year filings.

## Prerequisites

The quality of tax prep depends entirely on the quality of the underlying data. Before generating reports, the user should have: processed receipts, categorized expenses, and ideally reconciled bank statements. If any are missing, run those skills first. Fastest path from zero: capture receipts, categorise (`transaction-categorisation-rules`), reconcile (`bank-reconciliation`), then generate tax reports.

## Step 1: Gather business context

| Question | Why it matters |
|----------|---------------|
| Entity type? | Sole prop/single-member LLC → Schedule C. Partnership → 1065. S-Corp → 1120-S. C-Corp → 1120. |
| Tax year? | Calendar (Jan–Dec) or fiscal? Which year? |
| Accounting method? | Cash basis (most small businesses) or accrual? |
| State(s)? | State tax obligations, nexus, state-specific rules. |
| First year of business? | Startup costs: up to $5,000 immediate, rest amortized over 180 months. |
| Employees? | Triggers Forms 940, 941/944, W-2s. |
| Contractors? | See **contractor-1099-reporting** skill for filing rules. |
| Home office? | See **home-office-deduction** skill for simplified vs. actual method. |
| Vehicle? | See **vehicle-expense-deduction** skill for mileage rate vs. actual. |
| Equipment purchases? | See **us-tax-depreciation-179-macrs** skill for Section 179, bonus, MACRS. |
| Health insurance? | Self-employed health insurance → Form 1040 Line 17, NOT Schedule C. |
| Retirement contributions? | SEP/SIMPLE/Solo 401(k) → Form 1040 Line 20, NOT Schedule C. |
| Prior year carryforwards? | NOLs, depreciation, Section 179 carryover. |

## Step 2: Generate the P&L mapped to Schedule C

```
REVENUE
  Gross receipts or sales                    $XXX,XXX.XX
  Returns and allowances                     −$X,XXX.XX
  ─────────────────────────────────────────
  Net revenue                                $XXX,XXX.XX

COST OF GOODS SOLD (if applicable)
  Cost of goods sold                         $XX,XXX.XX

GROSS PROFIT                                 $XXX,XXX.XX

OPERATING EXPENSES (Schedule C Part II)
  Line 8:  Advertising                       $X,XXX.XX
  Line 9:  Car and truck expenses            $X,XXX.XX
  Line 10: Commissions and fees              $X,XXX.XX
  Line 11: Contract labor                    $X,XXX.XX
  Line 13: Depreciation (Form 4562)          $X,XXX.XX
  Line 14: Employee benefit programs         $X,XXX.XX
  Line 15: Insurance (other than health)     $X,XXX.XX
  Line 16b: Interest (other)                 $X,XXX.XX
  Line 17: Legal and professional services   $X,XXX.XX
  Line 18: Office expense                    $X,XXX.XX
  Line 20b: Rent (business property)         $X,XXX.XX
  Line 21: Repairs and maintenance           $X,XXX.XX
  Line 22: Supplies                          $X,XXX.XX
  Line 23: Taxes and licenses                $X,XXX.XX
  Line 24a: Travel                           $X,XXX.XX
  Line 24b: Meals (at 50%)                   $X,XXX.XX
  Line 25: Utilities                         $X,XXX.XX
  Line 26: Wages                             $X,XXX.XX
  Line 27a: Other expenses                   $X,XXX.XX
  Line 30: Business use of home              $X,XXX.XX
  ─────────────────────────────────────────
  Total expenses                             $XX,XXX.XX

NET PROFIT (Line 31)                         $XX,XXX.XX
```

## Step 3: Generate quarterly breakdown

Essential for estimated tax payments (see **estimated-tax-and-tax-prep-organiser** skill):

| | Q1 (Jan–Mar) | Q2 (Apr–Jun) | Q3 (Jul–Sep) | Q4 (Oct–Dec) | Full Year |
|---|---|---|---|---|---|
| Revenue | | | | | |
| COGS | | | | | |
| Gross profit | | | | | |
| Expenses | | | | | |
| Net profit | | | | | |

## Step 4: Flag items needing special treatment

These categories require attention beyond basic categorization:

**Meals** — Record at full value; only 50% is deductible on the return. See **business-meals-deduction** skill for documentation requirements and the 2026 on-premises change.

**Home office** — Two methods with very different deductions. See **home-office-deduction** skill for the calculation.

**Vehicle** — Standard mileage vs. actual, method lock-in. See **vehicle-expense-deduction** skill.

**Depreciation** — Assets >$2,500 need Section 179, bonus, or MACRS treatment. See **us-tax-depreciation-179-macrs** skill.

**1099 contractors** — Anyone paid ≥$600 (≥$2,000 starting 2026) needs a 1099-NEC by Jan 31. See **contractor-1099-reporting** skill for the full filing process.

**Self-employment tax** — Net profit × 92.35% × 15.3%. Social Security caps at $168,600 (2024). Half is deductible on Form 1040 Line 15. See **estimated-tax-and-tax-prep-organiser** skill for the calculation.

**Startup costs (first year only)** — Up to $5,000 deductible immediately (reduced dollar-for-dollar above $50,000 total). Remainder amortized over 180 months. Organizational costs have a separate $5,000 deduction.

**Net operating loss** — If Schedule C shows a loss, it offsets other income. Post-TCJA: NOLs offset up to 80% of taxable income, unlimited carryforward.

## Step 5: Compile documentation

For each category, prepare supporting evidence:

**Email receipts** — Digital receipts with sender, timestamp and content intact provide strong audit documentation: the original sender, timestamp, and content establish authenticity independently.

**Bank statements** — Reconciled statements proving book entries match actual bank activity.

**Mileage log** — Date, destination, purpose, miles for every business trip.

**Meal log** — Date, place, amount, purpose, attendees, relationship for every business meal.

**Asset register** — Description, date acquired, cost, business-use %, method, accumulated depreciation.

**Contractor records** — W-9s, payment history, 1099s filed.

## Step 6: Deliver the tax package

The final deliverable:

1. **P&L** — full year + quarterly, mapped to Schedule C lines
2. **Expense detail** — transaction list by category with receipt references
3. **1099 contractor summary** — names, TINs, totals, filing status
4. **Depreciation schedule** — all assets with current and accumulated depreciation
5. **Home office calculation** — method, square footage, expenses, deduction
6. **Vehicle log** — method, miles or actual expenses, business-use %, deduction
7. **Meals log** — each meal with all five required documentation elements
8. **Bank reconciliation** — all accounts reconciled through year-end
9. **Prior-year carryforwards** — NOLs, depreciation, Section 179 carryover
10. **Estimated tax payment history** — dates and amounts paid

Export as spreadsheet (preferred by accountants), PDF (archive), or accounting software import format.

## US context and approval boundaries

See [references/us-bookkeeping-context.md](references/us-bookkeeping-context.md) for the intake fields, what is safe to draft, what needs owner approval and what needs professional review.

## Related skills

- **schedule-c-expense-categories** — Which expense goes on which Schedule C line
- **transaction-categorisation-rules** — How to assign categories to transactions
- **business-meals-deduction** — 50% rule, documentation, entertainment at 0%
- **home-office-deduction** — Simplified vs. actual, Form 8829
- **vehicle-expense-deduction** — Standard mileage vs. actual, method lock-in
- **us-tax-depreciation-179-macrs** — Section 179, bonus depreciation, MACRS
- **contractor-1099-reporting** — W-9 collection, 1099-NEC filing, penalties
- **estimated-tax-and-tax-prep-organiser** — Quarterly payment calculation and safe harbors
