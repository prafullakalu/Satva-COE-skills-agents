# Account health preflight

Run this on the portal **before** preparing figures or automating anything. It
takes a few minutes and it exists because most "the portal won't let me file"
situations are visible in advance. Automating into a blocked account wastes the
user's time and occasionally makes things worse.

Everything here is Tier 0 — read-only. No confirmation needed; just do it and
report.

Record the results in `work/engagement.md` and log the run in the action log.

## 1. Identity

- [ ] Logged in to the **correct GSTIN** — matched against `work/engagement.md`
- [ ] Legal name and trade name match the registration certificate
- [ ] State matches the expected state code
- [ ] If the login covers multiple GSTINs, the correct one is selected **now** and
      will be re-verified after every navigation away from the returns dashboard

A return filed against the wrong GSTIN of the same group is a serious problem and
the portal will not warn you. This is the first check for a reason.

## 2. Registration status

- [ ] Status is **Active** (not Suspended, not Cancelled)
- [ ] If suspended — reason identified from the intimation or REG-31
- [ ] If cancelled — cancellation order date noted, and the 90-day REG-21 window
      computed
- [ ] No open **REG-17** show-cause notice for cancellation (7 working day reply)
- [ ] No pending cancellation application
- [ ] Aadhaar authentication complete; no biometric verification pending
- [ ] Bank account furnished (Rule 10A) — its absence causes suspension
- [ ] Any pending core-field amendment noted

→ Anything off here: `references/14-exception-flows.md`, before doing anything else.

## 3. Filing history

- [ ] Every prior period's GSTR-1 filed
- [ ] Every prior period's GSTR-3B filed
- [ ] CMP-08 / GSTR-4 filed, if composition
- [ ] GSTR-6 / GSTR-7 / GSTR-8 filed, if applicable
- [ ] GSTR-9 / GSTR-9C filed for prior years where applicable
- [ ] Backlog listed oldest-first with due dates, if any

Returns are sequential. A gap anywhere blocks everything after it.

## 4. Three-year bar

- [ ] `scripts/due_dates.py --timebar` run for the oldest unfiled period
- [ ] Anything already barred identified and separated — it cannot be filed
- [ ] Anything within 90 days of the bar flagged as the most urgent item in the
      engagement, and said to the user first

## 5. Notices and orders

- [ ] **View Notices and Orders** checked
- [ ] **View Additional Notices and Orders** checked — notices routinely appear
      only here, and deadlines get missed because nobody looked
- [ ] Any **DRC-01B** (GSTR-1 vs 3B liability mismatch) — 7-day reply, blocks GSTR-1
- [ ] Any **DRC-01C** (2B vs 3B ITC mismatch) — 7-day reply, blocks GSTR-1
- [ ] Any **ASMT-10** scrutiny notice
- [ ] Any **ASMT-13** best-judgement assessment — **note the order date and compute
      the 60-day window**, this is often the highest-value item in the engagement
- [ ] Any **GSTR-3A** non-filing notice
- [ ] Any show-cause notice under §73 / §74 / §74A
- [ ] **REG-17 checked via Services → Registration → Application for Filing
      Clarifications** — a registration SCN may not appear in either notices view,
      and "not in the notices tab" is not evidence there is no notice
- [ ] Any refund **RFD-03** deficiency memo, with the remaining §54 limitation
- [ ] Reply deadlines listed with days remaining

## 6. Ledgers

- [ ] Electronic **cash** ledger balance recorded, by head
- [ ] Electronic **credit** ledger balance recorded, by head
- [ ] Cess balance recorded separately (usable only against cess)
- [ ] Credit ledger **not blocked under Rule 86A** — if blocked, note the amount and
      the date imposed, and check whether the one-year auto-lapse has passed
- [ ] Liability ledger checked for anything outstanding
- [ ] Any unutilised challan or unclaimed payment identified

## 7. E-way bill status

- [ ] Generation **not blocked** under Rule 138E
- [ ] If blocked, the two-period default identified and the operational impact
      raised with the user immediately — goods cannot legally move

## 8. Exporters only

- [ ] **LUT valid for the current financial year**, ARN recorded — an expired LUT
      silently converts a zero-rated supply into a taxable one
- [ ] Export invoices checked against the Rule 96A windows (3 months for goods,
      1 year for payment on services)
- [ ] Any pending refund application status noted

## 9. Thresholds and scheme

- [ ] AATO for the preceding FY confirmed, PAN-wide across all GSTINs
- [ ] E-invoicing applicability confirmed (any FY since 2017-18 above ₹5 crore)
- [ ] 30-day IRN reporting window applicable? (AATO ≥ ₹10 crore)
- [ ] QRMP opt-in status matches what the user believes
- [ ] Composition status and eligibility still valid
- [ ] Any threshold crossed during the year, and given effect

## 10. Outcome

- [ ] Results written to `work/period-state.md`, including any notice reference
      and deadline
- [ ] No blockers → proceed to Step 4 (evidence and reconciliation)
- [ ] Blockers found → dependency chain written out and stated to the user in plain
      language before any remedy is proposed, e.g.:

      "E-way bills are blocked because two GSTR-3Bs are unfiled. The older one is
      40 days from the three-year bar, so it has to go first. It needs cash
      because the credit ledger is blocked under Rule 86A, and that block was
      imposed 14 months ago so it should have lapsed — worth challenging before
      you find the money."

People make better decisions when they can see the chain. Give them the chain.
