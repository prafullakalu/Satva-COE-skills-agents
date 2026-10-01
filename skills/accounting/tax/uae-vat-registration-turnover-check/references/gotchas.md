# EmaraTax gotchas

The portal is a SAP UI5 single-page app with sharp edges. These are the failure modes that actually bite, each with symptom, cause, and fix, followed by general defensive habits. The first four are shared with the Corporate Tax form; the rest are specific to the VAT application and its turnover section.

## 1. The uploader silently keeps only one file

**Symptom.** You attach two or three PDFs to an upload control, the section seems fine, but later validation complains a document is missing, or the review screen shows only one file.

**Cause.** When several files go into the control at once it keeps only one, without an error. The list of uploaded files also renders lower down on the page than the control itself, so a quick glance at the control does not show what was actually kept.

**Fix.** Upload one file at a time. After each upload, scroll to the file list and check the "Add/View(n)" count went up by exactly one and that the file name is the one you just sent. Only then upload the next file. This matters most in the turnover section, which can take several evidence files.

## 2. The landline field is mandatory

**Symptom.** Contact details refuses to validate, complaining about the landline, and the user has no landline. Most single-founder companies do not.

**Cause.** The form marks the landline as required regardless of whether the business has one.

**Fix.** Reuse the mobile digits so the section validates. The field caps at 8 digits, so enter the part of the mobile number that fits. Tell the user you did this and why, so the value on the review screen does not surprise them.

## 3. Emirates ID rows do not save without Validate

**Symptom.** You fill in an owner or signatory, move on, and the row is gone, or the form blocks progress on the ID field.

**Cause.** The Emirates ID must be checked against the federal database with the Validate button before the row can save. The validation also returns the person's official registered name.

**Fix.** After typing the ID number, click Validate and wait for the response before filling the rest of the row. Use whatever name the validation returns, even when it differs slightly from the licence or passport spelling; the portal treats the federal record as authoritative. If validation fails, read the error to the user and check the number against the physical card; do not retry with a guessed variant.

## 4. Escape closes the whole dialog

**Symptom.** You press Escape to dismiss a dropdown or a date picker inside a dialog, and the entire dialog closes, discarding everything entered in it.

**Cause.** The Escape key is bound to the dialog, not to the inner control, so it bubbles up and cancels the whole entry.

**Fix.** Never press Escape inside the portal. To close a dropdown or picker, click a neutral spot on the dialog background instead. If a dialog does get lost, re-open it and re-enter the row; check whether a partial row was saved first so you do not create a duplicate.

## 5. Turnover fields want AED, excluding VAT, as whole numbers

**Symptom.** A turnover field rejects the value, or accepts it and the review screen shows a figure that does not match the ledger, or the FTA later asks why the declared turnover differs from the invoices.

**Cause.** The fields expect amounts in AED, net of any VAT, and normally as whole numbers without separators or currency symbols. Invoices in foreign currency, gross amounts that include VAT, or a figure copied with a thousands separator all produce a wrong entry silently or a validation error.

**Fix.** Build the ledger in AED excluding VAT before you open the section, so every field is a copy, not a calculation. Enter digits only; watch what the field does with decimals and separators and follow it. After entering each figure, read the field back against the ledger line. If the invoices are gross, the ledger must back the VAT out using the rate the invoice states, and say so in the report; if the invoice states no rate, that line is unclassified, not assumed.

## 6. The portal expects supporting financial documents and a signed turnover schedule

**Symptom.** The turnover section will not complete without an upload, or the application is submitted and comes back with a request for "supporting financial documents" or a "turnover declaration", stalling approval by weeks.

**Cause.** The FTA expects evidence for the turnover figures: invoices, bank statements, an audit report, or a self-prepared turnover schedule. In practice the reviewers often expect that schedule on the FTA's own turnover declaration template, downloadable from tax.gov.ae or linked from the application's guidelines page, signed and stamped by the authorised signatory. The exact document list and whether the template is required are on the screen and in the guidelines; they change.

**Fix.** Before opening the section, prepare the turnover schedule from the ledger: a month-by-month table of taxable supplies (and taxable expenses, if counted) in AED excluding VAT for the period, with the 12-month total, the expected next-30-days figure, and the crossing date. If the guidelines page or the FTA site offers a template, look for it and fill that template with the ledger figures rather than your own layout. Give it to the user to sign and stamp, then upload the signed version together with the evidence behind it (bank statements, invoices, accounts). Tell the user that a reviewer may still ask for more; the reference number and the EmaraTax inbox are where that request arrives.

## 7. Bank details validation can take time

**Symptom.** After entering the IBAN and clicking validate, the section shows a pending or processing state, or nothing visibly happens, and it is tempting to re-enter the IBAN or reload.

**Cause.** The IBAN check runs against an external service and can be slow; the SAP UI5 screen does not always show a spinner while it waits, and a reload or re-entry restarts the check or creates a duplicate row.

**Fix.** Click validate once, then Save as Draft and wait. Read the page again after a pause rather than acting on a stale view. If the status has not changed after a reasonable wait, tell the user and either continue with the next section and come back, or leave the draft and resume later, depending on what the screen allows. Never re-type the IBAN because the screen looks stuck; if a second attempt is really needed, delete the first row visibly before adding another. If validation fails outright, read the error to the user and check the IBAN against the bank letter character by character; a common cause is an account holder name that does not match the legal name.

## 8. The 12-month window is rolling

**Symptom.** The turnover entered is the calendar year or the financial year to date, and it does not match the invoices when the FTA checks, or the crossing date reported to the user is wrong.

**Cause.** The threshold tests look at the 12 months ending on the day of the test, and separately at the 30 days after it, not at any fixed year. The application's "last 12 months" field means the 12 months ending now.

**Fix.** The ledger computes a rolling 12-month total at every month end, and the figure entered is the one ending in the current month. When reporting the crossing date, use the earliest date at which the rolling total reached the threshold, not the end of the year in which it happened. Say explicitly in the report which 12-month window each figure covers.

## 9. Unexpected warnings about an existing TRN or a linked licence

**Symptom.** On starting the application, or when the licence is entered, the portal warns that a TRN already exists for this entity, that the trade licence is already linked to another EmaraTax account, or that a registration for this tax type is already in progress.

**Cause.** The company was registered before (by a free zone, an agent, a previous owner, or the user in a forgotten attempt), or a second Taxable Person profile was created when the Corporate Tax profile should have been reused.

**Fix.** Stop. Do not click past the warning. Read it to the user, explain the likely cause, and let them decide: recover access to the existing account, contact the FTA, or ask the prior agent. Continuing creates a duplicate that the FTA rejects, usually weeks later.

## Defensive habits for the whole portal

These are not tied to one screen; treat them as standing practice.

**Save as Draft at every section.** The VAT application is long, the bank validation can stall, and the portal will expire an idle session, taking everything not saved as a draft with it. Click Save as Draft at the end of every section and before any pause, including when you stop to ask the user a question or wait for a validation. When the session does expire, the user must log in again themselves; you never enter credentials or an OTP.

**Stale element references break after re-renders.** SAP UI5 re-renders tables and sections after saves, validations, and section changes, so an element located earlier may no longer exist even though the screen looks the same. Re-locate every element after each save or navigation instead of reusing references, and re-read the page before acting when anything has changed.

**Type dates instead of clicking through pickers.** The date pickers are slow to drive and are one of the places an Escape reflex causes damage. Click the date field and type the value in dd/mm/yyyy format, then confirm the field shows the date you intended.

**Uploads are PDF only, with a size cap stated on screen.** Image files are rejected for most uploads, and each control states its maximum file size next to it. Check the file is a PDF under that limit before uploading; when a file is too large, ask the user for a smaller export rather than converting it yourself into something they have not seen. A combined invoices PDF is the usual candidate for hitting the cap; split it by quarter if it does.

**Every number traces to the ledger.** If you cannot point at the ledger line a turnover figure came from, do not enter it. The ledger and the report you gave the user are the audit trail for what was declared; keep them with the reference number.
