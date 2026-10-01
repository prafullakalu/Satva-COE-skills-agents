---
name: tax-aligned-bookkeeping
description: >-
  Tax-aligned bookkeeping for US individuals and small businesses: chart of accounts mapped to Schedule C, Form 1065 and 1120-S lines, transaction categorisation rules, expense-maximisation checks, record-keeping and retention, 1099 tracking, home-office and vehicle tracking, quarterly review checklist, multi-LLC consolidated books. Use for 'categorize business expenses for tax', 'tax chart of accounts', 'what records do I need to keep', 'multi-LLC bookkeeping', 'deductible expenses'. Not tax advice.
metadata:
  department: "accounting"
  domain: "tax"
  owner: "satva-coe"
  status: "beta"
  license: "MIT"
  source: "https://github.com/davidjelinekk/tax-skills-claude-code/tree/main/skills/tax-bookkeeping"
---
<!-- Adapted from davidjelinekk/tax-skills-claude-code skills/tax-bookkeeping (MIT, Copyright (c) 2025-2026; the LICENSE file names no holder). Modified by Satva: renamed from tax-bookkeeping, cross-references repointed, currency caveat added. -->

> **Tax year and jurisdiction.** Upstream targets US federal tax for tax years 2025 and 2026 (post-OBBBA, P.L. 119-21, signed 4 July 2025) with Illinois as the default state. Figures, thresholds and sunset dates change: verify against current IRS and state guidance. Illinois-specific material applies only to Illinois taxpayers. Educational guidance, not tax advice; a licensed CPA or tax attorney makes the binding call.

# Tax Bookkeeping — Transaction Categorization & Financial Organization

Help categorize transactions, build/review chart of accounts, ensure record-keeping
compliance, and prepare books for tax filing. All categories map directly to IRS
form lines for seamless tax preparation.

## When to Use This Skill

- Setting up a chart of accounts for a new LLC or business
- Categorizing a batch of transactions (bank/credit card imports)
- Reviewing whether expenses are properly categorized
- Determining which IRS expense line a transaction belongs to
- Checking record-keeping compliance (retention periods, documentation)
- Tracking 1099 issuance requirements
- Quarterly or year-end bookkeeping review
- Multi-LLC consolidated bookkeeping questions

## Context Needed

Before categorizing transactions, establish:
1. **Entity type** — Sole prop (Schedule C), Partnership (Form 1065), S-Corp (1120-S)
2. **Industry/NAICS code** — Affects which expenses are typical
3. **Cash vs accrual basis** — Most small businesses use cash basis
4. **Fiscal year** — Calendar year (Jan-Dec) is most common for small businesses

## Core Workflow

### Transaction Categorization
When the user provides transactions (CSV, bank statement, or list):

1. **Load reference**: Read `references/schedule-c-mapping.md` for the IRS category mapping
2. **Classify each transaction** to the correct IRS line item
3. **Flag ambiguous items** — ask the user rather than guessing
4. **Flag personal expenses** that may have been mixed in
5. **Note split transactions** — e.g., cell phone bill that's 60% business
6. **Track 1099 candidates** — any vendor paid $600+ in the tax year

### Chart of Accounts Setup/Review
When building or reviewing a COA:

1. **Load reference**: Read `references/chart-of-accounts.md` for the tax-aligned template
2. **Map to IRS form lines** — every expense account should map to a specific form line
3. **Keep it simple** — 40-60 accounts is typical for an LLC; avoid over-creating
4. **Use sub-accounts** for detail that rolls up to main categories
5. **Include an "Ask My Accountant" suspense account** (code 6999) for uncertain items

### Record-Keeping Review
When checking compliance:

1. Verify receipts exist for expenses over $75 (best practice: all expenses)
2. Check travel/meal documentation has all 5 required elements (amount, date, place, business purpose, business relationship)
3. Verify mileage log is contemporaneous (not reconstructed)
4. Confirm home office measurements and exclusive-use documentation
5. Check 1099-NEC filing for all contractors paid $600+

## Key Rules

### De Minimis Safe Harbor
- Items under **$2,500** per item/invoice can be expensed immediately (no capitalization)
- Items under **$5,000** if the business has an Applicable Financial Statement (audited financials)
- Must make annual election on tax return (statement attached to return)

### Meals Deduction
- **50% deductible** for business meals (2023 forward)
- The temporary 100% restaurant meal deduction expired 12/31/2022
- Must document: who, what business was discussed, where, when, business relationship

### 1099 Filing Requirements
- **1099-NEC**: Any contractor/vendor paid **$600+** in the tax year (due January 31)
- **1099-K**: Third-party payment networks report at **$600** threshold
- **Penalties for late/missing 1099s**: $60 (within 30 days), $130 (by Aug 1), $310 (after Aug 1), $660 (intentional disregard)

### Record Retention Periods

| Record Type | Keep For |
|-------------|----------|
| Tax returns + supporting docs | 3 years from filing |
| If >25% income underreported | 6 years |
| Fraud or no return filed | Indefinite |
| Employment tax records | 4 years |
| Asset/depreciation records | Life of asset + 3 years |
| Business formation docs | Permanent |
| Bad debt / worthless securities | 7 years |

### Separating Personal and Business
- **CRITICAL**: Use separate bank accounts and credit cards for each LLC
- Mixing personal and business expenses is the #1 way to lose LLC liability protection AND trigger audit attention
- Owner withdrawals go through "Owner's Draw" account (equity), NOT through expenses
- Contributions go through "Owner's Contribution" account

## Multi-LLC Bookkeeping

When the user has multiple LLCs:
- Each LLC needs its own set of books (separate bank accounts, separate COA)
- Inter-company transactions must be documented (management fees, loans, rent)
- Loans between entities need promissory notes with AFR interest rates
- Management fees must reflect arm's-length fair market value
- Consolidated reporting for the owner's personal tax return (all K-1s flow to 1040)

## Quarterly Review Checklist

Guide the user through these quarterly:
1. Reconcile all bank and credit card accounts
2. Review uncategorized transactions (clear the suspense account)
3. Verify all contractor payments tracked for 1099 reporting
4. Check estimated tax payment was made on time
5. Review accounts receivable — any bad debts to write off?
6. Verify payroll tax deposits current (if applicable)
7. Back up all financial records
8. Review home office and vehicle logs are current

## Commonly Missed Deductions & Expense Timing

When reviewing books or preparing for tax filing, check for commonly overlooked deductions:

1. **Load reference**: Read `references/expense-maximization.md` for the full catalog
2. **Review missed deductions**: Business gifts ($25/person), bad debt write-offs, startup/organizational costs, Section 197 intangibles, casualty/theft losses, LTC insurance premiums, disability insurance strategy
3. **Home office mileage strategy**: A qualifying home office makes ALL trips from home deductible business miles — flag this for any client without a home office deduction
4. **Vehicle method selection**: Evaluate standard mileage vs actual expense; remind users of the first-year lock-in rule (start with standard mileage to preserve flexibility)
5. **Year-end timing**: Accelerate expenses using the 12-month prepayment rule, stock up on supplies, prepay insurance/rent/subscriptions, place equipment in service before Dec 31
6. **De minimis safe harbor**: Ensure the annual election is made; items under $2,500 can be expensed immediately
7. **Repairs vs improvements**: Apply the 3-part test (betterment, restoration, adaptation) before capitalizing
8. **Per diem for travel meals**: Offer as an alternative to tracking individual meal receipts during overnight business travel

## Reference Files

- `references/chart-of-accounts.md` — Complete tax-aligned COA template with account numbers
- `references/schedule-c-mapping.md` — Line-by-line mapping of transactions to IRS form lines
- `references/expense-maximization.md` — Missed deductions, expense timing strategies, vehicle optimization, home office strategy, per diem rates, QOZ investments
