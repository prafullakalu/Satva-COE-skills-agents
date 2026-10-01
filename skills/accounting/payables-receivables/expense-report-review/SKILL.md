---
name: expense-report-review
description: >-
  Review employee expense reports and travel and entertainment (T&E) claims against policy before reimbursement: receipt substantiation, policy limits, duplicate and split claims, personal-versus-business and meals and entertainment rules, mileage and per diem, foreign-currency claims, card-versus-cash clearing, coding to the ledger, tax recovery and reimbursement payment. Use for "check this expense report", "T&E review", "expense claim approval", "reimburse employee", "missing receipts", "duplicate expense claim", "mileage claim", "per diem", "corporate card expenses to code". Reviews and proposes; it does not approve, reject or discipline.
metadata:
  department: "accounting"
  domain: "payables-receivables"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Expense report review

Employee expenses are small individually and a steady source of error, leakage and fraud collectively. A good review is quick, rule-based and consistent: it confirms each line is real, in policy, supported, correctly coded and paid once. Anomalies are prompts for a person to ask, never conclusions about anyone's honesty.

## 1. Inputs
The claim (employee, period, purpose, lines with date, vendor, category, amount, currency), receipts or invoices, the expense policy (limits by category and location, approval levels, what needs pre-approval, mileage and per diem rates, entertainment rules), the corporate-card feed, the approver's decision, travel authorisation, and the chart of accounts and tax codes in the ledger. If no written policy exists, say so, review on reasonableness and the tax rules, and recommend writing one.

## 2. Line tests (each line, in this order)
1. **Real and business purpose**: dated within the claim period, a stated business reason, attendees and their organisations for meals and entertainment. Weekend, holiday or off-itinerary spend is queried, not rejected.
2. **Substantiation**: itemised receipt or tax invoice for the amount (card slips alone are weak), legible, in the claimant's or company's name where tax recovery needs it. Missing receipt: record the reason; allow only under the policy's missing-receipt rule (small value, signed declaration), otherwise hold.
3. **Policy**: category limit, nightly hotel cap, class of travel, alcohol, upgrades, tips, pre-approval for large or unusual items. Over-limit: reimburse the policy amount and treat the excess as personal or approved exception.
4. **Duplicate and split**: same employee, vendor, date and amount in the same or an earlier claim, or paid by card and also claimed in cash; one cost split into several lines just under an approval limit; the same receipt reused across employees; resubmission after a rejection with a higher amount.
5. **Personal element**: mixed receipts (family members, personal items on a hotel folio, a minibar, a fuel top-up for a private car) are separated; the personal part is repaid or deducted.
6. **Mileage and per diem**: distance from the route record and the policy rate, no double claim with fuel receipts or a company car; per diem by location and days, meals provided on the trip deducted.
7. **Currency**: foreign amounts converted at the documented rate for the transaction date (card statement rate for card spend); do not mix conversion bases within one claim.
8. **Arithmetic and totals**: lines add to the total; advances and corporate-card items are removed from the amount payable.

## 3. Corporate card and advances
Card transactions are already paid by the company: the employee substantiates them and they are coded, not reimbursed (`credit-card-reconciliation`). Cash advances are cleared against the claim; an unspent balance is repaid. The card feed is also the source for finding unclaimed card spend and missing receipts. Employee reimbursements and card repayments are tracked in separate clearing accounts that must reconcile to zero.

## 4. Coding and tax
Code by nature and department or project (travel, accommodation, meals, entertainment, training, client gifts, small equipment; capital items above the capitalisation threshold to assets). Entertainment and client gifts usually have tax-deductibility and input-tax limits; staff meals and travel have different rules; reverse-charge applies to some foreign suppliers. Use only the tax codes configured in the ledger, apply the jurisdiction's rules, and record the tax invoice details needed to claim input tax. Taxable benefits (personal use, allowances above exempt rates) go to payroll (`payroll-accounting`).

## 5. Approval and payment
The approver is the line manager (not the claimant, not a subordinate); senior claims go one level up; finance reviews policy, coding and tax. Nobody approves their own claim, or the claim of someone who approves theirs. Payment is by the payment run (`ap-invoice-processing`) with bank details from the employee master, not from the claim; changes to an employee's bank details are verified by a call. Retain claim, receipts, approval evidence and payment confirmation for the statutory period.

## 6. Reporting
Monthly: spend by category, department and claimant; policy exceptions; late submissions; missing-receipt rate; top claimants; unclaimed card spend; claims older than 60 days; reimbursement and card clearing balances. Repeated exceptions by one person or approver go to the manager and finance lead with the evidence.

## Output
Per claim: line table (date, vendor, category, amount, test result, issue, proposed amount payable, coding and tax code), summary (claimed, payable, excluded, held, with reasons), questions for the claimant, and a draft posting. Anomalies are worded as questions ("claimed twice on 12 March: please confirm"), not accusations.

## Do not
- Approve, reject, recover or discipline; recommend and route.
- Pay from a photo of a receipt that cannot be read, or without a business purpose.
- Take bank details from a claim or an email.
- Treat a policy breach as fraud, or ignore a pattern because each item is small.
- Reimburse card items already paid by the company.
