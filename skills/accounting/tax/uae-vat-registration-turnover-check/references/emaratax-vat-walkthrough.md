# EmaraTax VAT registration, field by field

This is the working script for driving the form. It expands the flow in `SKILL.md`. Portal facts below match that file; where the exact label or layout is not certain, the note says what to look for so you can read the screen and adapt rather than guess. The portal is updated by the FTA from time to time, so treat every label here as "normally", verify against the live screen, and follow what the screen actually says.

Three rules apply throughout and are not repeated at every section: the user handles login and any OTP themselves; you never tick the final declaration or click Submit; and every number in the turnover section comes from the ledger you built in Part A of `SKILL.md`, never from memory or estimate. Also make a habit of clicking Save as Draft at the end of every section and before any pause, so a portal glitch, a slow bank validation, or a session timeout costs nothing.

The sections below are in the order the application normally presents them: Entity details, Identification details, Contact details, Business relationships, Bank details, Business activities and turnover, Declaration. If the live form shows them in a different order, splits one, or merges two, follow the screen and use this script section by section rather than step by step.

## Step 0: Taxable Person setup

1. The user logs in at eservices.tax.gov.ae and tells you when they are on the dashboard. Take over from there.
2. In the top bar there is a user-type switcher. Set it to "Taxable Person". If the control looks different from this description, look for whatever element switches between account contexts and read its options.
3. The Taxable Person profile is shared across tax types. If the company already registered for Corporate Tax, the profile exists: open it, do not create another. If the dashboard shows no profile at all, create one; the creation form asks for the company's name in English and Arabic, a preferred language, and an email. Use the legal name from the trade licence and the email from the data checklist.
4. Open the profile. The dashboard lists tax types as rows or tiles; find the VAT one and choose Register. If the action is labelled differently, look for the entry point that starts a new VAT registration. If the VAT row already shows a status other than "not registered" (for example an application in progress, or a TRN), stop and show the user; that is an existing registration or a prior attempt, and it is their call how to proceed.
5. The registration opens as a multi-section form. Expect an instructions or guidelines screen first with a confirmation checkbox before the sections begin; if one appears, read it, and this pre-form acknowledgement (not the final declaration) is fine to tick to proceed. The guidelines page normally lists the documents the FTA expects for this application; compare that list to what the user has gathered and raise any gap now.

## Section 1: Entity details

This section has the same content as the Corporate Tax form. If the CT registration exists, expect some fields to be pre-filled from the profile; read every pre-filled value against the documents anyway, because a wrong value here propagates.

1. Entity Type: for a company incorporated in the UAE, select "Legal Person - Incorporated". A free zone FZCO normally takes the sub-type "UAE Private Company". If the user's entity is neither, read the option list to them and let them choose; do not map an unusual entity type on your own.
2. Country: United Arab Emirates.
3. Date of incorporation: from the certificate of incorporation or formation, not the trade licence. Type the date rather than clicking through the picker (see `gotchas.md`).
4. Uploads: certificate of incorporation and the MOA. Upload one file at a time and verify the count after each (see `gotchas.md` on the uploader).
5. The section may ask whether the applicant is registering as a tax group or applying for an exception from registration. Both are tax decisions. The default for a single company registering on its own is No to both; if the user wants anything else, stop and refer them to a tax agent before continuing.
6. Save as Draft, then proceed to the next section.

## Section 2: Identification details

1. Upload the trade licence as a PDF first; the section may only unlock its fields after the upload, so if fields look disabled, do the upload and re-check.
2. Licence fields, each read off the licence itself: issuing authority, licence number, issue date, expiry date. Authority names in the dropdown may not match the licence wording exactly; pick the closest official name and confirm with the user if there is any ambiguity.
3. Legal name in English, legal name in Arabic, and trade name, exactly as printed on the licence. Copy the Arabic from the licence or the user's text; do not transliterate.
4. Business activities: use the "Add Business Activity" control for each activity on the licence. Search by the activity name and let the portal fill the activity code itself; do not type codes by hand. Mark one activity as primary (the user says which; on most licences it is the first listed). Repeat until every activity on the licence has a row, and count the rows against the licence before moving on.
5. Owners: the form asks for the owners or shareholders of the entity, normally with a threshold question (whether any owner holds 25% or more) similar to the Corporate Tax form. Answer from the MOA. For each owner: type natural person, Emirates ID number, then click Validate and wait for the federal database response. Use the name the validation returns, even if it differs slightly from the licence spelling. Enter the shareholding percentage. Save the row and confirm it appears in the owners table before adding the next. If the section also asks for managers or directors, add them from the MOA the same way.
6. Local branches: No, unless the company has UAE branches operating under this licence. If the user says yes, the form will open branch fields; fill them from the branch licences the same way.
7. Save as Draft, then proceed.

## Section 3: Contact details

1. Country: United Arab Emirates. Selecting UAE switches the address block to UAE-format fields: building, area, emirate. Fill them to match the registered address on the trade licence. If the licence address is terse (many free zone licences give only a zone and office reference), enter what the licence shows and ask the user to fill any field the licence does not cover.
2. Mobile number: the UAE mobile from the checklist. Watch how the field wants the number formatted (country code handling varies); enter it the way the field's placeholder or validation indicates.
3. Email: from the checklist. This is where the FTA sends requests for more information during review, so confirm the user actually reads it.
4. Landline: mandatory in this form even though most single-founder companies have no landline. If the user has none, reuse the mobile digits; the field caps at 8 digits, so use the local part that fits. Tell the user you did this and why.
5. Save as Draft, then proceed.

## Section 4: Business relationships

This section asks whether the owners, directors, or managers of the applicant are, or have been, involved in other businesses in the UAE. The exact wording and the look-back period are on the screen; read them to the user and take their answer literally.

1. If the user says No, answer No and move on. Do not answer No on their behalf because the list is empty in your notes; ask.
2. If Yes, add one row per relationship. The row normally asks for the person, the other business's legal name, its TRN if it is VAT-registered, the person's role (owner, director, manager), and whether the relationship is current. If the row asks for something this list does not cover, read the field to the user and enter what they say.
3. Where the row asks for a TRN and the user does not know whether the other business is registered, leave it for them to check; do not guess a TRN and do not enter a Corporate Tax TRN in a field asking for a VAT TRN unless the screen says either is acceptable.
4. Confirm each row appears in the table before adding the next. Count the rows against the user's list.
5. Save as Draft, then proceed.

## Section 5: Bank details

The FTA uses these details for refunds and the portal validates the IBAN, so accuracy matters and patience matters.

1. Bank name: from the bank letter or statement. The bank list is a dropdown of UAE banks; pick the exact bank, not a similarly named one.
2. Account holder name: exactly as printed on the bank letter. It should match the legal name on the licence; if it does not (a trade name, an abbreviation), show the user both and let them decide whether to proceed or fix the bank record first, because a mismatch is a common reason for a later request for more information.
3. IBAN: type it from the letter, without spaces unless the field wants them, and read it back digit by digit before validating. Never construct an IBAN from an account number.
4. Validate: the section normally has a validate or verify action for the IBAN and may also show a status that updates after a delay. Click it once, Save as Draft, and wait; see `gotchas.md` on bank validation. Do not re-enter the IBAN because the screen looks stuck.
5. Upload the bank letter or statement as evidence, one file, verify the count.
6. If the company has no UAE bank account yet, the section may allow you to proceed and provide details later, or it may block. Read the screen; if it blocks, stop and tell the user this is a prerequisite they need to complete with the bank.
7. Save as Draft, then proceed.

## Section 6: Business activities and turnover

This is the section the invoice ledger exists for. Every amount is entered in AED, excluding VAT, from the report you produced in Part A. Have the ledger open beside the form and enter each figure exactly as reported; if you find yourself rounding or estimating, stop and go back to the ledger.

1. Business activity description: a plain-language description of what the company does, consistent with the licence activities. Take it from the user or from the licence wording; do not embellish.
2. Taxable supplies in the last 12 months: the rolling 12-month figure ending on the date you are filing, from the ledger. If the ledger has unclassified invoices, use the figure the user chose after seeing both totals, and note in your summary which one was entered.
3. Expected taxable supplies in the next 30 days: the committed figure from contracts and purchase orders. If the user gave nothing for this, the figure is what they tell you it is; record that it is their statement, not a ledger computation.
4. Taxable expenses in the last 12 months and expected in the next 30 days: from the purchase-invoice side of the ledger, if built. If the user chose not to count expenses, enter what the screen allows for "none" (often zero) and say so in the summary.
5. Basis of registration: the section normally asks whether the applicant is registering on a mandatory or voluntary basis, and may ask for the date the threshold was reached or is expected to be reached. Show the user the ledger figures next to the thresholds and let them select the basis; enter the crossing date from the ledger. If the figures sit above the mandatory threshold, the portal's own definitions point to mandatory, and you may say so, but the selection is theirs, and you do not advise on whether registering at all is right.
6. Zero-rated supplies: the section may ask whether the company expects to make zero-rated supplies, or only zero-rated supplies. Answer from the invoice classifications the user confirmed. If the honest answer is "all zero-rated", that opens exception questions that are a tax position; stop and refer.
7. Imports and exports: whether the company imports goods into the UAE or exports goods from it. Answer from the user's business, then, if Yes, the customs registration fields: customs code number and the emirate of the customs registration, read off the customs certificate. If the company imports but has no customs code yet, say so to the user; do not invent one.
8. GCC activities: whether the company supplies to or buys from other GCC states, and whether it is VAT-registered in any of them (with that registration's number if so). Answer from the user. The list of GCC states and any per-state fields are on the screen; read them and adapt.
9. Supporting financial documents: the upload for evidence of the turnover figures. Upload the signed turnover schedule described in `gotchas.md`, then the evidence behind it (bank statements, a sample or the full set of invoices, audited accounts if any), one file at a time, verifying the count after each. If the control accepts only a limited number of files, combine the invoices into one PDF with the user's agreement and upload that.
10. Any question in this section that this script does not cover is a question you read to the user verbatim, and enter their answer. Do not fill turnover-adjacent fields from inference.
11. Save as Draft, then proceed.

## Section 7: Declaration

Do not submit. Do not tick the declaration.

1. The section normally starts with, or is preceded by, the authorised signatory details: name, Emirates ID with Validate, designation, mobile, email, and the source of authority (Memorandum of Association for a manager named in the MOA, or a Power of Attorney if that is what applies), with the corresponding document uploaded. Fill those from the checklist the same way as the owners rows. If the form placed the signatory in an earlier section instead, it will already be done; do not add a second one.
2. The review screen shows everything entered. Walk it section by section and read it against the user's documents and the ledger one more time.
3. Produce a summary for the user in chat: entity type, incorporation date, licence details, activities, owners and percentages, business relationships, bank details (IBAN masked except the last four digits), every turnover figure with the ledger line it came from, the basis of registration selected and the crossing date, imports and customs details, GCC answers, the documents uploaded, and the signatory. Flag anything you were unsure about and repeat the list of unclassified invoices.
4. Hand off. The user reads the review screen, ticks the declaration themselves, and clicks Submit themselves. The declaration is a legal attestation by the authorised signatory; it is theirs to make.
5. If anything needs correcting, the sections are navigable from the review screen (look for edit links or the section header navigation); fix it, save, and return to review.

## After the user submits

1. Capture the reference number from the confirmation screen and give it to the user in chat.
2. Tell them the SKILL.md facts: the FTA's stated processing time is around 20 business days, faster or slower in practice; requests for more information arrive in the EmaraTax account and by email; on approval the FTA issues a VAT TRN, an effective date of registration, and a downloadable certificate in the EmaraTax account; they should download and keep the certificate. Tell them to verify current processing times on tax.gov.ae.
3. Remind them, without advising, that registration is separate from filing returns, that invoicing obligations change from the effective date, and that the flagged invoices and any treatment questions belong with a registered tax agent.

## If the flow does not match this script

The FTA revises the portal. If a section is missing, renamed, split, or asks something this script does not cover, do not improvise an answer. Read the screen to the user, enter what they tell you, and keep the guardrails: their invoices and documents are the source of truth, every turnover number traces to the ledger, warnings stop the flow, and the declaration and Submit are theirs.
