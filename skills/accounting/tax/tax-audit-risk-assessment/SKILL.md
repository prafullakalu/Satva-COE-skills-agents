---
name: tax-audit-risk-assessment
description: >-
  Score a US return's IRS audit risk (1-100, letter grade) from 30+ quantified red flags: Schedule C deduction ratios, meals share, home office plus loss, hobby-loss history, S-corp reasonable compensation, related-party LLC transactions, large charitable and crypto items. Also quantifies penalty exposure, documentation gaps and statute-of-limitations dates. Use for 'audit risk', 'is this deduction risky', 'IRS red flags', 'penalty exposure', 'hobby loss', 'reasonable compensation'. Directional guidance, not a prediction and not tax advice.
metadata:
  department: "accounting"
  domain: "tax"
  owner: "satva-coe"
  status: "beta"
  license: "MIT"
  source: "https://github.com/davidjelinekk/tax-skills-claude-code/tree/main/skills/tax-audit-risk"
---
<!-- Adapted from davidjelinekk/tax-skills-claude-code skills/tax-audit-risk (MIT, Copyright (c) 2025-2026; the LICENSE file names no holder). Modified by Satva: renamed from tax-audit-risk, cross-references repointed, currency caveat added. -->

> **Tax year and jurisdiction.** Upstream targets US federal tax for tax years 2025 and 2026 (post-OBBBA, P.L. 119-21, signed 4 July 2025) with Illinois as the default state. Figures, thresholds and sunset dates change: verify against current IRS and state guidance. Illinois-specific material applies only to Illinois taxpayers. Educational guidance, not tax advice; a licensed CPA or tax attorney makes the binding call.

# IRS Audit Risk Assessment — Red Flag Detection & Risk Scoring

Score a tax return's audit probability, identify specific red flags, quantify
penalty exposure, and recommend improvements to documentation and compliance.

**DISCLAIMER**: Audit risk scoring is based on publicly available data about IRS
enforcement patterns and practitioner experience. The IRS's actual DIF scoring
algorithm is classified. This tool provides directional guidance, not a guarantee
of audit or non-audit outcome.

## When to Use This Skill

- Reviewing a return before filing to identify audit red flags
- Assessing whether a specific deduction or position is risky
- Understanding penalty exposure for an aggressive tax position
- Checking documentation adequacy for claimed deductions
- Evaluating whether an entity structure creates audit risk
- Understanding statute of limitations for a prior return
- Assessing hobby loss risk for a side business
- Evaluating related party transaction compliance across multiple LLCs
- Checking crypto/trading income reporting compliance

## Context Needed

For a comprehensive risk assessment, collect:
1. **Filing status and AGI** — Audit rates vary dramatically by income level
2. **Income sources** — W-2, Schedule C, K-1, investments, crypto
3. **Specific deductions claimed** — Home office, vehicle, charitable, meals, travel
4. **Entity types** — Sole prop, LLC, S-Corp (each has different risk profile)
5. **Years of profitability/loss** — Consecutive losses trigger hobby loss scrutiny
6. **Documentation status** — Do they have receipts, mileage logs, etc.?
7. **Any prior audits?** — History affects future selection

## Risk Scoring Methodology

### Overall Risk Score (1-100)

Load `references/risk-scoring.md` for the complete weighted scoring model.

Score each applicable category, then calculate weighted average:

| Category | Weight | Description |
|----------|--------|-------------|
| Income Reporting | 25% | Unreported income, 1099 matching, cash business |
| Deduction Ratios | 20% | Schedule C deductions vs income, specific item thresholds |
| Entity Compliance | 15% | Reasonable comp, K-1 accuracy, basis tracking |
| Documentation | 15% | Receipt quality, contemporaneous records, logs |
| Special Positions | 15% | Home office, hobby loss, REPS, crypto |
| Historical Factors | 10% | Prior audits, compliance history, return complexity |

### Grading Scale

| Grade | Score | Risk Level | Action |
|-------|-------|------------|--------|
| A | 0-15 | Very Low | No action needed |
| B | 16-35 | Low | Minor documentation improvements |
| C | 36-55 | Moderate | Review flagged items, improve documentation |
| D | 56-75 | High | Consider amending or adjusting positions |
| F | 76-100 | Very High | Professional review strongly recommended |

## Red Flag Checks

Load `references/red-flags.md` for complete thresholds and scoring.

### Critical Red Flags (Score: 8-10 each)
1. **Unreported income** — 1099/W-2 mismatch with return. IRS computers catch this automatically.
2. **Cash business, low reported income** — Income below BLS industry averages for NAICS code.
3. **Schedule C losses 3+ consecutive years** — Triggers hobby loss inquiry (IRC Section 183).
4. **S-Corp zero/minimal officer compensation** — Known IRS enforcement target.
5. **Offshore accounts not disclosed** — FBAR/FATCA non-compliance.
6. **Related party transactions without documentation** — Between commonly-owned LLCs.
7. **Crypto trading with no Form 8949** — "Digital Assets" question answered incorrectly.

### High Red Flags (Score: 5-7 each)
8. **Schedule C deduction ratio >60%** — Well above DIF norms for most industries.
9. **Income >$500K** — Higher audit rate bracket (~0.8%+).
10. **Home office + Schedule C loss** — Combined signals draw attention.
11. **Vehicle 100% business use** — IRS presumes some personal use for passenger vehicles.
12. **Charitable donations >10% of AGI** — Above average; non-cash >$5K requires appraisal.
13. **Rental losses + REPS claim** — 750-hour test is heavily challenged.
14. **Multiple Schedule C businesses** — Especially if some show losses to offset others.
15. **Large non-cash charitable donations** — Conservation easements especially targeted.

### Moderate Red Flags (Score: 3-4 each)
16. **Schedule C deduction ratio 50-60%** — Somewhat above norms.
17. **Income $200K-$500K** — Increasing scrutiny bracket.
18. **Charitable donations 5-10% of AGI** — Above average but not extreme.
19. **Round number expenses** — Multiple expenses at exactly $500, $1,000, etc.
20. **Meals >10% of gross receipts** — Elevated for most business types.
21. **Complex return** — Many schedules, foreign accounts, unusual items.
22. **Late-filed return** — Correlates with compliance issues.
23. **Large education credits** — Must substantiate enrollment and expenses.

### Lower Red Flags (Score: 1-2 each)
24. **W-2 only income <$200K** — Very low audit rate (~0.2%).
25. **Standard deduction taken** — Removes itemized deduction scrutiny.
26. **All income has information reporting** — W-2, 1099 matching is clean.
27. **Clean compliance history** — No prior audits or penalties.

## Assessment Workflow

When the user provides their tax situation:

### Step 1: Collect Information
Gather the context listed above. Calculate key ratios:
- Schedule C deduction-to-gross-receipts ratio
- Charitable donations as % of AGI
- Meals/entertainment as % of gross receipts
- Vehicle business use percentage claimed

### Step 2: Score Each Category
Apply the scoring from `references/risk-scoring.md`:
- Score each applicable red flag (0-10)
- Calculate category scores (weighted by severity)
- Calculate overall weighted score

### Step 3: Generate Risk Report

Structure the output as:

```
## Audit Risk Assessment

### Overall Score: [X]/100 (Grade [A-F])
**Risk Level**: [Very Low / Low / Moderate / High / Very High]

### Risk Breakdown by Category
| Category | Score | Key Findings |
|----------|-------|-------------|
| Income Reporting | X/100 | ... |
| Deduction Ratios | X/100 | ... |
| Entity Compliance | X/100 | ... |
| Documentation | X/100 | ... |
| Special Positions | X/100 | ... |
| Historical | X/100 | ... |

### Red Flags Identified
[List each flag with severity, explanation, and recommendation]

### Penalty Exposure
[Calculate potential penalties if positions are challenged]

### Documentation Gaps
[Specific records that should be improved or created]

### Recommendations
[Prioritized action items to reduce audit risk]

### Statute of Limitations
[When the IRS can no longer audit this return]
```

### Step 4: Penalty Exposure Calculation
Load `references/penalty-guide.md` and calculate:
- Accuracy-related penalty (20% of underpayment) if positions are challenged
- Failure to file/pay penalties if applicable
- Information return penalties (1099s) if missing
- Partnership/S-Corp late filing penalties

### Step 5: Recommendations
Prioritize by impact:
1. **Immediate fixes** — Items that can be corrected before filing
2. **Documentation improvements** — Records to create or improve
3. **Position adjustments** — Deductions to reduce or support better
4. **Structural changes** — Entity or compliance changes for future years

## Illinois-Specific Audit Triggers

- Federal-state mismatch (IL requires 120-day amended return after federal changes)
- Use tax non-compliance (online purchases without IL sales tax)
- Residency audit risk (moved out of IL but maintain IL ties)
- PTE tax credit/deduction mismatch between entity and individual
- Sales tax compliance for tangible goods sellers

## Reference Files

- `references/risk-scoring.md` — Complete weighted scoring model with calculations
- `references/red-flags.md` — All 30+ red flags with specific thresholds and DIF factors
- `references/penalty-guide.md` — Penalty amounts, calculation methods, and abatement rules
