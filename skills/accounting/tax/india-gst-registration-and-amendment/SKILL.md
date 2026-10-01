---
name: india-gst-registration-and-amendment
description: >-
  Handle Indian GST registration and changes: new registration (REG-01) from PAN, Aadhaar and premises documents, document checklist by constitution, Part A/Part B tab values; amendments (REG-14 core and non-core), voluntary cancellation (REG-16) with stock and ITC reversal working, REG-17 show cause and REG-18 reply, REG-21 revocation. Prepares intake sheet, field-by-field values and Rules-used block; the CA signs in, authenticates and submits. Use for "GST registration karni hai", "REG-01", "TRN", "change business address on GSTIN", "cancel GST registration", "GST suspended show cause".
metadata:
  department: "accounting"
  domain: "tax"
  owner: "satva-coe"
  status: "beta"
  license: "Apache-2.0"
  source: "https://github.com/amit-voais/fortax-skills/tree/main/skills/fortax-gst-registration (+ fortax-gst-amendment-cancellation)"
---

<!-- Adapted from amit-voais/fortax-skills skills/fortax-gst-registration and skills/fortax-gst-amendment-cancellation (Apache-2.0, Copyright 2026 Fortax). Modified by Satva: merged the two skills, removed dependence on the Fortax hosted engine and browser-tool instructions; time limits, thresholds and fees are looked up on the official portal. -->

> Currency: upstream written mid-2026. Registration time limits, thresholds, fees and portal screens change by notification; verify each on the GST portal or CBIC notification before use. For a REG-17 reply, the sibling skill india-gst-compliance (references/16) has a detailed response guide.

# Part 1: GST registration (REG-01)


## Do the whole registration. Ask for two things only.

When the CA hands you the details and the documents, you register — not "prepare for". Read the documents,
fill Part A, take the TRN, fill every tab of Part B, upload every file, and run the application up to the
authentication screen. The CA operates the portal: produce the filled intake sheet and a tab-by-tab click path with the exact value
for every field.

**You ask the CA for exactly two things, and only when the portal asks:**

1. A captcha, whenever one appears (the CA solves it on their screen).
2. The final authentication: the Part A OTPs, and the Aadhaar OTP, EVC or DSC at Verification — and the
   final Submit.

Everything else is yours. Do not ask the CA to type a field you can type, upload a file you can upload, or
confirm a value that is in the documents in front of you. Ask only for what is genuinely missing, and ask
for all of it at once, not one item at a time.

Open with one line: what you are about to do and the two points where you will need them. Then start.

## Reading what the CA gave you

Photographs and scans are readable — a PAN card, an Aadhaar, a rent agreement, an electricity bill, a
cancelled cheque. Read each file and take the fields from it rather than asking.

Check what you read against what the CA typed. Where the document and the message disagree — a name spelt
differently, a PAN that does not match — say which two sources disagree and which you used. Never silently
pick one.

## Step 1 — the intake sheet

Write `<Client>/GST/Registration/<date>_GST_registration_intake.md` and fill what you were given. Ask only
for what is missing, and only what the CA alone knows.

| Field | Needed for |
|---|---|
| Legal name, exactly as on PAN | Part A, and it must match or Part A fails |
| PAN | Part A |
| Constitution (proprietor, partnership, LLP, company, HUF, trust) | Part B, and it decides the documents |
| Mobile and email of the primary authorised signatory | Part A OTP |
| State and district | Part A |
| Principal place of business, with pincode | Part B |
| Nature of possession of premises (own, rented, leased, consent) | Part B, decides the address proof |
| Bank account (optional at registration, required later) | Part B |
| Goods and services actually dealt in | Part B, HSN/SAC |
| Date of commencement, and date liability arose | Part B |

Validate the PAN format (5 letters, 4 digits, 1 letter) and check the 4th character against the stated
constitution: P individual/proprietor, F firm or LLP, C company, H HUF, T trust, A AOP, B BOI, L local
authority, J artificial juridical person, G government. A mismatch is a flag, not something to correct
silently.

## Step 2 — the document checklist

Build the list from the constitution, not from a generic list. For each document say whose it is, what form
it must be in, and whether it is already in the client folder.

Typical shape, to be confirmed for the constitution and the state:

- Identity: PAN and Aadhaar of the proprietor, each partner, or each director.
- Photograph of the promoter and the authorised signatory.
- Proof of principal place of business, matched to the nature of possession: ownership document, or
  rent/lease deed, or a consent letter with the owner's ownership proof, plus a recent utility bill.
  **A rented premises without the agreement stops the filing** — flag it now, not at Part B.
- Constitution proof: partnership deed, certificate of incorporation, trust deed.
- Authorisation: letter of authorisation, or a board resolution for a company or LLP.
- Bank proof: cancelled cheque, or the first page of a passbook, or a statement.

Anything you cannot see in the folder goes in a short "please send" list at the top.

## Step 3 — Part A

Open the new registration page on the GST portal (services.gst.gov.in -> Services -> Registration -> New
Registration). Fill legal name, PAN, state, district, mobile and email exactly as in the intake sheet.

Then stop. **The mobile and email OTPs are the CA's.** Tell them precisely which two OTPs are coming, to
which number and which address, and that you continue the moment they are entered. Wait. Do not guess, do
not resend, do not ask for the OTP to be typed to you.

When the TRN appears, record it in the intake sheet with the date. The TRN has a limited life (the portal
and the TRN mail state the expiry — commonly 15 days; confirm on screen), so say when it expires and keep
the rest of the work inside it.

## Step 4 — Part B, tab by tab

Work the tabs in the portal's own order and record what you filled in each: Business Details, Promoter and
Partners, Authorised Signatory, Authorised Representative, Principal Place of Business, Additional Places,
Goods and Services, State Specific Information, Aadhaar Authentication, and Verification.

- Fill from the intake sheet and the documents in the folder. Never invent a date, an HSN, a turnover
  figure or an address line.
- Name each upload file as the portal expects, from the client folder only. After each upload, confirm the portal shows the file before moving on.
- Check each file against the portal's stated format and size limit first. Where a document is missing,
  keep going with the rest and list what is left at the end.
- HSN and SAC codes come from what the business actually sells. Where the CA has not said, list your
  reading and ask them to confirm before you enter it.
- Some fields are state specific — professional tax, shops and establishment, excise. Look them up for that
  state rather than assuming.
- Save at each tab. A registration lost to a session timeout is an hour of the CA's day.

## Step 5 — stop at Verification

Fill the verification tab's name and place. Then stop.

Aadhaar authentication, EVC and DSC are the CA's or the taxpayer's, always. Hand over with:

- What is filled, tab by tab, and what is still blank and why.
- Which authentication route applies for this constitution (DSC is mandatory for companies and LLPs).
- The exact next click, and that the ARN appears after it.
- **Check before submitting**: legal name against PAN, address against the proof uploaded, the signatory's
  details, and the HSN list.

## Step 6 — after the ARN

Record the ARN and the date in the intake sheet. Tell the CA that a query in REG-03 may follow, that it is
answered in REG-04 within the stated window, and that the certificate arrives as REG-06. Do not state the
window, the physical verification rule or any fee from memory: look each up on the official portal or notification, and
cite it in the **Rules used** block.

## Rules used

End every reply that relies on a time limit, threshold or fee with a **Rules used** block: the rule, the law
or notification it comes from, and either the source URL with date checked or "confirm on the portal".
An unverified recollection is not a source.

## Output

In the client's GST folder, dated: the intake sheet with the TRN and ARN, the document checklist with what is
still missing, and a short note of what was filled where. Never a submitted application.

# Part 2: GST amendment, cancellation and revocation


## Do the work, then stop at the last click

Each of these ends in an EVC, a DSC or an Aadhaar authentication — the last step, not the whole job.
**Refusing the job because its final click is the CA's is a failure.** The fields, the stock working, the
annexures, the portal navigation and the draft reply are yours. Say where you stop, then start.

Portal work: the CA logs in (password, captcha, OTP are theirs). Then give the CA the click path with the value for every field.

## Step 1 — decide which job this actually is

| What the CA says | What it is | Form |
|---|---|---|
| Address changed, partner added, trade or legal name changed | Amendment | REG-14 |
| Business closed, transfer, merger, constitution changed with new PAN | Cancellation by the taxpayer | REG-16 |
| Notice received proposing cancellation | Officer-initiated cancellation | REG-17, reply in REG-18 |
| Already cancelled by the officer, client wants it back | Revocation | REG-21 |
| Cancellation effective, nothing filed since | Final return | GSTR-10 |

A change needing a new PAN — proprietorship to partnership or company, or a shift to another state — is a
fresh registration (the registration section above) plus a cancellation, never an amendment. Say this before any
form is opened.

## Step 2 — amendment (REG-14)

Core fields go to the officer for approval; non-core fields are approved on the portal without one. The split
decides how long the client waits and whether an ARN needs tracking. Typically core: legal name of the
business, principal place of business, any additional place, and addition, deletion or retirement of
promoters, partners, karta, directors or trustees. Typically non-core: bank account, goods and services,
state specific information, most other details. **Do not rely on this list.** The portal's amendment tabs
mark which fields are core: read them, confirm before touching a field, and record what you found in
**Rules used**. The authorised signatory's contact details follow their own OTP route.

Prepare `<Client>/GST/Registration/<date>_GST_amendment_<GSTIN>.md`: field changed, old value, new value,
date of change, reason, and the document that proves it. Then open the amendment application and fill each
changed field, attaching only files already in the client folder.

Stop at Verification. For a core amendment, tell the CA an ARN follows, that the officer may raise a query in
REG-03 answered in REG-04, and that approval comes as an order in REG-15. The window for filing after the
change, and the window to reply to REG-03, are time limits — look them up with
look each up on the official portal or notification, never from memory.

## Step 3 — cancellation by the taxpayer (REG-16)

Clear the ground first. All returns due up to the intended date of cancellation must be filed and dues
cleared, or the portal blocks the application. List what is pending before drafting. Then build:

- Reason: discontinuance, transfer or amalgamation, change in constitution needing a new PAN, no longer
  liable, or death of the proprietor. And the date sought, with why that date.
- Stock held on the day immediately before it: inputs as such, inputs in semi-finished and finished goods,
  and capital goods, valued from the stock register and purchase invoices with a source column.
- Tax payable on that stock, as the rule prescribes for the period (section 29(5) and Rule 44) — broadly the
  higher of the ITC involved or the output tax on it, capital goods worked on the prescribed remaining useful
  life. Confirm the current text; state neither the useful life nor any rate from memory.
- Particulars of the last return filed, with ARN and period. For a transfer, the transferee's GSTIN.

Write `<Client>/GST/Registration/<date>_REG16_stock_and_liability_<GSTIN>.xlsx` with live formulas, fill the
portal form from it, stop at the verification step.

## Step 4 — cancellation by the officer (REG-17 and REG-18)

The notice is REG-17. Pull three things off it: the exact ground alleged, the periods covered, and the date
the reply is due. Do not assume the reply window; read it off the notice. Then cure, do not merely draft:
the missing returns get filed and what is admitted gets paid (the CA files and pays), and you collect the
ARNs and challans. A reply saying the defect is cured, with ARNs listed, beats argument. Draft REG-18 as an
annexure-backed letter: ground, facts, what has been done, evidence list, prayer. Satisfied, the officer
drops proceedings in REG-20; otherwise cancellation is ordered in REG-19. Attach the reply and annexures on
the portal and stop at the signature.

## Step 5 — revocation (REG-21)

Revocation applies only where the officer cancelled the registration; a taxpayer who applied for their own
cancellation cannot revoke it. Check the order before promising anything. Before REG-21 can succeed, every
return up to the effective date must be filed and the tax, interest and late fee paid. Build that list from
the portal's return dashboard, get the returns filed, then draft the application stating the ground on which
cancellation was ordered and how it has since been cured. The officer may propose rejection by notice in
REG-23, answered in REG-24; revocation is ordered in REG-22. The window to apply, and any extension of it,
are time limits — look them up and cite them.

## Step 6 — GSTR-10, the final return

GSTR-10 is filed once, after cancellation, separately from the periodic returns. It reports the stock held on
the day immediately preceding the effective date of cancellation, the tax payable on it, and the ARN of the
cancellation order. Reuse the REG-16 stock working rather than rebuilding it, and reconcile the two: if the
effective date in the order differs from the date applied for, the stock date moves and the figures change.
Where the rule requires the stock statement to be certified by a practising CA or CMA, say so and name what
the certificate must cover. The due date and the late fee for GSTR-10 are looked up, never recalled.

## Rules used

Every time limit, threshold, rate, useful life or fee goes in a **Rules used** block at the end: the rule, the
section / rule / notification, and the `kb` source URL with captured date, or "confirm on the portal /
notification". An unverified recollection is not a source.

## What the CA gets

Dated files in the client's GST folder: the amendment note or the stock and liability working, the draft
reply with its annexure index, and a one-page status note carrying every ARN and date. Raw client files are
never renamed or deleted. Always end with **Rules used**, and:

**Check before filing**
- GSTIN, legal name and effective date on the form against the order or the proving document.
- Whether the amended field is core or non-core, as the portal marks it, and the approval route.
- Every pending return filed and every due paid, with ARNs and challans listed.
- Stock date matched to the effective date of cancellation, totals computed by formula from the rows.
- Which authentication applies — EVC or DSC — and that the CA presses it.
