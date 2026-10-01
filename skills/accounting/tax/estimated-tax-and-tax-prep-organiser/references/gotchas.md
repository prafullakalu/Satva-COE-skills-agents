<!-- Adapted from anthropics/knowledge-work-plugins small-business/skills/tax-season-organizer/reference/gotchas.md (Apache-2.0). Modified by Satva: kept the estimated-tax patterns only (1099 patterns live in contractor-1099-reporting). -->

# Good / Bad Patterns

Common failure modes and how to avoid them.

---

## Calculations

**BAD:** Apply 22% to gross revenue.
```
Gross revenue: USD 120,000
Tax estimate: USD 120,000 × 22% = USD 26,400  ← wildly wrong
```

**GOOD:** Apply bracket rate to net profit AFTER SE tax deduction.
```
Gross revenue: USD 120,000
Expenses:      USD 45,000
Net profit:    USD 75,000
SE tax:        USD 75,000 × 92.35% × 15.3% = USD 10,628
Deductible ½: USD 5,314
Adjusted net:  USD 75,000 − USD 5,314 = USD 69,686
Fed. tax est.: USD 69,686 × 22% = USD 15,331
Total:         USD 10,628 + USD 15,331 = USD 25,959
```

---

## Assumptions

**BAD:** State a dollar figure without any context.
> "Your Q2 estimated payment is USD 6,500."

**GOOD:** State the figure with the assumptions table.
> "Based on 22% federal bracket, sole proprietor structure, and no prior-year
> safe harbor data: **Q2 payment ≈ USD 6,500**. State taxes not included.
> QBI deduction not applied. Review with your accountant."

---

## Tax advice boundary

**BAD:** "You should use a SEP-IRA to reduce your tax bill."

**GOOD:** "Your accountant may recommend a SEP-IRA or Solo 401(k) contribution to
reduce taxable income — these can significantly change the estimate above."

The skill surfaces options; the accountant advises.

---

## S-corp owners

**BAD:** Apply SE tax to an S-corp owner's full income.

**GOOD:** Note that SE tax applies only to W-2 wages for S-corp shareholders, not to
K-1 distributions — and ask the user to confirm their business structure before
running calculations. If unsure, default to sole prop math and note the assumption.

