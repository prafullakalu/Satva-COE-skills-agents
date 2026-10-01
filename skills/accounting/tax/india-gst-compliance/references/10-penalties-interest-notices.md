# Late fee, interest, penalties and notices

LAST_VERIFIED: 2026-07-29
VOLATILE: late-fee caps and any amnesty in force. Interest rates are statutory but
have been amended retrospectively before — check §50 and Rule 88B as they stood
for the period concerned.

## Late fee (§47)

| Return | Late fee per day | Cap |
|---|---|---|
| GSTR-1 / GSTR-3B, with tax | ₹50 (₹25 CGST + ₹25 SGST) | AATO ≤ ₹1.5 cr: ₹2,000. ₹1.5–5 cr: ₹5,000. > ₹5 cr: ₹10,000 |
| GSTR-1 / GSTR-3B, nil | ₹20 (₹10 + ₹10) | ₹500 |
| GSTR-4 | ₹50 (nil: ₹20) | ₹2,000 (nil: ₹500) |
| GSTR-7 | ₹50 (nil: ₹20) | ₹2,000 |
| GSTR-9 / 9C, AATO ≤ ₹5 cr | ₹50 (₹25 + ₹25) | 0.04% of turnover in the state/UT |
| GSTR-9 / 9C, AATO ₹5–20 cr | ₹100 (₹50 + ₹50) | 0.04% of turnover in the state/UT |
| GSTR-9 / 9C, AATO > ₹20 cr | ₹200 (₹100 + ₹100) | 0.50% of turnover in the state/UT |

Late fee is computed by the portal and cannot be edited in GSTR-3B. It applies per
return per GSTIN, so a multi-state taxpayer in default accumulates it several times
over. No late fee applies to PMT-06.

The caps are set by notification and have been revised more than once. Verify
before quoting a figure to a client.

## Interest (§50)

| Situation | Rate | Base |
|---|---|---|
| Delayed payment of tax (§50(1)) | 18% p.a. | Net cash liability, where the return is filed late but before proceedings under §73/§74 commence. Otherwise the gross liability |
| ITC wrongly availed **and utilised** (§50(3), Rule 88B(3)) | 18% p.a. | The utilised amount, from the date of utilisation to the date of reversal or payment |
| Delayed refund (§56) | 6% p.a. | Beyond 60 days from the application |
| Refund arising from an appellate order (§56 proviso) | 9% p.a. | |

Two points worth being precise about, because both are commonly stated wrongly:

- **Credit availed but not utilised does not attract interest.** Rule 88B(3) turns
  on utilisation. Reversing an ineligible credit before it is used costs nothing in
  interest.
- **§50(3) is 18%, not 24%.** The rate was substituted with retrospective effect
  from 1 July 2017. Older material still says 24%; it is out of date.

Interest is **self-assessed and declared** in GSTR-3B Table 5.1. The portal
computes a suggested figure but the taxpayer's declaration governs, and the
suggested figure is not always right for the fact pattern.

## Penalties

- **§122** — a long list of specified offences, with penalty generally the higher of
  ₹10,000 or the tax involved. Supplying without an invoice, issuing an invoice
  without a supply, availing credit on a fake invoice, and collecting tax without
  paying it within three months all sit here.
- **§122(1A)** — the same penalty on a person who retains the benefit of specified
  transactions and at whose instance they were conducted. This reaches beyond the
  registered entity.
- **§125** — general penalty up to ₹25,000 where no specific penalty is provided.
- **§73** (non-fraud) — for periods up to FY 2023-24: penalty of 10% of tax or
  ₹10,000, whichever is higher; nil if tax and interest are paid before the show
  cause notice, and nil if paid within 30 days of the notice.
- **§74** (fraud, wilful misstatement, suppression) — penalty of 100% of tax, with
  reductions to 15% if paid before the notice, 25% within 30 days of the notice,
  and 50% within 30 days of the order.
- **§74A** — applies to **FY 2024-25 onwards**, unifying the limitation framework
  for both fraud and non-fraud cases with differentiated penalties. Which section
  applies therefore depends on the period, not on the nature of the allegation
  alone.
- **§129 / §130** — detention, seizure and confiscation of goods in transit. Tax
  paid under these sections is a blocked credit under §17(5).
- **Prosecution under §132** for offences above the prescribed thresholds, with
  arrest powers under §69.

## Limitation

| Provision | Period | Order within |
|---|---|---|
| §73 (up to FY 2023-24) | Notice at least 3 months before the order deadline | 3 years from the due date of the annual return |
| §74 (up to FY 2023-24) | Notice at least 6 months before | 5 years from the due date of the annual return |
| §74A (FY 2024-25 onwards) | Notice within 42 months of the annual return due date | 12 months from the notice, extendable |

## Automated mismatch notices

| Form | Trigger | Reply window | Consequence of ignoring |
|---|---|---|---|
| **DRC-01B** | Liability in GSTR-1 exceeds GSTR-3B beyond the prescribed threshold (Rule 88C) | 7 days | GSTR-1 for the next period is blocked |
| **DRC-01C** | ITC in GSTR-3B exceeds GSTR-2B beyond the prescribed threshold (Rule 88D) | 7 days | GSTR-1 for the next period is blocked |
| **ASMT-10** | Scrutiny of returns under §61 | As specified | Proceeds to §73/§74/§74A |
| **GSTR-3A** | Return not filed | 15 days | Best-judgement assessment under §62 |

Both DRC-01B and DRC-01C are automated and unforgiving about the deadline. If
either is open, resolve it before preparing the current return — the blocking
cascades into e-way bills and then into despatches.

A **§62 best-judgement assessment** is withdrawn if the return is filed within 60
days of the order (extendable to 120 days with additional late fee). That window
is easy to miss and worth checking for immediately whenever a client mentions an
assessment order.

## Payments and adjustments

- **DRC-03** — voluntary payment, or payment against a notice. Must specify the
  correct cause and period. Annual-return additional liability is paid here, in
  cash.
- **DRC-03A** — adjusts a DRC-03 payment against a confirmed demand order, so that
  the demand is actually closed on the portal. A DRC-03 without the corresponding
  DRC-03A leaves the demand outstanding even though the money has been paid — a
  common and avoidable problem.
- **§128A amnesty** — waiver of interest and penalty for §73 demands covering
  FY 2017-18 to 2019-20, subject to full payment of tax by the notified date and
  the prescribed conditions. Excludes §74 fraud cases, late fees and erroneous
  refunds. Check whether the window is still open for the taxpayer before
  presenting it as an option.

## Appeals

| Stage | Form | Time limit | Pre-deposit |
|---|---|---|---|
| First appeal to the Appellate Authority | APL-01 | 3 months from the order (condonable by 1 month) | 10% of disputed tax |
| Appeal to the GST Appellate Tribunal | APL-05 | 3 months from the first appellate order | An additional 10% (subject to the current cap) |
| High Court | | 180 days | |
| Supreme Court | | | |

The GSTAT is now operational, and its Principal Bench has been designated the
National Appellate Authority for Advance Ruling. Pre-deposit percentages and caps
have been amended — verify the current figures before advising on the cost of an
appeal.
