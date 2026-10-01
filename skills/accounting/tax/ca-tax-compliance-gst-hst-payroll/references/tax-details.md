# Canadian Tax Deep Reference

## GST/HST ITC Documentation Requirements

To support an Input Tax Credit claim, CRA requires the following on invoices:

| Annual Purchases from Supplier | Required Information |
|-------------------------------|---------------------|
| Under $30 | Supplier name, invoice date, total paid, indication that GST/HST is included |
| $30 – $149.99 | Above + supplier's GST/HST registration number |
| $150 or more | All of the above + purchaser's name, description of supply, terms of payment, GST/HST charged (shown separately or as a rate) |

**Common ITC claim errors:**
- Missing supplier GST/HST number on invoices over $30
- Claiming ITCs on expenses with no business purpose documentation
- Claiming 100% ITC on expenses that are partially personal (vehicles, home office, meals)
- Missing invoices (credit card statement alone is insufficient)

**Meals and entertainment:** Only 50% of GST/HST paid on meals and entertainment is recoverable as an ITC (matching the 50% income tax deductibility rule).

## Payroll Deduction Worked Example

**Scenario:** Employee in Ontario, annual salary $75,000, standard TD1 claim (basic personal amount only)

Approximate monthly payroll calculation (2025):

| Item | Monthly Amount |
|------|---------------|
| Gross salary | $6,250.00 |
| CPP deduction | ~$308.33 |
| EI deduction | ~$86.45 |
| Federal income tax | ~$965.00 |
| Ontario provincial tax | ~$387.00 |
| **Net pay** | ~$4,503.22 |

**Employer remittance (monthly):**
| Item | Amount |
|------|--------|
| Employee CPP | $308.33 |
| Employer CPP (match) | $308.33 |
| Employee EI | $86.45 |
| Employer EI (1.4×) | $121.03 |
| Employee income tax | $1,352.00 |
| **Total remittance to CRA** | ~$2,176.14 |

Use CRA's Payroll Deductions Online Calculator (PDOC) at canada.ca/pdoc for exact amounts.

## Payroll Compliance Checklist

- [ ] Employee completed TD1 Federal and TD1 Provincial forms on hire (and on any changes)
- [ ] CPP, EI, and income tax deducted each pay period using current year rates
- [ ] Remittances made on time according to remittance schedule
- [ ] T4 slips issued and filed by February 28
- [ ] T4A issued for contractor/freelancer payments of $500+ in calendar year (Box 048)
- [ ] Record of Employment (ROE) issued within 5 calendar days of employee's interruption of earnings
- [ ] Payroll records retained for 6 years after the year to which they relate

## SR&ED Eligibility Self-Assessment

Work qualifies for SR&ED if it meets all three criteria:

**1. Scientific or Technological Uncertainty**
Was there genuine uncertainty about whether the goal was achievable or how to achieve it — uncertainty that could not be resolved by standard practice or routine engineering?

**2. Scientific or Technological Content**
Did the work involve formulating hypotheses, testing, and analyzing results in a systematic way?

**3. Technological Advancement**
Did the work attempt to advance the general body of knowledge in a scientific or technological field?

**Common qualifying activities:**
- Developing new software architectures or algorithms where standard approaches are insufficient
- Prototyping and testing new materials or processes where the outcome is uncertain
- Resolving technical bugs that arise from novel interactions (not routine debugging)
- Developing new manufacturing processes with uncertain outcomes

**Commonly non-qualifying activities:**
- Routine software development, bug fixes, or UI improvements
- Market research, quality control testing, or social science research
- Routine data collection or analysis using standard techniques
- Style/design changes without technological uncertainty

## CRA Audit Triggers — Common Risk Factors

**GST/HST:**
- Large or frequent ITC claims relative to revenue
- Zero-rated or exempt supply classifications that reduce net tax
- Late-filed returns or remittances
- Significant variance between GST/HST reported and revenue reported on T2

**Payroll:**
- High ratio of T4A (contractors) to T4 (employees) — may trigger worker classification review
- Payroll remittances declining while revenues increase
- Late or missing T4/T4A filings

**Corporate:**
- Significant shareholder loans (s.15 shareholder benefits)
- Large SR&ED claims, especially first-time claims
- Revenue or expense patterns inconsistent with industry norms
- Related-party transactions (transfer pricing, even domestic)
- Losses claimed over multiple consecutive years

## GST/HST Place of Supply Rules (Summary)

The province where GST/HST is calculated depends on the "place of supply":

| Supply Type | Place of Supply |
|------------|----------------|
| Tangible personal property | Where delivery takes place |
| Services (general) | Where the recipient is located |
| Telecommunications | Where the service is received |
| Real property | Where the property is located |
| Digital services to consumers | Recipient's province |

**Practical impact:** A BC business shipping goods to an Ontario customer charges 13% HST (Ontario rate), not 5% GST. Ensure your billing system applies the correct rate based on ship-to address.
