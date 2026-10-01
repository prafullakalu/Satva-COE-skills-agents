---
name: contractor-1099-reporting
description: >-
  Independent contractor payment tracking and year-end information reporting (US Form 1099-NEC/1099-MISC style, with notes for other jurisdictions): W-9 collection, thresholds, payment-method exclusions, vendor classification, filing prep and error handling. Use for "1099 prep", "contractor payments report", "who needs a 1099", "W-9 missing", "contractor vs employee check". Not tax or legal advice.
metadata:
  department: "accounting"
  domain: "tax"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Contractor information reporting (1099 workflow)

**Boundary: not tax or legal advice.** Thresholds, forms, deadlines and penalties change; confirm current IRS (or local authority) instructions before filing. Worker classification is a legal determination: flag, do not decide.

## Year-round controls (cheaper than year-end clean-up)
1. **Onboarding:** collect a signed W-9 (US) or equivalent (W-8BEN/W-8BEN-E for foreign payees; other countries have their own self-certification) BEFORE the first payment. Store legal name, tax ID type and number, address, entity type. Tax IDs are sensitive: keep in the ledger's secure field or a restricted store, never in email or chat.
2. **Vendor flag:** mark each vendor "reportable" or "not reportable" with reason; set the reportable payment category (non-employee compensation, rent, royalties, other).
3. **Tax ID matching** against the authority's service where available to reduce notices.
4. Backup withholding (US, currently 24%): apply if the payee gives no valid TIN or after a notice; remit and report it.

## Year-end procedure (US pattern)
1. Pull payments by vendor for the **calendar year paid** (cash basis for reporting, regardless of accrual books). Include checks, ACH, wire, cash, and crypto/in-kind where applicable.
2. **Exclude:** payments to corporations (with common exceptions: attorneys' fees, medical/healthcare payments), payments by credit/debit card or third-party network (PayPal, Stripe-style): these are reported by the processor on 1099-K; payments for merchandise/inventory; wages (belong on payroll); personal payments; reimbursements under an accountable plan when separately invoiced at cost (confirm treatment).
3. **Threshold:** nonemployee compensation of 600 or more triggers 1099-NEC for payments in earlier years; for payments made after 2025 the threshold rises to 2,000 under recent law. Verify the figure for the tax year in question. Rent/royalty/other categories have their own thresholds (royalties 10).
4. Classify each reportable vendor: NEC (services), MISC (rent, prizes, other), box assignment.
5. **Reconcile:** total of reportable + excluded payments by vendor = total vendor payments in the AP/cash disbursement report. Investigate vendors with payments but no W-9 on file and chase before the deadline.
6. **Deadlines (US):** 1099-NEC to recipients and to the IRS by January 31; paper/e-file thresholds apply (e-file required at 10 or more information returns in aggregate). Check state filing and withholding requirements separately.
7. File through the filing service or ledger integration; keep the acknowledgement. For corrections: file a corrected return, do not file a duplicate.

## Classification red flags (route to adviser)
Contractor works fixed hours set by you, uses your equipment, works for you exclusively for a long period, is paid regular amounts like salary, performs your core business function, or has no other clients. Mislabelled employees create payroll-tax exposure.

## Other jurisdictions (examples, verify locally)
UK: Construction Industry Scheme deductions; Canada: T4A for fees; Australia: Taxable Payments Annual Report for specified industries; EU: services reverse-charge VAT. The pattern is the same: certify the payee, track payments, report annually.

## Evidence to keep
W-9s/forms with dates, vendor payment report, exclusion rationale list, filed returns and acknowledgements, correspondence on corrections. Retention: typically 4 years minimum.

## Do not
Do not use invoices (accrual) instead of payments for reporting amounts. Do not email full TINs. Do not issue a form for a payment already reported by a processor on 1099-K.

## Output
Vendor-level table: vendor | TIN on file (Y/N, last 4 only) | category | total paid | excluded amount and reason | reportable amount | form | status; plus a missing-W-9 chase list.

See also: `vendor-setup-and-1099-data` (overlapping topic; this skill covers its own scope, that one covers the other side).
