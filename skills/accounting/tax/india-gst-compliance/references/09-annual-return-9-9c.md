# Annual return — GSTR-9 and GSTR-9C

LAST_VERIFIED: 2026-07-29
VOLATILE: which tables are optional for a given financial year. This changes
almost every year by notification and is the single most common source of wasted
effort in annual return work.

## Applicability

| AATO in the FY | GSTR-9 | GSTR-9C |
|---|---|---|
| Up to ₹2 crore | Optional | Not required |
| ₹2 crore to ₹5 crore | Mandatory | Not required |
| Above ₹5 crore | Mandatory | Mandatory, self-certified |

Due **31 December** following the financial year. For FY 2025-26 that is
**31 December 2026**.

Not required from: Input Service Distributors, TDS deductors under §51, TCS
collectors under §52, casual taxable persons, and non-resident taxable persons.
Composition taxpayers file **GSTR-9A** where notified, not GSTR-9.

GSTR-9C has been **self-certified** since FY 2020-21 — no CA or cost accountant
certification is required. That reduced the cost, not the exposure: the taxpayer
now certifies the reconciliation themselves, so the quality of the underlying
work matters more, not less.

Missing the annual return has a cascading effect: it can block subsequent monthly
filings and it fixes the outer limit for §16(4) ITC where it is filed before
30 November.

## What the annual return actually is

GSTR-9 is a consolidation of what was **filed** during the year, reconciled to what
should have been filed. It is not an opportunity to re-file the year. There are
only two things you can do in it:

1. **Declare additional liability** not declared in the monthly returns, and pay it
   through **DRC-03** in cash (with interest). You cannot pay annual-return
   liability from the credit ledger through GSTR-9.
2. **Report** amendments and reversals that were already effected in the returns of
   April to November of the following year.

You **cannot** claim ITC that was missed and is now time-barred under §16(4).
You **cannot** claim a refund through GSTR-9. Both are frequently expected by
clients and both need saying early.

## Structure

| Part | Tables | Contents |
|---|---|---|
| I | 1–3 | Basic details, auto-populated |
| II | 4–5 | Outward supplies: taxable (4), and nil/exempt/non-GST and zero-rated (5) |
| III | 6–8 | ITC availed (6), reversed (7), and reconciliation with GSTR-2A/2B (8) |
| IV | 9 | Tax paid as declared in returns |
| V | 10–14 | Transactions of the FY declared in the next FY's returns (April–November) |
| VI | 15–19 | Demands and refunds, deemed supplies from job work, HSN summary for outward (17) and inward (18), late fee payable |

**Table 8** is the pressure point: the difference between ITC as per GSTR-2A/2B and
ITC availed. Differences here draw scrutiny notices, so each one needs a reason
recorded in the working paper — supplier filed late, credit deliberately not taken,
blocked credit, credit taken in the next year, and so on.

**Tables 17 and 18** (HSN summary of outward and inward supplies) are where most of
the preparation time goes. Inward HSN reporting has been relaxed in some years for
smaller taxpayers — check the notification for the specific FY before building it.

## Reconciliations that must be done before filing

1. **Books turnover → GSTR-1 → GSTR-3B → GSTR-9 Table 4/5.** List and quantify every
   reconciling item: unbilled revenue, revenue recognised in a different year,
   supplies without consideration under Schedule I, discounts, credit notes, and
   income booked net.
2. **Books ITC → GSTR-3B Table 4A → GSTR-2B → GSTR-9 Table 6/8.**
3. **Tax paid per GSTR-3B → cash and credit ledgers → GSTR-9 Table 9.**
4. **Rule 42/43 annual finalisation**, with interest on any shortfall from the
   monthly provisional reversals.
5. **RCM completeness for the whole year** — the annual return is the last practical
   chance to catch a missed RCM liability before an audit does.
6. **Credit notes issued after year end** but relating to the year, within the
   §34(2) time limit (30 November following the FY, or the annual return, whichever
   is earlier).
7. **Turnover per GSTR-9 → audited financial statements → income tax return and
   Form 26AS/AIS.** Departments cross-check these, so a difference you have not
   explained is a difference someone else will ask about.

## GSTR-9C

A reconciliation between the audited annual financial statements and GSTR-9.

| Part | Contents |
|---|---|
| A | Reconciliation of turnover (Tables 5–8), including unreconciled differences and reasons |
| B | Reconciliation of tax paid (Tables 9–11), with additional liability |
| C | Reconciliation of ITC (Tables 12–16), including expense-head-wise ITC in Table 14 |
| D | Auditor's/self-certified recommendation of additional liability |

Where the entity has multiple GSTINs under one PAN, the financial statements are
entity-level while GSTR-9C is **GSTIN-level**. A state-wise apportionment working
is needed and should be documented — it is the first thing asked for on scrutiny.

Table 14 (expense-head-wise ITC) is optional in some years. Check before building
it; it is expensive to prepare.

## Practical sequence

1. Confirm applicability from AATO, and confirm whether the taxpayer wants to file
   voluntarily where it is optional (filing a voluntary GSTR-9 fixes the §16(4)
   date if filed before 30 November — usually a reason **not** to file early).
2. Download the system-computed GSTR-9 and all monthly GSTR-1, GSTR-3B and GSTR-2B
   data for the year.
3. Build the reconciliations above in `work/`, one worksheet per reconciliation.
4. Quantify additional liability and pay through DRC-03 in cash before filing.
5. Complete the HSN summaries.
6. Review against `checklists/annual-return.md`.
7. Hand the pack to the taxpayer with the sign-off — GSTR-9, once filed, **cannot
   be revised**.
