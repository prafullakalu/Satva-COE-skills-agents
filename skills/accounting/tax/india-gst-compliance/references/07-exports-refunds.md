# Zero-rated supplies, LUT and refunds

LAST_VERIFIED: 2026-07-29
VOLATILE: the risk-based provisional refund mechanism and its scope; refund
formulae under Rules 89(4) and 89(5); documentation requirements per circular.

## Zero-rated supplies (§16 IGST)

Exports of goods and services, and supplies to an SEZ developer or unit for
authorised operations. Two routes:

**Route A — under LUT, without payment of IGST.** Claim a refund of unutilised
input tax credit under Rule 89(4).

**Route B — on payment of IGST.** Claim a refund of the IGST paid. For goods, the
shipping bill itself operates as the refund application and the refund flows
automatically once GSTR-1 and GSTR-3B are filed consistently and the data reaches
ICEGATE.

Route A preserves cash flow and is the default for most exporters. Route B is
faster and needs no separate application for goods, but it means paying tax and
waiting. Route B is not available where the supplier has availed certain
concessional or exemption benefits on inputs (the Rule 96(10) family of
restrictions has been amended repeatedly — verify the current position before
recommending it).

## LUT (Form RFD-11)

- Filed on the portal, **annually**, before 1 April of the financial year or before
  the first zero-rated supply of the year.
- Valid for the financial year. **A fresh LUT is needed every year** — an expired
  LUT is one of the most common export compliance failures, and it converts what
  the taxpayer thinks is a zero-rated supply into a taxable one.
- If no valid LUT exists at the time of supply, the exporter must either export on
  payment of IGST or furnish a bond with a bank guarantee.
- Record the LUT ARN and its validity in the working paper for every export
  engagement, and check it covers the tax period being filed.

## Rule 96A conditions

Exports under LUT must be completed within:

- **Goods**: 3 months from the invoice date (extendable by the Commissioner).
- **Services**: payment in convertible foreign exchange within 1 year from the
  invoice date.

If either is breached, the exporter must pay IGST with interest at 18% from the
invoice date within 15 days. The tax can be recovered back once the export is
completed or the payment is received. Track ageing of export invoices and
outstanding foreign receivables — this liability accrues silently.

## Refund of unutilised ITC — Rule 89(4)

```
Refund = (Turnover of zero-rated supply of goods and services x Net ITC)
         ------------------------------------------------------------
                          Adjusted total turnover
```

- **Net ITC** is ITC availed on inputs and input services during the period. Credit
  on capital goods is excluded.
- **Turnover of zero-rated supply of goods** is capped at 1.5 times the value of
  like goods supplied domestically by the same or a similarly placed supplier.
- **Adjusted total turnover** excludes exempt supplies other than zero-rated.

## Refund on inverted duty structure — Rule 89(5)

```
Refund = (Turnover of inverted rated supply x Net ITC / Adjusted total turnover)
         - (tax payable on such inverted rated supply x Net ITC / ITC availed on
            inputs and input services)
```

The formula was amended to give partial relief for input services; the current
text must be used. **ITC on input services and capital goods is still not fully
refundable** under this route, which is why an inverted-duty refund never equals
the accumulated credit and clients are routinely surprised.

Note also that a refund is not available where the output supply is nil-rated or
fully exempt, and that specified goods (certain construction and textile entries)
are notified as ineligible for inverted-duty refund.

## Other refund categories

Excess balance in the electronic cash ledger; tax paid on a supply not made or a
refunded supply; tax wrongly paid as inter-state instead of intra-state or vice
versa (§77 CGST / §19 IGST); deemed exports; refund to UN bodies and embassies;
excess payment of tax; assessment or appellate orders in the taxpayer's favour.

## Process and timelines

| Step | Rule / section | Timing |
|---|---|---|
| Application in **RFD-01** | Rule 89 | Within **2 years** of the relevant date (§54) |
| Acknowledgement **RFD-02** or deficiency memo **RFD-03** | Rule 90 | 15 days |
| **Provisional refund RFD-04** — 90% | Rule 91 | 7 days from acknowledgement |
| Show cause **RFD-08**, reply **RFD-09** | Rule 92 | 15 days to reply |
| Final order **RFD-06** and payment order **RFD-05** | Rule 92 | 60 days from the complete application |
| Interest on delayed refund | §56 | 6% p.a. beyond 60 days; 9% where the refund arises from an appellate order |

**Risk-based 90% provisional sanction.** Rule 91(2) was amended so that
system-assessed low-risk claims for zero-rated supplies are provisionally
sanctioned at 90% without detailed scrutiny — operational from around November
2025, reducing typical turnaround from weeks to days. The scope was extended to
**inverted duty structure** claims filed on or after 1 October 2025. An officer can
still withhold provisional sanction, but must record reasons in writing. The
₹1,000 minimum threshold for IGST-paid export refunds was removed, which matters
for high-volume low-value e-commerce exporters.

A "relevant date" under §54 differs by category — for export of goods it is the
date the ship or aircraft leaves India, for services the date of receipt of
foreign exchange or the invoice date depending on which came first, for unutilised
ITC the due date of the return for the period. Compute it, do not assume it is the
invoice date; the two-year limitation is strictly applied.

## Documentation to assemble before filing RFD-01

- Statement in the prescribed format for the refund category (Statement 1 to 7).
- Valid LUT/ARN covering the period, or proof of IGST payment.
- Export invoices, shipping bills with EGM and port details, or FIRC/BRC for
  services.
- Purchase invoices supporting Net ITC, and confirmation that every one appears in
  GSTR-2B.
- Reconciliation of GSTR-1, GSTR-3B and the refund claim — these three must tie or
  a deficiency memo follows.
- Undertaking that no refund has been claimed elsewhere, and a self-declaration
  that the incidence of tax has not been passed on (or a CA certificate where the
  amount exceeds ₹2 lakh).

A deficiency memo in RFD-03 requires a **fresh application**, and time already
spent does not extend the two-year limit. Completeness at first filing is
therefore worth real effort.
