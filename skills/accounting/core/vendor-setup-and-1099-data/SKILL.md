---
name: vendor-setup-and-1099-data
description: >-
  Set up and maintain the vendor master with verification, bank-detail change control and the tax data needed to file contractor information returns (US 1099-NEC/MISC and equivalents elsewhere). Use for "add a new vendor", "collect W-9", "1099 vendors", "vendor bank change", "duplicate vendors", "contractor payments year end", or "withholding on supplier payments".
metadata:
  department: "accounting"
  domain: "ap-ar"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Vendor setup and contractor tax data

The vendor master is a fraud and compliance control. Creating a vendor and paying a vendor are separate privileges. Tax rules differ by jurisdiction; this skill gives the data discipline and flags where rules must be confirmed with the current official guidance.

## 1. New vendor onboarding

Collect before the first payment:

| Item | Check |
|---|---|
| Legal name and trading name | Matches the tax document and bank account name |
| Entity type | Individual, sole proprietor, partnership, corporation, government |
| Tax identification | From the vendor's signed tax form (W-9 for US persons; W-8 series for foreign vendors; equivalent local form elsewhere). Validate format; verify with the tax authority's matching service where available |
| Tax registration (VAT/GST number) | Validate against the registry; needed to claim input tax |
| Address and contact | Business address; independent contact for verification |
| Bank details | On letterhead or the vendor portal; verified by call-back to a known number |
| Payment terms and currency | From contract |
| Documentation | Contract or quote; for contractors, proof of business status |
| Sanctions and related-party screen | Per policy, plus flag where the vendor is connected to an employee or owner |

Segregation: the requester proposes, a finance person creates, and the approver of payments is someone else. Record who set up each vendor and when.

## 2. Maintain

- **Bank detail changes**: the highest-risk event. Verify with the vendor using details already on file, log the verification (who, when, how), have a second person approve, and hold payments briefly after the change. Run a report of bank changes before each payment run.
- **Duplicates**: periodic check on normalised name, tax ID, bank account, address. Merge or inactivate duplicates; never delete vendors with history.
- **Inactive vendors**: deactivate after a stated period without activity; reactivation re-verifies details.
- **Annual review**: refresh tax forms where they expire or change, and confirm status.

## 3. Contractor information returns (US example; confirm each year)

Flag each vendor at setup: reportable or not, and payment type. In outline for the US:

- Payments for services to non-corporate vendors (individuals, sole proprietors, partnerships, certain LLCs) are generally reportable on Form 1099-NEC when they reach the annual threshold; the threshold and form rules change, so verify against current IRS instructions before filing.
- Typically excluded: payments to corporations (with exceptions), payments by credit or debit card or through payment networks (these are reported by the processor on 1099-K), reimbursements of documented expenses under an accountable plan, payments for goods only, and non-US persons (different forms and possible withholding).
- Rents, royalties, prizes, attorney proceeds and others use other boxes or forms.
- Backup withholding applies when a valid tax ID is not provided; track and remit.
- Record payments on a cash basis in the calendar year paid. Report the gross amount, including the part reimbursed through the vendor if included in the contract.

Equivalent regimes exist elsewhere (for example withholding at source on contractor or professional fees under local rules, with annual certificates). When the client is outside the US, identify the local rule and record it in the client file; do not apply US logic.

## 4. Year-end process

1. Run the paid-vendor report for the calendar year by vendor and payment method.
2. Filter reportable vendors; exclude card and network payments.
3. Reconcile totals to the ledger expense accounts; investigate vendors flagged reportable with no tax ID on file and chase missing forms before year end, not in January.
4. Reconcile name and tax ID to the tax form; correct mismatches.
5. Prepare the filing drafts and recipient copies; submit only after approval by the responsible person.
6. File and deliver by the legal deadlines; retain forms and proof for the retention period.

## Data protection

Tax IDs and bank numbers are sensitive. Store in the vendor system or secure vault with role-based access; mask in reports and chat; never paste full identifiers into free-text notes.

## Output

Vendor setup checklist with status, exception list (missing tax form, unverified bank details, duplicates), and the year-end reportable-vendor table with totals and gaps.

## Do not

- Pay a new vendor before verification is complete.
- Accept bank detail changes by email alone.
- Assume reportability from the vendor name.
- Report on accrual basis when the rule is payment basis.
- Keep full tax identifiers in unprotected notes.

See also: `contractor-1099-reporting` (overlapping topic; this skill covers its own scope, that one covers the other side).
