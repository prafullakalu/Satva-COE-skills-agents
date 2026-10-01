---
name: adjusting-entries-register
description: >-
  Build the period-end adjusting entries register: roll forward accruals and reversals, prepaid amortisation, depreciation and deferred revenue schedules, run an unrecorded-liabilities search and a completeness scan, tie every schedule to its control account, and emit an approved-only import CSV. Use for "month-end adjusting entries", "roll the schedules", "book accruals and reversals", "prepaid and depreciation run", "JE register", or "did we miss any accruals".
metadata:
  department: "accounting"
  domain: "journal-entries"
  owner: "satva-coe"
  status: "beta"
  license: "MIT"
  source: "https://github.com/hazlijohar95/skills/tree/main/skills/financial-close/adjust"
---

<!-- Adapted from hazlijohar95/skills skills/financial-close/adjust (MIT, Copyright (c) 2026 Hazli Johar). Modified by Satva: plugin-specific tooling, question-tool mechanics and house-style linting removed; checks reworded to be tool-agnostic. -->

# Adjusting entries register

Turn schedules and exceptions into a register of every adjusting entry the period needs, each with a workpaper, each waiting on explicit approval. Approved entries leave as an import-ready CSV for the user's own system. This skill posts nothing anywhere. The entry contract (balanced, cited source, stable memo) is in `journal-entry-controls`; schedule arithmetic for routine accruals is in `accruals-deferrals-prepaids`.

## Scope

In scope, the routine core:

- Accrued expenses and revenue, with automatic reversal of prior-period accruals.
- Prepaid amortisation.
- Depreciation and amortisation from a fixed asset schedule.
- Deferred revenue for streams whose invoices match delivery: one obligation, billed for its own service period, no variable terms. Bundles, set-up fees, ramps, usage terms, credits and amendments are revenue judgments, not schedule rows; route them to the revenue skills.
- Reclassification and capitalisation entries approved in cleanup or raised by reconciliation, where a journal is how the amount moves.

Out of scope, each with its manual path: inventory and COGS (needs a count or costing method), FX remeasurement (needs a rate policy), tax provision, equity compensation, intercompany (needs both entities' books), AR allowance and bad debts (the reserve is the preparer's policy call), impairments (measurement needs a valuation judgment), contract cost estimates and loss provisions. Name these in the deliverable when the data suggests they exist; never attempt them. If the user supplies the governing judgment (an allowance percentage, an estimated total cost, a costing method), record it as theirs, offer to save it to the client profile, then run it like any authorised policy.

## Inputs

- The client profile (see `client-close-profile`): recurring schedules, estimation policies, materiality.
- Schedules: prepaid, fixed asset register, deferred revenue, standing accruals. Formats in [references/schedule-formats.md](references/schedule-formats.md).
- Exceptions raised by reconciliation and `transaction-review-and-cleanup`.
- GL detail and trial balance for control-account tie-outs.

## Workflow

1. **Collect the work**: schedules to roll forward, adjustment-required items from the exceptions list, standing accruals due this period.
2. **Check reversals first.** Every prior-period accrual marked auto-reverse must have its reversal in this period's GL, or have been settled directly against the liability (a payment debiting the accrual, documented on the schedule), or get a reversal proposed here. Relieved neither way: first entry on the register. Relieved both ways: a double-relief flag. The prior period's register carries the auto-reverse obligations; fall back to the GL pattern if it is missing.
3. **Roll each schedule forward** per the formats file, including the optional loan roll-forward with interest recalculation when a lender statement is on hand. Each schedule closing balance equals the trial-balance balance of its control account exactly; rounding is a labelled line on the schedule, never absorbed silently.
4. **Completeness scan, both directions.** New payment to a prepaid-type vendor with no schedule row; asset-sized purchase not on the register; and the easy one to miss, a new billing whose service period runs past the close ("annual", "12 months") sitting fully in revenue. Check the exceptions list first: an item already dispositioned is settled, not re-asked. Each hit is a question or a new schedule row.
5. **Unrecorded liabilities search.** Read all post-period evidence: early next-period GL and bank activity, bills dated after period end for period services, late statements. Payroll cutoff is the classic case: a pay cadence whose last run predates period end means earned, unpaid wages. Each catch is a proposed accrual with the evidence cited. File the search as its own small workpaper listing what was searched and found, including a clean result. With no post-period data, say the search is limited to bills and statements on hand.
6. **Draft each entry** under the entry contract with a workpaper: source, calculation, tie-out.
7. **Missing source data blocks that adjustment.** It goes on the register as blocked with what is missing; it is never estimated into existence unless a named estimation policy covers exactly that item (then apply it and label the figure "estimated per policy"). A method gap blocks the same way: inventory costing, depreciation convention, FX rates and contract recognition run under the client's stated method or stop with a question.
8. **Present the register for approval.** Itemise entries above materiality; offer the rest as a reviewed batch. Do not mark any entry approved without explicit confirmation.
9. **Emit the CSV** of approved entries only, per `journal-entry-controls` references, verify it foots overall and per entry, and file it with the register.

Cash-basis client: steps 2 to 5 collapse to a reversal and carryover check; accrual conversion is an explicit opt-in.

## When to ask and when to proceed

- **Fact**: the schedule and GL settle it. Derive it; do not ask.
- **Precedent**: the client books it the same way every period. Follow and note.
- **Judgment**: more than one defensible treatment. Below materiality take the conservative treatment, proceed and disclose. Above materiality, hard to reverse, or in a flagged risk area, queue a question.

Write each question down the moment it is queued (close log or exceptions list). Track the running total of proceed-and-disclose judgments: when the aggregate crosses materiality, convert the open ones to questions and say the aggregate out loud. Twenty immaterial guesses are one material guess. Running unattended, leave every entry proposed with the register complete; approval never happens without a human.

## Degradation

| Missing input | Fallback |
|---|---|
| A profile schedule | Rebuild from GL history when the pattern is unambiguous, labelled rebuilt; else blocked with a request |
| Fixed asset register | Depreciation blocked; carry the prior entry only if the profile authorises it as policy |
| Exceptions list | Work from provided schedules only and say cleanup items were not sourced |
| Prior-period GL | Reversal check limited to what the user confirms; each unverified reversal disclosed |

## Anti-patterns

- **The estimate that closes the gap**: a schedule that will not tie gets a rounding entry. Tell: a memo that cannot name a source or policy. Put the gap on the register instead.
- **The permanent accrual**: it repeats every period but its reversal never posts, doubling the liability. Tell: a liability that only grows. Check reversals before drafting new accruals.

## Completion criteria

- [ ] Every schedule ties to its control account exactly, rounding documented.
- [ ] Every prior-period auto-reverse accrual is reversed, or its missing reversal is on the register.
- [ ] Every entry is approved, declined, or blocked with the missing source named.
- [ ] The CSV holds approved entries only and foots.
- [ ] Out-of-scope adjustments the data suggests are named.

## Output

```
JE register: <client>, <period>
| # | Entry | Dr | Cr | Amount | Source | Status (approved/proposed/blocked) |
Schedules: each closing balance, control account, tie-out result
Reversals: prior accruals reversed or flagged
Blocked: each with the missing source
Out of scope observed: named with manual path, or omitted
CSV: path, entry count, total Dr = total Cr
```

## Do not

- Mark anything approved silently; batch approval is fine, silent approval is not.
- Post to any system; the CSV is the handoff.
- Assume a method because it is common.
- Re-ask an item already settled in cleanup.
