# E-invoicing and e-way bills

LAST_VERIFIED: 2026-07-29
VOLATILE: the AATO thresholds, the IRN reporting window and its threshold, and
e-way bill validity and blocking rules.

## E-invoicing

### Who it applies to

Mandatory where **aggregate annual turnover exceeded ₹5 crore in any financial year
from 2017-18 onwards**. The test looks back at every year, not just the immediately
preceding one — once you cross, you stay in, even if turnover later falls.

Applies to B2B supplies, supplies to SEZ, exports and deemed exports. **Not** to
B2C supplies (though a dynamic QR code requirement applies separately for B2C
where turnover exceeds ₹500 crore).

Exempt entities regardless of turnover: banks, NBFCs and other financial
institutions, insurers, goods transport agencies, passenger transport services,
suppliers of admission to cinematographic exhibitions, SEZ **units** (but not SEZ
developers), and government departments and local authorities.

### The 30-day reporting window

Taxpayers with **AATO of ₹10 crore or more** must report an invoice, credit note or
debit note to the Invoice Registration Portal within **30 days of the document
date**. From 1 April 2025 this applies at the ₹10 crore level, having previously
applied at ₹100 crore.

After 30 days the IRP will not generate the IRN at all. There is no extension.
Since a document without an IRN is not a valid tax invoice where e-invoicing
applies, this is not a procedural lapse — it can invalidate the document and put
the recipient's credit at risk, while the supplier's liability stands.

Check invoice ageing against this window every month, and check it first for any
month where the client mentions a backlog.

### Mechanics

- Generate the JSON in the current schema, report to any IRP, receive the **IRN**
  (a 64-character hash), the signed invoice and the **QR code**.
- Print the QR code on the invoice. The IRN itself need not be printed but usually
  is.
- E-invoice data auto-populates GSTR-1 and can auto-generate Part A of the e-way
  bill.
- **An IRN cannot be amended.** It can be **cancelled within 24 hours** of
  generation, and only if no e-way bill is active against it. After 24 hours the
  only route is a credit note, or an amendment in GSTR-1 — which then diverges from
  the IRP record.
- Duplicate IRN generation for the same document number in the same financial year
  is blocked.
- 2FA is mandatory on the portals.

### Checks worth running

- Count and value of the sales register against the IRN dump, per month.
- Every B2B invoice has an IRN, and no IRN exists without a corresponding invoice.
- Invoices cancelled in books but with a live IRN, and vice versa.
- Invoices approaching or past the 30-day window.
- IRN data against what actually appears in GSTR-1 — auto-population is not always
  complete, and the return is what counts.

## E-way bills

### When required

For movement of goods where the consignment value exceeds **₹50,000** — inter-state
in all cases; intra-state as per each state's threshold, which varies (some states
set a higher limit, and some exempt intra-city movement). Verify the state rule.

Also required regardless of value in specified cases, including inter-state
movement of goods for job work and inter-state movement of handicraft goods by an
unregistered person.

Not required for: non-motorised transport, movement from a port/airport/land
customs station to an inland container depot for customs clearance, specified
exempt goods, and goods under customs bond or supervision.

### Validity

| Cargo | Validity |
|---|---|
| Regular | 1 day per 200 km, or part thereof |
| Over-dimensional cargo | 1 day per 20 km, or part thereof |

The day runs to midnight of the following day from the time of generation.
Extension is possible within 8 hours before or after expiry, by the transporter.

### Restrictions introduced from 1 January 2025

- An e-way bill **cannot be generated for a document older than 180 days**.
- Total extension is capped at **360 days from the original generation date**.
- 2FA is mandatory.

### Blocking (Rule 138E)

E-way bill generation is blocked for a GSTIN that has not filed:

- GSTR-3B for **two consecutive tax periods** (or two quarters, for QRMP), or
- GSTR-1 where required, or
- CMP-08 for two consecutive quarters (composition).

This is the point at which a filing backlog becomes an operational crisis, because
goods cannot legally move. Unblocking follows filing, generally within a day, or by
application in **EWB-05** to the Commissioner. When a client says "we can't
despatch", check the return status first.

### Part A and Part B

Part A carries the invoice and consignment details; Part B carries the vehicle
number. A movement cannot start without Part B (except for a first or last leg
under 50 km within the state, where Part B may be omitted). Vehicle changes require
Part B to be updated before the goods move onward.

### Consequences of moving without a valid e-way bill

Detention and seizure under **§129**, with tax and penalty payable to release the
goods and the conveyance. The penalty is substantial, the goods are stuck, and
**the tax paid under §129 is a blocked credit under §17(5)**. Practically this is
one of the most expensive routine mistakes in GST.

## Reconciliation across the three systems

For any period, these should agree, and each difference should be explainable:

| Comparison | What a difference usually means |
|---|---|
| Sales register vs IRN dump | Missing e-invoice, or an IRN generated for a cancelled invoice |
| IRN dump vs GSTR-1 | Auto-population failed, or the return was edited after auto-population |
| E-way bills vs sales register | Goods moved without an invoice, an invoice raised without movement (which may be fine — services, or a bill-to-ship-to leg), or a value mismatch |
| E-way bill value vs invoice value | Undervaluation exposure, or a rate error |

Departments run exactly these comparisons. Running them first is cheaper.
