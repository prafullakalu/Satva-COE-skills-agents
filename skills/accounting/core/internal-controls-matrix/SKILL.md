---
name: internal-controls-matrix
description: >-
  Design, document and test internal controls: risk and control matrix (RCM), segregation of duties, key-control selection, sampling and test procedures, deficiency evaluation. Works for SMEs and SOX-style programmes. Use for "build a control matrix", "segregation of duties review", "test our controls", "control deficiency", "SOX-lite for a small company".
metadata:
  department: "accounting"
  domain: "audit-controls"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Internal controls matrix

Framework reference: COSO Internal Control - Integrated Framework (control environment, risk assessment, control activities, information and communication, monitoring). For listed US companies SOX 404 applies; the same method scales down for SMEs.

## Step 1: Scope by process and risk
Cycles: order-to-cash, procure-to-pay, payroll, inventory, treasury/cash, fixed assets, financial close and reporting, tax, IT general controls. Include entities/accounts above materiality (planning materiality commonly 0.5-1% of revenue or 5% of pre-tax income); aggregate smaller ones if risk is high.

## Step 2: Risk and control matrix (RCM)
One row per control:
| Field | Content |
|---|---|
| Process / risk ID | e.g. P2P-03: payment to a fictitious vendor |
| Risk statement | what can go wrong and which assertion fails (existence, completeness, accuracy, cut-off, valuation, rights, presentation) |
| Control description | who does what, how often, with which evidence |
| Type | preventive / detective; manual / automated / IT-dependent manual |
| Frequency | per transaction, daily, weekly, monthly, quarterly, annual |
| Owner and reviewer | named roles, not teams |
| Key control? | Y if it alone addresses the risk |
| Evidence | report, screenshot, signed checklist, system log |
| Test procedure and sample | see step 4 |

Write controls so a stranger could re-perform them. "Management reviews monthly" is not a control; "Controller reviews the AP aging report > 60 days by vendor, signs and dates, follows up on items > 5,000" is.

## Step 3: Core controls library (SME baseline)
- **Cash:** monthly bank reconciliations by someone who does not post cash, reviewed within 10 days; dual approval for payments over a limit; bank signatory list reviewed; no cash handling by the person who reconciles.
- **P2P:** PO before commitment above threshold; three-way match (PO, receipt, invoice); vendor master changes (bank details) verified by call-back to a known number and approved by someone other than the AP clerk; duplicate invoice check.
- **O2C:** pricing and credit-limit approvals; credit notes approved by someone outside billing; shipments matched to invoices; customer master changes controlled.
- **Payroll:** HR-authorised changes only; payroll approved by an independent person; exception report reviewed (payroll-accounting).
- **Journals:** manual journals above threshold or to sensitive accounts require independent approval with support; recurring journal list reviewed; post-close entries logged.
- **Close:** checklist with sign-offs; balance sheet reconciliations; flux review (month-end-close).
- **Fixed assets:** capitalisation approval, annual physical check.
- **IT:** user access reviews quarterly, joiner-mover-leaver process, admin rights limited, backups tested, change management for finance systems, MFA.

## Segregation of duties (SoD) matrix
Rows = duties: create vendor, approve invoice, enter bill, release payment, reconcile bank, post journals, approve journals, run payroll, change payroll rates. Mark combinations that one person must not hold (create vendor + release payment; enter bill + release payment; post journals + approve own journals; reconcile bank + handle cash; HR master data + payroll processing). Where staff is too small, document the compensating control: owner reviews bank statements directly and monthly vendor-change report.

## Step 4: Test
1. **Design effectiveness:** walkthrough one item end to end; does the control address the risk?
2. **Operating effectiveness:** sample size by frequency (typical): annual 1, quarterly 2, monthly 2-5, weekly 5-15, daily 20-40, per-transaction 25-60 (higher for high risk, lower for automated controls tested once plus ITGC). Select randomly across the period; include period end.
3. **Procedures:** inspect, re-perform, observe, inquire (inquiry alone never suffices). Record population, sample, attributes, exceptions.
4. **Exception handling:** 0 exceptions = effective; 1 exception in a small sample = extend sample once; repeat exception = deficiency.

## Step 5: Evaluate deficiencies
Classify by (a) likelihood and (b) magnitude of potential misstatement: **control deficiency** < **significant deficiency** (important enough to merit attention of those overseeing reporting) < **material weakness** (reasonable possibility that a material misstatement will not be prevented or detected on a timely basis). Consider compensating controls and whether fraud is involved (indicator of at least significant). Remediation plan: owner, action, date, retest.

## Do not
Do not test only the controls that are easy; do not accept "no exceptions noted" without the sample listing; do not let the control owner test their own control.

## Output
RCM workbook, SoD matrix with conflicts and compensating controls, test results with samples, deficiency log with severity and remediation plan.
