# Pre-filing checklist — GSTR-3B

Copy into `work/`. Do not start this until GSTR-1 (and GSTR-1A, if needed) for the
period is settled — GSTR-3B outward tables are locked to it.

## Prerequisites

- [ ] GSTR-1 / IFF for the period filed
- [ ] GSTR-1A filed if corrections were needed, **or** confirmed not needed
- [ ] Previous period's GSTR-3B filed (otherwise GSTR-2B will not generate)
- [ ] GSTR-2B for the period downloaded, and its generation date noted
- [ ] IMS actions completed **before** the 14th; if taken after, **Recompute
      GSTR-2B** clicked and the fresh 2B downloaded
- [ ] No open DRC-01B or DRC-01C

## Outward tables (locked — verify, do not adjust)

- [ ] Auto-populated Table 3.1 matches the computed outward liability to the rupee
- [ ] Auto-populated Table 3.2 (inter-state to unregistered / composition / UIN)
      matches
- [ ] Any difference traced to GSTR-1, and **not** compensated elsewhere in 3B
- [ ] Table 3.1.1 (§9(5) e-commerce supplies) reviewed

## Reverse charge — Table 3.1(d)

- [ ] Expense ledger screened against `references/05-rcm.md`, including the
      negatives ("checked, none")
- [ ] Rent from unregistered landlords, legal fees, GTA, security, director
      payments, sponsorship, metal scrap all specifically considered
- [ ] **Import of services** considered: software subscriptions, cloud, overseas
      consultants, intra-group charges, advertising platforms
- [ ] Time of supply applied (30 days goods / 60 days services from the supplier's
      invoice, or earlier payment/receipt)
- [ ] Self-invoices raised under §31(3)(f), and included in GSTR-1 Table 13
- [ ] Payment vouchers issued under §31(3)(g)
- [ ] RCM liability will be paid **in cash** — not from the credit ledger

## ITC — Table 4

- [ ] Purchase register reconciled to GSTR-2B **at invoice level**, classified
      A to F per `references/04-itc-and-ims.md`
- [ ] Table 4A(1) does not exceed GSTR-2B eligible credit
- [ ] Credit claimed outside 2B is limited to import IGST (BoE), RCM, ISD (GSTR-6)
      and re-availment — each with its own evidence
- [ ] §16(2) conditions satisfied for every claim
- [ ] §17(5) screen run against the expense ledger, not from memory
- [ ] Rule 42 / 43 reversal computed where there are exempt or non-business supplies
- [ ] Rule 37 reversal for suppliers unpaid beyond 180 days
- [ ] Rule 37A checked against the 2B indication
- [ ] §16(4) time limit checked — nothing claimed beyond 30 November of the
      following FY
- [ ] Re-availment in Table 4D(1) supported by the earlier reversal
- [ ] Ineligible credit reported in 4B/4D(2), not silently dropped
- [ ] Import IGST agreed to ICEGATE / Bill of Entry data

## Computation and payment

- [ ] Net liability computed with `scripts/gst_compute.py`, not by hand
- [ ] Recomputed a second way (line-item vs rate-wise aggregate); the two agree
- [ ] Interest under §50 computed for any late payment or utilised wrong credit
- [ ] Late fee checked against the caps for this AATO
- [ ] Electronic cash and credit ledger balances confirmed from the portal
- [ ] Credit utilisation order applied correctly (IGST first, then CGST/SGST within
      their own restrictions)
- [ ] **Rule 86B** tested: taxable turnover above ₹50 lakh in the month means at
      least 1% of output liability in cash, unless an exception applies
- [ ] Cess liability and cess credit kept separate (cess credit only against cess)
- [ ] Challan generated in advance if the cash balance is short

## Reconciliations that must tie

- [ ] GSTR-1 outward tax = GSTR-3B Table 3.1 + 3.2
- [ ] Books turnover = GSTR-1 turnover, or a listed reconciling item
- [ ] GSTR-2B eligible ITC = Table 4A less listed reversals
- [ ] Output − ITC = net payable
- [ ] Ledger balances agree with the portal

## Self-review and sign-off

- [ ] `checklists/self-review.md` completed
- [ ] Difference register has no unexplained items of any size
- [ ] Red-flag list in SKILL.md Step 8 reviewed; none triggered, or escalated
- [ ] Filing pack prepared
- [ ] Named reviewer has signed off
- [ ] User reminded: **GSTR-3B cannot be revised once filed**, and filing it closes
      the GSTR-1A window for the period permanently
