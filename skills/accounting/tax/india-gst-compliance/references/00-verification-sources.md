# Verification sources and the freshness discipline

LAST_VERIFIED: 2026-07-29
VERIFIED_AGAINST: CBIC and GSTN public material plus secondary tax commentary, as
available on the date above. Nothing here is a substitute for reading the
notification itself.

## Why this file exists

GST is not a stable body of law. Between September 2025 and February 2026 alone
the rate structure was rewritten twice, compensation cess was abolished, the
outward tables of GSTR-3B became non-editable, IMS became the gate for input tax
credit, and a hard three-year bar on filing old returns switched on. A reference
file written six months ago can be confidently, precisely wrong.

The failure this causes is specific and nasty: a stale number *looks* researched.
Nobody questions "18%" in a working paper. So the discipline is not "be careful",
it is "verify the specific items that move, and write down that you did".

## Primary sources, in order of authority

1. **CBIC GST notifications and circulars** — https://cbic-gst.gov.in
   Central Tax, Central Tax (Rate), Integrated Tax, Integrated Tax (Rate),
   Compensation Cess. This is the law. Cite by number and date, e.g.
   "Notification No. 09/2025-Central Tax dated 11 February 2025".
2. **GST Council press releases and meeting recommendations** —
   https://gstcouncil.gov.in. Recommendations, not law: a Council decision only
   binds once notified. Check for the corresponding notification before relying
   on it. This gap is a common source of premature advice.
3. **GSTN advisories on the portal** — https://www.gst.gov.in ("News and
   Updates") and https://tutorial.gst.gov.in. These govern *portal behaviour*:
   what is editable, when GSTR-2B generates, what IMS does. Portal behaviour and
   statutory law are different things and both matter.
4. **The bare Acts and Rules** — CGST Act 2017, IGST Act 2017, UTGST Act 2017,
   State GST Acts, CGST Rules 2017, GST (Compensation to States) Act 2017 and its
   successor levies. Always read the current amended text; several provisions have
   been amended retrospectively.
5. **CBIC instructions and internal circulars** — relevant for refund processing,
   audit and investigation conduct.
6. **e-invoice and e-way bill portals** — https://einvoice.gst.gov.in,
   https://ewaybillgst.gov.in for schema versions, thresholds and validations.
7. **Judicial decisions** — Supreme Court and High Courts. Note that a High Court
   decision binds only within its jurisdiction, and that the legislature has
   more than once reversed a decision retrospectively (see the "plant or
   machinery" amendment following *Safari Retreats*).
8. **Advance rulings (AAR/AAAR)** — persuasive only, binding only on the applicant
   and the jurisdictional officer. Contradictory rulings across states are common.
   Never present an AAR as settled law.

Secondary commentary (ClearTax, Taxguru, CAclubindia, IRIS, Tally, the Big Four
alerts, professional bodies) is useful for *finding* the change and for
explanation. It is not a source for a figure that goes into a return. Use it to
locate the notification, then cite the notification.

## Volatile items — verify every engagement

Do not use any of the following from memory or from a stale reference file:

- **Rate on a specific HSN/SAC.** Rates moved 22 Sep 2025 (GST 2.0) and again for
  tobacco/pan masala on 1 Feb 2026. Assume the rate you remember is wrong.
- **Whether compensation cess or a successor levy applies** to the goods in hand.
- **Due dates**, including any state-specific or disaster-related extension for the
  period being filed. Extensions are issued mid-month and are easy to miss.
- **Late fee caps and interest rates** applicable to the period.
- **Turnover thresholds** — registration, e-invoicing, HSN digits, QRMP,
  composition, GSTR-9/9C, Rule 86B.
- **GSTR-3B editability.** Tables 3.1/3.2 are locked. Whether Table 4A (ITC) is
  also locked, and from which period, must be checked on the portal for the
  period being filed — this was slated for rollout around mid-2026.
- **IMS mechanics** — which records are eligible for "pending", for how long,
  and how partial credit-note reversal is declared. The advisory has been revised
  more than once.
- **The three-year filing bar** and the status of the "Application for Unbarring
  Returns" facility.
- **Refund processing** — the risk-based 90% provisional sanction, its scope, and
  the categories it applies to.
- **Anything decided at a GST Council meeting after the LAST_VERIFIED date.** As
  of that date the 57th Council meeting was pending, with registration, refund and
  audit simplification on its expected agenda.

## How to verify, in practice

For each volatile item the engagement actually depends on:

1. Identify what you need to know and for which tax period. Law applies as it
   stood in the tax period, not as it stands today — this matters constantly when
   filing a late return or an annual return.
2. Find the governing notification, circular or advisory from a primary source.
3. Record it in `work/verification-log.md` in this shape:

   ```
   | Item | Value used | Source (number + date) | Verified on | By |
   |------|-----------|------------------------|-------------|-----|
   | GST rate, HSN 8517 | 18% | NT 09/2025-CT(R) dt 17.09.2025 | 2026-07-29 | (checker) |
   ```

4. If you cannot verify it, write `UNVERIFIED` in the log with the reason, tell
   the user, and treat any figure depending on it as provisional. Do not silently
   fall back to the stale value.

An engagement where three items are verified and one is honestly marked
UNVERIFIED is in far better shape than one where all four are quietly assumed.

## Maintaining the reference files themselves

When you discover that a reference file is out of date:

1. Fix the specific fact and cite the notification inline.
2. Update `LAST_VERIFIED` at the top of that file.
3. Add a line to `references/01-law-changes-2025-26.md` so the change is visible
   to the next engagement, not buried in a detail page.

Leaving a corrected fact undated is almost as bad as leaving it wrong, because the
next reader cannot tell what has been checked.
