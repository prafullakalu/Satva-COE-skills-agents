---
name: accounting-firm-client-onboarding-sop
description: >-
  A standard operating procedure for onboarding a new client into an accounting or bookkeeping practice: intake and risk screening, engagement and KYC, access and data collection, opening-balance and prior-period review, workflow setup, kickoff, and a 30-day stabilisation checklist. Use when a firm wants a repeatable onboarding process, or says "new client onboarding checklist", "client intake", "onboarding SOP", "taking over from another accountant", "client kickoff" or "predecessor accountant letter". For the books themselves see client-books-onboarding.
metadata:
  department: "accounting"
  domain: "advisory"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Client onboarding SOP (accounting firm)

Onboarding sets the margin on the engagement for the next three years: clean access, signed scope and verified opening balances make every later month cheaper. The SOP below covers the *firm's* process; technical set-up of the books is in `client-books-onboarding`, and the engagement letter in `accounting-firm-engagement-letters-and-pricing`. To audit a firm's SOP library see `sop-library-auditor`.

## Roles

Partner/owner (accepts the client, signs the letter), engagement manager (runs onboarding), preparer or bookkeeper (does the set-up), admin/ops (accounts, portal, billing). Name a single accountable owner per client.

## Stage 1: Intake and acceptance (days 0 to 3)

1. Discovery call and intake form: entity type and structure, ownership, industry, revenue and transaction volume, accounting basis, systems, banks, payroll provider, sales-tax footprint, prior accountant, deadlines, pain points, expectations.
2. Risk screen: integrity of management, nature of business (cash-intensive, crypto, regulated, high-risk jurisdiction), unpaid tax or fines, litigation, urgency that smells of a problem, prior-firm disputes. Escalate red flags to the partner; document an accept/decline decision.
3. Conflict and independence check against existing clients and services.
4. Capacity check: hours required against the team's calendar.
5. Scope and price proposal; client signs the engagement letter and the data-processing terms before any data is exchanged.
6. AML/KYC where required: verify identity of beneficial owners and the entity, retain evidence, run sanctions screening, record the risk rating.

## Stage 2: Authorisations and access (days 3 to 7)

1. **Predecessor communication:** with client written consent, request a professional clearance and files from the previous accountant (prior returns, workpapers, closing trial balance, fixed-asset register, loan schedules).
2. Read-only access wherever possible: bank feeds or statements, accounting software, payroll, payment processors, sales channels, tax portals (via delegated authority such as a power of attorney or authorised-agent filing, never by sharing a personal login).
3. Individual accounts for each team member; no shared credentials; multi-factor authentication; record who has access to what in the client file; remove access when the engagement ends.
4. Secure portal for documents; a folder structure standard (Admin, Bank, Payroll, Tax, Close, Supporting).

## Stage 3: Data collection and review (days 5 to 15)

1. Checklist of documents: formation documents, tax IDs and filing status, prior-year returns and financials, closing trial balance, bank and card statements for the period, loan agreements, leases, payroll registers, fixed-asset listing, inventory counts, AR/AP agings, sales-tax filings, contracts for revenue recognition.
2. Review the **opening position**: do opening balances agree to the prior returns or financials? Do bank balances tie to statements? Are there stale uncleared items, unexplained suspense or owner accounts, negative AR, unfiled returns, unrecorded liabilities?
3. Produce a **findings memo** and a clean-up estimate (hours and cost); agree with the client whether clean-up is included, extra or phased. Never proceed on unknown opening balances.
4. Decide the conversion date and cutover rules (balances only vs transaction history); see `client-books-onboarding`.

## Stage 4: Workflow set-up (days 10 to 20)

1. Work-management: create the client record, recurring tasks (monthly close, payroll, sales tax, annual filings), due dates and owners, templates per service.
2. Close calendar agreed with the client: when they upload, when you reconcile, when reports go out.
3. Standard reports, KPIs and the delivery format; the monthly reporting template.
4. Billing set-up: invoice schedule, payment method, first invoice issued per the letter.
5. Communication plan: primary contacts, response times, escalation path, meeting cadence.

## Stage 5: Kickoff and stabilisation (days 15 to 45)

1. Kickoff call: recap scope, responsibilities, timeline, and how to send documents; show the first dashboards.
2. First month: complete bank reconciliation, review and categorise, adjust, issue reports; run internal review by a second person.
3. Day 30 review: what was cleaned, what remains, data quality score, time vs budget, client feedback; adjust scope or price if the actuals diverge.
4. Day 45 close-out of onboarding: tick every checklist item, store sign-offs, move the client to steady-state workflow.

## Quality gates

| Gate | Evidence |
|---|---|
| Accept | Risk screen and conflict check on file, partner sign-off |
| Engage | Signed engagement letter, KYC complete |
| Access | Access register complete, MFA confirmed |
| Opening balances | Tied to source, findings memo agreed |
| Go-live | First reconciliation reviewed, client kickoff held |
| Stabilised | 30-day review done, actual hours vs budget recorded |

## Failure modes

- Working from unsigned scope.
- Accepting a "temporary" shared login.
- Opening balances taken from the prior books without verification.
- No named owner, so tasks stall between roles.
- Clean-up work done free and never repriced.
- Client data left in personal email or chat tools.

## Output

Intake form, risk and acceptance record, onboarding checklist with owners and dates, access register, findings memo, close calendar, 30-day review note.
