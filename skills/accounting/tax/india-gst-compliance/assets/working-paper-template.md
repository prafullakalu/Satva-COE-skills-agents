# Working paper — <GSTIN> — <period>

Keep this in `work/`. Update it as you go rather than writing it at the end;
context gets compacted, files do not.

## 1. Engagement (from the Step 2 intake gate)

| | |
|---|---|
| Legal name / trade name | |
| GSTIN (checksum validated?) | |
| State | |
| Tax period / FY | |
| Scheme | Regular monthly / QRMP / Composition |
| AATO, preceding FY | |
| E-invoicing applicable? | |
| HSN digits required | 4 / 6 |
| Registrations held | Regular / ISD / TDS / TCS / other |
| Business profile | Goods / services / exports / SEZ / e-commerce |
| Exempt or nil-rated supplies? (Rule 42/43) | |
| Prior periods all filed? | |
| Time-bar risk on any period? | |
| Open notices (check **both** notice tabs) | |
| Reviewer and filer (named human) | |

Unanswered items are open questions, not defaults. List them here:

## 2. Documents received

| Document | Received? | Period covered | Notes |
|---|---|---|---|
| Sales register | | | |
| Purchase register | | | |
| GSTR-1 filed summary | | | |
| GSTR-2B | | | |
| IMS export | | | |
| E-invoice / IRN dump | | | |
| E-way bill report | | | |
| Bills of Entry / ICEGATE | | | |
| Expense ledger / trial balance | | | |
| Ledger balances (cash / credit) | | | |
| LUT ARN and validity | | | |

**Not received**, and the effect on the return:

## 3. Independent totals

| Register | Rows | Taxable value | IGST | CGST | SGST | Cess | Agrees with stated total? |
|---|---|---|---|---|---|---|---|
| Sales | | | | | | | |
| Purchases | | | | | | | |

## 4. Outward position

| Table | Value | Source | Notes |
|---|---|---|---|

Place-of-supply exceptions considered:
Rate-change (§14) items considered:
Non-obvious supplies considered (assets, scrap, branch transfer, Schedule I,
employee recoveries, free samples, advances):

## 5. RCM sweep

| Expense head | Amount | RCM? | Entry / notification | Self-invoice? | Tax |
|---|---|---|---|---|---|

Heads checked with a nil result (record these — the negative is evidence):

## 6. ITC position

| Class | Count | Taxable value | Tax | Treatment |
|---|---|---|---|---|
| A — matched | | | | Claim |
| B — books not in 2B | | | | Not claimed; tracked |
| C — 2B not in books | | | | Investigate |
| D — value differs | | | | |
| E — GSTIN/POS/head differs | | | | |
| F — 2B ineligible | | | | Report in 4D(2) |

Reversals: Rule 42 ___ Rule 43 ___ Rule 37 ___ Rule 37A ___ §17(5) ___

## 7. Computation

Attach or reference the `scripts/gst_compute.py` output. Record both routes:

| | Route 1 (line-item) | Route 2 (rate-wise aggregate) | Agree? |
|---|---|---|---|
| Output tax | | | |
| ITC | | | |
| Net payable | | | |

Rule 86B tested: yes / no / not applicable — working:

## 8. Verification log

| Item | Value used | Source (notification/advisory + date) | Verified on | By |
|---|---|---|---|---|

Unverified items and their effect:

## 9. Self-review

Outcome of `checklists/self-review.md`, including what was checked and found clean:

Answer to "if this is wrong in six months, what will the explanation be?":

## 10. Open questions

| # | Question | Asked of | Asked on | Answer | Effect if unanswered |
|---|---|---|---|---|---|
