---
name: fraud-red-flags
description: >-
  Detect and triage accounting fraud and error indicators in ledger data: vendor and payment anomalies, journal-entry tests, payroll and expense abuse, revenue manipulation, with analytic tests (Benford, duplicates, round amounts) and an escalation protocol. Use when asked to "check for fraud", "unusual transactions review", "duplicate payments test", "journal entry testing", "something looks off in the ledger".
metadata:
  department: "accounting"
  domain: "audit-controls"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Fraud red flags and analytics

A red flag is a reason to look, not proof. Use this to prioritise review and to design tests; accusations and investigations belong to management, legal counsel or internal audit.

## Fraud triangle
Pressure (targets, debts, covenants), opportunity (weak controls, override, unreviewed access), rationalisation. Controls reduce opportunity (internal-controls-matrix).

## Analytic tests (run on the full population, then investigate hits)
**Vendors and payables**
- Duplicate payments: same vendor + amount + date within 30 days, or same invoice number with variations (trailing characters, spaces, O/0).
- Vendor bank account shared with an employee, or vendors sharing a bank account or address; vendor address equals employee address or a PO box.
- New vendor paid immediately and in round amounts; vendors with only one invoice and a large amount; invoices just below approval limits (cluster at 95-99.9% of limit); invoice number sequence with no gaps for a vendor claiming many customers.
- Vendor bank detail changes followed by a payment in the next run.
- Payments without a PO or receipt; payee name differs from vendor master.

**Journals**
- Manual entries to revenue, reserves, accruals or cash near period end; entries posted on weekends/holidays/after hours; entries by users who rarely post; round-thousand amounts; entries with blank or vague descriptions; entries reversed next period; entries to unusual account combinations (revenue credited against unbilled/other receivables, expenses credited to capitalised assets).
- Post-close entries after the lock date; top-side adjustments not in the sub-ledger.

**Revenue**
- Spike in credit notes after period start; sales to new customers just before period end; unusual bill-and-hold or consignment; revenue without delivery evidence; growing receivables vs revenue (DSO up >10%); large unapplied cash.

**Payroll**
- Ghost employees (no HR file, no leave history, duplicate bank accounts or tax IDs); pay without timesheet; overtime outliers; terminated employees still paid; rate changes without HR approval.

**Expenses/cards**
- Same receipt submitted twice; weekend and holiday spending; split purchases to stay under limits; round-amount reimbursements; personal merchants; mileage over theoretical maximum.

**Cash**
- Lapping (customer payments applied to older balances so a theft stays hidden); unusual voids and refunds; large cash deposits not matching invoices; reconciling items aged over 60 days.

**Statistical**
- Benford's law on first digits of invoice amounts: expected frequency of digit d is log10(1 + 1/d) (1: 30.1%, 2: 17.6%, 3: 12.5%, 9: 4.6%). Flag a digit group where deviation is significant (chi-square or MAD) and review the underlying items; results show where to look, never proof.
- Z-score outliers within vendor/account (|z| > 3); month-over-month spikes.

## Behavioural/organisational flags
Employee never takes leave or insists on handling a process alone, lifestyle beyond means, resists audits, close relationship with a vendor, high turnover in finance, management override of controls, pressure to hit targets, frequent last-minute adjustments.

## Triage and escalation
1. Rule out error: confirm data, timing, and business explanation with the process owner (but not if the owner is the suspect).
2. Score: high (amount over materiality or pattern suggests intent) / medium / low. Document hits with evidence and date.
3. Preserve evidence: snapshot reports, audit logs and system access; do not alter records.
4. **Escalate to the controller/owner/audit committee or counsel**, per policy, without confronting the individual. Use the whistleblower channel if one exists.
5. Contain: freeze payment, change access, rotate credentials if appropriate, on instruction from authorised management.
6. Remediate controls afterwards.

## Do not
Do not conclude fraud from an analytic hit; do not discuss suspicions broadly; do not delete or "fix" suspicious entries; do not investigate alone once potential intentional misstatement is found.

## Output
Test log (test, population, hits, reviewed, disposition), prioritised exception list with evidence references, recommended control changes, escalation memo if required.

See also: `forensic-accounting` for the investigation phase once a red flag is substantiated (evidence handling, Benford script, report structure).
