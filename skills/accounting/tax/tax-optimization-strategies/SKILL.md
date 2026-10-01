---
name: tax-optimization-strategies
description: >-
  Legal tax-planning for individuals and small businesses under post-OBBBA US law: S-corp election break-even and operating playbook (accountable plan, reasonable salary), retirement plans (SEP, Solo 401(k), defined benefit), QBI, SALT and PTE election, Section 179 and bonus depreciation, loss harvesting, charitable bunching, family strategies, crypto, year-end planning. Use for 'reduce my taxes', 'should I elect S-corp', 'SEP vs solo 401k', 'QBI deduction', 'year-end tax planning'. Educational, not tax advice; flag audit risk on aggressive positions.
metadata:
  department: "accounting"
  domain: "tax"
  owner: "satva-coe"
  status: "beta"
  license: "MIT"
  source: "https://github.com/davidjelinekk/tax-skills-claude-code/tree/main/skills/tax-optimize"
---
<!-- Adapted from davidjelinekk/tax-skills-claude-code skills/tax-optimize (MIT, Copyright (c) 2025-2026; the LICENSE file names no holder). Modified by Satva: renamed from tax-optimize, cross-references repointed, currency caveat added. -->

> **Tax year and jurisdiction.** Upstream targets US federal tax for tax years 2025 and 2026 (post-OBBBA, P.L. 119-21, signed 4 July 2025) with Illinois as the default state. Figures, thresholds and sunset dates change: verify against current IRS and state guidance. Illinois-specific material applies only to Illinois taxpayers. Educational guidance, not tax advice; a licensed CPA or tax attorney makes the binding call.

# Tax Optimization — Strategies to Minimize Tax Liability

Identify and implement legal tax-saving strategies for individuals and small
businesses. All strategies reflect post-OBBBA (One Big Beautiful Bill Act) law
effective for 2025+ tax years.

**DISCLAIMER**: Tax optimization strategies must be evaluated in the context of
your complete tax picture. Always verify with a qualified CPA before implementing.

## When to Use This Skill

- Evaluating S-Corp election for an LLC
- Comparing retirement plan options (SEP vs Solo 401k vs DB plan)
- Maximizing QBI deduction (Section 199A)
- Year-end tax planning
- Deciding whether to use Section 179 vs bonus depreciation
- Tax loss harvesting strategy (stocks, crypto)
- Charitable giving optimization
- 529 plan contribution strategy
- Multi-LLC structure optimization
- SALT deduction and IL PTE tax election analysis
- Estimated tax payment strategy
- Cryptocurrency tax reporting and DeFi transactions
- Day trading / Section 475 mark-to-market election analysis
- Section 1256 contract (futures/index options) tax treatment
- R&D tax credit eligibility and calculation
- Energy credits (solar, EV, efficiency upgrades)
- ACA premium tax credit optimization
- Net operating loss (NOL) planning and carryforward strategy
- Like-kind exchange (1031) structuring
- Installment sale tax deferral
- Passive activity loss rules and material participation
- Alternative minimum tax (AMT) exposure analysis

## Context Needed

Before recommending strategies, collect:
1. **Filing status and dependents** — Affects brackets, credits, phase-outs
2. **Approximate AGI** — Critical for phase-out analysis
3. **Entity types and income** — Each LLC's net profit, how it's taxed
4. **Current retirement plans** — What's already in place
5. **Age** — Affects retirement plan limits, catch-up contributions
6. **Specific goal** — Reduce current-year taxes? Long-term planning? Both?

## Strategy Categories

### 1. Entity Structure Optimization
**When to analyze**: User asks about S-Corp, reasonable salary, or SE tax reduction.

Load `references/entity-structure.md` for:
- S-Corp election break-even analysis (typically $50K-$60K net profit threshold)
- Reasonable salary determination (40-60% of net income, benchmarked to industry)
- SE tax savings calculation
- QBI deduction interaction (salary is NOT QBI-eligible)
- IL-specific considerations (replacement tax, PTE election compatibility)
- Form 2553 filing deadline (March 15 of election year)

### 2. Retirement Plan Strategies
**When to analyze**: User asks about retirement, tax sheltering, or reducing taxable income.

Load `references/retirement-plans.md` for:
- SEP IRA: 25% of net SE income, max $70,000 (2025) / $72,000 (2026)
- Solo 401(k): $23,500 employee + 25% employer (2025), total max $70,000
- Catch-up contributions: $7,500 (age 50+), $11,250 super catch-up (age 60-63)
- Defined Benefit/Cash Balance: $120K-$359K/year depending on age
- Comparison matrix at different income levels
- Roth options and backdoor Roth strategies
- HSA as stealth retirement account ($4,300 self / $8,550 family in 2025)

### 3. Deduction Strategies
**When to analyze**: User asks about deductions, depreciation, charitable giving, or SALT.

Load `references/deduction-strategies.md` for:
- **QBI (Section 199A)**: 20% deduction, now permanent. SSTB phase-outs, W-2 wage limits
- **Section 179**: Up to $2,500,000 (2025, post-OBBBA). Cannot create business loss
- **Bonus depreciation**: 100% permanently restored for property acquired after 1/19/2025
- **SALT**: Cap raised to $40,000 (2025-2029). Phase-down above $500K AGI
- **IL PTE tax**: 4.95% at entity level, deducted as business expense (bypasses SALT cap)
- **Charitable giving**: Bunching, DAFs, appreciated stock. New 0.5% AGI floor starting 2026
- **Tax loss harvesting**: Wash sale rules (securities vs crypto differences)
- **529 plans**: IL deduction $10K/individual, $20K/couple per beneficiary
- **Child Tax Credit**: $2,200/child (OBBBA), ACTC $1,700 refundable
- **Timing strategies**: Income deferral, expense acceleration, 12-month prepayment rule

### 4. Multi-LLC Optimization
**When to analyze**: User has multiple LLCs and asks about structure or passive income.

Key considerations:
- Grouping elections (IRC Section 469) for material participation
- Passive vs active income management
- Self-rental rule (rental income from property rented to own business = nonpassive)
- Related party transaction rules (IRC Section 267) — arm's length requirement
- IL Series LLC option for asset isolation with single filing fee
- Inter-entity management fees, loans, rent — documentation requirements

### 5. Year-End Tax Planning
**When to analyze**: Q4 planning, or user asks "what should I do before year-end?"

Checklist approach:
1. Maximize retirement contributions (Solo 401k employee deferrals by Dec 31)
2. Harvest tax losses (mind wash sale rules for securities)
3. Bunch charitable contributions if near standard deduction threshold
4. Review estimated tax payments — ensure safe harbor met
5. Accelerate Section 179 / bonus depreciation purchases (placed in service by Dec 31)
6. Consider Roth conversion if in a low-income year
7. Fund HSA to maximum
8. Make 529 contributions for IL state deduction
9. Prepay deductible business expenses (12-month rule)
10. Review S-Corp reasonable salary — adjust Q4 payroll if needed

### 6. Estimated Tax Optimization
**When to analyze**: User asks about quarterly payments, underpayment penalties, or cash flow.

Key strategies:
- Safe harbor: 100% of prior year tax (110% if AGI > $150K)
- Annualized income method for uneven income (Form 2210, Schedule AI)
- W-2 withholding as Q4 catch-up (treated as paid evenly throughout year)
- Coordinate federal + IL estimated payments
- Apply prior-year refund to next year's estimates

### 7. Crypto & Trading Tax Strategies
**When to analyze**: User trades crypto, day trades stocks, or uses futures/options.

Load `references/crypto-trading.md` for:
- Crypto as property — every disposition is taxable (IRS Notice 2014-21)
- Form 8949 reporting, cost basis methods (specific ID, FIFO, average cost)
- 1099-DA (new form phasing in 2025-2026) from centralized exchanges
- Staking/mining = ordinary income at FMV when received
- DeFi: liquidity pools, yield farming, token swaps — all taxable events
- NFTs: collectibles rate (28%) vs regular capital gains
- Wash sale: does NOT apply to directly-held crypto (DOES apply to crypto ETFs)
- Digital Assets question on Form 1040 page 1 — false answer = false statement
- Section 475 mark-to-market election: trader vs investor status, unlimited loss deduction, no wash sale issues
- Section 1256 contracts: 60/40 LTCG/STCG for regulated futures, index options (Form 6781)
- Straddle rules (Section 1092) for options traders
- IRS blockchain analytics (Chainalysis/CipherTrace) and FBAR considerations

### 8. Credits & Incentives
**When to analyze**: User asks about tax credits, R&D activities, energy improvements, EV purchases, or ACA subsidies.

Load `references/credits-incentives.md` for:
- **R&D Credit (Section 41)**: 4-part test, QREs, ASC method (14%), Form 6765
- **Small business R&D payroll offset**: <$5M gross receipts, up to $500K/year for 5 years (OBBBA)
- **Section 174 amortization**: R&D costs must be amortized over 5 years (not expensed)
- **ERC status**: Program ended, IRS moratorium on new claims, high audit risk — do NOT pursue without counsel
- **Residential Clean Energy Credit**: 30% for solar, wind, geothermal, battery storage (Form 5695)
- **Energy Efficient Home Improvement Credit**: 30% up to $3,200/year
- **Clean Vehicle Credit**: up to $7,500 new EV, $4,000 used EV
- **Business energy credits**: ITC (6%/30%), PTC, commercial vehicle credit
- **ACA Premium Tax Credit**: Form 8962 reconciliation, MAGI reduction strategies for larger subsidies

### 9. Advanced Tax Strategies
**When to analyze**: User has NOLs, real estate exchanges, installment sales, passive activity questions, or AMT exposure.

Load `references/advanced-strategies.md` for:
- **NOL rules**: Carry forward indefinitely, 80% of taxable income limit, no carryback (except farming)
- **Excess business loss limitation (Section 461(l))**: $305K/$610K threshold, excess becomes NOL carryforward
- **Like-kind exchanges (1031)**: Real property only, 45-day ID + 180-day close, qualified intermediary required
- **Installment sales (Section 453)**: Spread gain over payment period, gross profit ratio, imputed interest rules
- **Passive activity losses (Section 469)**: 7 material participation tests, self-rental rule, $25K rental exception
- **Grouping elections**: Combine activities for material participation testing
- **Disposition rule**: All suspended passive losses deductible on full disposition
- **AMT**: 2025 exemptions ($88,100/$137,000), common triggers (ISOs, SALT, private activity bonds)
- **AMT credit carryforward (Form 8801)**: Recover prior AMT from timing differences

### 10. Family Employment & Dependent Strategies
**When to analyze**: User asks about hiring children, hiring spouse, dependent care, kiddie tax, education savings, or family tax planning.

Load `references/family-strategies.md` for:
- **Hiring children**: FICA exemption for sole prop/partnership (IRC 3121(b)(3)(A)), S-Corp workaround via management company
- **Age-based work guidelines**: Suitable tasks and reasonable pay rates by age (7-17)
- **Tax savings**: Up to ~$7,095/year per child (32% bracket + SE tax), plus Roth IRA funding
- **Hiring spouse**: Section 105 medical reimbursement plan, QSEHRA ($6,350/$12,800), ICHRA
- **Dependent Care FSA**: $5,000 (2025), $7,500 (2026+ OBBBA) pre-tax
- **Child and Dependent Care Credit**: Form 2441, FSA vs credit comparison by AGI
- **Kiddie tax**: Form 8615 thresholds ($1,300/$2,600 in 2025), strategies to minimize
- **Education savings**: Coverdell ESA ($2,000/year), Series EE/I bonds education exclusion
- **Custodial accounts**: UGMA/UTMA vs 529 for FAFSA impact
- **Filing child's return**: Standard deduction, Roth IRA eligibility, tax filing history

### 11. S-Corp Operational Strategies
**When to analyze**: User already has an S-Corp and asks about accountable plan, Augusta Rule, fringe benefits, home office reimbursement, distributions, basis tracking, or year-end compensation planning.

Load `references/scorp-playbook.md` for:
- **Accountable plan**: Tax-free reimbursement of home office, vehicle, cell, internet (~$6K+/year savings)
- **Augusta Rule (Section 280A(g))**: Rent home to S-Corp for up to 14 days tax-free
- **Fringe benefits**: >2% shareholder rules for health insurance, HSA, W-2 Box treatment
- **Year-end compensation planning**: Salary vs distribution timing, bonus strategy, payroll tax optimization
- **Retirement contributions**: Solo 401(k) / SEP through S-Corp, salary optimization for max contributions
- **Distribution planning**: Basis tracking (Form 7203), distribution timing, reasonable compensation documentation
- **Startup/organizational costs**: Section 195 and Section 248 deduction and amortization rules

## Analysis Framework

When the user provides their situation, structure your response as:

1. **Current Tax Position**: Summarize their current structure and estimated tax
2. **Opportunities Identified**: List strategies ranked by estimated savings
3. **Implementation Steps**: Specific actions, forms, deadlines
4. **Risk Considerations**: Any audit flags or compliance concerns
5. **Annual Savings Estimate**: Quantify where possible

Always cross-reference with `tax-audit-risk-assessment` when recommending aggressive positions.

## Reference Files

- `references/entity-structure.md` — S-Corp vs LLC analysis, reasonable salary, Form 2553
- `references/retirement-plans.md` — SEP, Solo 401k, DB plan comparison with limits
- `references/deduction-strategies.md` — QBI, depreciation, SALT, charitable, 529, credits
- `references/crypto-trading.md` — Crypto taxation, Form 8949, 1099-DA, DeFi, NFTs, Section 475/1256, straddles
- `references/credits-incentives.md` — R&D credit, ERC status, energy credits, clean vehicle credits, ACA PTC
- `references/advanced-strategies.md` — NOLs, 1031 exchanges, installment sales, passive activity rules, AMT
- `references/scorp-playbook.md` — Accountable plan, Augusta Rule, fringe benefits, distribution planning, year-end compensation
- `references/family-strategies.md` — Hiring children, hiring spouse, dependent care, kiddie tax, education savings, custodial accounts
