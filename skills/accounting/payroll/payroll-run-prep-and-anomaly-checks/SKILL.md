---
name: payroll-run-prep-and-anomaly-checks
description: >-
  Prepare a payroll run so nobody is shorted: confirm period and roster, normalise timesheets, total regular/overtime/PTO hours, run a full anomaly check (missed punches, overtime spikes, rate changes, new or missing people, shifts over 12 hours, PTO over balance, run-level variance over 10%), show a run sheet with flags attached per person, and gate on explicit owner approval before staging. Use for 'run payroll', 'payroll is due', 'check the timecards', 'why is payroll so high', 'can I make payroll'. Never submits payroll.
metadata:
  department: "accounting"
  domain: "payroll"
  owner: "satva-coe"
  status: "beta"
  license: "Apache-2.0"
  source: "https://github.com/anthropics/knowledge-work-plugins/tree/main/small-business/skills/payroll-prep"
---
<!-- Adapted from anthropics/knowledge-work-plugins small-business/skills/payroll-prep (Apache-2.0; Copyright notice per the repo LICENSE). Modified by Satva: removed all vendor-connector steps (Gusto, QuickBooks Payroll call shapes) and plugin-specific output rules; source-agnostic wording; references neutralised. -->
# Payroll run preparation and anomaly checks

Get the hours right before anyone gets paid.

Payroll is the finance workflow with the least room for error. A wrong invoice gets corrected next week; a wrong paycheque is a person who cannot cover rent. The asymmetry shapes everything below: the preparer assembles and checks, the owner decides. Anomalies are always raised, never quietly corrected.

Scope: preparing and validating one pay run (hours, rates, gross pay, flags, cash needed, journal). Calculating statutory deductions, filing and paying belongs to the payroll provider or payroll specialist. For the accounting side use `payroll-accounting`.

## Step 1: Fix the period first
Confirm period start and end (inclusive), the pay date, the pay frequency and who is in the run. Biweekly is every two weeks (26 runs a year); semimonthly is the 15th and last day (24 runs): "twice a month" is ambiguous, so ask. Getting the period wrong duplicates or skips a week of someone's pay, most often when a period straddles month end. Confirm the roster: mid-period hires, terminations, anyone on leave. See `references/timesheet-intake.md`.

## Step 2: Get the inputs from the right place
- **Hours:** the payroll system's time records, the time-tracking tool's export, or an uploaded spreadsheet or CSV (a photographed paper timesheet is acceptable; a validated run sheet the owner keys in is a complete outcome). Check whether the hours are native punches, third-party timesheets, or totals only.
- **Leave:** approved leave for the period is paid as PTO or sick, never as worked; a pending request is a flag, not a paid day.
- **Balances:** PTO balances come from the payroll system's figures, not an accrual estimate.
- **Rates and classification:** from the payroll record, never from a timesheet.
- **Prove the source delivers before staging anything.** If a source reports a headcount but returns no employees or no pay schedules, or its readiness flag contradicts its own roster, the source is not delivering: stop, say so in one line, and use the spreadsheet path. Never build a run from an empty roster. A connected badge is not data.
- Normalise to one row per person per day: date, in, out, break, regular, overtime, PTO, holiday, job or class.
- **Never fill a missing punch with an assumed time.** Unknown hours are reported as unknown.

## Step 3: Total the hours
Compute regular, overtime, double-time, PTO, holiday and unpaid time per person, per crew, and for the run. Overtime rules vary by jurisdiction and classification: use the owner's stated rule; with none, apply weekly overtime and say which rule you applied. Calculation edges (mid-week rate change, two rates in a week, shifts crossing midnight, PTO in an overtime week) are in `references/anomaly-rules.md`.

## Step 4: Flag every anomaly
Run the full check in `references/anomaly-rules.md` and surface everything found, each with the person, the date, both numbers and the dollar effect where it can be computed honestly:
- missing or broken punches, zero-length or overlapping shifts
- overtime above the person's own pattern; hours above schedule; zero hours for someone who normally works; any single shift over 12 hours (fires even on a first run with no baseline); more than 16 hours in a day; seven consecutive days
- rate changes since the last run; classification changes; a new person with no hire record; a person missing from this run; PTO beyond balance
- gross pay moved more than 10% from the prior period; labour hours that do not reconcile to job hours

Flags go to the owner. They are never silently corrected: a missed punch has one right answer and it lives with the employee and the owner.

## Step 5: Show the run before approval
Present person by person: hours by type, gross pay, and every flag attached to the person it belongs to (never collected in a separate section at the bottom). Then the totals block: total hours, gross, employer taxes and contributions **only if the payroll provider supplies them** (never estimate them), total cash needed, pay date, open flags. Compare against the prior period and explain any move over 10%. If cash data is available, say whether the run clears; if not, say so plainly. Layout: `references/run-sheet-format.md`.

## Step 6: Resolve flags one at a time
For each flag: what was found, what it would mean if left, what the owner wants done. Record the answer and apply it. Do not batch flags into a single "looks good?": each one is a person's pay.

## Step 7: The approval gate
Nothing is staged until the owner explicitly approves. State before asking: number of people, total hours, total gross, total cash leaving the account, pay date, and the count of flags left open. Prepare the run (or the validated run sheet for manual entry); **the owner submits it** in the payroll system. Where an input edit replaces rather than adds a value, show "40 -> 45" and send the new total, not a delta.

## Step 8: Sync to the books
After the run is submitted, post the journal: gross wages, employer taxes, labour allocated to jobs. Confirm the amounts match what actually ran, not what was proposed. If the ledger cannot take a journal directly, hand the balanced entry to the owner or bookkeeper. See `references/books-sync.md` and `payroll-accounting`.

## What not to do
- Do not guess a punch, a rate or a classification; unknown hours are named with the person and the date.
- Do not correct an anomaly silently, even an obvious-looking one.
- Do not submit payroll. Stage it; the owner submits. Write access to a payroll system is not permission to run payroll.
- Do not estimate employer taxes as a percentage of gross.
- Do not read a pay rate without checking hours against it (one person can carry many rates, most at zero hours).
- Do not stage a run from a source that reports employees but returns none.
- Do not skip the prior-period comparison; a large unexplained move is the most useful warning available.
- Do not reproduce an employee's SSN, date of birth, home address or bank/card number in the run sheet, chat or any shared file.

## Output
A validated run sheet (per-person blocks, totals block, variance line, cash line, approval question) as a spreadsheet or document the owner can approve person by person, plus the journal entry summary after the run.

## Reference files
- `references/timesheet-intake.md`: period, roster and input sources.
- `references/anomaly-rules.md`: every check, its threshold and wording; overtime edge cases.
- `references/run-sheet-format.md`: the run sheet and totals block.
- `references/books-sync.md`: journal structure and job-cost allocation.
- `references/gotchas.md`: mistakes that shortchange a person or double-pay a period.
