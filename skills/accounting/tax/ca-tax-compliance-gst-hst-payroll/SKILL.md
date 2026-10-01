---
name: ca-tax-compliance-gst-hst-payroll
description: >-
  Canadian business tax reference: GST/HST/PST/QST rates and registration, ITC rules, CPP/EI/income-tax payroll deductions and remittance schedules, T4/T4A deadlines, corporate tax and instalments, SR&ED, and the CRA employee-vs-contractor test. Use for "do we need to register for HST", "CRA payroll remittance due date", "T4A for contractors", "personal services business", "GST/HST ITC documentation". Figures target 2025; verify with CRA.
metadata:
  department: "accounting"
  domain: "tax"
  owner: "satva-coe"
  status: "beta"
  license: "MIT"
  source: "https://github.com/caseonix/canadian-regulatory-compliance/tree/main/skills/canadian-tax-compliance"
---

<!-- Adapted from caseonix/canadian-regulatory-compliance skills/canadian-tax-compliance/SKILL.md (MIT, Copyright (c) 2026 Srivatsa Kasagar). Modified by Satva: added verify-current-figures caveat; merged contractor GST/HST review as a reference. -->

# Canadian Tax Compliance

## GST/HST — Goods and Services Tax / Harmonized Sales Tax

### Rates by Province/Territory

| Province/Territory | GST | Provincial | Total HST/GST |
|-------------------|-----|-----------|--------------|
| Ontario | — | — | 13% HST |
| British Columbia | — | 5% PST (separate) | 5% GST + 5% PST |
| Alberta | — | None | 5% GST only |
| Quebec | — | 9.975% QST (separate) | 5% GST + 9.975% QST |
| Nova Scotia | — | — | 15% HST |
| New Brunswick | — | — | 15% HST |
| Newfoundland & Labrador | — | — | 15% HST |
| PEI | — | — | 15% HST |
| Manitoba | — | 7% RST (separate) | 5% GST + 7% RST |
| Saskatchewan | — | 6% PST (separate) | 5% GST + 6% PST |
| Territories (YT, NT, NU) | — | None | 5% GST only |

### Registration Thresholds
- **Mandatory registration:** Annual taxable supplies exceed **$30,000** in a single calendar quarter or over 4 consecutive quarters
- **Small supplier exemption:** Under $30,000 — may choose not to register, but cannot collect or claim ITCs
- **Voluntary registration:** Advisable even below threshold if significant B2B activity (to claim Input Tax Credits)
- **Non-resident registration:** Non-residents supplying digital services to Canadian consumers must register under the simplified GST/HST regime if supplies exceed $30,000

### Filing Periods and Deadlines

| Annual Taxable Revenue | Filing Frequency | Return Due |
|-----------------------|-----------------|-----------|
| Up to $1.5M | Annual | 3 months after fiscal year-end (payment due same date) |
| $1.5M – $6M | Quarterly | 1 month after quarter-end |
| Over $6M | Monthly | 1 month after month-end |

**Annual filers with $3,000+ net tax:** Must make quarterly instalment payments.

### Input Tax Credits (ITCs)
- Registrants can claim ITCs to recover GST/HST paid on business expenses
- ITCs must be claimed within **4 years** of the reporting period they relate to (2 years for large businesses)
- Requires supporting documentation: invoices showing supplier name, GST/HST number, date, description, and amount
- Partial ITC rules apply for expenses with mixed personal/business use

### Provincial Sales Taxes (PST/QST/RST)
PST (BC, SK), QST (QC), and RST (MB) are separate from GST and have their own registration, collection, and remittance rules:

**BC PST:** Register if making taxable sales in BC; rate is 7% (12% for carbonated beverages/liquor)
**Saskatchewan PST:** 6%; broad base including many services
**Quebec QST:** 9.975%; administered by Revenu Québec (not CRA); file separately
**Manitoba RST:** 7%; administered by Manitoba Finance

---

## Payroll — CPP, EI, and Income Tax Deductions

### Employer Obligations
Every employer paying employment income must:
1. Deduct Canada Pension Plan (CPP) contributions
2. Deduct Employment Insurance (EI) premiums
3. Deduct federal and provincial income tax
4. Remit all deductions to CRA plus employer's share of CPP and EI

### 2025 Rates (verify annually at canada.ca/cra)

| Deduction | Employee Rate | Employer Rate | Annual Maximum (Employee) |
|-----------|--------------|--------------|--------------------------|
| CPP | 5.95% | 5.95% (match) | ~$3,867 |
| CPP2 (second additional) | 4.00% on earnings $73,200–$81,200 | 4.00% (match) | ~$396 |
| EI | 1.66% | 1.66% × 1.4 = 2.32% | ~$1,049 |

Income tax: Use CRA Payroll Deductions tables (TD1 federal + provincial TD1 form)

### Remittance Schedules

| Average Monthly Withholding | Remittance Frequency | Due Date |
|---------------------------|---------------------|---------|
| Less than $3,000 | Monthly | 15th of following month |
| $3,000 – $49,999 | Twice monthly | 25th (for 1st–15th payroll) / 10th of next month (for 16th–end) |
| $50,000+ | Accelerated (up to 3× weekly) | Next Wednesday or Friday after payday |
| New employers (first year) | Monthly | 15th of following month |

**Penalty for late remittance:** 3–10% of amount due, depending on days late; second offence in a calendar year doubles the penalty.

### T4 Slips and Summaries
- **Deadline:** February 28 of the following year (February 29 in leap years)
- Issue T4 to every employee who received employment income in the calendar year
- File T4 Summary with CRA
- **T4A:** For self-employed/contractor payments of $500+ in a calendar year (fees for services in Box 048)
- Penalties for late T4 filing: $10 per day (minimum $100, maximum $7,500)

---

## Corporate Income Tax

### Federal and Provincial Rates (2025)

| Rate Type | Federal | Ontario | BC | Alberta |
|-----------|---------|---------|-----|---------|
| General corporate | 15% | 11.5% | 12% | 8% |
| Small business (on first $500K active income) | 9% | 3.2% | 2% | 2% |
| Combined general (approx.) | — | 26.5% | 27% | 23% |
| Combined small business (approx.) | — | 12.2% | 11% | 11% |

**Small business deduction:** Available to Canadian-Controlled Private Corporations (CCPCs) on the first $500,000 of active business income. Phases out if taxable capital exceeds $10M.

### Filing Deadlines
- **T2 Corporate Income Tax Return:** Within **6 months** of fiscal year-end
- **Balance of tax owing:** Within **2 months** of fiscal year-end (3 months for CCPCs claiming small business deduction)
- **Instalments:** Quarterly (monthly for large corporations) — due 2 or 3 months after quarter-end

### SR&ED Tax Credits (Scientific Research & Experimental Development)
One of Canada's most valuable tax incentives:
- **Federal:** 15% refundable/non-refundable ITC on qualifying expenditures; **35% refundable** for CCPCs on first $3M
- **Provincial:** Additional credits (e.g., Ontario 3.5–8%, BC 10%)
- **Claim deadline:** 18 months after the end of the fiscal year in which the expenditures were incurred
- Qualifying work: basic research, applied research, or experimental development aimed at technological advancement
- File Form T661 with T2; consider engaging an SR&ED consultant for larger claims

---

## Contractor vs. Employee — CRA's Test

CRA uses a multi-factor test (similar to the employment law test but with tax consequences):

| Factor | Employee | Independent Contractor |
|--------|----------|----------------------|
| Control | Payer controls how work is done | Worker controls method |
| Tools and equipment | Payer provides | Worker provides own |
| Subcontracting | Cannot subcontract | Can hire helpers |
| Financial risk | No financial risk | Bears financial risk |
| Integration | Work integral to payer's business | Work is accessory |

**Tax consequences of misclassification:**
- Employer liable for **both employer and employee CPP/EI contributions** for the period of misclassification
- Plus **interest and penalties**
- CRA may reassess up to 3 years (or longer if misrepresentation)

**Personal Services Business (PSB):** If an incorporated contractor would be an employee but for their corporation, CRA may deem them a PSB — resulting in loss of small business deduction and most expense deductions. Significant tax cost.

**Ruling request:** File Form CPT1 (Request for a CPT1 Ruling) to get CRA's determination of status before engagement begins.

---

## Key CRA Deadlines Calendar

| Month | Deadline |
|-------|---------|
| February 28 | T4/T4A slips and summaries due |
| March 31 | T3 trust returns due (60 days after Dec 31) |
| April 30 | Personal tax returns due (T1); balance owing due |
| June 15 | Self-employed individuals' T1 return due (balance still due April 30) |
| 2 months after FYE | Corporate tax balance owing |
| 3 months after FYE | Corporate tax balance owing (eligible CCPCs) |
| 6 months after FYE | T2 corporate return due |
| Monthly 15th | Standard payroll remittance due |

## Reference Files

- `references/tax-details.md` — GST/HST ITC documentation requirements, payroll deduction worked examples, and SR&ED eligibility criteria

- `references/gst-hst-contractor-review.md` - GST/HST registration and ITC fact review for a sole-proprietor contractor

All rates and thresholds above are the 2025 figures the upstream targeted; verify every figure at canada.ca/cra and Revenu Quebec before use. This overview is preparation guidance, not tax advice.
