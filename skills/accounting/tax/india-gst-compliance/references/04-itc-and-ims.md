# Input tax credit, IMS and GSTR-2B reconciliation

LAST_VERIFIED: 2026-07-29
VOLATILE: IMS mechanics (which records can be kept pending, and for how long),
the rollout of GSTR-3B Table 4A locking, and the treatment of partially reversed
credit notes. Check the current GSTN advisory before relying on the detail here.

This is the highest-risk area in GST. Wrongly availed credit carries interest,
penalty and — where the officer alleges intent — proceedings under §74/§74A. It is
also where the taxpayer's own money sits, so under-claiming is a real cost too.
The job is to claim everything defensible and nothing else.

## Contents

- [The five conditions](#the-five-conditions-16)
- [The time limit](#the-time-limit-164)
- [IMS](#the-invoice-management-system)
- [GSTR-2B reconciliation method](#gstr-2b-reconciliation-method)
- [Blocked credits](#blocked-credits-175)
- [Reversals](#reversals)
- [RCM credit](#rcm-credit)
- [Ledger restrictions](#ledger-restrictions-rule-86a-and-86b)
- [Mismatch notices](#mismatch-notices)

## The five conditions (§16)

All must be satisfied. Failing any one means no credit, however genuine the
expense.

1. **§16(2)(a)** — possession of a tax invoice or debit note issued by a registered
   supplier. Where e-invoicing applies to the supplier, a document without a valid
   IRN is not a valid tax invoice.
2. **§16(2)(aa)** — the supplier has furnished the details in their GSTR-1/IFF and
   they have been communicated to the recipient in GSTR-2B. This is what makes 2B
   the ceiling for B2B credit.
3. **§16(2)(b)** — the goods or services have been received. Bill-to/ship-to
   deliveries to a third party count as receipt by the person on whose direction
   they were delivered. Where goods arrive in lots, credit is available only on
   receipt of the last lot.
4. **§16(2)(ba)** — the credit has not been restricted under §38 (that is, it is not
   flagged in 2B as restricted).
5. **§16(2)(c)** — the tax has actually been paid to the Government by the supplier.
   This condition is the basis of Rule 37A recovery from the recipient.
6. **§16(2)(d)** — the recipient has furnished the return under §39.

Plus the **second proviso to §16(2)**: where the recipient does not pay the supplier
within **180 days** of the invoice date, the credit must be reversed with interest,
and can be re-availed when payment is made (Rule 37). There is no time limit on
re-availment.

## The time limit (§16(4))

Credit for an invoice or debit note relating to a financial year cannot be availed
after the **earlier of**:

- 30 November of the following financial year, or
- the date of filing the annual return for that year.

For FY 2025-26 that means **30 November 2026**. Any credit not taken by then is
lost, permanently. Flag approaching deadlines prominently — this is a hard date
that costs real money.

Two carve-outs remain relevant to arrears work: **§16(5)** protects credit for
FY 2017-18 to 2020-21 taken in a GSTR-3B filed up to 30 November 2021, and
**§16(6)** deals with periods where registration was cancelled and later revoked.

## The Invoice Management System

IMS sits between the supplier's GSTR-1 and the recipient's GSTR-2B. Records
reported by suppliers — B2B invoices, debit notes, credit notes, amendments, and
supplies made through e-commerce operators under §9(5) — appear on the IMS
dashboard for action.

| Action | Effect |
|---|---|
| **Accept** | Flows into GSTR-2B as eligible credit and auto-populates GSTR-3B Table 4A |
| **Reject** | Does not enter GSTR-2B. For a credit note, rejection increases the supplier's liability in their next period |
| **Pending** | Held back from GSTR-2B, actionable in a later period (subject to eligibility and time limits, and always within §16(4)) |
| **No action** | **Treated as accepted.** There is no neutral state |

Operational points that catch people out:

- **GSTR-2B is generated on the 14th.** Whatever the IMS state is at that moment is
  what flows through.
- **If the previous period's GSTR-3B was filed late, GSTR-2B for this period is
  never generated at all** — the system does not backfill it. Compute it manually:
  action every IMS record, then use **Recompute GSTR-2B**. This is the normal path
  when clearing a backlog, and it is easy to waste time waiting for a statement
  that is not coming.
- **If you act in IMS after the 14th, click "Recompute GSTR-2B"** before preparing
  GSTR-3B. Otherwise you are filing against a superseded snapshot, and the
  difference will surface later as a DRC-01C.
- **Pending is not available for every record type**, and where it is available it
  is time-limited (broadly one tax period for monthly filers, one quarter for
  quarterly filers). Verify the current advisory rather than assuming.
- **Rejecting a credit note has a consequence for the supplier**, not just for you.
  Reject only where the credit note is genuinely wrong, and tell the supplier —
  otherwise you create a dispute they discover at their own filing.
- Recent advisories added the ability to **accept a credit note while declaring a
  smaller ITC reversal** where only part of the credit was originally availed.
  Confirm the current mechanics before using it.
- IMS actions are the recipient's decision with legal consequence. **Prepare a
  recommended action list for each invoice and let the user execute it on the
  portal.** Do not take IMS actions on their behalf.

## GSTR-2B reconciliation method

Reconcile the purchase register against GSTR-2B at invoice level, not at total
level. A matched total can hide two offsetting errors.

Match on supplier GSTIN + invoice number + invoice date, then fall back to fuzzy
matching on GSTIN + value + date where the invoice number format differs (leading
zeros, prefixes and slashes are the usual culprits). Classify every line into:

| Class | Meaning | Usual remedy |
|---|---|---|
| **A** | In books, in 2B, all values agree | Claim |
| **B** | In books, not in 2B | Supplier has not filed, filed late, or reported the wrong GSTIN. Credit cannot be claimed now. Chase the supplier; track for a later period within §16(4) |
| **C** | In 2B, not in books | Missing purchase entry, or an invoice wrongly addressed to this GSTIN. Investigate before accepting — accepting a stranger's invoice is how a fake-invoice chain reaches you |
| **D** | Matched, value differs | Rate, quantity, discount or a credit/debit note not recorded. Claim the lower of the two pending resolution |
| **E** | Matched, GSTIN / POS / tax-head differs | IGST claimed as CGST+SGST or vice versa is **not** correctable by set-off. Supplier must amend |
| **F** | In 2B, marked ineligible | §17(5), POS in another state, or time-barred. Do not claim; report in Table 4D(2) |

Write the full classification to `work/difference-register.csv`. The register is
the deliverable, not the summary — it is what lets someone else finish the job.

**Then bring in payment evidence before deciding IMS actions.** Two sources cannot
tell you whether an unmatched IMS record is a missing document or somebody else's
invoice, and that is exactly the decision IMS forces. `scripts/ims_triage.py` adds
the bank/payment side and recommends an action per record. Treating every
untouched IMS record as safe because it "looks fine" is the same mistake as taking
no action — see `references/15-tds-and-payment-evidence.md` for why a payment from
a partner's personal account does not, on its own, disqualify anything.

**Never claim more ITC than GSTR-2B shows for B2B supplies.** Credits legitimately
outside 2B are limited and specific: import IGST (from ICEGATE/BoE), ITC on RCM
self-invoices, ISD credit via GSTR-6, and re-availment of previously reversed
credit. Each goes in its own table in GSTR-3B and each needs its own evidence.

## Blocked credits (§17(5))

Work through this list against the expense ledger every engagement. Reasoning from
memory reliably misses two or three.

- **Motor vehicles** for transport of persons with seating capacity ≤ 13 (including
  driver) — blocked, unless used for further supply of such vehicles, passenger
  transportation, or driving instruction. Related insurance, servicing, repair and
  maintenance is blocked on the same footing.
- **Vessels and aircraft**, with parallel exceptions.
- **Food and beverages, outdoor catering, beauty treatment, health services,
  cosmetic and plastic surgery**, and leasing/renting/hiring of the blocked
  vehicles above — unless used to make an outward supply of the same category, or
  where the employer is obliged to provide it under a law in force.
- **Membership of a club, health and fitness centre.**
- **Travel benefits to employees on vacation** (leave or home travel concession).
- **Works contract services** for construction of immovable property, except plant
  and machinery, and except where it is an input service for a further works
  contract.
- **Goods or services received for construction of immovable property on one's own
  account**, including when capitalised — again excepting plant and machinery.
  Note that the *Safari Retreats* reading of "plant or machinery" was reversed by a
  retrospective amendment substituting "plant and machinery"; check the current
  text before advising on a leasing or mall-construction fact pattern.
- **Goods or services on which composition tax is paid** under §10.
- **Goods or services received by a non-resident taxable person**, except goods
  imported.
- **Goods or services used for CSR obligations** under the Companies Act
  (blocked since 1 October 2023).
- **Goods lost, stolen, destroyed, written off, or disposed of by way of gift or
  free samples.** This includes writing off obsolete stock — a routine year-end
  entry with a GST consequence people forget.
- **Tax paid under §74, §129 and §130** (fraud demands, detention, confiscation).
- Personal consumption.

Blocked credit is reported in GSTR-3B Table 4B(1), not simply omitted. The portal
compares 4A against 2B; unexplained omissions generate their own questions.

## Reversals

- **Rule 42** — inputs and input services used partly for exempt or non-business
  purposes. Reverse monthly on a turnover ratio, then finalise for the year by
  September of the following FY, with interest on any shortfall.
- **Rule 43** — capital goods on the same principle, spread over 60 months.
- **Rule 37** — supplier not paid within 180 days. Reverse with interest; re-avail
  on payment.
- **Rule 37A** — where the supplier has not filed their GSTR-3B for the period by
  **30 September** following the FY, the recipient must reverse the credit by
  **30 November** following the FY. Re-availment is allowed when the supplier
  eventually files. GSTR-2B carries a Rule 37A indication; check it, because this
  reversal is entirely dependent on somebody else's behaviour and is easy to miss.
- **§17(2)/(3)** — proportionate reversal where there are exempt supplies. Note that
  "exempt supply" for this purpose includes certain transactions in securities and
  the value of land and completed buildings.

## RCM credit

RCM has two sides and both must appear:

1. **Liability** — declared in GSTR-3B Table 3.1(d) and **paid in cash**. It can
   never be discharged from the electronic credit ledger.
2. **Credit** — claimed in Table 4A(3), subject to the normal §17(5) tests, once
   the tax has been paid and the self-invoice raised.

Where the supplier is unregistered, a **self-invoice** under §31(3)(f) is mandatory
and a **payment voucher** under §31(3)(g) is required on payment. Without the
self-invoice, the credit is exposed even though the tax was paid. Check that the
self-invoice series exists and is reported in GSTR-1 Table 13.

## Ledger restrictions (Rule 86A and 86B)

- **Rule 86A** — the department can block the electronic credit ledger where credit
  is believed to have been fraudulently availed. If the ledger is blocked, filing
  changes materially. Check the ledger balance before computing utilisation.
- **Rule 86B** — a registered person whose taxable turnover in a month exceeds
  ₹50 lakh (other than exempt and zero-rated supplies) must discharge **at least 1%
  of the output tax liability in cash**. Exceptions apply, including where the
  person or specified officers have paid more than ₹1 lakh of income tax in each of
  the last two years, where a refund above ₹1 lakh was received on account of
  zero-rated supplies or inverted duty, and for government bodies and PSUs. Test
  this before assuming full credit utilisation.

## Mismatch notices

- **DRC-01B** — liability declared in GSTR-1 exceeds that in GSTR-3B beyond the
  prescribed threshold. Reply within 7 days or subsequent GSTR-1 filing is blocked.
- **DRC-01C** — ITC claimed in GSTR-3B exceeds GSTR-2B beyond the prescribed
  threshold. Same 7-day reply window and same blocking consequence.

Both are automated and both block further filing if ignored, which then cascades
into e-way bill blocking. If either is open, deal with it before preparing the
current return — see `10-penalties-interest-notices.md`.
