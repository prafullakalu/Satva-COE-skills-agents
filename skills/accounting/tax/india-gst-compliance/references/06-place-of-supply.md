# Place of supply — IGST vs CGST/SGST

LAST_VERIFIED: 2026-07-29

## Why this is worth per-invoice care

Getting the place of supply wrong means the tax went to the wrong government. It
is not a set-off you can correct in the next return: the correct tax has to be
paid again, and the wrongly paid tax has to be claimed as a refund under §77 of
the CGST Act / §19 of the IGST Act — a slow process with its own limitation
period. Meanwhile the recipient's credit fails, because a POS mismatch shows up in
GSTR-2B as ineligible.

The rule is mechanical: compare the **location of the supplier** with the **place
of supply**. Same state or UT → CGST + SGST/UTGST. Different → IGST. The
recipient's billing address is an input to the determination, not the answer.

## Goods within India — §10 IGST Act

| Situation | Place of supply |
|---|---|
| Supply involves movement of goods | Location where movement terminates for delivery to the recipient |
| **Bill-to / ship-to** — goods delivered to a third party on the direction of the buyer | The **principal place of business of the third person who directed it** (the bill-to party), not the physical delivery location |
| No movement of goods | Location of the goods at the time of delivery |
| Goods assembled or installed at site | Place of installation or assembly |
| Goods supplied on board a conveyance | Location where the goods were taken on board |
| Cannot be determined | As prescribed |

Bill-to/ship-to is the classic trap. A Maharashtra supplier billing a Delhi trader
and shipping to Karnataka charges **IGST**, because the POS is Delhi. The Delhi
trader then makes an onward supply with POS Karnataka. Two supplies, both
inter-state. Treating it as one Maharashtra-to-Karnataka movement is wrong.

## Import and export of goods — §11

- **Import**: place of supply is the location of the importer. IGST is levied and
  collected as customs duty at the point of import, and the credit is taken from
  the Bill of Entry — not from GSTR-2B.
- **Export**: place of supply is the location outside India.

## Services where both parties are in India — §12

**General rule (§12(2))**: supply to a **registered** person → the recipient's
location. Supply to an **unregistered** person → the address on record; if there is
no address on record, the supplier's location.

The specific overrides matter more than the general rule in practice:

| Service | Place of supply |
|---|---|
| Immovable property — including architects, interior decorators, hotel accommodation, accommodation in a property for a function, and ancillary services | **Location of the immovable property.** Applies regardless of the recipient's registration or location |
| Restaurant, catering, personal grooming, fitness, beauty, health services | Location where the service is performed |
| Training and performance appraisal | Registered recipient: recipient's location. Unregistered: where performed |
| Admission to an event, amusement park, cultural/sporting/scientific event | Where the event is held or the park is located |
| Organising an event, sponsorship | Registered: recipient's location. Unregistered: where the event is held |
| Transportation of goods, including by mail or courier | Registered: recipient's location. Unregistered: where the goods are handed over for transport |
| Passenger transportation | Registered: recipient's location. Unregistered: where the passenger embarks for the continuous journey |
| Services on board a conveyance | First scheduled point of departure |
| Telecom, broadcasting, cable, DTH | Fixed line/leased circuit: place of installation. Post-paid mobile: billing address. Pre-paid: address of the selling agent or where payment is received |
| Banking, financial and stockbroking services | Recipient's location on the supplier's records; if unavailable, the supplier's location |
| Insurance | Registered: recipient's location. Unregistered: address on the supplier's records |
| Advertisement to Government | Each state where the advertisement is disseminated, in proportion |

The immovable property rule is the one most often applied incorrectly. A hotel in
Goa billing a Delhi company charges **CGST + Goa SGST**. The Delhi company cannot
take that credit, because the POS is in a state where it is not registered. This
is not a mistake to fix — it is a structural cost, and worth telling the client
about in advance of the booking rather than after.

## Services with a foreign party — §13

**General rule (§13(2))**: location of the recipient. Where the recipient's location
is not available in the ordinary course of business, the supplier's location.

Overrides include: services requiring physical presence of goods (location of the
goods), services requiring physical presence of the individual (where performed),
services relating to immovable property (property location), admission to or
organising an event (where held), banking and intermediary services and hiring of
means of transport up to one month (**supplier's location**), and goods
transportation (destination of the goods).

The **intermediary** rule is the recurring dispute. If an Indian entity is an
intermediary under §2(13) IGST — arranging or facilitating a supply between two
other persons rather than supplying on its own account — the POS is India, the
supply is not an export, and IGST or CGST+SGST applies despite foreign currency
receipt. Marketing support, back-office and commission arrangements are argued
both ways; classification depends on the contract's substance. Where this is
live, flag it as a position requiring professional advice, and point to CBIC
Circular 159/15/2021-GST for the department's view.

## Export of services — all five conditions (§2(6) IGST)

1. Supplier located in India.
2. Recipient located outside India.
3. **Place of supply outside India.**
4. Payment received in convertible foreign exchange, or in Indian rupees where
   permitted by the RBI.
5. Supplier and recipient are not merely establishments of the same person
   (Explanation 1 to §8 IGST).

All five. A supply to a foreign parent's Indian branch, or by an Indian branch of
a foreign company to its own head office, fails condition 5. Receiving USD does
not by itself make something an export.

## Practical checks

- Compare the POS state code in the sales register against the recipient's GSTIN
  state code, and list every row where they differ from the tax head charged.
- SEZ supplies are zero-rated inter-state supplies — always IGST (or under LUT
  without payment), never CGST+SGST, even where the SEZ is in the same state.
- For B2C inter-state supplies above ₹2.5 lakh per invoice, GSTR-1 Table 5 requires
  invoice-level POS reporting; below that, Table 7 requires a state-wise
  consolidated split. Both need the POS to be right.
- GSTR-3B Table 3.2 (inter-state supplies to unregistered persons, composition
  taxpayers and UIN holders) is now locked and derived from GSTR-1. A wrong POS in
  GSTR-1 therefore locks a wrong 3.2, correctable only through GSTR-1A.
