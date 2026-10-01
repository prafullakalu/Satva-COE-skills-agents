<!-- Adapted from anthropics/knowledge-work-plugins small-business/skills/payroll-prep/reference/timesheet_intake.md (Apache-2.0). Modified by Satva: vendor sections merged into one source-agnostic section. -->

# Timesheet Intake

Setting the period, the roster, and getting hours in from wherever they live.

---

## Period setup

Confirm all four before pulling anything:

- **Period start and end** — inclusive dates
- **Pay date** — when money actually lands
- **Pay frequency** — weekly, biweekly, semimonthly, monthly
- **Who is in this run** — hourly crew, salaried staff, or both

Biweekly and semimonthly get mixed up constantly. Biweekly is every two weeks, 26 runs a year. Semimonthly is the 15th and the last day, 24 runs. If the owner says "twice a month" and the last period ran the 1st through the 14th, ask rather than assume.

**Period boundaries matter most at month end.** A week that straddles the 31st has hours in two months for job costing but one paycheck. Keep the pay period whole and let the books sync handle the split.

---

## Roster

Pull the active employee list and compare it to the last run.

| Change | What to do |
|---|---|
| New hire mid-period | Confirm the start date and that hours before it are excluded |
| Termination | Confirm the final date, unused PTO payout if owed, and whether a final check has different timing under state rules |
| On leave | Confirm paid or unpaid, and whether PTO is being drawn |
| Someone paid last period, absent now | Flag it. This is either a termination nobody recorded or a missing timesheet |
| Someone new with no hire record | Flag it. Never pay a person who is not on the roster |

---

## Source: payroll system or time-tracking export

Pull, for the period: hours (check whether they are native punches with breaks, third-party timesheets, or totals only), approved leave (paid as PTO or sick, not as worked; pending is a flag), balances per leave policy (feeds the over-balance check), roster with rates and classifications, and the last processed run's per-person totals for the comparison.

Prove the source is delivering before staging: pull the roster and the pay schedules. A company that reports a headcount while either list comes back empty, or a readiness flag that contradicts the roster, is a connected but non-delivering source. Stop, say so in one line, and use the spreadsheet path. Rates come from the payroll record, never from the timesheet: a rate written on a paper timesheet is a note, not a record.

Three cautions for any payroll system:

- **Employment status and the active flag can be separate fields.** Someone flagged active can still be not-on-payroll or on paid leave. Read both before including anyone.
- **One employee can carry many pay rates**, most at zero hours. Total from the rate with hours against it, not the first one listed.
- **Rosters page.** Read every page before totalling; a partial roster silently shorts whoever fell off the end.

A missing punch the owner fills in is recorded only with times the owner stated, shown to them first, as an update of the existing shift rather than a second entry.

---

## Source: spreadsheet upload

The fallback path, and a common one. Small crews run on paper, a shared sheet, or a photo of a whiteboard.

Accept any reasonable layout and map it. Expected columns, however they are named:

- Employee name or ID
- Date
- Time in, time out
- Break minutes, or a flag that breaks are already deducted
- Hours, if the sheet is already totaled
- Job, class, or cost code, if tracked
- Pay type: regular, PTO, holiday, unpaid

**Ask which convention the sheet uses for breaks.** A sheet that already nets out lunch, processed as though it doesn't, shortchanges everyone by half an hour a day. This one question prevents the most common upload error there is.

When the sheet is already totaled, still recompute from the punches when punches exist. When only totals exist, use them and say so — the anomaly checks that depend on punch times will not run, and the owner should know which safety nets are off.

---

## Normalizing

Produce one row per person per day:

```
person | date | in | out | break_min | regular | ot | pto | holiday | job
```

Rules that keep this honest:

- A shift crossing midnight belongs to the day it started, unless the owner's policy says otherwise
- Overlapping entries for one person are never merged automatically — they are flagged
- A row with an in and no out gets hours recorded as unknown, not estimated
- Rounding follows the owner's stated policy; with no policy, do not round at all

---

## Worked example

Okonkwo Mechanical, week ending 3/15, five on the crew.

- No payroll system export. Ray uploaded a shared sheet with in and out times, breaks not deducted.
- Confirmed: breaks are 30 minutes unpaid, taken daily, not punched.
- Roster matched last period except one new apprentice, Dee, started Wednesday.
- One row for Marcus on 3/12 has a 6:40 AM in and no out.

Reported: 5 people, 214 hours readable, 1 shift with no clock-out (Marcus, Thursday), 1 new hire to confirm hours for (Dee, started 3/12).
