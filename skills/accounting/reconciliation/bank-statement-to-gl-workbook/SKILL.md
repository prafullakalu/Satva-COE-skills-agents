---
name: bank-statement-to-gl-workbook
description: >-
  Reconcile a bank statement (Excel, or a simple text PDF) to a general-ledger export with a bundled dependency-free Python script and produce a reviewable Excel workbook with Summary, Recon Results, Unreconciled Bank and Unreconciled GL tabs. Matches by shared keys (batch, invoice, vendor or payment references), one-to-one, one-to-many and grouped totals within a threshold, then by name grouping. Use for "reconcile this statement to the GL file", "match bank lines to ledger lines in Excel", "convert the statement PDF to a workbook", "which bank items are unmatched", when volume makes manual matching slow. The workbook is a working paper that a person reviews; it is not the sign-off.
metadata:
  department: "accounting"
  domain: "reconciliation"
  owner: "satva-coe"
  status: "beta"
  license: "MIT"
  source: "https://github.com/ChipmunkRPA/bank-recon-skill/tree/main/skill"
---
<!-- Adapted from ChipmunkRPA/bank-recon-skill skill/ (MIT, Copyright (c) 2026 ChipmunkRPA). Modified by Satva: frontmatter, limits section and review controls added; script unchanged. -->

# Bank statement to GL workbook

Reconcile bank statement rows against GL rows and produce an `.xlsx` workbook an accountant can review in minutes. Use it for the matching grind; the reconciliation statement, sign-off and entries still follow `bank-reconciliation`.

## Workflow
1. Identify the bank statement file (`.xlsx`, or a text-based `.pdf`) and the GL workbook. Both are read from their first worksheet as three columns: date, amount, description or memo.
2. If the bank file is a PDF, the script first extracts the statement lines into a companion workbook (`<name>_extracted.xlsx` beside the PDF), then reconciles that. Open the extracted workbook and check the row count against the statement before trusting any result.
3. Confirm the threshold with the user. Default `0.00` (exact). A tolerance such as 0.02 to 1.00 is for rounding or fee noise and should be recorded in the working paper.
4. Run:
   ```bash
   python3 scripts/recon_logic.py <bank_xlsx_or_pdf> <gl_xlsx> <output_xlsx> [threshold]
   ```
5. Report matched bank rows, matched GL rows, unreconciled bank rows and unreconciled GL rows, then work the two unreconciled tabs first.

The script uses only the Python standard library, makes no network calls, and writes only the output workbook (and the extracted workbook for a PDF input). Never point the output path at a source file.

## Output workbook
- `Summary`: threshold, matched and unmatched counts, totals, matched total difference
- `Recon Results`: matched groupings with match basis and variance notes
- `Unreconciled Bank`: bank rows with no GL match
- `Unreconciled GL`: GL rows with no bank match

## Matching logic
1. Original signs are preserved in the output.
2. Amounts are compared by absolute value so bank polarity and debit/credit polarity can reconcile.
3. Shared extracted keys (batch ids, invoice ids, vendor or customer ids, tax or payment references) are matched first.
4. One-to-one, one-to-many, many-to-one and grouped many-to-many matches are allowed when totals fall within the threshold.
5. Remaining items use semantic name grouping plus summed-amount comparison.
6. Anything unmatched stays in its own tab; nothing is dropped.

## Limits you must state when reporting
- **Sign blindness.** Matching on absolute value can pair a receipt with an equal payment. Review every match whose bank and GL signs differ and every match made on name grouping rather than a key.
- **Grouped matches are hypotheses.** A many-to-many group that nets within threshold is not proof; spot-check large groups against remittance or batch documents.
- **PDF extraction is narrow.** It reads one family of PDF structure (text streams using ASCII85 plus Flate encoding, as written by common report generators). On the bundled sample under Windows line endings it extracted zero rows. Scanned PDFs need OCR. If the extracted workbook is empty or short, convert the statement to Excel or CSV instead of trusting the run. Never report "all reconciled" from a run that read zero bank rows.
- Only the first worksheet of each input is read, and the format is three columns with a date and a numeric amount in the second column.
- No opening or closing balance proof is produced. Confirm the statement opening balance equals the prior reconciled closing balance, and prove the adjusted bank and book balances in `bank-reconciliation` form.

## Review controls
The preparer runs the script; a different person reviews the unmatched tabs and a sample of matched groups. Unmatched items are classified (timing, bank item not in ledger, ledger error, bank error, unidentified) and carried forward per `bank-reconciliation`. Entries for bank fees and interest are drafted, approved, then posted; rerun after posting.

## Do not
- Treat a high match rate as reconciliation. The reconciliation is the zero difference between the adjusted balances.
- Raise the threshold to make unmatched rows disappear.
- Send statement or ledger files outside the engagement; the data is client financial data.
