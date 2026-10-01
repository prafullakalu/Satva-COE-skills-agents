# Entity Structure Optimization — S-Corp vs LLC Analysis

## The Core Decision

An LLC is a **legal entity** (state-level). S-Corp is a **tax classification** (IRS).
They are not mutually exclusive. Most small businesses form an LLC and elect S-Corp
taxation via Form 2553.

## How S-Corp Saves Money

### Default LLC (Sole Prop or Partnership)
- All net profit subject to **15.3% self-employment tax**
  - 12.4% Social Security (up to wage base: $176,100 in 2025, $184,500 in 2026)
  - 2.9% Medicare (no cap)
  - 0.9% Additional Medicare on income >$200K (single) / >$250K (MFJ)
- SE tax calculated on 92.35% of net income
- 50% of SE tax deductible above-the-line

### S-Corp Elected LLC
- Owner pays payroll taxes ONLY on **reasonable salary** (W-2 wages)
- Remaining profit distributed as **dividends** (no SE tax)
- Net result: SE tax savings on the distribution portion

## Break-Even Analysis

### S-Corp Additional Costs
- Payroll service: $500-$2,000/year
- Form 1120-S preparation: $500-$1,500/year
- Payroll tax filings (Form 941 quarterly): included in payroll service
- IL replacement tax: 1.5% of net income (applies to both LLC and S-Corp)
- Additional bookkeeping complexity

### Break-Even Calculation

| Net Profit | LLC SE Tax | S-Corp SE Tax (40% salary) | S-Corp Costs | Net Savings |
|------------|-----------|---------------------------|--------------|-------------|
| $40,000 | ~$5,652 | ~$2,448 | ~$2,000 | ~$1,204 |
| $60,000 | ~$8,478 | ~$3,672 | ~$2,000 | ~$2,806 |
| $80,000 | ~$11,304 | ~$4,896 | ~$2,000 | ~$4,408 |
| $100,000 | ~$14,130 | ~$6,120 | ~$2,000 | ~$6,010 |
| $150,000 | ~$21,194 | ~$9,180 | ~$2,000 | ~$10,014 |
| $200,000 | ~$26,532 | ~$12,240 | ~$2,500 | ~$11,792 |

**Rule of thumb**: S-Corp typically makes sense at **$50,000-$60,000+ net profit** after
considering all additional costs.

## Reasonable Salary Determination

### IRS Requirements
- Must be "reasonable compensation" for services actually rendered
- IRS examines: training, experience, duties, time devoted, comparable salaries

### Key Court Cases
- **David E. Watson, P.C. v. US** (2012): CPA paying $24K salary on $200K+ income — reclassified
- **Joseph M. Grey Public Accountant** (2003): Zero salary rejected
- **Veterinary Surgical Consultants** (2002): $0 salary on $600K+ income rejected
- **Sean McAlary Ltd** (2013): Real estate agent's below-market salary upheld by Tax Court

### Safe Harbor Approach
- **40-60% of net business income** as salary is the commonly cited range
- Benchmark against BLS Occupational Employment Statistics for your role
- Consider: hours worked, complexity, local market rates
- Document the analysis — create a reasonable compensation memo

### Risk of Getting It Wrong
- IRS can reclassify distributions as wages retroactively
- Results in: back payroll taxes + penalties + interest
- Both employee AND employer portions assessed
- Late deposit penalties (up to 15%) may apply

## QBI Deduction Interaction

### The Trade-Off
- S-Corp salary is **NOT** qualified business income (QBI)
- Only the pass-through profit (distribution) qualifies for the 20% QBI deduction
- Higher salary = lower QBI deduction BUT lower SE tax
- Must optimize both together

### Example at $150,000 Net Profit (MFJ, below SSTB threshold)

| Scenario | Salary | Distribution | SE Tax Savings | QBI Lost | Net Benefit |
|----------|--------|-------------|----------------|----------|-------------|
| LLC (no S-Corp) | N/A | $150K as SE income | Base | 20% of $150K = $30K QBI | Base |
| S-Corp 40% salary | $60K | $90K | ~$8,262 saved | 20% of $90K = $18K QBI | ~$5,862 net |
| S-Corp 50% salary | $75K | $75K | ~$6,885 saved | 20% of $75K = $15K QBI | ~$4,385 net |
| S-Corp 60% salary | $90K | $60K | ~$5,508 saved | 20% of $60K = $12K QBI | ~$2,508 net |

*Net benefit = SE tax saved minus value of lost QBI deduction (at marginal rate)*

### SSTB Considerations (Specified Service Trades or Businesses)
SSTBs include: health, law, accounting, consulting, athletics, financial services, brokerage

- Below SSTB threshold: full 20% QBI deduction regardless of business type
- Above threshold: QBI deduction phases out for SSTBs
- If fully phased out, the QBI trade-off disappears — maximize S-Corp savings

**2025 SSTB phase-out**: $191,950-$241,950 (Single), $383,900-$483,900 (MFJ)
**2026 SSTB phase-out (OBBBA expanded)**: ~$196K-$246K (Single), ~$392K-$542K (MFJ)

## Form 2553 Filing

### Deadline
- **March 15** of the year the election is to take effect
- That's 2 months and 15 days into the tax year (for calendar year taxpayers)

### Late Election Relief
- Available under **Rev. Proc. 2013-30** if:
  - Election intended to be effective for the tax year
  - Reasonable cause for late filing
  - All shareholders consent
  - Entity has been treated as S-Corp on all filed returns
- Can be filed with the first Form 1120-S if eligible

### Revocation
- S-Corp election can be revoked with consent of shareholders holding >50% of shares
- Effective date: beginning of tax year (if filed by March 15) or beginning of next year
- After revocation, cannot re-elect S-Corp for 5 tax years without IRS consent

## Illinois-Specific Considerations

### IL Replacement Tax
- 1.5% on net income for both partnerships AND S-Corps (no difference)
- Not a factor in the LLC vs S-Corp decision

### IL PTE Tax Election
- Available for both partnerships and S-Corps
- Works identically regardless of entity choice
- 4.95% at entity level, credit to owners

### IL Annual Report
- $75 fee regardless of entity type (LLC requirement)
- S-Corp election doesn't change state LLC status

## Multi-LLC Considerations

When the user has multiple LLCs, each must be analyzed separately:
- S-Corp election is per-entity
- Some LLCs may benefit from S-Corp while others don't
- Consider aggregate reasonable salary across all entities
- Payroll can sometimes be consolidated through one entity

## When NOT to Elect S-Corp

- Net profit consistently below $40,000
- Business has significant losses (S-Corp basis rules are more restrictive)
- Owner needs to contribute and withdraw capital frequently (S-Corp has one class of stock rule)
- Business has foreign shareholders (S-Corp restriction)
- Business has more than 100 shareholders (S-Corp limit)
- Real estate with significant depreciation (LLC/partnership gives better flexibility)
- Planning to take on investors with different economic rights
