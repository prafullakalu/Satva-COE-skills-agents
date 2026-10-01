# When something is blocked or has gone wrong

LAST_VERIFIED: 2026-07-29
VOLATILE: reply windows, condonation limits and the availability of amnesty
schemes. Verify the current position before telling anyone a deadline — several of
these windows are short and non-extendable.

Most of these situations share a shape: **the portal blocks filing, the liability
keeps accruing, and the block cascades.** Non-filing suspends registration;
suspension blocks e-way bills; blocked e-way bills stop despatches. So the order of
operations matters more than the individual remedy, and the first job is always to
work out what is actually blocking what.

## Contents

- [Triage](#triage-what-is-actually-blocking)
- [Registration suspended](#registration-suspended)
- [Registration cancelled](#registration-cancelled)
- [Voluntary cancellation](#voluntary-cancellation-reg-16)
- [Credit ledger blocked (Rule 86A)](#credit-ledger-blocked-rule-86a)
- [E-way bill blocked (Rule 138E)](#e-way-bill-blocked-rule-138e)
- [DRC-01B and DRC-01C](#drc-01b-and-drc-01c)
- [ASMT-10 scrutiny](#asmt-10-scrutiny)
- [Best-judgement assessment](#best-judgement-assessment-s62)
- [Time-barred returns](#time-barred-returns)
- [Return backlog](#return-backlog)
- [Negative liability](#negative-liability-in-cmp-08--gstr-4)
- [GSTR-2B not generated](#gstr-2b-not-generated)
- [Payment made but not reflected](#payment-made-but-not-reflected)
- [Refund deficiency memo](#refund-deficiency-memo-rfd-03)
- [Registration data problems](#registration-data-problems)

## Triage: what is actually blocking

Run this before proposing any remedy. It takes five minutes and prevents solving
the wrong problem.

1. **Registration status** — Search Taxpayer, or the dashboard header. Active,
   suspended, or cancelled?
2. **Is there an open SCN?** Both notice tabs. REG-17 (cancellation SCN) changes
   everything about the timeline.
3. **Which periods are unfiled?** Returns dashboard, every FY back to registration.
4. **Is any period within 90 days of the three-year bar?** Run
   `scripts/due_dates.py --timebar`.
5. **Are the ledgers usable?** Cash balance, credit balance, and whether the credit
   ledger is blocked.
6. **Is e-way bill generation blocked?**
7. **Any open DRC-01B / DRC-01C / ASMT-10 / ASMT-13?**

Then state the dependency chain to the user before doing anything: *"e-way bills
are blocked because two GSTR-3Bs are unfiled; the older one is 40 days from the
three-year bar; that one has to be filed first and it needs a cash payment because
the credit ledger is blocked under Rule 86A."* People make better decisions when
they can see the chain.

## Registration suspended

Suspension is not cancellation. The registration exists, but outward supplies
cannot be made under it and e-way bills are blocked.

**Common causes**: non-filing of returns for the prescribed continuous period; a
significant GSTR-1 vs GSTR-3B or GSTR-3B vs GSTR-2B mismatch flagged in **REG-31**;
an application for cancellation pending; Aadhaar authentication or physical
verification failure; bank account not furnished within the prescribed period
(Rule 10A).

**What to do**

1. Find the reason. It is in the suspension intimation or REG-31 in the notices
   tab — do not guess, because the remedy differs entirely.
2. If **non-filing**: file every pending return, oldest first. Suspension is
   generally revoked automatically once the defaults are cleared. Check the three-
   year bar first, because some of the backlog may be unfilable.
3. If **REG-31 mismatch**: reply within the stated window (typically 30 days)
   explaining the difference with a reconciliation. This is exactly the difference
   register the skill already produces — attach it.
4. If **Rule 10A bank account**: add the bank account through non-core amendment
   (REG-14). This is usually the fastest of all these to fix.
5. If **Aadhaar / physical verification**: complete the authentication or cooperate
   with the site visit.

**While suspended**: do not raise tax invoices. The liability for supplies actually
made still exists and still has to be declared once filing resumes — suspension
suppresses the ability to comply, not the obligation.

## Registration cancelled

### By the officer

Preceded by **REG-17** (show cause) with a **7 working day** reply window in
**REG-18**. Replying properly at this stage is far cheaper than revocation later —
treat an REG-17 as urgent regardless of what the user originally asked for.

If cancellation has already happened (order in **REG-19**):

**Revocation — REG-21**

- Apply within **90 days** of the cancellation order.
- Beyond 90 days, extension is discretionary — by the Additional or Joint
  Commissioner, and then the Commissioner, up to a further 180 days in total.
  Discretionary means it may be refused.
- **All pending returns must be filed before REG-21 can be submitted.** The portal
  enforces this. So the sequence is: clear the backlog, pay tax, interest and late
  fee, then apply.
- Revocation is only available where the **department** cancelled. A voluntary
  cancellation cannot be revoked — the only route is a fresh registration.
- The officer may issue **REG-23** seeking clarification; reply in **REG-24**
  within 7 working days. Missing this reply loses the application.
- Order in **REG-22** (revoked) or **REG-05** (rejected).

**If revocation is not available or fails**: apply for fresh registration. Note
that the old GSTIN's liabilities survive, ITC on the old registration is generally
lost, and the department may query why a fresh registration is being sought — be
straightforward about it.

**GSTR-10 final return** is due within three months of cancellation or the
cancellation order, whichever is later, with reversal of ITC on stock in hand under
§29(5). This is owed even where revocation is being pursued, and it accrues late
fee independently.

## Voluntary cancellation (REG-16)

**Tier 3 — the user submits this themselves.** It is an irreversible business
decision that cannot be revoked, and getting it wrong means re-registering from
scratch.

Before it is even considered, make sure the user understands: all returns up to the
cancellation date must still be filed; GSTR-10 is due within three months; ITC on
stock in hand must be reversed under §29(5); and if they later need registration
they start over with a new GSTIN and no continuity.

## Credit ledger blocked (Rule 86A)

The department can block the electronic credit ledger where it believes credit was
fraudulently availed or is ineligible. The credit is not erased — it cannot be
used.

**Practical effect**: everything must be paid in cash. This can be sudden and large,
and it is the reason to check ledger usability in the preflight rather than
discovering it at the payment step.

**What to do**

1. Screenshot the blocked balance and the block details from the ledger screen.
2. Find out why. There may be no notice — Rule 86A does not require a prior hearing,
   which is itself frequently litigated.
3. Assemble the evidence for the affected credit: invoices, proof of receipt, proof
   of payment to the supplier, and the supplier's filing status.
4. Make a written representation to the jurisdictional Commissioner or Joint
   Commissioner. Representations are expected to be decided within about 15 days.
5. **A Rule 86A block lapses automatically after one year** from the date it was
   imposed. If the block is older than a year, say so — the ledger should have been
   released.
6. Meanwhile the return still has to be filed on time. Compute the cash requirement
   early and tell the user the number, because arranging it takes days.

Where the amount is significant or the block looks unfounded, this is a
writ-petition situation. Recommend a professional; do not draft litigation.

## E-way bill blocked (Rule 138E)

Triggered by non-filing of GSTR-3B for **two consecutive tax periods** (two
quarters for QRMP), or CMP-08 for two consecutive quarters.

This is the point where a compliance problem becomes an operational one — goods
cannot legally move, and moving them anyway risks detention under §129 with tax and
penalty, and tax paid under §129 is a blocked credit under §17(5). Treat it as
urgent.

**Fastest route**: file the pending returns. Unblocking is generally automatic
within a day; the EWB portal also has an update-from-common-portal option to pull
the status through immediately.

**If filing is not possible right now** (funds, or a barred period): apply in
**EWB-05** to the jurisdictional Commissioner with reasons. Services → User
Services → My Applications → "Application for unblocking of e-way bill". The
officer may grant unblocking in **EWB-06** for a specified period, or reject after a
hearing. It is discretionary and slower than just filing, so treat it as the
fallback rather than the plan.

## DRC-01B and DRC-01C

Automated, unforgiving of deadlines, and they block further filing.

| | DRC-01B | DRC-01C |
|---|---|---|
| Rule | 88C | 88D |
| Trigger | GSTR-1 liability exceeds GSTR-3B beyond the threshold | ITC in GSTR-3B exceeds GSTR-2B beyond the threshold |
| Reply | Part B, within **7 days** | Part B, within **7 days** |
| Options | Pay the difference through DRC-03, or explain it | Same |
| If ignored | GSTR-1 for the next period is blocked | Same |

**How to reply well**: the reply is a reconciliation, not an assertion. Take the
difference register, isolate the rows explaining the gap, and give the reason with
figures — supplier filed late, credit deliberately not taken, credit note timing,
RCM credit correctly claimed outside 2B, import IGST from a Bill of Entry. A reply
saying "the difference is on account of timing" without the rows behind it invites
an ASMT-10.

Where the difference is genuine tax, paying through **DRC-03** before the deadline
usually costs less than arguing, because interest keeps running.

Submitting the reply is Tier 2 — show the user the full text and the attachments
first.

## ASMT-10 scrutiny

Scrutiny of returns under §61. Reply in **ASMT-11** within the stated period
(commonly 30 days). A satisfactory reply closes it with **ASMT-12**; an
unsatisfactory one leads to §65 audit, §67 inspection, or a demand under §73/§74/
§74A.

Take these seriously and answer every parameter raised individually, with the
supporting reconciliation attached. Where the notice has a point, say so and pay —
partial candour is more effective than blanket denial, and the department's next
step is more expensive than the tax.

## Best-judgement assessment (§62)

Where a return was not filed after a **GSTR-3A** notice, the officer may assess on
a best-judgement basis and issue **ASMT-13**. The assessed amount is usually far
higher than the real liability.

**The important detail, and it is easy to miss:** the ASMT-13 order is **deemed
withdrawn if the return is filed within 60 days** of the order — extendable to 120
days on payment of an additional late fee. Interest and late fee still apply, but
the inflated assessment disappears.

So whenever a client mentions an assessment order, find the date immediately and
work out how many days are left. This is often the single highest-value thing to
notice in an engagement. After the window closes, the only routes are appeal
(APL-01, within 3 months, 10% pre-deposit) or rectification.

## Time-barred returns

Under §37(5), §39(11), §44(2) and §52(15) a return cannot be furnished after
**three years from its due date**, and the portal enforces it.

State the consequences plainly, because people assume a barred return means a
forgiven liability:

- The liability does not disappear. It is recovered through assessment and demand
  instead — usually best-judgement, usually for more than the correct amount.
- **The ITC for those periods is lost**, because credit can only be claimed in a
  return.
- Late fee and interest continue to accrue on the underlying liability.

There is an **Application for Unbarring Returns** on the portal for
officer-approved exceptions. It is discretionary, and — this matters — **it does
not cure the §16(4) ITC time limit**. Unbarring lets you file; it does not give the
credit back.

If any period is within 90 days of the bar, that is the most urgent item in the
engagement regardless of what the user asked about. Say so first, before anything
else.

## Return backlog

1. List every unfiled period, oldest first, with the due date and days to the
   three-year bar.
2. Anything already barred goes to the unbarring route or to assessment — separate
   it out, because it cannot be filed and time spent preparing it is wasted.
3. File strictly oldest-first. Returns are sequential and **GSTR-2B does not
   generate for a period until the previous period's GSTR-3B is filed**, so ITC for
   the whole backlog is invisible until you start clearing it.
4. Compute the cumulative late fee and interest up front and give the user the
   total before starting. It is often large, and the decision about sequencing
   sometimes changes once they see it.
5. Check whether §16(4) has already extinguished the ITC for the older periods —
   filing a return whose credit is time-barred still costs late fee and tax without
   recovering the credit, which changes the arithmetic.
6. Check whether any amnesty is currently open (§128A covered FY 2017-18 to
   2019-20 for §73 demands, subject to conditions and cut-offs). Verify whether the
   window is still available before offering it.

Filing a long backlog is a Tier 2/Tier 3 marathon. Do one period completely —
reconcile, compute, file, download the ARN — before starting the next. Do not
prepare six periods and file them in a batch; if something is wrong in the
approach, you want to find it after one period, not six.

## Negative liability in CMP-08 / GSTR-4

A long-standing composition problem: a negative liability arising in CMP-08 gets
carried into the negative liability statement and then wrongly adjusted, and GSTR-4
shows tax payable that has in substance already been paid.

Check the negative liability statement before filing GSTR-4, and if there is an
unexplained balance, raise a grievance rather than paying twice. Do not simply pay
the figure the portal shows.

## GSTR-2B not generated

Almost always one of:

- The previous period's GSTR-3B is not filed. Clear it.
- It is before the 14th. Wait.
- QRMP — 2B is quarterly, not monthly.
- Recompute is pending after IMS actions.

Do not prepare GSTR-3B without a current 2B. Doing so means the ITC figure is
unverified, which is the one figure in the return that most needs verifying.

## Payment made but not reflected

1. Check **Challan History** for the CIN.
2. If the amount left the bank but no CIN was generated, raise a **PMT-07**
   grievance with the bank reference. Do not pay again — a duplicate payment sits
   in the cash ledger and getting it refunded is slow.
3. NEFT/RTGS payments can take hours; over a weekend, longer. Factor this into the
   deadline rather than discovering it at 23:00 on the 20th.
4. Where a payment was made under the wrong head or the wrong GSTIN, use **PMT-09**
   to transfer between heads. PMT-09 cannot move money between GSTINs — that needs
   a refund claim.

## Refund deficiency memo (RFD-03)

A deficiency memo requires a **fresh application**, and the time already spent does
not extend the two-year limitation under §54. So completeness on the first filing
is worth real effort.

Read the memo's specific deficiency, fix it, and re-file with a covering note
mapping each deficiency to the document that answers it. Check the remaining
limitation period before doing anything else — if it is close, that changes the
priority.

## Registration data problems

- **Core field amendment** (legal name, principal place of business, addition of a
  place of business, partners/directors) — REG-14, requires officer approval,
  typically within 15 working days.
- **Non-core amendment** (bank account, email, mobile, minor details) — REG-14,
  auto-approved. This is the route for the Rule 10A bank account problem.
- **PAN cannot be amended.** A PAN change means a new registration.
- **Aadhaar authentication / biometric verification** pending will hold up
  registration, amendment and refunds. In several states biometric verification at
  a GST Suvidha Kendra is required — the appointment has to be booked and attended
  by the person, so flag it early.
- **Legal name mismatch with PAN** blocks several actions and is fixed at the PAN
  end first, then amended here.
