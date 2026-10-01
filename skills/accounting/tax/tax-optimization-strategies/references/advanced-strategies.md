# Advanced Tax Strategies — NOLs, 1031 Exchanges, Installment Sales, PALs, AMT

## Net Operating Loss (NOL) Rules

### Post-TCJA Framework
- NOLs generated in 2018+ carry forward **indefinitely**
- **No carryback** (except farming losses: 2-year carryback)
- Deduction limited to **80% of taxable income** (cannot fully eliminate tax liability)
- Remaining 20% of taxable income always subject to tax

### NOL Calculation for Individuals
- NOL arises when total deductions exceed total income
- Calculated at the **individual level** (all income and loss sources combined)
- Form 172 used to compute the NOL amount
- Modifications required: remove personal exemption, remove NOL deduction from other years, limit capital losses to capital gains, remove nonbusiness deductions exceeding nonbusiness income

### Excess Business Loss Limitation (Section 461(l))
- **Threshold (2024)**: $305,000 (single) / $610,000 (MFJ)
- **Threshold (2025)**: Indexed for inflation (~$313,000 single / ~$626,000 MFJ)
- Business losses exceeding the threshold are **NOT deductible** in the current year
- Excess becomes an **NOL carryforward** to the following year
- Applied BEFORE the NOL deduction calculation
- Extended through **2028** by OBBBA (was set to expire 2026)
- **Includes pass-through losses**: LLC, S-Corp, partnership losses flowing to individual

### How to Use NOL Carryforwards
1. Calculate current-year taxable income (before NOL deduction)
2. Apply NOL deduction: limited to 80% of taxable income
3. Remaining NOL carries forward to next year
4. Track NOL vintages and amounts on a schedule

### Strategic Considerations
- 80% limitation means NOLs take longer to absorb than pre-TCJA
- In low-income years, NOL deduction may be small (80% of small number)
- Consider timing large deductions to avoid creating excess NOLs that may take years to use
- **State NOL rules vary** — IL follows federal with modifications

## Like-Kind Exchanges (Section 1031)

### Current Law (Post-TCJA)
- Applies ONLY to **real property** (real estate)
- Personal property (equipment, vehicles, artwork, crypto) no longer qualifies
- Both relinquished and replacement property must be held for business or investment use
- Primary residences do NOT qualify (but mixed-use properties may partially qualify)

### Mechanics

**Timeline** (starts when relinquished property closes):
- **Day 0**: Close on sale of relinquished property. Proceeds go to Qualified Intermediary (QI)
- **Day 45**: Must **identify** replacement property in writing to QI
- **Day 180**: Must **close** on replacement property

**Identification rules** (choose one):
- **3-property rule**: Identify up to 3 properties of any value
- **200% rule**: Identify any number of properties whose FMV doesn't exceed 200% of relinquished property
- **95% rule**: Identify any number if you acquire 95% of aggregate FMV identified

### Qualified Intermediary (QI)
- **Mandatory**: Taxpayer cannot touch the funds at any point
- QI holds sale proceeds and uses them to acquire replacement property
- Cannot use: agent, attorney, accountant, broker, or related party as QI
- QI should be bonded/insured — no federal requirement for QI licensing

### Boot — Taxable Portion
- **Boot**: Any non-like-kind property received in the exchange
- Common boot: cash received, debt relief (mortgage paid off without replacement)
- Boot is taxable to the extent of realized gain
- **Mortgage boot**: If replacement property has less debt than relinquished, the debt relief = boot
- Strategy: Ensure replacement property value AND debt equal or exceed relinquished property

### Depreciation Recapture
- Unrecaptured Section 1250 gain is NOT deferred — it carries forward to the replacement property
- If boot is received, depreciation recapture is recognized first (before capital gain)
- Replacement property continues the depreciation schedule of the relinquished property (for the exchanged basis)
- New basis portion (any additional investment) starts fresh depreciation

### Reverse Exchange
- Acquire replacement property BEFORE selling relinquished property
- Exchange Accommodation Titleholder (EAT) holds title to replacement property
- Must complete exchange within 180 days
- More complex and expensive than standard forward exchange
- Useful in competitive real estate markets

### Related Party Rules
- Related party exchanges allowed BUT both parties must hold their properties for **2 years**
- If either party disposes within 2 years: exchange is disqualified, gain recognized retroactively
- Related parties: family members, >50% owned entities (Section 267(b))

### Common Strategies
- **Upgrade**: Exchange smaller rental for larger rental (scale portfolio)
- **Diversify**: Exchange single property for multiple properties
- **Relocate**: Exchange property in one market for another
- **Eliminate management**: Exchange hands-on rental for NNN lease or DST
- **Step-up at death**: Hold 1031 property until death — heirs get stepped-up basis

### Form 8824
- Filed for the year of the exchange
- Report relinquished and replacement property details
- Calculate recognized gain, deferred gain, and new basis
- Must file even if all gain is deferred

## Installment Sales (Section 453)

### How It Works
- Spread gain recognition over the payment period (defer tax)
- Each payment contains: return of basis + gain + interest
- **Gross profit ratio** = Total gain / Total contract price
- Taxable gain per payment = Payment x Gross profit ratio

### Example
Property sold for $500,000. Basis = $200,000. Gain = $300,000.
- Gross profit ratio = $300,000 / $500,000 = 60%
- Buyer pays $100,000/year for 5 years
- Each year: $100,000 x 60% = $60,000 taxable gain + interest on unpaid balance

### Form 6252
- Filed each year a payment is received
- Calculates installment sale income
- Separate Form 6252 for each installment sale

### Interest Requirements
- Seller must charge adequate interest (at least the Applicable Federal Rate)
- If interest is below AFR: IRS **imputes** interest at AFR (Sections 483, 1274)
- Imputed interest: portion of each payment reclassified from principal to interest
- Increases seller's interest income, decreases gain recognized
- Current AFRs published monthly by IRS (Revenue Rulings)

### Restrictions — Cannot Use Installment Method For
- **Inventory**: Dealer sales of property held for sale to customers
- **Depreciable property between related parties**: Gain recognized in year of sale (Section 453(g))
- **Publicly traded securities**: Gain recognized when disposed
- **Depreciation recapture**: Section 1245 recapture recognized in full in year of sale (not spread)
- Section 1250 recapture: also recognized in year of sale

### Election Out
- Taxpayer can elect to recognize ALL gain in the year of sale
- Election made on return for the year of sale
- Why elect out: if expecting higher tax rates in future years, or want to use losses/deductions currently available

### Common Scenarios
- **Selling a business**: Earn-out or seller financing over 3-10 years
- **Real estate**: Seller financing to buyer (carry the note)
- **Retirement**: Spread gain over retirement years (lower tax brackets)
- **Related party sales**: Complex rules — gain may be accelerated if buyer resells within 2 years

### Related Party Resale Rule (Section 453(e))
- If related-party buyer resells within **2 years**: remaining deferred gain is triggered for the original seller
- Prevents using installment sales between family members as a tax avoidance step transaction

### Pledge Rule
- If installment obligation is used as **collateral for a loan**: treated as a payment (gain recognized)
- Prevents borrowing against the note to access cash while deferring tax

## Passive Activity Loss Rules (Section 469) — Detail

### Two Categories of Income
1. **Active/nonpassive**: Wages, business income where taxpayer materially participates, portfolio income (interest, dividends, capital gains)
2. **Passive**: Business income where taxpayer does NOT materially participate, rental income (generally passive by definition)

### Core Rule
- Passive losses can ONLY offset passive income
- Cannot offset active income, wages, or portfolio income
- Excess passive losses are **suspended** and carried forward
- Released when: passive income arises, or the activity is disposed of

### 7 Material Participation Tests (Any ONE Is Sufficient)

| Test | Requirement |
|------|------------|
| 1 | **500+ hours** of participation in the activity during the year |
| 2 | Taxpayer's participation constitutes **substantially all** participation by all individuals |
| 3 | **100+ hours** AND more than any other individual's participation |
| 4 | **Significant participation activities**: 100+ hours each in multiple activities, with **aggregate 500+ hours** across all |
| 5 | Materially participated in the activity in **any 5 of the prior 10 years** |
| 6 | Activity is a **personal service activity** and taxpayer participated in **any 3 prior years** |
| 7 | **Regular, continuous, and substantial** participation based on facts and circumstances (rarely used, >100 hours minimum) |

### Documentation
- Maintain contemporaneous logs (calendar, time sheets)
- Record: date, hours, activity description
- IRS frequently challenges material participation claims — documentation is critical
- Appointment calendars, emails, and meeting records all help

### Self-Rental Rule (Reg. 1.469-2(f)(6))
- **Rule**: If you rent property to your own business in which you materially participate, net rental **income** is recharacterized as **nonpassive**
- Net rental **losses** remain passive (asymmetric treatment)
- **Impact**: Cannot use self-rental income to absorb passive losses from other activities
- Common scenario: Owner rents office/warehouse to their S-Corp
- The rental income becomes nonpassive, but losses from other rentals stay passive

### $25,000 Rental Exception (Section 469(i))
- **Active participation** in rental real estate (lower bar than material participation)
- Deduct up to **$25,000** of rental losses against active/nonpassive income
- Active participation: making management decisions (approving tenants, repairs, terms)
- **Phase-out**: Reduced by 50% of AGI exceeding $100,000
- **Fully phased out** at $150,000 AGI
- Does NOT apply to limited partners

### Real Estate Professional Exception (Section 469(c)(7))
- If qualifying: rental activities are NOT automatically passive
- **Requirements** (BOTH must be met):
  1. More than 50% of personal services are in real property trades/businesses
  2. More than **750 hours** in real property trades/businesses
- Each rental activity must still meet a material participation test (or elect to group)
- Grouping election: treat all rental activities as a single activity for material participation
- **Spouse's hours count** for the 750-hour test

### Grouping Election (Reg. 1.469-4)
- Combine multiple activities into a **single activity** for material participation testing
- Once grouped, evaluate material participation for the combined activity
- **Factors for appropriate grouping**: common ownership, common control, geographic proximity, business interdependencies
- Election made by filing return treating activities as grouped
- Generally **cannot regroup** once elected (absent material change in facts)
- Strategic: Group activities where participation in one is high to pull others above 500-hour threshold

### Form 8582 Mechanics
1. List each passive activity's income or loss
2. Separate activities with net income from activities with net loss
3. Net passive income offsets passive losses dollar-for-dollar
4. Remaining net passive loss = suspended (carried forward)
5. Apply $25,000 rental exception if applicable
6. Allocate allowed losses among passive activities proportionally

### Disposition Rule
- When you **dispose of your entire interest** in a passive activity in a **fully taxable transaction**:
  - ALL suspended passive losses from that activity become deductible
  - Losses are first applied against gain from the disposition
  - Remaining losses offset other passive income
  - Any remaining losses offset nonpassive income (active, portfolio)
- Must be complete disposition (not partial sale)
- Gift: suspended losses added to basis of gifted interest (not deducted)
- Death: suspended losses deducted on final return only to extent exceeding basis step-up

## Alternative Minimum Tax (AMT)

### 2025 Exemption Amounts

| Filing Status | Exemption | Phase-out Begins | Phase-out Complete |
|--------------|-----------|-----------------|-------------------|
| Single | $88,100 | $626,350 | $978,750 |
| MFJ | $137,000 | $1,252,700 | $1,800,700 |
| MFS | $68,500 | $626,350 | $900,350 |

Phase-out: Exemption reduced by 25 cents for each $1 above threshold.

### AMT Rates
- **26%** on AMTI up to $248,300 (MFJ) / $124,150 (MFS)
- **28%** on AMTI above those thresholds
- LTCG and qualified dividends taxed at regular preferential rates (0%/15%/20%) under AMT

### AMT Calculation
1. Start with taxable income
2. Add back AMT preference items and adjustments
3. Result = Alternative Minimum Taxable Income (AMTI)
4. Subtract AMT exemption
5. Apply AMT rates (26%/28%)
6. Result = Tentative Minimum Tax (TMT)
7. **AMT = TMT minus regular tax** (only pay AMT if TMT > regular tax)

### Common AMT Triggers

**Incentive Stock Options (ISOs)**:
- Bargain element (FMV minus exercise price) at exercise is an AMT adjustment
- NOT included in regular income at exercise — only at AMT
- Can create massive AMT liability in the year of exercise
- **Strategy**: Exercise ISOs gradually over multiple years; sell some shares in the same year to manage AMT exposure

**State and Local Taxes (SALT)**:
- SALT deduction is fully disallowed for AMT purposes
- Post-TCJA $40,000 SALT cap means this is less of an AMT trigger (already limited for regular tax)

**Tax-Exempt Interest from Private Activity Bonds**:
- Interest from private activity bonds is an AMT preference item
- Regular municipal bond interest is NOT an AMT preference
- Check bond type before investing in tax-exempt securities

**Accelerated Depreciation**:
- Pre-TCJA: Difference between accelerated and straight-line depreciation was an AMT adjustment
- **Post-TCJA**: Section 179 and bonus depreciation are generally NOT AMT preference items
- No add-back required for most depreciation under current law

**Other Adjustments**:
- Medical expenses: 7.5% AGI floor applies for both regular and AMT (no difference post-TCJA)
- Miscellaneous itemized deductions: Not deductible for regular OR AMT (no difference post-TCJA)
- Standard deduction: Cannot use for AMT (use itemized amounts — but most AMT adjustments are moot due to TCJA changes)

### Post-TCJA Reality
- **Most taxpayers are NOT subject to AMT** under current law
- Higher exemption amounts + SALT cap + elimination of miscellaneous deductions = fewer AMT triggers
- Primary remaining AMT risk groups:
  - ISO exercises
  - High-income taxpayers in states with income tax above $40K SALT cap
  - Private activity bond investors
  - Taxpayers with large long-term capital gains (lower regular rate can trigger TMT > regular tax)

### AMT Credit Carryforward (Form 8801)
- If you paid AMT due to **timing differences** (not permanent preferences), you generate an AMT credit
- Timing differences: ISO exercise (AMT paid now, but basis adjusted — recovered when stock is sold), depreciation timing
- Permanent preferences: SALT deduction, tax-exempt interest — these do NOT generate AMT credit
- AMT credit can offset regular tax in future years (when regular tax > TMT)
- Carry forward indefinitely until used
- Form 8801: Calculates credit for prior year minimum tax — individuals

### AMT Planning Strategies
1. **ISO exercise planning**: Spread exercises across years, model AMT impact before exercising
2. **Avoid private activity bonds** if near AMT threshold
3. **Time deductions**: Some deductions help for regular tax but not AMT (less relevant post-TCJA)
4. **Capital gains timing**: Large LTCG can push into AMT due to rate differential
5. **Run projections**: Use tax software to model AMT before year-end decisions

## Section 1202 — Qualified Small Business Stock (QSBS)
- **100% exclusion** of gain on sale of QSBS held 5+ years (OBBBA expanded)
- Maximum exclusion: **$10M** or **10x adjusted basis**, whichever is greater (OBBBA increased from $10M)
- OBBBA changes (2025+):
  - Gross asset threshold raised to **$75M** (from $50M)
  - Exclusion cap raised to **$15M** (from $10M)
  - Tiered holding period: 50% exclusion at 3 years, 75% at 4 years, 100% at 5 years
- **Requirements**:
  - Stock must be in a **C-Corporation** (not LLC, S-Corp, or partnership)
  - Corporation must have gross assets under $75M at all times before and immediately after issuance
  - Stock acquired at **original issuance** (not purchased on secondary market)
  - Corporation must be in an **active business** (not investing, banking, insurance, farming, hospitality, professional services)
  - Technology/SaaS businesses generally qualify
- **Excluded gain is also excluded from NIIT** (3.8% net investment income tax)
- LLC-to-C-Corp conversion: If an LLC elects C-Corp treatment (Form 8832), stock issued on conversion may qualify if properly structured
- **Stacking with Section 1244**: Use Section 1244 for downside protection, QSBS for upside (on the same stock if it qualifies for both)
- Form: No specific form — excluded gain simply not reported on Schedule D

## Section 1244 — Small Business Stock Ordinary Loss
- Allows **ordinary loss** treatment (not capital loss) on worthless or sold-at-a-loss stock
- Maximum: **$50,000** per year (single) / **$100,000** (MFJ)
- Excess over the limit is treated as capital loss
- **Requirements**:
  - Stock issued by a **domestic small business corporation** (aggregate paid-in capital ≤ $1M at time of issuance)
  - Stock acquired at **original issuance** for money or property (not services)
  - Corporation derived more than 50% of gross receipts from operations (not passive income) in the 5 years preceding the loss
- **Why it matters**: Ordinary loss offsets ordinary income (wages, business income) dollar-for-dollar with no $3,000 annual limit. Capital losses can only offset capital gains + $3,000 of ordinary income.
- Can apply to both C-Corp and S-Corp stock
- Should be documented at the time of stock issuance (maintain records showing the $1M test was met)

## Section 83(b) Election — Restricted Stock
- When founders/employees receive restricted stock subject to vesting, they can elect under **Section 83(b)** to pay tax on the stock's value at **grant date** rather than at **vesting date**
- Must file the election with the IRS within **30 days** of receiving the stock — no extensions, no exceptions
- **Strategy**: If stock is worth very little at grant (early-stage startup), pay minimal tax now. If the company grows, all appreciation is taxed as capital gain (not ordinary income) when eventually sold.
- **Risk**: If the stock never vests (you leave the company), you cannot recover the tax paid
- Particularly valuable for: startup founders receiving initial stock grants, early employees with stock grants
- The election applies to the specific stock grant, not globally

## Controlled Group Rules for Retirement Plans (Section 414)
- When one person owns **80%+ of two or more businesses** (directly or through attribution), the businesses are a **controlled group**
- IRC Section 414(b) (parent-subsidiary) and 414(c) (brother-sister)
- **Impact on retirement plans**: All employees of ALL entities in the controlled group must be considered together for:
  - Coverage testing (Section 410(b))
  - Nondiscrimination testing (Section 401(a)(4))
  - Top-heavy testing (Section 416)
  - Contribution/benefit limits
- **Practical effect**: If one LLC has employees, you may need to cover them in ANY retirement plan maintained by ANY entity in the group
- **Strategy**: If controlled group applies, consider a single plan covering all entities or carefully structure plans to pass coverage testing
- **Solo 401(k) risk**: A Solo 401(k) is only available if you have no eligible employees other than the owner and spouse. If a controlled group entity has employees, the Solo 401(k) in another entity may be disqualified.
- Consult with a retirement plan administrator if you own multiple businesses with employees
