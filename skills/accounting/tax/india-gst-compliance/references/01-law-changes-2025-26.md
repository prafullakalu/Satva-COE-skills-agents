# What changed recently, and from when

LAST_VERIFIED: 2026-07-29

Read this before any engagement. Most GST errors in 2026 are not exotic — they
are last year's rules applied to this year's period, or this year's rules applied
to last year's period. Effective dates are the whole game here.

## The short version

| From | Change |
|---|---|
| 1 Oct 2024 | IMS launched (optional at first). Commercial rent from an unregistered landlord, and metal scrap from unregistered persons, brought under RCM. |
| 1 Nov 2024 | §128A amnesty (waiver of interest and penalty for §73 demands, FY 2017-18 to 2019-20) and §16(5)/(6) retrospective ITC relief operative. §74A introduced for periods from FY 2024-25. |
| 1 Jan 2025 | E-way bill restrictions: no EWB for documents older than 180 days; extension capped at 360 days from generation. 2FA on the EWB/e-invoice portals. |
| 1 Feb 2025 | GSTR-7 and GSTR-8 formats revised to invoice-level detail (NT 09/2025-CT). |
| 1 Apr 2025 | ISD registration and GSTR-6 distribution mandatory where common input services are shared across GSTINs under one PAN. 30-day IRN reporting limit extended to AATO ≥ ₹10 crore. |
| May 2025 | GSTR-1 Table 12 HSN reporting Phase 3 — dropdown selection, B2B/B2C split, value validations; Table 13 (documents issued) mandatory. |
| Jul 2025 | **GSTR-3B outward tables hard-locked.** Tables 3.1 and 3.2 auto-populate from GSTR-1/1A/IFF and are not editable. Corrections only via GSTR-1A. |
| 22 Sep 2025 | **GST 2.0 rate rationalisation.** 12% and 28% slabs withdrawn; structure becomes Nil / 5% / 18% with a 40% demerit rate. Special rates (3% precious metals, 0.25% rough diamonds) retained. |
| 1 Oct 2025 | IMS fully operational as the mechanism driving GSTR-2B. Risk-based 90% provisional refund extended to inverted duty structure claims filed on or after this date. |
| 1 Nov 2025 | Simplified/optional registration route for small taxpayers with low monthly output tax liability, with auto-approval in a short window (Rule 14A). Risk-based 90% provisional refund for zero-rated supplies operational. |
| Nov 2025 | GSTR-3B Table 3.2 (inter-state supplies to unregistered persons/composition/UIN) locked as well. |
| Around Dec 2025 – Jan 2026 | **Three-year filing bar enforced on the portal.** Returns not filed within three years of their due date can no longer be filed; an "Application for Unbarring Returns" facility exists for officer-approved exceptions. *The exact switch-on date was reported inconsistently — confirm on the portal for the period in hand.* |
| 1 Feb 2026 | Tobacco, pan masala and similar goods move to **40% GST**; **compensation cess abolished**; replaced by additional excise duty and a new Health & National Security (HSNS) cess. RSP-based valuation under Rule 31D for these goods. |
| Expected around Jul 2026 | **Phase 2 of GSTR-3B hard-locking: ITC.** Table 4A(1) expected to be driven by GSTR-2B/IMS with no manual B2B entry. Tables 4A(2) (import of services), 4B (reversals) and 4D (reclaim) expected to stay manual. **Verify the current status on the portal — this is the single most consequential open item for FY 2026-27 filings.** |
| Pending | 57th GST Council meeting — expected agenda includes registration, refund and audit simplification, removal of the goods/services distinction for refunds, and a decision on the post-cess levy path. Nothing is law until notified. |

## The three changes that most often break a return

### 1. Outward liability is no longer yours to type

Since the July 2025 period, GSTR-3B Tables 3.1 and 3.2 are auto-populated and
locked. The practical consequences:

- If the 3B figure is wrong, **GSTR-1 or the IFF is wrong**. Fix it there.
- The only same-period correction route is **GSTR-1A**, which can be filed **once**
  and cannot be revised. Compile every correction before filing it.
- The GSTR-1A window runs from after GSTR-1 is filed (or its due date) until
  GSTR-3B for that period is filed. Filing 3B closes it permanently.
- Sequence matters: GSTR-1 → review → GSTR-1A if needed → GSTR-3B. There is no
  going back a step.

### 2. Silence in IMS is consent

Invoices reported by suppliers land in the Invoice Management System. You may
Accept, Reject, or mark Pending. **Taking no action means the record is treated as
accepted** and flows into GSTR-2B. There is no neutral option.

If you act in IMS *after* GSTR-2B has been generated for the period, you must
trigger **Recompute GSTR-2B** on the portal before preparing GSTR-3B. Otherwise the
return is built on a superseded snapshot, and the mismatch surfaces later as a
DRC-01C. See `04-itc-and-ims.md`.

### 3. Rate changes have a time-of-supply problem, not a date problem

For supplies straddling 22 September 2025 or 1 February 2026, the applicable rate
is decided by **§14 of the CGST Act** (change in rate of tax), which looks at the
timing of the supply, the invoice and the payment together — not simply the
invoice date. Advances, continuous supplies and works contracts are where this
bites. Work it out per transaction; see `03-rates-and-classification.md`.

## Older reliefs still relevant to arrears work

- **§16(5)** — for FY 2017-18 to 2020-21, ITC in a GSTR-3B filed up to
  30 November 2021 is protected notwithstanding §16(4).
- **§16(6)** — relief where registration was cancelled and later revoked.
- **§128A** — waiver of interest and penalty for §73 demands covering FY 2017-18
  to 2019-20, subject to full payment of tax and the prescribed conditions and
  cut-offs. Fraud cases under §74, late fees and erroneous refunds are outside it.
  Check whether the taxpayer's window has closed before offering it as an option.
- **§74A** — for periods from FY 2024-25 onwards, replaces the separate §73/§74
  tracks with a common limitation framework and differentiated penalties.
