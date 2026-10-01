# IRS Audit Red Flags — Complete Reference

30+ specific audit triggers with thresholds, severity scores, and mitigation strategies.

## Critical Red Flags (Severity: 8-10)

### RF-01: Unreported Income (1099/W-2 Mismatch)
- **Severity**: 10
- **How detected**: IRS Automated Underreporter (AUR) program matches information returns to tax returns
- **Threshold**: Any discrepancy between issued 1099s/W-2s and reported income
- **Result**: Automatic CP2000 notice (proposed adjustment)
- **Mitigation**: Report ALL income. If a 1099 is incorrect, report it and attach explanation. Contact issuer for corrected 1099.

### RF-02: Cash Business with Low Reported Income
- **Severity**: 9
- **How detected**: DIF score compares reported income to BLS industry averages for NAICS code
- **Threshold**: Reported income significantly below industry median for business type
- **Industries targeted**: Restaurants, bars, car washes, laundromats, hair salons, taxi/rideshare, cash-heavy retail
- **IRS methods**: Bank deposit analysis, net worth method, markup method
- **Mitigation**: Use POS system, document all income sources, maintain daily cash logs

### RF-03: Schedule C Losses 3+ Consecutive Years (Hobby Loss)
- **Severity**: 8
- **How detected**: IRS tracks pattern of losses across tax years
- **Threshold**: Business shows net loss in 3 or more of the last 5 consecutive years (2 of 7 for horse activities)
- **IRC Section**: 183 — Activities Not Engaged in for Profit
- **Consequence**: All expenses disallowed; income still taxable (2018-2025 under TCJA)
- **Mitigation**: Show profit in at least 3 of 5 years. Document business intent (business plan, separate bank account, expertise, time spent). Consider Form 5213 to defer determination (but this flags the return).

### RF-04: S-Corp Zero/Minimal Officer Compensation
- **Severity**: 9
- **How detected**: IRS targets S-Corps with distributions but zero/low W-2 wages to officers
- **Threshold**: Officer compensation below reasonable market rate for services performed
- **Key cases**: Watson v. Commissioner ($24K on $200K+ reclassified), Grey ($0 salary rejected)
- **Consequence**: IRS reclassifies distributions as wages — back payroll taxes + penalties + interest
- **Mitigation**: Pay 40-60% of net income as salary, benchmark against BLS data, document reasonable comp analysis

### RF-05: Offshore Accounts Not Disclosed
- **Severity**: 10
- **How detected**: FBAR (FinCEN 114), FATCA (Form 8938), foreign bank reporting, John Doe summonses
- **Threshold**: Foreign accounts with aggregate balance >$10,000 at any point during year
- **Penalties**: Non-willful: up to $16,117/violation. Willful: greater of $161,177 or 50% of account balance
- **Mitigation**: File FBAR by April 15 (auto-extension to Oct 15). File Form 8938 if thresholds met. Consider Streamlined Filing Compliance if late.

### RF-06: Related Party Transactions Without Documentation
- **Severity**: 8
- **How detected**: IRS examines transactions between commonly owned entities
- **Threshold**: Any transaction between entities with >50% common ownership (IRC Section 267/707)
- **Targeted items**: Management fees, rent, loans, shared expenses between LLCs
- **Mitigation**: Arm's-length pricing, written agreements, promissory notes with AFR interest, contemporaneous documentation

### RF-07: Crypto Trading Without Form 8949
- **Severity**: 8
- **How detected**: IRS obtains data from exchanges via John Doe summonses + 1099-DA reporting (2025+)
- **Threshold**: Any disposition of cryptocurrency not reported; "Digital Assets" question answered "No" when should be "Yes"
- **Consequence**: Answering the digital assets question incorrectly is treated as a false statement
- **Mitigation**: Report every sale, trade, exchange on Form 8949. Use crypto tax software. Answer digital assets question truthfully.

## High Red Flags (Severity: 5-7)

### RF-08: Schedule C Deduction Ratio >60%
- **Severity**: 7
- **Threshold**: Total Schedule C deductions / Gross receipts > 60%
- **Context**: Average deduction ratios vary by industry (52-55% is typical for many service businesses)
- **Mitigation**: Ensure all deductions are legitimate and well-documented. Compare to industry averages.

### RF-09: High Income ($500K+)
- **Severity**: 6
- **Threshold**: AGI above $500,000
- **Audit rate**: ~0.8% ($500K-$1M), ~1.5%+ ($1M+)
- **Note**: IRS is dramatically increasing audits of $1M+ taxpayers with IRA funding
- **Mitigation**: Meticulous documentation on all items. Professional preparation recommended.

### RF-10: Home Office + Schedule C Loss
- **Severity**: 7
- **Combined signal**: Claiming home office while also reporting a business loss
- **Why flagged**: Home office deduction cannot create a loss (regular method). If business is already at a loss, the home office claim plus the loss looks suspicious.
- **Mitigation**: If legitimate, ensure exclusive-use test is met, document thoroughly. Consider simplified method ($5/sq ft) for lower profile.

### RF-11: Vehicle 100% Business Use
- **Severity**: 6
- **Threshold**: Claiming 100% business use of a passenger vehicle
- **Why flagged**: IRS presumes some personal use for non-commercial vehicles. Very few taxpayers truly use a vehicle 100% for business.
- **Exception**: Legitimate for dedicated commercial vehicles (work trucks, delivery vans)
- **Mitigation**: If truly 100% business, maintain detailed mileage log. Otherwise, claim actual business percentage (typically 60-80%).

### RF-12: Charitable Donations >10% of AGI
- **Severity**: 6
- **Threshold**: Cash or non-cash donations exceeding 10% of AGI
- **Non-cash over $5,000**: Requires Form 8283 + qualified appraisal
- **Non-cash over $500**: Requires Form 8283, Section A
- **Conservation easements**: Under extreme IRS scrutiny (listed transactions)
- **Mitigation**: Keep all receipts. Obtain contemporaneous written acknowledgment for donations $250+. Get qualified appraisals for non-cash >$5,000.

### RF-13: Real Estate Professional Status (REPS) Claim
- **Severity**: 6
- **Requirements**: 750+ hours in real property trades + more than 50% of total personal services
- **Why scrutinized**: Converts rental losses from passive to nonpassive (can offset W-2 income)
- **Common challenge**: IRS questions whether hours are sufficient, especially if taxpayer has a full-time W-2 job
- **Mitigation**: Contemporaneous time log (date, activity, hours, property). One spouse can qualify. Grouping election for multiple properties.

### RF-14: Multiple Schedule C Businesses
- **Severity**: 5
- **Threshold**: Two or more Schedule C businesses, especially if some show losses
- **Why flagged**: Appearance of using one business's losses to offset another's income
- **Mitigation**: Each business must have legitimate separate purpose. Consider entity formation (LLC) for each.

### RF-15: Large Non-Cash Charitable Donations
- **Severity**: 7
- **Threshold**: Non-cash donations >$5,000 (requires qualified appraisal), >$500,000 (must attach appraisal)
- **Specific target**: Syndicated conservation easement donations (listed transaction if value >2.5x investment)
- **Clothing/household items**: Must be in "good or better" condition
- **Mitigation**: Qualified appraisal by certified appraiser. Detailed description of donated property. Complete Form 8283.

## Moderate Red Flags (Severity: 3-4)

### RF-16: Schedule C Deduction Ratio 50-60%
- **Severity**: 4
- **Context**: Somewhat above typical norms but not extreme
- **Mitigation**: Well-organized documentation for all major expense categories

### RF-17: Income $200K-$500K
- **Severity**: 3
- **Audit rate**: ~0.3-0.5%
- **Trend**: Slightly increasing as IRS expands enforcement

### RF-18: Charitable Donations 5-10% of AGI
- **Severity**: 3
- **Context**: Above average for most income brackets but within legal limits
- **Mitigation**: Keep all receipts and acknowledgment letters

### RF-19: Round Number Expenses
- **Severity**: 4
- **Threshold**: Multiple expenses at exactly $500, $1,000, $5,000, etc.
- **Why flagged**: Suggests estimation rather than actual record-keeping
- **Mitigation**: Always report exact amounts. If you're rounding, stop.

### RF-20: Meals >10% of Gross Receipts
- **Severity**: 4
- **Context**: Elevated for most business types. Entertainment industry may be exception.
- **Mitigation**: Document all 5 elements for every meal: amount, date, place, business purpose, business relationship

### RF-21: Complex Return
- **Severity**: 3
- **Threshold**: 6+ schedules, foreign accounts, unusual deductions
- **More examination points**: Each additional schedule creates more DIF scoring opportunities

### RF-22: Late-Filed Return
- **Severity**: 3
- **Correlation**: Late filing correlates with other compliance issues
- **Note**: Filing on extension is NOT late — only filing after the extended due date

### RF-23: Large Education Credits
- **Severity**: 3
- **AOTC**: Up to $2,500/student — must substantiate enrollment (Form 1098-T) and expenses
- **Lifetime Learning**: Up to $2,000/return
- **IRS focus**: False claims of education credits are a known fraud pattern

## Lower Red Flags (Severity: 1-2)

### RF-24: W-2 Only Income Under $200K
- **Severity**: 1
- **Audit rate**: ~0.2%
- **Lowest risk profile when combined with standard deduction**

### RF-25: Standard Deduction Taken
- **Severity**: 1
- **Removes itemized deduction scrutiny entirely**

### RF-26: All Income Has Information Reporting
- **Severity**: 1
- **Clean 1099/W-2 matching eliminates primary auto-flag**

### RF-27: Clean Compliance History
- **Severity**: 1
- **No prior audits, no penalties, all returns filed on time**
- **Qualifies for First-Time Abatement if penalty assessed**

## Illinois-Specific Red Flags

### RF-IL-01: Federal-State Mismatch
- **Severity**: 5
- **Trigger**: IRS adjusts federal return but no amended IL-1040-X filed within 120 days
- **Consequence**: IL statute of limitations remains open indefinitely for that issue

### RF-IL-02: Use Tax Non-Compliance
- **Severity**: 3
- **Trigger**: Online purchases without IL sales tax collected; use tax line on IL-1040 left blank
- **IL actively audits this area**

### RF-IL-03: Residency Audit
- **Severity**: 6
- **Trigger**: Claimed move to no-income-tax state but maintains IL ties
- **Factors**: Driver's license, voter registration, where family resides, time spent in IL

### RF-IL-04: PTE Tax Mismatch
- **Severity**: 4
- **Trigger**: PTE tax paid by entity doesn't match credits claimed on partner's IL-1040

## Statute of Limitations Quick Reference

| Situation | Period | IRC Section |
|-----------|--------|-------------|
| Standard | 3 years from filing/due date | 6501(a) |
| >25% income omitted | 6 years | 6501(e)(1)(A) |
| Fraud | Unlimited | 6501(c)(1) |
| No return filed | Unlimited | 6501(c)(3) |
| Foreign assets >$5K not reported | 6 years | 6501(e)(1)(A) |
| FBAR violations | 6 years | 31 USC 5321 |
| IL: failure to report federal change | Indefinite | IL statute |
