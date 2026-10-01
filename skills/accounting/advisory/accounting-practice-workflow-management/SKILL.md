---
name: accounting-practice-workflow-management
description: >-
  Running an accounting or bookkeeping practice as a production system: work-in-progress pipeline, capacity planning, utilisation and realisation, review and quality control tiers, deadline management in busy season, recurring-task templates, practice KPIs and technology stack choices. Use when a firm struggles with missed deadlines, uneven workload, low realisation, or says "practice management", "capacity planning for tax season", "WIP report", "firm KPIs", "review process", "workflow bottleneck" or "utilisation target".
metadata:
  department: "accounting"
  domain: "advisory"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Accounting practice workflow management

A practice is a factory whose raw material is client documents and whose constraint is review capacity. Missed deadlines and burnout come from unmanaged queues, not from lack of effort.

## Step 1: Map the service lines and standard work

For each line (monthly bookkeeping, payroll, sales tax, individual and business tax, advisory, special projects): list the task stages, owner role, expected hours, due date rule, inputs required from the client, and the output. Convert each into a recurring template in the practice-management tool with checklists and review sign-offs. If a task has no template, it does not scale.

## Step 2: The work pipeline

Use five visible states for every job: **Waiting on client, Ready, In progress, In review, Done/Delivered**. Limit work in progress per preparer (finish before starting). Make blocked time explicit: jobs stuck on the client are the largest hidden cost; track days waiting and trigger reminders automatically (see `ar-collections-dunning` for the discipline, applied to documents).

Weekly pipeline meeting (30 minutes): overdue, due in the next 14 days, blocked jobs, review queue length, capacity gaps.

## Step 3: Capacity planning

1. Capacity = staff x available hours x target utilisation (commonly 70 to 85 percent for staff, lower for managers and partners) after leave and training.
2. Demand = recurring hours + seasonal peaks (tax season, year-end, audit prep) + project work + onboarding.
3. Plot by week for the next quarter. Gaps over 10 percent trigger action: reschedule non-urgent work, overtime caps, temporary or offshore support, accept fewer new clients, or raise prices.
4. Cross-train so that at least two people can run any recurring service.
5. Busy-season rules: extension strategy and client communication cut-offs, document cut-off dates a set time before deadlines, frozen scope, protected time off afterwards.

## Step 4: Review and quality control

Three tiers: (1) preparer self-check against the checklist; (2) reviewer checks analytics and exceptions (variance and reasonableness, tie-outs), not re-performance; (3) partner review for risk items, new clients, significant judgements and anything going to lenders or regulators. Review notes are logged; repeated notes by preparer or topic feed training. Keep a documented quality-management system proportionate to the firm's size: engagement acceptance, independence, supervision, monitoring (sample file inspection), and remediation of findings.

## Step 5: Metrics (monthly)

| Metric | Formula | Healthy signal |
|---|---|---|
| Utilisation | Billable hours / available hours | At or above target by role |
| Realisation | Billed fees / standard value of time | 90 percent or more for fixed-fee work tracked against budget |
| Effective hourly rate | Revenue / hours worked | Rising year on year |
| WIP days | Unbilled WIP / average daily revenue | Under 30 |
| Debtor days | AR / average daily revenue | Under 45 |
| On-time delivery | Jobs delivered by internal deadline / total | Above 95 percent |
| Rework rate | Hours on corrections / total hours | Falling |
| Revenue per FTE | Annual revenue / FTE | Benchmark against peers |
| Client profitability | Fees less cost of time by client | See `pricing-and-profitability-analysis` |

Time tracking is required even for fixed-fee work; otherwise profitability is guesswork.

## Step 6: Technology stack

Choose by workflow, not by feature list: practice management (jobs, templates, time), document collection and e-signature, client portal, accounting and payroll platforms, tax software, AI assistance under a written policy (approved tools, no client identifiers in unapproved tools, human review of output, disclosure in engagement letters), password manager and MFA, backup. Integrate where data crosses systems and name an owner for each integration.

## Failure modes

- Everything is "urgent", so nothing is scheduled.
- No work-in-progress limit; preparers juggle 40 jobs and finish none.
- Reviewers re-do the work, becoming the bottleneck.
- Time not recorded, so repricing is impossible.
- AI tools adopted ad hoc with client data and no policy.

## Output

Service-line templates, pipeline board definition, 13-week capacity plan, review checklist and quality log, practice KPI dashboard, technology map with owners.
