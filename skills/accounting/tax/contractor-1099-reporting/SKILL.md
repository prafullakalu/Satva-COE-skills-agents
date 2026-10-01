---
name: contractor-1099-reporting
description: >-
  Track independent-contractor payments and prepare US Form 1099-NEC/1099-MISC year-end reporting: W-9/W-8 collection, who is reportable (entity type, card-payment and corporate exclusions), cash-basis payee totals, thresholds ($600 historically, $2,000 from 2026), backup withholding, deadlines, penalty tiers, corrections and employee-vs-contractor red flags. Use for '1099 prep', 'who needs a 1099', 'W-9 missing', 'contractor payments report', 'do I need to file a 1099'. Not tax or legal advice.
metadata:
  department: "accounting"
  domain: "tax"
  owner: "satva-coe"
  status: "beta"
  license: "MIT"
  source: "https://github.com/Receiptor-AI/bookkeeping-skills/tree/main/skills/contractor-1099"
---
<!-- Adapted from Receiptor-AI/bookkeeping-skills skills/contractor-1099 (MIT, Copyright (c) 2026 Receiptor AI), with tracking-table and near-threshold ideas from openaccountant/skills business/contractor-tracking and anthropics/knowledge-work-plugins small-business/tax-season-organizer (MIT / Apache-2.0). Modified by Satva: removed vendor promotion, merged Satva's reconciliation, foreign-payee, exclusion and evidence checks, added currency caveat. -->

> **Currency of figures.** Thresholds, rates and penalty amounts below are the upstream's (written March 2026; penalty tiers and annual caps are the figures for returns due in 2025, and the threshold change is for payments made in 2026 onward). They change yearly: verify each against current IRS instructions (General Instructions for Certain Information Returns, Form W-9) before filing. This skill organises data and does not give tax or legal advice.

# 1099 Contractor Management

Track payments to independent contractors, determine who needs a 1099-NEC, collect W-9s, and file on time to avoid penalties. US federal pattern; other jurisdictions are listed at the end.

## When do you need to file a 1099-NEC?

File a 1099-NEC for each person or non-corporate entity to whom you paid **$600 or more** during the calendar year for services performed in the course of your trade or business.

**Threshold change for 2026:** Starting with tax year 2026, the reporting threshold increases from $600 to **$2,000**. This means fewer 1099s to file, but you should still track all contractor payments — the threshold could change again.

## Who needs a 1099-NEC?

| Payee type | 1099-NEC required? | Notes |
|-----------|-------------------|-------|
| Individual (sole proprietor, freelancer) | **Yes** if ≥$600 | Most common scenario |
| Single-member LLC (disregarded entity) | **Yes** if ≥$600 | Treated as individual for tax purposes |
| Partnership / Multi-member LLC | **Yes** if ≥$600 | |
| S-Corporation | **Generally no** | **Exception:** payments for legal services and medical/health care services always require a 1099 regardless of entity type |
| C-Corporation | **Generally no** | Same exceptions as S-Corp: legal and medical services |
| Payments via credit/debit card or third-party networks | **No** | The payment processor (Stripe, PayPal, Venmo, Square) reports these on **1099-K** instead. You don't double-report. |
| Employees | **No** | They get a W-2, not a 1099 |
| Rent paid to real estate agents | **No (1099-NEC)** | Gets 1099-MISC instead |
| Payments for merchandise/inventory | **No** | 1099-NEC is for services, not goods |

## The W-9: Get it before you pay

**Form W-9** (Request for Taxpayer Identification Number) collects the information you need to file a 1099. Collect it from every contractor **before making the first payment.** This is critical — chasing down W-9s in January when you're trying to file is miserable.

**What the W-9 provides:** Legal name, business name (if different), federal tax classification (individual, LLC, corporation, etc.), address, and TIN (Taxpayer Identification Number — either SSN or EIN).

**If a contractor refuses to provide a W-9:** You are required to begin **backup withholding** at **24%** of all future payments to that contractor. You must remit the withheld amount to the IRS using Form 945. This is not optional — failing to withhold when required makes you liable for the tax.

**Best practice:** Make W-9 collection part of your contractor onboarding process. No W-9, no first payment. Store W-9s securely — they contain SSNs.

## Tracking payments throughout the year

Don't wait until January to figure out who needs a 1099. Track continuously:

| Contractor | Entity type | TIN on file? | Payment method | Q1 | Q2 | Q3 | Q4 | YTD total | 1099 required? |
|-----------|------------|-------------|---------------|-----|-----|-----|-----|-----------|---------------|
| Jane Smith Design | Individual | SSN ✓ | ACH | $2,100 | $2,100 | $2,100 | $2,100 | $8,400 | Yes |
| Acme Dev LLC | LLC (single-member) | EIN ✓ | Check | $6,000 | $6,000 | $6,000 | $6,000 | $24,000 | Yes |
| CloudFlare Inc | C-Corp | EIN ✓ | Credit card | $300 | $300 | $300 | $300 | $1,200 | No (corp + card) |
| Bob's Plumbing | Individual | None ❌ | Check | $0 | $0 | $800 | $0 | $800 | Yes (get W-9!) |
| Legal Eagle LLP | Partnership | EIN ✓ | ACH | $0 | $5,000 | $0 | $0 | $5,000 | Yes |

**Monthly check:** During your monthly close, review contractor YTD totals. Flag anyone who has crossed or is approaching the threshold. Verify W-9s are on file for everyone above threshold.

## Filing deadline and forms

**Deadline:** **January 31** of the year following payment. Both the contractor's copy AND the IRS filing are due on January 31. There is **no extension** for 1099-NEC (unlike 1099-MISC, which has a March deadline for the IRS copy).

**What you file:**
- **Copy A** — to the IRS (electronically via FIRE system, or paper with Form 1096 transmittal)
- **Copy B** — to the contractor
- **Copy C** — for your records

**Electronic filing requirement:** If you're filing 10 or more information returns (any combination of 1099s, W-2s, etc.), you must file electronically. The threshold was 250 until 2024, when it dropped to 10.

**How to file:** Use the IRS FIRE (Filing Information Returns Electronically) system, or use a service like Tax1099.com, Track1099, QuickBooks, or Gusto that handles the filing for you. Paper filing with Form 1096 is still allowed if filing fewer than 10 total information returns.

## Penalties for late or incorrect filing

| When you file | Penalty per form |
|---|---|
| Within 30 days of deadline (by March 2) | **$60** |
| By August 1 | **$130** |
| After August 1 or not at all | **$330** |
| **Intentional disregard** (you knew and didn't file) | **$660** per form, **no maximum cap** |

**Annual maximums (for small businesses with gross receipts ≤$5 million):** $232,500 for the 30-day tier, $664,500 for the August tier, $1,328,500 for the "after August" tier. Intentional disregard has no maximum.

These penalties apply **per form** — if you have 20 contractors and miss all of them, multiply accordingly. The penalties also apply to incorrect forms (wrong TIN, wrong amount, wrong name).

## Correcting 1099s

If you discover an error after filing, file a corrected 1099-NEC:

**Type 1 correction:** Wrong amount, wrong code, or wrong checkbox. File a new 1099-NEC with the "CORRECTED" box checked and the correct information.

**Type 2 correction:** Wrong payee name or TIN. This requires two forms: one to zero out the incorrect payee, and one with the correct payee information.

File corrections as soon as you discover the error. If you correct before the IRS notices, you generally avoid penalties.

## Worker classification: Employee vs. contractor

This is the most dangerous area of 1099 compliance. If you classify a worker as a contractor when they should be an employee, you face:

- Back employment taxes (employer's share of FICA: 7.65% of all payments)
- Penalties for failure to withhold income tax
- Penalties for failure to file W-2s
- Interest on all of the above
- Potential state-level penalties (many states are even more aggressive than the IRS)

**Key factors the IRS considers (common law test):**

**Behavioral control:** Do you control how the work is done, or just the result? Contractors control their own methods. If you dictate hours, tools, processes, and work location, that looks like an employee.

**Financial control:** Does the worker have unreimbursed business expenses? Do they invest in their own tools/equipment? Can they profit or lose money? Do they offer services to the general public? Contractors typically say yes to all of these.

**Relationship:** Is there a written contract? Are there employee-type benefits (insurance, retirement, PTO)? Is the relationship permanent or project-based? Is the work a key part of your regular business? Employee indicators: ongoing relationship, benefits, work is core to the business.

**When in doubt:** File Form SS-8 with the IRS to request a worker classification determination. Or consult an employment attorney. The cost of getting it wrong vastly exceeds the cost of getting professional advice.

## Year-end checklist

By December 15:
- [ ] Review all contractor YTD totals
- [ ] Verify W-9 is on file for every contractor above threshold
- [ ] Request W-9s from any contractor without one
- [ ] Verify TINs match contractor names (consider TIN matching via IRS e-Services)

By January 31:
- [ ] Generate 1099-NEC forms for all qualifying contractors
- [ ] Mail or electronically deliver Copy B to each contractor
- [ ] File Copy A with the IRS (electronically if ≥10 forms)
- [ ] Retain Copy C for your records

After filing:
- [ ] Monitor for any IRS notices about mismatches
- [ ] File corrections promptly if errors are discovered

## Reconciling the 1099 population to the books

Do this before generating any form. It is where most wrong forms and missed payees are found.

1. Pull payments by vendor for the **calendar year paid**, on a cash basis, regardless of whether the books are accrual (a December invoice paid in January belongs to next year). Include checks, ACH, wire, cash and in-kind.
2. Source every payee from all payment channels: the ledger's bill payments, direct bank/credit-card spend coded to contractor-type accounts (contract labor, professional fees, commissions, rent), and payment-platform payouts. A vendor paid only by card is excluded (1099-K), but you must be able to show it was a card/third-party-network payment.
3. Tie out: reportable + excluded payments by vendor = total vendor payments in the AP / cash-disbursement report for the year. Investigate any vendor with payments and no entity type or TIN status.
4. **Near-threshold watch:** flag payees within roughly 30% below the threshold at the monthly close, and any payee whose entity type is unknown. Do not merge look-alike payees ("John Smith" and "John A. Smith") automatically; flag them for a human.
5. **Exclusions to document per vendor:** C- or S-corporation (except legal and medical/healthcare payments), card/third-party-network payments, merchandise or inventory, wages (belong on payroll), personal payments, and reimbursements billed at cost under an accountable plan (confirm treatment with the preparer).
6. Reportable categories beyond 1099-NEC: rent, royalties (lower threshold), prizes/awards, attorney proceeds, other income go on 1099-MISC; verify the box and threshold for each.

### Tracking report format

```
1099 CONTRACTOR TRACKING - Tax year [YYYY]  (cash basis, payments made in the calendar year)
Payee            Entity    TIN?   Method   Paid YTD   Excluded (reason)   Reportable   Status
Jane Smith Des.  Indiv.    Y      ACH      12,400     0                   12,400       REPORTABLE
Acme Dev LLC     SMLLC     Y      Check    24,000     0                   24,000       REPORTABLE
Cloud Host Inc.  C-corp    Y      Card     1,200      1,200 (card/1099-K) 0            Not reportable
Bob's Plumbing   Indiv.    N      Check    800        0                   800          REPORTABLE - W-9 MISSING
Totals: payees n | reportable n | missing-TIN n | total contractor spend
```

Show TINs as last four digits only. Chase list: every reportable or near-threshold payee without a W-9, with the date requested.

## Foreign payees and tax ID matching

- A non-US payee furnishes Form W-8BEN (individual) or W-8BEN-E (entity), not a W-9. Payments of US-source income may need Form 1042-S and withholding; this is a different regime, so route to the preparer.
- Where the authority offers TIN matching (IRS e-Services), run it before filing to cut mismatch notices (CP2100/B notices that start backup withholding).
- Keep TINs in the ledger's restricted field or a secure store. Never email or paste a full SSN/EIN into chat or a shared sheet.

## Other jurisdictions (pattern is the same: certify the payee, track payments, report annually)

UK: Construction Industry Scheme deductions and monthly returns; Canada: T4A for fees; Australia: Taxable Payments Annual Report for specified industries; EU: services purchased from abroad may need reverse-charge VAT. Verify locally; see also the jurisdiction skills in this stage.

## Evidence to keep

Signed W-9s or W-8s with dates, the vendor payment report, the per-vendor exclusion rationale, filed returns and acknowledgements, correspondence on corrections. Retention is typically four years minimum from the filing due date.

## Do not

- Do not use invoice (accrual) amounts instead of cash paid in the year.
- Do not issue a 1099 for a payment already reported by a processor on 1099-K.
- Do not decide worker classification yourself: flag it and route to the adviser.
- Do not file or transmit returns without owner approval; do not store full TINs in shared documents.
