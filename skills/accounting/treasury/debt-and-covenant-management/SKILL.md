---
name: debt-and-covenant-management
description: >-
  Debt accounting and covenant management for finance teams: loan schedules and amortisation, interest accrual, issuance costs and OID, current vs non-current classification, financial covenant calculations (leverage, interest cover, DSCR, current ratio), compliance certificates, cure and waiver process, refinancing and modification accounting. Use when a company has loans or credit lines, or someone says "covenant calculation", "compliance certificate", "DSCR", "net debt to EBITDA", "debt classification current vs non-current", "loan amortisation schedule" or "covenant breach".
metadata:
  department: "accounting"
  domain: "treasury"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Debt and covenant management

A covenant breach turns long-term debt into on-demand debt overnight. The accounting job is therefore two jobs: record debt correctly, and know weeks ahead whether the next compliance date will pass.

## Step 1: Debt register

For every facility: lender, type, currency, limit, drawn, rate basis (fixed or benchmark plus margin, floor), payment dates, maturity, amortisation, prepayment terms, security, guarantors, financial covenants and definitions, information deadlines, events of default, cross-default links, and where each lives in the ledger. Keep the agreement and amendments with the register.

## Step 2: Accounting mechanics

1. **Initial measurement:** proceeds less directly attributable costs (arrangement fees, legal). Fees reduce the carrying amount (US GAAP presents debt issuance costs as a deduction from the debt, except revolver fees which may be an asset) and are amortised over the term using the effective interest method.
2. **Interest:** accrue monthly: balance x rate x days / day-count basis (act/360 or act/365 per the agreement). Floating-rate loans reset on the reference rate; keep a rate-history table.
3. **Amortisation schedule:** payment split into interest and principal; reconcile the lender statement to the schedule each month and book differences.
4. **Classification:** principal due within 12 months of the balance-sheet date is current. If a covenant is breached at the balance-sheet date and the lender has not waived for at least 12 months (or the cure is not probable under the relevant standard), classify as current. For IFRS, covenants to be met after the reporting date generally do not affect classification but need disclosure.
5. **Modifications and extinguishments:** compare present value of the new cash flows to the old (10 percent test for derecognition under IFRS 9; ASC 470-50 for US GAAP); modification adjusts the effective rate, extinguishment books a gain or loss and expenses unamortised costs. Capitalise third-party fees on modification as appropriate to the outcome.
6. **Embedded features:** convertible and warrant-linked debt, put/call options, and floors may need bifurcation; escalate to a technical review.

## Step 3: Covenant calculations

Use the agreement definitions exactly; they usually differ from reporting GAAP.

| Covenant | Common formula | Common traps |
|---|---|---|
| Leverage | Net debt / covenant EBITDA | Which debt (leases, guarantees, preferred); cash netting caps |
| Interest cover | Covenant EBITDA / net interest expense | Capitalised interest, hedging costs |
| DSCR | (EBITDA - taxes - maintenance capex) / (interest + scheduled principal) | Whether voluntary prepayments count |
| Current ratio | Current assets / current liabilities | Treatment of revolver classification |
| Minimum liquidity | Cash plus undrawn availability | Trapped cash, restricted cash, availability conditions |
| Fixed-charge cover | (EBITDA - capex - taxes) / (interest + principal + rent) | Rent included or not |

Covenant EBITDA = net income + interest + taxes + D&A + permitted add-backs (non-recurring, stock comp, run-rate synergies) up to the cap in the agreement. Document every add-back with support and check the cap. Test on the contractual basis: trailing twelve months or quarterly annualised, at each test date.

## Step 4: Forward-looking monitor

1. Build a covenant calendar: test dates, certificate due dates, fee dates, rate resets, maturities.
2. Each month, project the next two test dates from the budget and 13-week cash forecast; show headroom in percent and in EBITDA terms (how far EBITDA can fall before breach).
3. Amber at less than 20 percent headroom, red at less than 10 percent or any breach in a downside case; the action thresholds are agreed with the CFO.
4. Draft the compliance certificate from the same workbook; the signing officer receives the calculation and add-back support.

## Step 5: If breach is likely

1. Notify the CFO immediately; do not wait for the test date.
2. Options: cure rights (equity cure, EBITDA cure), amendment or waiver, reset of the covenant, cost actions, asset sale, refinancing.
3. Approach the lender early with a plan, a revised forecast and proposed terms; expect a fee or margin step-up.
4. Reassess debt classification, going-concern disclosure and cross-defaults on other agreements.
5. Record waivers and amendments in the register with effective dates.

## Failure modes

- Computing the covenant on reported rather than agreement-defined figures.
- Unsupported add-backs above the cap.
- Missing a reporting deadline (a technical default).
- Not checking cross-default clauses when one facility trips.
- Presenting debt as non-current in a breach year.
- Interest accrued on the wrong day-count basis.

## Output

Debt register, amortisation and interest schedules, monthly covenant model with headroom, covenant calendar, compliance certificate draft, and a breach-response memo when needed.
