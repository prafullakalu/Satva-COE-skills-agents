# Returns, forms and due dates

LAST_VERIFIED: 2026-07-29
VOLATILE: every due date below can be extended by notification for a specific
period or state. Before relying on a date, check gst.gov.in "News and Updates"
for an extension covering that period. Late-fee caps and interest also change.

## Contents

- [Which returns apply](#which-returns-apply)
- [Due date table](#due-date-table)
- [Sequencing rules that cannot be broken](#sequencing-rules-that-cannot-be-broken)
- [GSTR-1 / IFF table by table](#gstr-1--iff-table-by-table)
- [GSTR-1A](#gstr-1a)
- [GSTR-2B](#gstr-2b)
- [GSTR-3B table by table](#gstr-3b-table-by-table)
- [QRMP](#qrmp)
- [Other returns](#other-returns)
- [The three-year bar](#the-three-year-bar)

## Which returns apply

| Taxpayer | Returns |
|---|---|
| Regular, AATO > ₹5 cr | GSTR-1 monthly, GSTR-3B monthly, GSTR-9, GSTR-9C |
| Regular, AATO ≤ ₹5 cr, monthly | GSTR-1 monthly, GSTR-3B monthly, GSTR-9 (optional ≤ ₹2 cr) |
| Regular, AATO ≤ ₹5 cr, QRMP | GSTR-1 quarterly (+ optional IFF), PMT-06 monthly, GSTR-3B quarterly |
| Composition (§10) | CMP-08 quarterly, GSTR-4 annual |
| ISD | GSTR-6 monthly |
| TDS deductor (§51) | GSTR-7 monthly |
| E-commerce operator collecting TCS (§52) | GSTR-8 monthly |
| Non-resident taxable person | GSTR-5 monthly |
| OIDAR supplier from outside India | GSTR-5A monthly |
| UIN holder claiming refund | GSTR-11 |
| Registration cancelled | GSTR-10 final return |
| Job work despatches | ITC-04 |

A taxpayer can be in several rows at once — a manufacturer that is also a TDS
deductor and an ISD files three separate streams. Ask, do not assume.

## Due date table

Dates are the day of the month **following** the tax period unless stated.

| Form | Period | Due |
|---|---|---|
| GSTR-1 | Monthly | 11th |
| GSTR-1 (QRMP) | Quarterly | 13th of the month after the quarter |
| IFF (QRMP, optional) | Months 1 and 2 of a quarter | 13th |
| GSTR-1A | Same period as GSTR-1 | From filing of GSTR-1 (or its due date) until GSTR-3B for that period is filed |
| GSTR-2B | Auto-generated | 14th (quarterly for QRMP, after quarter end) |
| GSTR-3B | Monthly | 20th |
| GSTR-3B (QRMP) | Quarterly | 22nd or 24th, by state group |
| PMT-06 (QRMP) | Months 1 and 2 | 25th |
| CMP-08 | Quarterly | 18th |
| GSTR-4 | Annual (composition) | 30 June following the FY |
| GSTR-5 | Monthly | 13th |
| GSTR-5A | Monthly | 20th |
| GSTR-6 | Monthly | 13th |
| GSTR-7 | Monthly | 10th |
| GSTR-8 | Monthly | 10th |
| GSTR-9 / 9C | Annual | 31 December following the FY |
| GSTR-10 | Final return | Within 3 months of cancellation or the cancellation order, whichever is later |
| GSTR-11 | Monthly | 28th |
| ITC-04 | AATO > ₹5 cr: half-yearly | 25 October and 25 April |
| ITC-04 | AATO ≤ ₹5 cr: annual | 25 April |
| LUT (RFD-11) | Annual | Before 1 April of the FY, or before the first zero-rated supply |
| CMP-02 (opt into composition) | Annual | 31 March preceding the FY |

**QRMP GSTR-3B state groups.** The 22nd applies to one group of states/UTs and the
24th to the other; the grouping is set by notification and is geographical
(broadly southern and western states in the first group, northern and eastern in
the second). Do not guess — confirm the group for the taxpayer's state.
`scripts/due_dates.py` carries the mapping and prints the source note; verify it
against the current notification for any period where the date is tight.

For FY 2025-26: GSTR-9 and GSTR-9C are due 31 December 2026.

## Sequencing rules that cannot be broken

- Returns are **strictly sequential**. GSTR-3B for a period cannot be filed until
  all earlier GSTR-3Bs are filed. Same for GSTR-1.
- **GSTR-2B for a period is not generated until the previous period's GSTR-3B is
  filed.** A taxpayer in arrears therefore has no 2B, which means no reliable ITC
  figure, which means the arrears must be cleared oldest-first.
- **GSTR-1 must be filed before GSTR-3B** for the same period.
- Filing GSTR-3B **closes the GSTR-1A window** for that period permanently.
- Two consecutive GSTR-3B defaults (or two quarters for a QRMP taxpayer) block
  **e-way bill generation** under Rule 138E, which stops despatches. This escalates
  from a compliance problem to an operational one fast.
- Continued default leads to notice in **GSTR-3A**, best-judgement assessment under
  **§62**, and can lead to suspension and cancellation of registration.

## GSTR-1 / IFF table by table

| Table | Contents | Watch for |
|---|---|---|
| 4 | B2B supplies (incl. SEZ, deemed exports) | Recipient GSTIN validity; POS per invoice |
| 5 | B2C inter-state, invoice value > ₹2.5 lakh | Threshold applies per invoice |
| 6 | Zero-rated: exports, SEZ, deemed exports | Shipping bill number/date; with or without payment of IGST |
| 7 | B2C others (consolidated, rate-wise, state-wise) | State-wise split is required, not optional |
| 8 | Nil-rated, exempt, non-GST outward supplies | Frequently left blank in error; feeds Rule 42/43 |
| 9 | Amendments to earlier periods (9A/9B/9C) | Original details must match exactly or the amendment fails |
| 10 | Amendments to B2C others | |
| 11 | Advances received / adjusted | Applies to services; goods are outside §12 advance liability |
| 12 | HSN summary | Phase 3: dropdown selection, split into B2B and B2C tabs, validated against other tables. 4 digits for AATO ≤ ₹5 cr, 6 digits above. Two digits is not accepted. |
| 13 | Documents issued | Invoice/CN/DN/delivery-challan series with from-to numbers, total issued and cancelled |

Table 12 and Table 13 are now validated against the rest of the return. Warnings
that appear at this stage are usually real — investigate rather than override.

## GSTR-1A

An optional amendment return for the **same** tax period, introduced so that
GSTR-3B's locked outward tables can still be corrected.

- Available after GSTR-1 is filed (or after its due date), until GSTR-3B for that
  period is filed.
- **Can be filed only once per tax period, and cannot itself be revised.**
- Cannot be used to change the recipient's GSTIN. That requires an amendment in a
  later period's GSTR-1 Table 9.
- Amendments made through GSTR-1A flow into the same period's GSTR-3B, which is
  the entire point of it.

Because of the one-shot rule, prepare a complete correction schedule first, get it
reviewed, and only then let the user file GSTR-1A.

## GSTR-2B

Auto-drafted, static ITC statement generated on the 14th (for QRMP, quarterly).
It is the reference for ITC — GSTR-2A is dynamic and is a reconciliation aid, not
a basis for claim.

- Generated from the supplier's GSTR-1/IFF/GSTR-5 **as filtered by IMS actions**.
- Splits ITC into eligible, ineligible under §17(5), and ineligible due to POS or
  time limits.
- If IMS actions are taken after generation, **Recompute GSTR-2B** must be clicked
  before GSTR-3B is prepared.
- Not generated for a period until the previous period's GSTR-3B is filed.

## GSTR-3B table by table

| Table | Contents | Editable? |
|---|---|---|
| 3.1(a) | Outward taxable supplies (other than zero-rated, nil, exempt) | **Locked**, from GSTR-1/1A |
| 3.1(b) | Zero-rated outward supplies | **Locked** |
| 3.1(c) | Other outward supplies (nil-rated, exempt) | **Locked** |
| 3.1(d) | **Inward supplies liable to reverse charge** | Manual — this is yours to get right |
| 3.1(e) | Non-GST outward supplies | **Locked** |
| 3.1.1 | Supplies under §9(5) via e-commerce operators | Auto-populated |
| 3.2 | Of 3.1(a): inter-state supplies to unregistered persons, composition taxpayers, UIN holders | **Locked** (since the November 2025 period) |
| 4A(1) | ITC on inward supplies (B2B) | Auto-populated from GSTR-2B; **expected to be locked from around July 2026 — verify** |
| 4A(2) | ITC on import of services | Manual |
| 4A(3) | ITC on inward supplies liable to reverse charge | Manual |
| 4A(4) | ITC from ISD | From GSTR-6 |
| 4A(5) | All other ITC | |
| 4B(1) | Reversal under Rules 38, 42, 43 and §17(5) | Manual |
| 4B(2) | Other reversals | Manual |
| 4D(1) | ITC reclaimed (previously reversed under Rule 37 etc.) | Manual |
| 4D(2) | Ineligible ITC under §16(4) or POS rules | Manual |
| 5 | Exempt, nil-rated and non-GST inward supplies | Manual |
| 5.1 | Interest and late fee | Late fee is system-computed; interest is declared |
| 6.1 | Payment of tax | Cash vs credit utilisation, subject to Rule 86A/86B |

Table 3.1(d) is the most commonly understated line in the whole return. RCM
liability must be paid **in cash** — it can never be discharged from the credit
ledger.

## QRMP

Available to taxpayers with AATO up to ₹5 crore in the preceding FY. Opt in or out
quarterly, within the window preceding the quarter.

- **Payment**: PMT-06 by the 25th for months 1 and 2, using either the **fixed sum**
  method (35% of the previous quarter's cash tax, or 100% of the previous month's
  where the last quarter was monthly) or the **self-assessment** method (actual
  liability less available credit). Fixed sum is safer against interest for a
  stable business; self-assessment is better where turnover has dropped.
- **IFF** for months 1 and 2 is optional but matters commercially — without it the
  recipient's credit is delayed to the quarter end. Capped at ₹50 lakh per month.
- **Interest** under the fixed sum method is charged only if the quarterly GSTR-3B
  liability exceeds what was paid, and only from the GSTR-3B due date, provided
  PMT-06 was paid on time. Under self-assessment, a shortfall attracts interest
  from the PMT-06 due date. This asymmetry is worth explaining to the user.
- **Late fee** does not apply to PMT-06.

## Other returns

- **CMP-08** — quarterly statement-cum-challan for composition taxpayers, tax paid
  in cash, no ITC. **GSTR-4** annually by 30 June following the FY. Note that a nil
  GSTR-4 still attracts late fee if missed, and the negative-liability issue from
  earlier years should be checked before filing.
- **GSTR-6** — ISD distribution. Mandatory since 1 April 2025 wherever common input
  services are procured for multiple GSTINs under one PAN. Cross-charge under
  §25(4) and ISD distribution are different mechanisms; do not conflate them.
- **GSTR-7 / GSTR-8** — now require invoice-level detail. The deductee's or
  supplier's credit depends on these being filed correctly and on time.
- **GSTR-10** — final return within three months of cancellation. Missing it keeps
  the registration alive for compliance purposes and accrues late fee.

## The three-year bar

Under §37(5), §39(11), §44(2) and §52(15), a return cannot be furnished after
**three years from its due date**. The portal now enforces this.

Consequences worth stating plainly to a taxpayer with arrears:

- The liability does not disappear. It becomes recoverable through assessment and
  demand proceedings instead, typically on a best-judgement basis under §62 or
  §63, usually for more than the correct amount.
- ITC for those periods is lost, because it can only be claimed in a return.
- An **Application for Unbarring Returns** exists on the portal for officer
  approval, but it is discretionary and does not cure the §16(4) ITC time limit.

If any period is approaching three years, that is the most urgent item in the
engagement regardless of what the user originally asked about. Say so.
