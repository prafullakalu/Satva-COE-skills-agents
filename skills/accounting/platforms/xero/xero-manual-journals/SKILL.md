---
name: xero-manual-journals
description: >-
  Prepares, validates and posts manual journals in Xero through the Satva Xero MCP: accruals, prepayments,
  depreciation, reclassifications, FX or clearing adjustments, reversals and corrections. Use for "post a journal in
  Xero", "accrue this expense", "reclass these amounts", "reverse the journal", "journal won't balance", "manual
  journal narration", "move balance between accounts", "tracking on a journal".
metadata:
  department: "accounting"
  domain: "journals"
  platform: "xero"
  owner: "satva-coe"
  status: "stable"
  license: "Satva-original"
  source: "original"
---

# Xero manual journals

Follow `xero-mcp-operating-rules`. A manual journal changes the ledger directly with no source document; treat it as
the highest-risk routine write.

## Tools used

Read: `list-manual-journals`, `list-accounts`, `list-tax-rates`, `list-trial-balance`, `list-profit-and-loss`,
`list-report-balance-sheet`, `list-organisation-details`, `list-history`, `list-journals` (read-only system
ledger; scope-gated).
Write: `create-manual-journal`, `update-manual-journal`, `add-history-note`, `upload-attachment`.

## Parameters (verified)

`create-manual-journal`: `narration` (required), `manualJournalLines[]` (min 2) each `{lineAmount, accountCode,
description?, taxType?}`, `date?` (YYYY-MM-DD), `lineAmountTypes?` (EXCLUSIVE | INCLUSIVE | NO_TAX, default NO_TAX),
`status?` (DRAFT default | POSTED), `url?` (link to support), `showOnCashBasisReports?` (default true).
`lineAmount`: **debits positive, credits negative.** Lines must sum to zero.
`update-manual-journal`: same fields plus `manualJournalID`; works only on DRAFT journals; send every line.
The tool exposes no tracking field for journal lines (tracking cannot be set through this MCP).

## Workflow

1. **State the business reason** in one sentence and identify the evidence (schedule, invoice, calculation). No
   evidence, no journal.
2. **Check the period.** `list-organisation-details`: if the journal date is on/before `Period Lock Date`, stop and
   tell the user. Do not move the date to dodge the lock.
3. **Resolve accounts.** `list-accounts`: every code must exist and be ACTIVE. Avoid journalling to control accounts
   (Accounts Receivable, Accounts Payable) and bank accounts: it breaks sub-ledger and reconciliation tie-outs. Xero
   journals to AR/AP need a contact, which this tool does not carry. Redirect: use an invoice/credit note or bank
   transaction instead.
4. **Build and prove balance.** Write the lines in a table with Dr/Cr columns, sum debits = sum credits to the cent.
   Show the effect on both accounts' current balance (`list-trial-balance` at the journal date).
5. **Tax.** With `NO_TAX` (the default) no tax is posted; if a line must carry tax (input/output) set `taxType` and
   `lineAmountTypes` deliberately, and confirm with `xero-tax-rates-and-sales-tax`. A reclass between two
   expense accounts with the same tax treatment needs no tax lines.
6. **Narrate** so a stranger understands it in 2 years: what, why, period, reference. e.g. `Accrue Oct hosting - INV
   pending - reverses 1 Nov`.
7. **Create as DRAFT first** (default). Show the user the resulting draft with the deep link. Only then either ask them
   to post in Xero or call `update-manual-journal status=POSTED` after confirmation.
8. **Verify** with `list-manual-journals manualJournalId` and `list-trial-balance`; confirm the balances moved as
   shown in step 4.
9. **Support.** Attach the schedule with `upload-attachment entityType=manual-journals` (1 MB max), or put a link in
   `url`. A `add-history-note` is permanent, so only for durable context.

## Common patterns

| Case | Lines (Dr / Cr) | Notes |
|---|---|---|
| Accrued expense | Dr expense / Cr accrued liabilities | reverse next period |
| Prepayment release | Dr expense / Cr prepaid asset | schedule per period |
| Depreciation | Dr depreciation expense / Cr accumulated depreciation | check fixed-asset register (`list-assets`) first if Xero asset module is used, to avoid double booking |
| Reclass | Dr correct account / Cr wrong account | same date range; narrate original document |
| Clearing/suspense clear | Dr real account / Cr suspense | list underlying items first |
| Reversal | swap signs of the original lines | there is no reverse tool; create a new journal dated the reversal day |

Auto-reversing is not a parameter here: create the second journal explicitly and note both IDs in the narrations.

## Pitfalls

- Sign convention inverted (credits entered positive) is the single most common error: re-read each sign.
- Journals do not appear on the invoice/bill ageing; do not use them to "settle" a receivable.
- `showOnCashBasisReports` true can put an accrual-type adjustment into cash-basis reports; for accruals/prepayments
  consider false, and confirm the org's reporting basis first.
- A POSTED journal cannot be edited through this MCP. Correct with a reversing journal, never by deleting history.
- Posting many journals: 1 call each, rate-limit aware; verify the first before sending the rest.
- Do not write a plug line to force balance; if it doesn't balance, a figure is missing.

## Output format

```
Org | date | period | lock date
Reason + evidence
Table: Dr/Cr | account code - name | amount | tax | description
Check: debits <x> = credits <x>; balances before -> after
Status: DRAFT/POSTED; ID + link; reversal plan (date, who)
```
