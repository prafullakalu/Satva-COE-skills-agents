# Adversarial self-review

Run this after the return is prepared and before anything is shown to the user as
final. The point is not to confirm the work — it is to break it. Approach it
expecting to find something, because on a real engagement you usually will.

Record the outcome in `work/computations.md`, including the checks that found
nothing. "Reviewed, no exceptions" is only meaningful if you can name what you
looked at.

## 1. Attack the biggest number

- Which single figure, if wrong, moves the tax most? Re-verify it from source —
  the actual invoice or ledger, not your own extract.
- Which figure am I least confident about? Say so out loud rather than rounding
  the discomfort away.
- If an officer picked one line to question, which would it be? Is the supporting
  document actually in `source/`?

## 2. Hunt for the missing supply

Understated liability is more dangerous than overstated, because it accrues
interest and can be characterised as suppression. Ask specifically:

- Sale of a fixed asset, or scrap.
- Branch or stock transfer to another state under the same PAN.
- Supply to a related party or distinct person without consideration (Schedule I).
- Free samples, gifts, promotional goods.
- Recoveries from employees — notice pay, canteen, transport.
- Advances received for services.
- Income booked net of expenses, or credited directly to a reserve.
- Barter, exchange or a non-cash settlement.
- Interest, late payment charges or penalties recovered from customers (§15(2)(d)).
- Reimbursements that do not satisfy the pure agent test in Rule 33.

## 3. Attack the credit

- For each material claim: could I show an officer the invoice, proof of receipt,
  and its presence in GSTR-2B, today?
- Is anything claimed that §17(5) blocks? Re-run the list rather than recalling it.
- Is any credit claimed for a period whose §16(4) deadline has passed?
- Is any credit claimed on an invoice from a supplier whose registration status I
  have not checked?
- Have I claimed and also failed to reverse — Rule 42/43, Rule 37, Rule 37A?
- Is any credit claimed twice, once through 2B and once as RCM or import?

## 4. Attack the classification

- Any rate I used because it "is" the rate, without checking the notification for
  this tax period?
- Any supply crossing 22 Sep 2025 or 1 Feb 2026 where I applied the invoice date
  rather than §14?
- Any bundled supply I treated as composite that might be mixed (and taxed at the
  highest rate)?
- Any place of supply I inferred from the billing address?

## 5. Attack the arithmetic

- Did I use `scripts/gst_compute.py`, or did I do arithmetic in prose somewhere?
- Does the line-item total equal the rate-wise aggregate total?
- Do the tax heads add up: IGST + CGST + SGST + cess = total tax?
- Is CGST exactly equal to SGST on every intra-state line?
- Are there rounding differences accumulating in one direction?

## 6. Attack the period

- Have I confused the tax period with the filing month anywhere?
- Does this return contradict what was filed last period — an amendment made
  twice, or a credit taken twice?
- Does it create a problem for next period — an unadjusted advance, a pending IMS
  record, a reversal due?
- Is anything in this return inconsistent with the annual return already filed?

## 7. Attack the process

- Did I use any rate, threshold, due date or portal behaviour from a reference file
  without verifying it in Step 0? List them.
- Is `work/verification-log.md` complete, with sources cited by notification
  number?
- Does `work/difference-register.csv` contain every unresolved item, with an owner?
- Have I anywhere written a summary that reads as reconciled when it is not?
- Would someone else, given only the files in this folder, reach the same numbers?

## 8. The honest question

If this return turns out to be wrong in six months, what will the explanation most
likely be?

Write the answer down. Then go and check that specific thing.
