# ITC eligibility screen

Run per invoice for material items, and per expense head for the ledger sweep.
Any "no" or "unknown" means the credit is not claimed this period — it goes to the
difference register with an owner and a next action.

## Gate 1 — the invoice

- [ ] Tax invoice or debit note held, in the taxpayer's name and GSTIN
- [ ] Supplier's GSTIN valid and active on the invoice date
- [ ] Invoice carries all particulars required by Rule 46
- [ ] Where the supplier is covered by e-invoicing, a **valid IRN and QR code** are
      present — without them it is not a valid tax invoice
- [ ] Place of supply on the invoice is consistent with the tax head charged
- [ ] The tax head charged matches what the recipient can use (IGST wrongly charged
      as CGST+SGST, or vice versa, cannot be corrected by set-off)

## Gate 2 — receipt

- [ ] Goods or services actually received
- [ ] Where goods were delivered to a third party on the taxpayer's direction, the
      bill-to/ship-to condition is satisfied
- [ ] Where goods arrive in lots, the **last lot** has been received
- [ ] Supporting evidence exists: GRN, e-way bill, service acceptance, timesheet

## Gate 3 — the supplier's side

- [ ] Invoice appears in **GSTR-2B** for the period, marked eligible
- [ ] Not flagged as restricted under §38
- [ ] Rule 37A: supplier's GSTR-3B for the period filed by 30 September following
      the FY — if not, reverse by 30 November following the FY
- [ ] Supplier not showing as cancelled, suspended or non-existent

## Gate 4 — timing

- [ ] Within §16(4): not later than 30 November of the following FY, or the annual
      return date if earlier
- [ ] Claimed in the period in which it appears in 2B, or in a later period within
      the limit — never earlier
- [ ] Where the credit was kept Pending in IMS, it is still within time

## Gate 5 — §17(5) blocked credits

Tick each as "not applicable" or identify the amount to block:

- [ ] Motor vehicles ≤ 13 seats, and their insurance, servicing, repair and
      maintenance
- [ ] Vessels and aircraft, and related services
- [ ] Food and beverages, outdoor catering, beauty, health services, cosmetic
      surgery
- [ ] Club, health and fitness centre membership
- [ ] Employee life and health insurance (unless obligatory under a law in force)
- [ ] Travel benefits to employees on vacation / LTC
- [ ] Works contract for immovable property (except plant and machinery, and except
      as an input to a further works contract)
- [ ] Goods or services for own-account construction of immovable property,
      including where capitalised
- [ ] Goods or services on which composition tax was paid
- [ ] Received by a non-resident taxable person (except imported goods)
- [ ] **CSR expenditure**
- [ ] Goods lost, stolen, destroyed, **written off**, gifted, or given as free
      samples
- [ ] Tax paid under §74, §129 or §130
- [ ] Personal consumption

## Gate 6 — payment to the supplier

- [ ] Paid within **180 days** of the invoice date, or the credit is reversed with
      interest under Rule 37
- [ ] Where previously reversed and now paid, re-availment claimed in Table 4D(1)
      with the earlier reversal referenced

## Gate 7 — apportionment

- [ ] Where there are exempt or non-business supplies, Rule 42 (inputs and input
      services) and Rule 43 (capital goods) reversals computed
- [ ] Common credit correctly identified — not everything is common
- [ ] Annual finalisation by September of the following FY diarised, with interest
      on any shortfall

## Gate 8 — special routes

- [ ] Import IGST: agreed to the Bill of Entry and ICEGATE, claimed in Table 4A(1)
- [ ] RCM: liability paid in cash, self-invoice raised, credit in Table 4A(3)
- [ ] ISD: distributed through GSTR-6, claimed in Table 4A(4)
- [ ] Transitional or special claims (ITC-01, ITC-02) supported by the relevant form

## Ledger check

- [ ] Electronic credit ledger not blocked under Rule 86A
- [ ] Rule 86B tested where monthly taxable turnover exceeds ₹50 lakh
- [ ] Cess credit used only against cess liability
