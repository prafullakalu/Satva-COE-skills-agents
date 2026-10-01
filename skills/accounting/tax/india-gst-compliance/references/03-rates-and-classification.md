# Rates, classification, time of supply and valuation

LAST_VERIFIED: 2026-07-29
VOLATILE: **every rate**. The structure below is the framework; the rate for a
specific HSN/SAC must be verified against the current rate notification for the
relevant tax period. Do not lift a rate from memory or from this file into a
return.

## The rate structure after GST 2.0

From **22 September 2025** the four-slab structure was replaced:

| Rate | Broad coverage |
|---|---|
| Nil | Essential food, specified life-saving medicines, education and healthcare services, and other exempt entries |
| 5% | Merit rate — most items previously at 12%, plus essentials moved down |
| 18% | Standard rate — most goods and services, including most items previously at 28% |
| 40% | Demerit/luxury — tobacco and pan masala, aerated and caffeinated beverages, large passenger vehicles, motorcycles above 350cc, yachts and personal aircraft, casinos, betting, lotteries and online money gaming |
| 3% | Gold, silver, platinum, articles of precious metal |
| 0.25% | Rough and unworked diamonds and precious stones |
| 1.5% | Specified job work on diamonds |

The 12% and 28% slabs were withdrawn. If a working paper still shows 12% or 28%
for a supply after 22 September 2025, that is a finding.

**Tobacco and pan masala** stayed on the old rate-plus-compensation-cess basis
until **1 February 2026**, when they moved to 40% GST, compensation cess was
abolished, and additional excise duty plus a Health & National Security (HSNS)
cess were introduced. Valuation for these goods is on **retail sale price** under
Rule 31D rather than transaction value. If the engagement touches these goods,
verify the current position carefully — this was the most recent and least settled
of the rate changes.

**Compensation cess** was abolished from 1 February 2026. For periods before that,
it still applies and must be computed, reported and paid; the cess credit ledger
can only be used against cess liability.

## Finding the right rate

1. Classify the supply. Goods follow the **HSN** in the Customs Tariff; services
   follow the **SAC** in the scheme of classification of services. Classification
   is a legal question, not a lookup — the description in the tariff heading
   governs, read with the section and chapter notes and the General Rules for
   Interpretation.
2. Find the entry in the current rate notification (Notification 1/2017-CT(Rate)
   for goods and 11/2017-CT(Rate) for services, as amended, plus the exemption
   notifications 2/2017 and 12/2017).
3. Check for a conditional entry — many rates depend on conditions such as not
   availing ITC, or the recipient's status.
4. Record the HSN/SAC, the rate, and the notification in the working paper.

Where classification is genuinely arguable, present the options with the rate
difference and the risk, and let the taxpayer decide with their CA. Silently
picking the lower rate is how a demand under §74 starts.

## HSN reporting requirements

| AATO in preceding FY | Digits required on invoice and in GSTR-1 Table 12 |
|---|---|
| Up to ₹5 crore | 4 digits (B2B mandatory; B2C also required under Phase 3) |
| Above ₹5 crore | 6 digits |

Two-digit reporting is no longer accepted. In GSTR-1 Table 12 the HSN must be
picked from the portal dropdown, is split into B2B and B2C tabs, and is validated
against the values reported elsewhere in the return.

## Time of supply — and why it decides the rate

**§12 (goods)**: earlier of the date of invoice (or the last date on which it
should have been issued under §31) and the date of payment. In practice, for goods,
liability on advances was removed for most taxpayers, so the invoice date usually
governs.

**§13 (services)**: if the invoice is issued within the prescribed period, the
earlier of invoice date and payment date; otherwise, the earlier of the date of
provision of service and payment. **Advances received for services are taxable
when received.**

**Reverse charge (§12(3), §13(3))**: earliest of the date of receipt of goods (for
goods), the date of payment, or 30 days (goods) / 60 days (services) from the
supplier's invoice date. Missing this is the usual reason RCM is declared a period
or two late, with interest.

**§14 — change in rate of tax.** This is the provision that decides which rate
applies across 22 September 2025 and 1 February 2026. It works on a two-out-of-
three logic between the date of supply, the date of invoice and the date of
payment:

- Supply **before** the change: if both invoice and payment are after the change,
  the new rate applies. If either is before, the old rate applies.
- Supply **after** the change: if both invoice and payment are before the change,
  the old rate applies. If either is after, the new rate applies.

For continuous supplies, works contracts and long-running service contracts,
apply this per instalment. Do not apply a blanket cut-off by invoice date — that
is the shortcut that produces short payment plus interest.

## Valuation

**§15** — transaction value where the supplier and recipient are unrelated and
price is the sole consideration. It **includes** taxes other than GST, amounts the
recipient is liable to pay but the supplier has paid, incidental expenses,
packing, commission, interest or late fee for delayed payment, and subsidies
linked to price other than government subsidies. It **excludes** discounts given
before or at the time of supply and shown on the invoice, and post-supply
discounts only if agreed before the supply, linked to specific invoices, and the
recipient reverses the corresponding ITC.

That last condition is where post-sale discount schemes usually fail. If the
credit note does not satisfy it, the supplier cannot reduce their liability.

**Related-party and distinct-person supplies** (including branch transfers across
states, which are supplies even without consideration under Schedule I) are valued
under Rules 28–31. Where the recipient is eligible for full ITC, the invoice value
is deemed to be open market value — a practical safe harbour worth knowing.

Other valuation rules to watch: Rule 32 for specified suppliers (money changers,
air travel agents, life insurers, second-hand goods under the margin scheme),
Rule 33 for pure agent recoveries, and Rule 31D for RSP-based valuation of
tobacco and pan masala.

## Common classification traps

- **Composite vs mixed supply (§8).** A composite supply naturally bundled with a
  principal supply takes the principal supply's rate. A mixed supply takes the
  **highest** rate among its components. Getting this wrong on a bundled offering
  is a recurring demand issue.
- **Works contract** for immovable property is a service (Schedule II), with its
  own ITC restrictions under §17(5).
- **Restaurant and outdoor catering** rates are conditional on not availing ITC —
  taking the credit and the concessional rate together is not an option.
- **Job work** rates depend on whether the principal is registered.
- **Second-hand goods** under the margin scheme (Rule 32(5)) require no ITC to have
  been availed on purchase.
- **Free supplies and samples** — no ITC under §17(5)(h), and a supply to a related
  party without consideration is still taxable under Schedule I.
- **Schedule III** lists activities that are neither supply of goods nor services —
  employment services by an employee, sale of land, sale of completed buildings,
  actionable claims other than specified ones. Check this before taxing something
  that is not a supply at all.
