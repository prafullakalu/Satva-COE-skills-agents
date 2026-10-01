<!-- Adapted from anthropics/knowledge-work-plugins small-business/skills/payroll-prep/reference/books_sync.md (Apache-2.0). Modified by Satva: vendor and connector names removed. -->

# Books sync and job costing

Posting the payroll to the ledger after it runs: where the ledger has a journal-entry path, post it there; otherwise hand the balanced entry to the owner or bookkeeper to key in. Test the capability, not the product name.

---

## Timing

**Sync after the run is submitted, never before.** The proposed run and the run that actually happened differ any time the owner edited a line at the last step, and posting the proposal creates a journal entry that will not reconcile to the bank.

Pull the final figures from the payroll provider's register where possible. Where the owner ran payroll manually, ask them to confirm the final gross and tax amounts before posting.

---

## The entry

A standard payroll journal has these components:

| Account | Side | Source |
|---|---|---|
| Wages expense (or job cost) | Debit | Gross wages by person, allocated |
| Employer payroll tax expense | Debit | Employer share only |
| Payroll liabilities — taxes withheld | Credit | Employee withholding |
| Payroll liabilities — employer taxes | Credit | Employer share |
| Cash | Credit | Net pay actually disbursed |

The entry must balance. If it does not, something in the source figures is wrong — say so and stop rather than plugging the difference to a suspense account. A forced balance hides the error permanently.

---

## Job costing

When the business tracks labor to jobs, allocate wages expense by the job hours already captured on the timesheets.

- Allocate at **fully burdened cost** when the owner has given a burden rate. Otherwise allocate raw wages and label it as such.
- **Do not invent a burden rate.** A made-up 22% loading makes every job margin wrong in the same invisible direction.
- Hours with no job assigned go to unallocated labor, visibly, so the owner can see how much is drifting there. A large unallocated bucket is itself worth reporting.

---

## Reconciliation check

After posting, verify:

1. Total debits equal total credits
2. Net pay in the entry matches the actual bank debit from the payroll provider
3. Job-allocated hours sum to total paid hours, minus whatever went unallocated
4. The period the entry lands in matches the pay date, not the period end

Point 4 catches the month-end straddle. A period ending March 31 with an April 4 pay date posts to April cash and, if the owner accrues, March wages. Ask which treatment they use rather than picking one.

---

## Accruals

If the owner accrues wages at month end, the portion of the period worked in the prior month gets an accrual entry and a reversal. Ask once whether they accrue and remember the answer. Most small businesses do not, and adding accruals to books that have never had them makes the year harder to close, not easier.

---

## What to confirm back

After posting, report plainly:

> Posted to the ledger, March 20: USD 9,840 wages, USD 812 employer taxes, USD 10,652 cash.
> USD 7,210 allocated across four jobs, USD 2,630 unallocated.
> Entry balances and matches the payroll provider's bank debit.

Any of those three failing to line up gets said out loud, not smoothed over.
