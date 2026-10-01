# IRS Penalty Guide — Amounts, Calculations, and Abatement

## Civil Penalties

### Accuracy-Related Penalties (IRC Section 6662)

| Penalty | Rate | Trigger | IRC Section |
|---------|------|---------|-------------|
| Negligence | 20% of underpayment | Failure to make reasonable attempt to comply | 6662(b)(1) |
| Substantial understatement | 20% of underpayment | Understatement > greater of 10% of tax or $5,000 | 6662(b)(2) |
| Substantial valuation misstatement | 20% of underpayment | Value/basis claimed is 150%+ of correct | 6662(b)(3) |
| Gross valuation misstatement | 40% of underpayment | Value/basis claimed is 200%+ of correct | 6662(h) |
| Transaction lacking economic substance | 20% or 40% | Strict liability (no reasonable cause defense) | 6662(b)(6) |

**Substantial understatement** = understatement exceeds the GREATER of:
- 10% of the tax required to be shown on the return, OR
- $5,000 ($10,000 for C-Corps)

**Defense**: Adequate disclosure (Form 8275) + reasonable basis, OR substantial authority for position

### Fraud Penalty (IRC Section 6663)
- **Rate**: 75% of the underpayment attributable to fraud
- **Burden of proof**: IRS must prove fraud by clear and convincing evidence
- **Badges of fraud**: Understatement of income, fictitious deductions, two sets of books, destruction of records, concealment of assets, failure to cooperate

### Filing and Payment Penalties

| Penalty | Rate | Maximum | IRC Section |
|---------|------|---------|-------------|
| Failure to file | 5% of unpaid tax per month | 25% | 6651(a)(1) |
| Failure to pay | 0.5% of unpaid tax per month | 25% | 6651(a)(2) |
| Combined max (file + pay) | N/A | 47.5% (22.5% FTF + 25% FTP) | |
| Min FTF penalty (>60 days late) | Lesser of $510 or 100% of tax | | |
| FTP during installment agreement | 0.25% per month (reduced) | 25% | |

**If both apply**: Failure-to-file penalty is reduced by failure-to-pay penalty for overlapping months.

### Estimated Tax Underpayment (IRC Section 6654)
- **Rate**: Federal short-term rate + 3 percentage points (~7-8% as of 2025)
- **Calculated per quarter** — even if later quarters overpay, earlier underpayments still accrue
- **No penalty if**: Total tax owed after credits/withholding is less than $1,000

### Information Return Penalties (IRC Sections 6721-6722)

| Timing | Penalty Per Return | Max Per Year (Small Business) |
|--------|-------------------|------------------------------|
| Filed within 30 days | $60 | $630,500 |
| Filed by August 1 | $130 | $1,891,500 |
| Filed after August 1 or not filed | $310 | $3,783,000 |
| Intentional disregard | $660 (or 10% of amount) | No maximum |

Applies to: 1099-NEC, 1099-MISC, 1099-K, W-2, and all other information returns.

**Small business** = average annual gross receipts ≤$5M for the 3 prior years.

### Entity Late Filing Penalties

| Entity | Penalty | Maximum | IRC Section |
|--------|---------|---------|-------------|
| Partnership (Form 1065) | $235/partner/month | 12 months | 6698 |
| S-Corp (Form 1120-S) | $235/shareholder/month | 12 months | 6699 |

**Example**: 3-partner LLC files 1065 six months late:
- Penalty = $235 x 3 partners x 6 months = **$4,230**

### FBAR Penalties (31 USC 5321)

| Violation | Penalty |
|-----------|---------|
| Non-willful | Up to **$16,117** per violation (per account, per year) |
| Willful | Greater of **$161,177** or **50% of account balance** per violation |
| Criminal (willful) | Up to $250,000 fine + 5 years imprisonment |

### Other Penalties

| Penalty | Amount | Trigger |
|---------|--------|---------|
| Frivolous return | $5,000 | IRC 6702 |
| Erroneous refund claim | 20% of excessive amount | IRC 6676 |
| Failure to report foreign gifts >$100K | 5% of amount per month, max 25% | IRC 6039F |
| Failure to file Form 8300 (cash >$10K) | Up to $27,965 per violation | IRC 6721 |

## Penalty Exposure Calculation

### Step 1: Estimate the Understatement
For each questionable position, estimate:
- The amount of additional tax if the IRS disallows the position
- This is the "underpayment" that penalties are based on

### Step 2: Apply Applicable Penalty Rate

**If position lacks substantial authority:**
```
Accuracy penalty = Underpayment x 20%
```

**If civil fraud proven:**
```
Fraud penalty = Underpayment x 75%
```

### Step 3: Add Interest
- Interest runs from the due date of the return
- Rate = federal short-term rate + 3% (individual)
- Compounded daily
- Interest on both the tax AND the penalty

### Step 4: Total Exposure
```
Total = Additional Tax + Penalty + Interest
```

### Example Calculation
Questionable home office deduction generates $5,000 in additional tax:

| Component | Amount |
|-----------|--------|
| Additional tax | $5,000 |
| Accuracy penalty (20%) | $1,000 |
| Interest (~8% for 2 years) | ~$960 |
| **Total exposure** | **~$6,960** |

## Penalty Abatement

### First-Time Abatement (FTA)
**Eligibility requirements** (all must be met):
1. No penalties assessed in the **3 prior tax years** (penalties abated don't count)
2. All required returns have been **filed** (or valid extensions)
3. All tax has been **paid** (or on an approved installment agreement)

**Applies to:**
- Failure to file (FTF)
- Failure to pay (FTP)
- Failure to deposit (FTD) — payroll taxes

**Does NOT apply to:**
- Accuracy-related penalties
- Fraud penalties
- Estimated tax penalties
- Information return penalties
- Entity late filing penalties (1065, 1120-S)

**How to request:**
1. Call IRS at 800-829-1040 (easiest — agents can apply immediately)
2. Write a letter requesting FTA
3. Include: "I am requesting first-time abatement relief under IRM 20.1.1.3.6"

### Reasonable Cause
**When FTA is not available**, argue reasonable cause:

**Factors IRS considers:**
1. What happened and when
2. Whether taxpayer exercised ordinary business care and prudence
3. Whether circumstances were beyond taxpayer's control

**Common reasonable cause arguments:**
- Death, serious illness, or incapacitation of taxpayer or immediate family
- Fire, natural disaster, or other casualty
- Inability to obtain records
- Reliance on advice of tax professional (must show advisor was competent and given complete information)
- IRS error or misinformation
- First-time penalty (if FTA unavailable, reasonable cause may still work for first-time offenders)

**How to request:**
- Respond to penalty notice with explanation and supporting documentation
- Form 843 (Claim for Refund and Request for Abatement) if penalty already paid
- Include specific facts, dates, and documentation

### Statutory Exceptions for Estimated Tax
No penalty if:
1. Total tax after credits/withholding < $1,000
2. Withholding/estimated payments ≥ 90% of current year tax
3. Withholding/estimated payments ≥ 100% of prior year tax (110% if AGI > $150,000)
4. Taxpayer retired or became disabled during the tax year (after age 62)

### Penalty Abatement for Small Partnerships/S-Corps
Revenue Procedure 84-35 provides reasonable cause relief for small partnerships that file late if:
- Partnership has 10 or fewer partners
- Each partner reported their share of income on a timely return
- Partnership (not individual partners) failed to file on time

## Audit Defense Best Practices

### If You Receive a Notice
1. **Don't panic** — most notices are routine correspondence audits
2. **Read carefully** — identify exactly what the IRS is questioning
3. **Respond by the deadline** (usually 30 days)
4. **Provide only what's requested** — don't volunteer additional information
5. **Consider professional representation** (CPA, EA, or tax attorney)

### Types of IRS Notices

| Notice | What It Means |
|--------|--------------|
| CP2000 | Proposed adjustment — income mismatch |
| CP2501 | Information request — potential mismatch |
| Letter 525 | Audit notification — specific items under examination |
| Letter 566 | Examination appointment letter |
| CP504 | Intent to levy — unpaid balance |
| Letter 3172 | Final notice of intent to levy |

### Representation Rights
- CPA, Enrolled Agent, or attorney can represent you (Form 2848 — Power of Attorney)
- You do NOT need to attend an audit in person if properly represented
- Never go to a field audit without professional representation

### Burden of Proof
- **General rule**: Taxpayer has the burden of proof for deductions and credits
- **Exception**: IRC Section 7491 shifts burden to IRS if taxpayer:
  - Introduces credible evidence
  - Maintained required records
  - Cooperated with IRS requests
- **Fraud**: IRS always has the burden of proving fraud (clear and convincing evidence)

### Documentation That Satisfies Examiners
- **Contemporaneous records** — made at or near the time of the expense
- **Corroborating evidence** — bank statements + receipts (both, not just one)
- **Business purpose** — documented before or at the time, not reconstructed
- **Consistency** — records should be consistent across years
- **Organization** — well-organized records create a positive impression and expedite audits
