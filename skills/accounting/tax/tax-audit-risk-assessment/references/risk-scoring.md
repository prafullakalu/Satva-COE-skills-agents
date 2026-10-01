# IRS Audit Risk Scoring Model

Weighted scoring model for assessing audit probability. Score each applicable
category, then calculate weighted overall score.

## Category Weights

| Category | Weight | What It Measures |
|----------|--------|-----------------|
| Income Reporting | 25% | Unreported income, 1099 matching, cash business indicators |
| Deduction Ratios | 20% | Schedule C deductions vs income, specific item thresholds |
| Entity Compliance | 15% | Reasonable comp, K-1 accuracy, basis tracking, filing |
| Documentation | 15% | Receipt quality, contemporaneous records, logs |
| Special Positions | 15% | Home office, hobby loss, REPS, crypto, related party |
| Historical Factors | 10% | Prior audits, compliance history, return complexity |

## Scoring Each Category (0-100)

### Income Reporting (25% weight)

| Factor | Score | Trigger |
|--------|-------|---------|
| All income reported, clean 1099 matching | 0-5 | W-2/1099 income matches return exactly |
| Minor discrepancies in 1099 amounts | 10-20 | Small differences (rounding, timing) |
| Cash-intensive business, adequate records | 20-35 | Restaurant, retail, services — but with POS records |
| Some 1099 income potentially unreported | 40-60 | Discrepancies between issued 1099s and reported income |
| Cash business with no POS system | 50-70 | High cash volume, minimal documentation |
| 1099 income clearly unreported | 80-100 | IRS computer matching will auto-flag |

### Deduction Ratios (20% weight)

| Factor | Score | Trigger |
|--------|-------|---------|
| Deduction ratio <40% of gross receipts | 0-10 | Well within norms |
| Deduction ratio 40-50% | 10-25 | Normal range for most businesses |
| Deduction ratio 50-55% | 25-40 | Above average, documentation important |
| Deduction ratio 55-63% | 40-60 | Elevated DIF attention |
| Deduction ratio >63% | 60-85 | High DIF score territory |
| Schedule C loss (business deductions > income) | 70-90 | Especially if offsetting W-2 income |
| Schedule C loss 3+ consecutive years | 85-100 | Hobby loss trigger (IRC Section 183) |

**Specific deduction thresholds:**
- Charitable >5% AGI: +10 points
- Charitable >10% AGI: +20 points
- Charitable >20% AGI: +35 points
- Meals >10% of gross receipts: +15 points
- Vehicle 100% business use: +20 points
- Home office + Schedule C loss: +25 points

### Entity Compliance (15% weight)

| Factor | Score | Trigger |
|--------|-------|---------|
| All entity returns filed on time, K-1s match | 0-10 | Clean compliance |
| S-Corp with reasonable salary (40-60% of profit) | 0-15 | Within accepted range |
| S-Corp salary 30-40% of profit | 20-35 | Below typical range |
| S-Corp salary 20-30% of profit | 35-55 | IRS attention likely |
| S-Corp salary <20% of profit | 55-80 | High reclassification risk |
| S-Corp zero salary | 80-100 | Known enforcement target |
| Late-filed entity returns | 20-35 | Penalty + compliance flag |
| K-1 discrepancies between entities and 1040 | 30-50 | IRS computer matching catches this |
| Missing basis tracking (Form 7203) | 15-25 | Required for S-Corp shareholders |
| Related party transactions without documentation | 40-65 | Between commonly-owned entities |

### Documentation (15% weight)

| Factor | Score | Trigger |
|--------|-------|---------|
| Complete records, contemporaneous logs | 0-10 | Receipts, mileage log, home office docs |
| Most records available, some gaps | 10-25 | Missing some receipts but have bank statements |
| Relying primarily on bank statements | 25-45 | No individual receipts — bank statements alone are weak |
| Mileage log not contemporaneous | 30-50 | Reconstructed at year-end |
| Missing meal documentation (5 elements) | 20-40 | No record of who/purpose/relationship |
| No home office measurements documented | 25-40 | Claiming home office without floor plan |
| Major documentation gaps | 50-75 | Missing categories of records |
| No organized records | 75-100 | Significant compliance risk |

### Special Positions (15% weight)

| Factor | Score | Trigger |
|--------|-------|---------|
| No special positions claimed | 0-5 | Straightforward return |
| Home office (simplified method) | 5-10 | Low risk |
| Home office (actual method, profitable business) | 10-20 | Moderate risk |
| Home office (actual method, business loss) | 35-55 | Significant flag |
| REPS claimed (750+ hours documented) | 25-45 | Heavily scrutinized |
| REPS claimed (hours not well-documented) | 55-80 | Very high risk |
| Hobby loss risk (side business, 2+ years losses) | 30-50 | Approaching 3-of-5 test |
| Hobby loss trigger (3+ years of losses) | 65-85 | IRS presumption triggered |
| Crypto trading reported on Form 8949 | 5-15 | Compliant reporting |
| Crypto trading not fully reported | 50-80 | IRS has exchange data |
| Digital assets question answered incorrectly | 70-90 | False statement on return |
| Related party transactions between multiple LLCs | 25-50 | Depending on documentation quality |
| Conservation easement donation | 60-90 | Listed transaction territory |
| Large non-cash charitable donation without appraisal | 50-75 | Form 8283 requirement |

### Historical Factors (10% weight)

| Factor | Score | Trigger |
|--------|-------|---------|
| Clean compliance history, no prior audits | 0-5 | Lowest risk |
| W-2 only income <$100K | 0-5 | ~0.2% audit rate |
| Simple return, few schedules | 5-10 | Low complexity |
| Income $100K-$200K with Schedule C | 15-25 | Slightly elevated |
| Income $200K-$500K | 25-40 | ~0.5% audit rate bracket |
| Income $500K-$1M | 40-60 | ~0.8% audit rate bracket |
| Income $1M+ | 55-75 | ~1.5%+ audit rate, IRS focus area |
| Prior audit | 15-30 | Depending on outcome |
| Prior audit with changes/adjustments | 30-50 | Follow-up audits more likely |
| First-time filing (no prior returns) | 20-35 | Elevated scrutiny |
| Return filed significantly late | 15-30 | Compliance flag |
| Complex return (6+ schedules, foreign items) | 15-30 | More examination points |

## Overall Score Calculation

```
Overall Score = (Income_Score x 0.25) + (Deduction_Score x 0.20) +
               (Entity_Score x 0.15) + (Documentation_Score x 0.15) +
               (Special_Score x 0.15) + (Historical_Score x 0.10)
```

## Grading Scale

| Grade | Score | Risk Level | Recommended Action |
|-------|-------|------------|-------------------|
| A | 0-15 | Very Low | No action needed. Maintain current practices. |
| B | 16-35 | Low | Minor improvements. Strengthen documentation for claimed deductions. |
| C | 36-55 | Moderate | Review flagged items. Improve documentation. Consider adjusting aggressive positions. |
| D | 56-75 | High | Professional review recommended. Consider amending positions. Strengthen all documentation. |
| F | 76-100 | Very High | Immediate professional review. Likely compliance issues. Consider voluntary disclosure if warranted. |

## IRS Audit Rates by Income Level (FY 2024)

For context when presenting risk scores:

| Income Level | Approximate Audit Rate |
|---|---|
| Under $25K (with EITC) | ~1.0% (correspondence) |
| $25K-$100K | ~0.2% |
| $100K-$200K | ~0.3% |
| $200K-$500K | ~0.5% |
| $500K-$1M | ~0.8% |
| $1M-$5M | ~1.1-1.5% |
| $5M-$10M | ~2.0% |
| $10M+ | ~2.5-3.0%+ |
| Schedule C >$100K gross receipts | ~1-2% |

Note: IRS committed to NOT increasing audit rates for taxpayers under $400K AGI
using new IRA funding. Focus is on high-income non-compliance and large partnerships.

## DIF Score Factors (Classified, but Inferred)

The IRS Discriminant Information Function (DIF) score is secret, but these factors
are known to influence it based on practitioner experience:

1. **Deduction-to-income ratios** by line item vs. statistical norms for income bracket
2. **Schedule C profit margins** vs. NAICS industry code averages
3. **Charitable contributions as % of AGI** vs. bracket norms
4. **Itemized deductions vs. standard deduction gap** (unusually high itemized)
5. **Multiple Schedule C businesses** (especially with offsetting losses)
6. **Return complexity** (more schedules = more DIF points)
7. **Prior compliance history** (UIDIF score uses this separately)
