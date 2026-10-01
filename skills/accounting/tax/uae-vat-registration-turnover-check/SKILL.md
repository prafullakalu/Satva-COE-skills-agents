---
name: uae-vat-registration-turnover-check
description: >-
  Work out from a company's invoices whether and when it crossed the UAE VAT registration threshold (rolling 12-month taxable supplies, next-30-days test), build the turnover schedule the FTA EmaraTax application asks for, and walk the VAT registration form. Use for "do we need to register for VAT in the UAE", "get a VAT TRN", "EmaraTax VAT registration", "UAE VAT turnover schedule". Not for VAT returns or tax advice; the user submits the declaration.
metadata:
  department: "accounting"
  domain: "tax"
  owner: "satva-coe"
  status: "beta"
  license: "MIT"
  source: "https://github.com/imadbadreddine7-bot/uae-vat-registration-skill"
---

<!-- Adapted from imadbadreddine7-bot/uae-vat-registration-skill SKILL.md (MIT, Copyright (c) 2026 Squarezone Corporate Services LLC-FZ). Modified by Satva: kept as upstream; portal details change, verify against the live FTA portal. -->

# UAE VAT registration on EmaraTax

You are helping the user file their own company's VAT registration on the UAE Federal Tax Authority's EmaraTax portal (eservices.tax.gov.ae). You do two things: you read the user's invoices and turn them into the turnover figures the application asks for, and you drive the browser to fill the form from those figures and the user's documents. The user reviews and submits.

## The design principle: the user only gathers invoices

The user's only job is to collect their invoices (sales invoices issued, plus purchase invoices and expenses if they want those counted) and the standard company documents. Everything else that is mechanical is yours: reading the invoices, building a dated turnover ledger, working out when the running 12-month total crossed the threshold, producing the turnover schedule the portal wants uploaded, and filling every section of the application. Do not send the user off to compute their own turnover or to fill parts of the form themselves. If something is missing, ask for the document, not for the answer.

## Read this first: what you must and must not do

- **You are not a tax advisor.** Do not advise on whether registering is the right move, on the VAT treatment of any transaction, on exempt versus zero-rated classification disputes, on tax groups, on designated zones, or on what is correct for this company. You compute from what the invoices say and you enter data the user gives you. Anything ambiguous gets flagged, in writing, for a registered UAE tax agent on the FTA register (tax.gov.ae).
- **Never type the user's password or any OTP.** The user logs into EmaraTax themselves. You take over once they are logged in.
- **Never tick the final declaration or click Submit yourself.** When you reach the last section (Declaration), stop. Show the user a summary, let them read the review screen, and have them tick the declaration and submit. That declaration is a legal attestation by the authorised signatory.
- **Stop and ask on any warning you did not expect,** especially "a TRN already exists for this entity" or "this trade licence is already linked to another account." Do not push past it on your own. Explain it (it usually means the company is already registered, a free zone or a prior agent created an account, or the Corporate Tax profile is being duplicated) and let the user decide.
- **Verify, do not assume.** Read every value off the user's actual invoices and documents. Do not invent amounts, dates, an IBAN, a customs code, or a phone number. If an invoice is unreadable or a total does not add up, say so and ask for a clean copy.

## Prerequisites

Before starting, make sure the user has the items in `references/before-you-start.md`. The essentials:

- An EmaraTax account, logged in. If the company has already registered for Corporate Tax, the Taxable Person profile already exists and VAT is added to it; do not create a second profile.
- Invoices: every sales invoice issued in the last 12 months (PDF, images, a spreadsheet, or an export from the invoicing tool), purchase invoices if the user wants taxable expenses counted, and any signed contracts or purchase orders that evidence supplies in the next 30 days.
- Documents as PDF (the portal rejects images for most uploads): trade licence, MOA/AOA, certificate of incorporation, Emirates ID and passport of the owners and authorised signatory, a bank letter or statement showing the company's UAE IBAN, and the customs registration certificate if the company imports.
- Details to hand: legal name (English and Arabic), licence number and dates, business activities, owners and percentages, other businesses the owners or managers are involved in, registered address, a UAE mobile, an email, the IBAN and bank name.

If something is missing, ask the user to provide it before you reach the section that needs it. If you can read the user's files directly (a folder, a connected drive), pull the values from there and confirm them.

## Part A: build the turnover ledger from the invoices

Do this before opening the portal. The "Business activities and turnover" section of the application is entirely driven by these numbers, and the portal expects a supporting schedule.

1. **Ingest every invoice the user gives you.** PDFs, photos, a CSV, an accounting export: read each one and extract invoice number, invoice date, customer, currency, net amount (excluding VAT), and any VAT or rate the invoice itself states. Note the source file for each row. If two sources overlap (an export and the PDFs it generated), de-duplicate by invoice number and tell the user how many duplicates you dropped.
2. **Convert to AED excluding VAT.** The portal wants AED amounts net of VAT. If an invoice is in another currency, use the exchange rate printed on the invoice; if none is printed, ask the user which rate to use and record it. Do not pick a rate yourself.
3. **Classify only from what the invoice says.** Keep a column for the treatment the invoice states (standard-rated, zero-rated, exempt, out of scope, or nothing stated). For the threshold, the FTA counts taxable supplies, which means standard-rated and zero-rated supplies and imports, and does not count exempt supplies (verify on tax.gov.ae). If an invoice states nothing, or the user is unsure whether a supply is zero-rated or exempt, do not decide: list it under "unclassified", compute the totals both with and without it, and flag it for a tax agent.
4. **Build the monthly table.** Taxable supplies per calendar month over the whole period covered, then a rolling 12-month total ending each month (the window is rolling, not the calendar or financial year). Identify the first month, and the actual invoice date within it, at which the rolling total reached or exceeded each threshold.
5. **Next 30 days.** If the user gives contracts, purchase orders, or a pipeline, compute the expected taxable supplies in the next 30 days from what is signed and dated for delivery within that window. Keep this figure separate from the historical one and list what it rests on. Do not count unsigned pipeline as committed unless the user tells you to, and record that they did.
6. **Taxable expenses, if the user wants them counted.** From purchase invoices that show UAE VAT charged, build the same monthly and rolling totals of net expense amounts. This matters for the voluntary threshold.
7. **Report.** Give the user, in chat and as a file they can keep: the monthly table, the rolling totals, the expected next-30-days figure, the taxable expenses figure, the date the rolling total crossed each threshold (or a statement that it has not), and the list of flagged invoices. Then produce the turnover schedule described in `references/gotchas.md` so it can be uploaded in the turnover section.

State the thresholds as portal facts, with the standing note that the user should verify current figures on tax.gov.ae: mandatory registration threshold of AED 375,000 of taxable supplies and imports in the past 12 months or expected in the next 30 days; voluntary registration threshold of AED 187,500 of taxable supplies or taxable expenses over the same tests. The FTA also publishes a deadline for applying once the mandatory threshold is crossed; report the crossing date so the user can check it against that deadline, and do not characterise whether they are late.

What you do not do in Part A: you do not say whether the company should register, whether it can seek an exception, whether it should join a tax group, or whether a disputed line is really exempt. You compute, you show the working, and you flag.

## Part B: the EmaraTax flow

Full field-by-field detail is in `references/emaratax-vat-walkthrough.md`. The shape of it:

1. **Taxable Person setup.** After the user logs in, switch the portal to the "Taxable Person" user type (top bar). The profile is shared with Corporate Tax: if the company already registered for CT, open the existing profile and go to the VAT row; if not, create the profile with the company's name (English and Arabic), language, and email. Choose Register on the VAT row.

2. **Entity details.** Same content as the Corporate Tax form: entity type (a UAE-incorporated company is "Legal Person - Incorporated"; a free zone FZCO is normally "UAE Private Company"), country, date of incorporation from the certificate, and the entity evidence uploads. If the CT registration already exists, some of this may be pre-filled from the profile; read it against the documents rather than trusting it.

3. **Identification details.** Trade licence upload and fields (authority, number, issue and expiry dates, legal names, trade name), business activities added one by one from the licence, and the owners with Emirates ID validation and percentages.

4. **Contact details.** Registered address matching the licence, mobile, email, and the mandatory landline. See gotchas.

5. **Business relationships.** Whether the owners, directors, or managers are or were involved in other businesses in the UAE, and if so which. Take the list from the user; enter each relationship as the section asks (person, business name, TRN if that business is registered, role). Answer No only if the user says No.

6. **Bank details.** The company's UAE bank name, account holder name (must match the legal name), and IBAN, read off the bank letter or statement, with that document uploaded as evidence. The portal validates the IBAN and this can take time; see gotchas.

7. **Business activities and turnover.** The invoice-driven section. Taxable supplies in the last 12 months and expected in the next 30 days, taxable expenses on the same two tests, whether the company imports or exports, GCC activities and any GCC VAT registrations, customs registration details, and the supporting financial documents upload. Every number here comes from Part A; enter them exactly as reported and upload the turnover schedule and its evidence. Where the section asks the basis of registration (mandatory or voluntary), show the user the ledger figures next to the options and let them pick.

8. **Declaration.** Do not submit. Summarise everything for the user, confirm it matches the ledger and the documents, and hand off: they read the review, tick the declaration, and click Submit.

Save the application as a draft (there is a Save as Draft control) at the end of each section or whenever you pause, so nothing is lost if the portal glitches or the bank validation takes a while.

## Gotchas

The portal is a SAP UI5 app and has sharp edges. The recurring ones, with fixes, are in `references/gotchas.md`. The big ones:

- **The file uploader silently keeps only one file** when you upload several at once, and shows the list lower down than you expect. Upload one at a time and verify the "Add/View(n)" count.
- **The landline field is mandatory.** If the user has no landline, reuse the mobile digits (the field caps at 8 digits) so the section validates.
- **Emirates ID must be Validated** with the Validate button before the row saves; the ID also pulls the person's official name from the federal database, so use whatever name it returns.
- **Do not press Escape** to close a dropdown or picker: it closes the whole dialog and loses the entry. Click a neutral spot instead.
- **Turnover fields want AED excluding VAT,** whole amounts, and the portal expects a supporting schedule and evidence (invoices, bank statements, an audit report or a self-prepared turnover schedule), often on a signed FTA template.
- **The 12-month window is rolling.** Do not report a calendar-year or financial-year figure in a field that asks for the last 12 months.
- **Bank details validation can take time.** Save the draft and wait; do not re-enter the IBAN because the screen looks stuck.

## After submission

Once the user submits, capture the reference number from the confirmation screen. The FTA's stated processing time for VAT registration is around 20 business days, sometimes faster and sometimes longer if the FTA asks for more information (verify the current figure on tax.gov.ae). Requests for additional documents arrive in the EmaraTax account and by email; tell the user to watch both. On approval the FTA issues a VAT Tax Registration Number (TRN), the effective date of registration, and a downloadable VAT registration certificate, all in the EmaraTax account. Tell the user to download and keep the certificate.

Remind the user, without advising, that registering is separate from filing: VAT returns are a separate process with their own periods and due dates shown in the account, invoicing obligations change from the effective date of registration, and questions about any of that, or about the flagged invoices from Part A, belong with a registered tax agent. This skill does not prepare VAT returns.
