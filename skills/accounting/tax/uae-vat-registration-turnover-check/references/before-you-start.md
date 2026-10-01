# Before you start

Run through this checklist with the user before opening the portal. Everything here maps to a specific section of the EmaraTax VAT registration form or to the turnover ledger you build first, and missing items are the main reason a session stalls halfway through. The checklist is centred on invoices because the turnover section is what makes VAT registration different from Corporate Tax registration, and it is the part the user cannot skip.

## 1. An EmaraTax account, logged in

The user needs an account at eservices.tax.gov.ae. They can sign up with UAE Pass or with an email and password. Account creation and login are the user's job, not yours: you never enter their password or an OTP. Ask them to log in and tell you when they are on the EmaraTax dashboard, then take over.

Ask two things up front:

- **Has the company already registered for Corporate Tax?** If so, the Taxable Person profile already exists and you add VAT to it. Creating a second profile causes a duplicate and, later, a licence-already-linked warning.
- **Has anyone ever registered this company for VAT before,** for example a free zone, an agent, or a previous owner? If so, a TRN may already exist and the portal will say so; see `gotchas.md`. Better to know now than at the declaration step.

## 2. Invoices and turnover evidence

This is the part only the user can gather, and the part you then do all the work on. Any format is fine: PDFs, photos, a CSV or spreadsheet, or an export from the invoicing or accounting tool. Ask for the complete set, not a sample; a missing month makes the rolling total wrong.

| What | Why | Used at |
|---|---|---|
| Every sales invoice issued in the last 12 months (or since the company started trading, if less) | Source for taxable supplies per month and the rolling 12-month total; determines whether and when the mandatory threshold was reached; uploaded, or summarised in the turnover schedule, as supporting evidence | Ledger (Part A); Business activities and turnover |
| Credit notes issued in the same period | Reduce the supplies figure for the month they relate to; without them the ledger overstates turnover | Ledger (Part A) |
| Purchase invoices and expense receipts showing UAE VAT charged, last 12 months | Source for taxable expenses, which count toward the voluntary threshold; only needed if the user wants expenses counted | Ledger (Part A); Business activities and turnover |
| Signed contracts, purchase orders, or accepted quotes for supplies to be made in the next 30 days | Source for the expected next-30-days supplies figure, which is the second leg of both threshold tests | Ledger (Part A); Business activities and turnover |
| Bank statements for the period | Cross-check that invoiced amounts were real; the portal accepts them as supporting financial documents | Business activities and turnover |
| Audited or management accounts, if any exist | Alternative supporting financial document accepted by the portal; not required for a young company | Business activities and turnover |
| Any earlier VAT-related correspondence from the FTA | Reveals an existing TRN, a prior application, or an exception; stops a duplicate | Before you begin |

If invoices are in a foreign currency, ask whether the invoice prints an exchange rate; if not, ask the user which rate to apply and record the answer. You do not choose a rate.

## 3. Company documents, as PDFs

The portal rejects image files (JPG, PNG) for most uploads, so every document should be a PDF before you begin. Where each one is needed:

| Document | Why | Used at |
|---|---|---|
| Trade licence | Source for licence number, authority, issue and expiry dates, legal names, trade name, activities; uploaded as evidence | Identification details |
| Certificate of incorporation / formation | Source for the date of incorporation; uploaded as entity evidence | Entity details |
| MOA / AOA | Uploaded as entity evidence and as the signatory's source of authority; also confirms ownership percentages and who the manager is | Entity details; Declaration |
| Emirates ID of each owner | ID number and expiry for the ownership section; the portal validates the number against the federal database | Identification details |
| Emirates ID of the authorised signatory | Same validation, for the signatory record | Declaration (or wherever the form places the signatory) |
| Passport of owners and signatory | Backup identification; some entity configurations ask for it alongside the Emirates ID | Identification details; Declaration |
| Bank letter, or a recent statement, showing the company's UAE IBAN, account name, and bank | Source for the bank details fields; uploaded as evidence; the account name must match the legal name | Bank details |
| Customs registration certificate or customs code letter | Source for the customs code and the emirate of registration; only if the company imports or exports goods | Business activities and turnover |
| Details of other businesses the owners or managers are involved in (name, TRN if registered, role) | The business relationships section asks for them; a list from the user is enough, documents are rarely required | Business relationships |

If the user only has photos or scans as images, have them convert to PDF before you start filling the form, not when the upload fails.

## 4. Data checklist

Collect these values before starting, reading each one off the actual document rather than from memory:

- Legal name in English and in Arabic, exactly as on the trade licence
- Trade name, if different
- Trade licence number, issuing authority, issue date, and expiry date
- Date of incorporation, from the certificate of incorporation or formation
- Business activities exactly as written on the licence, and which is the main one
- Each owner's name, Emirates ID number and expiry, and shareholding percentage
- Whether the owners, directors, or managers are involved in any other UAE business, and if so its name, TRN, and their role
- The authorised signatory's name, Emirates ID, designation, mobile, and email
- A UAE mobile number for the company contact, and an email address
- The registered address as on the licence: building, area, emirate
- Bank name, account holder name, and IBAN, from the bank letter
- Whether the company imports or exports goods, and its customs code and emirate of customs registration if it does
- Whether the company does business with, or is VAT-registered in, any other GCC state
- The month the company started making supplies, so the ledger window is right

From the ledger, once you have built it:

- Taxable supplies in the last 12 months, AED excluding VAT
- Expected taxable supplies in the next 30 days, AED excluding VAT, and what evidences it
- Taxable expenses in the last 12 months and expected in the next 30 days, if the user wants them counted
- The date the rolling 12-month total reached each threshold, or a statement that it has not
- The list of invoices you could not classify from their face

If you can read the user's files directly, for example from a folder or a connected drive, extract these values yourself and read them back for confirmation. Confirmed values beat retyped ones.

## 5. Who registers

Registration thresholds are published by the FTA and are the only rule this skill relies on. As stated on the portal and FTA guidance, the mandatory threshold is AED 375,000 of taxable supplies and imports in the past 12 months or expected in the next 30 days, and the voluntary threshold is AED 187,500 of taxable supplies or taxable expenses on the same tests. Tell the user to verify the current figures on tax.gov.ae.

That is the extent of it. Whether this company should register, whether it should apply for an exception, whether a disputed supply is exempt or zero-rated, whether the company belongs in a tax group, deadlines, and penalties are for a registered tax agent on the FTA register at tax.gov.ae, not for you. If the user asks, say so plainly, show them the ledger figures against the thresholds, and continue with the data entry they have asked for.
