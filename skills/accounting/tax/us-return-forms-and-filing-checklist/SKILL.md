---
name: us-return-forms-and-filing-checklist
description: >-
  US return preparation guide for individuals and small-business entities: document gathering, filing-status determination, which forms to file (1040, Schedule C, 1065, 1120-S, K-1, 8829, 4562 and 20+ schedules), multi-entity coordination order, extensions, amended returns, and Illinois state return rules including the 120-day federal-change reporting rule. Use for 'what forms do I need', 'tax document checklist', 'extension', 'amended return', 'multi-entity filing', 'IL-1040'. Not tax advice.
metadata:
  department: "accounting"
  domain: "tax"
  owner: "satva-coe"
  status: "beta"
  license: "MIT"
  source: "https://github.com/davidjelinekk/tax-skills-claude-code/tree/main/skills/tax-prep"
---
<!-- Adapted from davidjelinekk/tax-skills-claude-code skills/tax-prep (MIT, Copyright (c) 2025-2026; the LICENSE file names no holder). Modified by Satva: renamed from tax-prep, cross-references repointed, currency caveat added. -->

> **Tax year and jurisdiction.** Upstream targets US federal tax for tax years 2025 and 2026 (post-OBBBA, P.L. 119-21, signed 4 July 2025) with Illinois as the default state. Figures, thresholds and sunset dates change: verify against current IRS and state guidance. Illinois-specific material applies only to Illinois taxpayers. Educational guidance, not tax advice; a licensed CPA or tax attorney makes the binding call.

# Tax Preparation — Return Filing Guide & Document Management

Guide taxpayers through return preparation: what documents to gather, which
forms to file, multi-entity coordination, and state return requirements.

**DISCLAIMER**: This skill provides guidance on tax return preparation. Complex
returns should be reviewed by a licensed CPA or Enrolled Agent before filing.

## When to Use This Skill

- Starting tax return preparation (what do I need?)
- Determining which forms to file for an LLC/S-Corp
- Creating a document gathering checklist
- Understanding K-1 flow from entities to personal return
- Filing IL state returns alongside federal
- Filing extensions
- Amending a return after discovering an error
- Coordinating multi-entity filing (multiple LLCs)

## Context Needed

1. **Tax year** being prepared
2. **Filing status** — Single, MFJ, MFS, HoH, QSS
3. **Entity types** — Each LLC and how it's taxed (disregarded, partnership, S-Corp)
4. **Income sources** — W-2 jobs, Schedule C businesses, K-1s, investments, rental
5. **Major life events** — Marriage, divorce, children born, home purchase/sale, business started/closed
6. **Prior year return available?** — Useful for comparison

## Filing Deadlines

### Federal
| Return Type | Original Due Date | Extended Due Date |
|-------------|-------------------|-------------------|
| Form 1040 (Individual) | April 15 | October 15 |
| Form 1065 (Partnership) | March 15 | September 15 |
| Form 1120-S (S-Corp) | March 15 | September 15 |
| Form 1120 (C-Corp) | April 15 | October 15 |

### Illinois
| Return Type | Original Due Date | Extended Due Date |
|-------------|-------------------|-------------------|
| IL-1040 (Individual) | April 15 | October 15 |
| IL-1065 (Partnership) | March 15 | September 15 |
| IL-1120-ST (S-Corp) | March 15 | September 15 |

**CRITICAL**: Entity returns (1065, 1120-S) are due BEFORE individual returns.
K-1s must be issued to partners/shareholders for them to file their 1040s.

### Late Filing Penalties
- **Partnership (1065)**: $235/partner/month, max 12 months
- **S-Corp (1120-S)**: $235/shareholder/month, max 12 months
- **Individual (1040)**: 5% of unpaid tax/month, max 25%. Min penalty for returns >60 days late: lesser of $510 or 100% of tax

## Form Selection Guide

### Which Forms Do I Need?

**Single-Member LLC (Disregarded Entity):**
- Schedule C (or Schedule E if rental) on Form 1040
- Schedule SE (self-employment tax)
- Form 8829 (home office, if applicable)
- Form 4562 (depreciation, if applicable)
- IL-1040 (Illinois individual return)

**Multi-Member LLC (Partnership):**
- Form 1065 (partnership return) with Schedule K-1 for each member
- IL-1065 (IL partnership return) with Schedule K-1-P for each member
- Schedule PTE (if PTE tax election made)
- Each member reports K-1 on their Form 1040, Schedule E

**LLC Electing S-Corp:**
- Form 1120-S with Schedule K-1 for each shareholder
- IL-1120-ST (IL S-Corp return)
- W-2 for shareholder-employees
- Form 941 (quarterly payroll tax return)
- Each shareholder reports K-1 on their Form 1040, Schedule E

**Individual (Form 1040) Supporting Schedules:**

| Schedule/Form | When Needed |
|--------------|-------------|
| Schedule 1 | Adjustments to income (SE tax deduction, SE health insurance, IRA, HSA) |
| Schedule 2 | AMT, excess premium tax credit repayment |
| Schedule 3 | Additional credits (education, foreign tax, estimated tax payments) |
| Schedule A | Itemized deductions (SALT, mortgage interest, charitable) |
| Schedule B | Interest/dividend income over $1,500 |
| Schedule C | Sole proprietorship / SMLLC income |
| Schedule D | Capital gains and losses |
| Schedule E | Rental, K-1 pass-through income |
| Schedule SE | Self-employment tax |
| Form 8829 | Home office deduction (regular method) |
| Form 4562 | Depreciation and amortization |
| Form 8949 | Sales of capital assets (stocks, crypto) |
| Form 8995 | QBI deduction (simplified) |
| Form 8995-A | QBI deduction (complex — above threshold or multiple businesses) |
| Schedule ICR (IL) | Property tax and education expense credits |

## Document Gathering Checklist

### Income Documents
- [ ] W-2s from all employers
- [ ] 1099-NEC (contractor/freelance income)
- [ ] 1099-K (payment processor income — PayPal, Stripe, etc.)
- [ ] 1099-INT (bank interest)
- [ ] 1099-DIV (dividends)
- [ ] 1099-B (brokerage/investment sales)
- [ ] 1099-R (retirement distributions)
- [ ] 1099-MISC (other income)
- [ ] Schedule K-1s from all partnerships/S-Corps
- [ ] Crypto exchange tax reports (1099-DA or equivalent)
- [ ] Rental income records (leases, rent rolls)
- [ ] Bank statements showing all deposits

### Expense Documents
- [ ] Business expense receipts (organized by category)
- [ ] Vehicle mileage log (date, destination, business purpose, miles)
- [ ] Home office measurements and home expense records
- [ ] Health insurance premium statements (Form 1095-A/B/C)
- [ ] Retirement plan contribution records
- [ ] Charitable donation receipts and acknowledgment letters
- [ ] Student loan interest (Form 1098-E)
- [ ] Mortgage interest (Form 1098)
- [ ] Property tax bills paid
- [ ] State/local tax payments made
- [ ] Childcare expense records (provider name, EIN, amounts)
- [ ] Education expenses (Form 1098-T)
- [ ] HSA contributions and distributions (Form 5498-SA, 1099-SA)

### Entity-Specific Documents
- [ ] Prior year tax returns (federal and IL)
- [ ] Estimated tax payment records (federal and IL)
- [ ] Payroll records and W-2s issued (S-Corps)
- [ ] 1099-NEC forms issued to contractors
- [ ] Business formation documents (EIN letter, Operating Agreement)
- [ ] Depreciation schedules from prior year
- [ ] Basis tracking worksheets (for K-1 limitations)

## Multi-Entity Filing Coordination

When the user has multiple LLCs:

### Filing Order (Critical)
1. **Entity returns first** (Form 1065, 1120-S) — due March 15
2. Wait for K-1s to be generated
3. **Individual return** (Form 1040) — due April 15
4. All K-1 income flows to Schedule E of the 1040

### K-1 Flow
```
LLC A (1065) → K-1 → Owner's 1040, Schedule E, Line 28
LLC B (1120-S) → K-1 → Owner's 1040, Schedule E, Line 28
LLC C (Schedule C) → Directly on 1040, Schedule C
```

### Basis Tracking
- Each entity requires separate basis tracking
- Basis limits the amount of loss that can be deducted (Section 704(d) / 1366(d))
- Basis is adjusted annually: + income, + contributions, - distributions, - losses
- Form 7203 (S-Corp Shareholder Basis) required starting 2021
- At-risk rules (Section 465) and passive activity rules (Section 469) apply after basis

## Extension Filing

### When to File an Extension
- Cannot gather all documents by the deadline
- K-1s not yet received from entities
- Need more time for complex planning decisions
- **An extension extends time to FILE, not time to PAY**

### How to File
- **Federal**: Form 4868 (individual), Form 7004 (partnership/S-Corp)
- **Illinois**: IL follows federal extension automatically if filed by the IL due date
- **Estimated payment**: Include estimated tax due with extension to avoid penalties

## Amended Returns

### Federal
- **Form 1040-X** for individual returns
- File within 3 years of original filing date (or 2 years from date of tax payment)
- E-filing of 1040-X now available for current and prior 2 tax years

### Illinois
- **Form IL-1040-X** for IL individual returns
- **120-DAY RULE**: If the IRS adjusts your federal return, you MUST file an amended IL return within **120 days** of the federal final determination. Failure extends IL statute of limitations indefinitely for that issue.

## Reference Files

- `references/filing-checklist.md` — Detailed document checklist by entity type and income source
- `references/form-guide.md` — Complete form selection guide with filing scenarios
