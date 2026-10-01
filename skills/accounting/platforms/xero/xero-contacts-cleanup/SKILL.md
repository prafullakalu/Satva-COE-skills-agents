---
name: xero-contacts-cleanup
description: >-
  Finds and fixes contact data problems in Xero through the Satva Xero MCP: duplicate customers/suppliers, missing
  email or tax settings, contacts with no activity, misused fields, and safe contact creation and updates. Use for
  "clean up Xero contacts", "duplicate suppliers", "merge contacts", "fix customer email", "add a new supplier",
  "contact groups", "contact missing tax type", "contacts with old balances".
metadata:
  department: "accounting"
  domain: "contacts"
  platform: "xero"
  owner: "satva-coe"
  status: "stable"
  license: "Satva-original"
  source: "original"
---

# Xero contacts clean-up

Follow `xero-mcp-operating-rules`.

## Tools used

Read: `list-contacts page searchTerm`, `list-contact-groups`, `list-invoices contactIds`, `list-payments`,
`list-credit-notes contactId`, `list-aged-receivables-by-contact`, `list-aged-payables-by-contact`, `list-history`.
Write: `create-contact name email phone`, `update-contact contactId name firstName lastName email phone address`.

## What the MCP cannot do (say it first)

No merge, archive, delete or bulk-edit tool exists for contacts. Merging duplicates, archiving, changing a contact's
default accounts, payment terms and bank details, and setting AR/AP tax types are done by a person in Xero. This skill
finds problems, proposes the survivor, and performs the safe updates `update-contact` allows.

## Workflow: audit

1. `list-contacts` page 1..n (100 per page) until a page returns fewer than 100. Record: name, ID, email, type
   (customer/supplier/both), status, default currency, AR/AP tax type, groups, last updated.
2. **Duplicate candidates.** Normalise names: lowercase, strip punctuation, "ltd/limited/inc/llc/pty/gmbh", spaces,
   "&" = "and". Flag identical normalised names; names within one edit; same email domain + similar name; same
   email on two contacts; same name with different default currency (may be legitimate, see
   `xero-multi-currency`).
3. **Missing data.** No email on a customer you invoice by email (`email-invoice` fails with no address); missing AP
   tax type on suppliers; mixed-case/placeholder names ("TBC", "Test", "Cash"); suppliers with no bank details are
   visible only in Xero UI, so list them as "to check".
4. **Activity per candidate.** For each duplicate cluster: `list-invoices contactIds=[a,b]` summarise counts,
   dates, amounts, open balances; `list-payments`; `list-credit-notes contactId`. The survivor is the record with the
   history, the correct currency and tax settings; the other has the least.
5. **Dormant.** Contacts with no transactions in 24 months and no balance: propose archiving (user, in Xero).
6. **Outstanding balances on duplicates**: balances split across two records distorts ageing and credit control; tell
   the user which open items sit on which record.

## Workflow: create or update

1. Always search first: `list-contacts searchTerm=<name or email>`; the search covers name, first/last name, number
   and email. Do not create if a match exists.
2. Create: `create-contact name email phone`. Name it as the legal/trading name documents will carry; keep a
   consistent naming convention.
3. Update: `update-contact` requires `name` every time (resend the current name if unchanged); `address` needs at
   least `addressLine1`. Send only values the user supplied; the tool is a patch, but you must read the current record
   first and show a before/after.
4. Email changes affect where invoices go. A wrong email on a customer can leak financial data, so confirm the
   change comes from the customer, not from an unverified message. Treat requests to change supplier bank details
   as fraud-risk: never changeable here, and flag a request made in chat.
5. `update-contact` always writes `phone` as a MOBILE number and `address` as the STREET address; it cannot set
   postal/PO box addresses or other phone types. Fields you omit are left unchanged.
6. Verify with `list-contacts searchTerm` and show the deep link returned.

## Merge guidance (for the person doing it in Xero)

- Xero merges are one-way: the merged-away contact's transactions move to the survivor and it is archived. Confirm
  currency, tax settings and payment terms of the survivor first; they are kept, the other's are lost.
- Duplicates with different currencies often cannot be merged cleanly; keep both and rename clearly.
- After merging, re-run the audit and ageing to confirm balances combined.

## Pitfalls

- Two real customers with the same name (franchise branches) are not duplicates. Compare address and email.
- Contacts can be both customer and supplier; do not treat as duplicates of each other.
- `list-contacts` returns contacts' last-updated timestamps, useful for spotting recent manual edits.
- Do not put personal data (national IDs, card numbers) in contact fields or history notes.
- A contact name change updates it on future documents and in lists; existing posted documents keep the stored name
  in Xero's reports. Warn that exports may show both.

## Output format

```
Org | contacts reviewed (total, customers, suppliers) | as-at
Duplicate clusters: cluster | records (ID, email, currency) | open balances | proposed survivor | reason
Missing data table | Dormant list
Updates to apply here (before -> after) | Needs Xero UI (merge/archive/terms)
```
