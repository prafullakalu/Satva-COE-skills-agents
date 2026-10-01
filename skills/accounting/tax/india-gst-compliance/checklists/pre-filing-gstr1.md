# Pre-filing checklist — GSTR-1 / IFF

Copy this into `work/` and fill it in. An unticked line is a finding, not a
formatting problem. Record "N/A — reason" rather than leaving anything blank.

## Scope and setup

- [ ] GSTIN confirmed and checksum-validated (`scripts/gstin_check.py`)
- [ ] Tax period and scheme (monthly / QRMP) confirmed
- [ ] Due date computed, including any extension notified for this period
- [ ] Period is not time-barred; all prior GSTR-1s are filed
- [ ] AATO of the preceding FY known (drives HSN digits and e-invoice applicability)

## Completeness of outward supplies

- [ ] Sales register totalled independently; total agrees with the accounting system
- [ ] Invoice series is continuous — no gaps, no duplicates, no numbers outside the
      declared series
- [ ] Cancelled invoices identified and excluded, and reported in Table 13
- [ ] Credit and debit notes issued during the period captured, with the original
      invoice reference
- [ ] Export invoices captured with shipping bill number and date
- [ ] SEZ supplies captured, with or without payment of IGST correctly marked
- [ ] Deemed export supplies captured
- [ ] Advances received against **services** captured (Table 11A), and advances
      adjusted against invoices reversed (Table 11B)
- [ ] Supplies through e-commerce operators captured, and §9(5) supplies separated
- [ ] Nil-rated, exempt and non-GST outward supplies captured (Table 8)
- [ ] **Non-obvious supplies considered**: sale of fixed assets and scrap, branch
      transfers to another state under the same PAN, supplies to related parties
      without consideration (Schedule I), recoveries from employees, free samples,
      barter and exchange, and any income booked net of an expense

## Accuracy

- [ ] Place of supply determined **per invoice**, not from the billing address
- [ ] IGST vs CGST/SGST consistent with the POS in every row
- [ ] Bill-to/ship-to transactions treated as two supplies where applicable
- [ ] Rate applied verified against the current notification for this tax period
- [ ] Any supply straddling a rate-change date tested under §14 (time of supply)
- [ ] Recipient GSTINs validated (format, checksum, and active status where the
      value is material)
- [ ] Taxable value reconciles to the invoice value less discounts shown on the
      invoice; post-supply discounts tested against §15(3)(b)
- [ ] Rounding applied consistently

## E-invoicing

- [ ] E-invoicing applicability determined from AATO in **any** FY since 2017-18
- [ ] Every B2B / SEZ / export invoice has a valid IRN
- [ ] Count and value of the IRN dump reconciled to the sales register
- [ ] No invoice past the 30-day IRN reporting window (AATO ≥ ₹10 cr)
- [ ] No live IRN against an invoice cancelled in books
- [ ] Auto-populated GSTR-1 data compared with the IRN dump, differences explained

## Tables 12 and 13

- [ ] HSN/SAC at the correct digit count (4 or 6 by AATO)
- [ ] HSN codes selected from the portal dropdown, B2B and B2C tabs both completed
- [ ] Table 12 values reconcile to the taxable values elsewhere in the return
- [ ] Table 13 document summary complete: invoices, credit notes, debit notes,
      delivery challans, receipt vouchers, payment vouchers, **RCM self-invoices**
- [ ] Issued and cancelled counts agree with the series

## Cross-checks before filing

- [ ] GSTR-1 turnover reconciled to books turnover, with every reconciling item
      listed and quantified
- [ ] Comparison against the previous period: any unexplained swing investigated
- [ ] E-way bill data compared with the sales register
- [ ] Any open DRC-01B from an earlier period resolved

## Sign-off

- [ ] Difference register has no unexplained items
- [ ] Filing pack prepared with the source of every figure
- [ ] Named reviewer has read the pack and signed off
- [ ] User has been told: once GSTR-1 is filed, the only same-period correction is
      **GSTR-1A, which can be filed once and cannot be revised**
