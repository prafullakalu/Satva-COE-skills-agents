# Responding to a REG-17 cancellation notice

LAST_VERIFIED: 2026-07-29
VOLATILE: the reply window and the portal route. Confirm the deadline stated on
the notice itself — it governs, not the general rule.

A REG-17 show-cause notice proposes to cancel the registration. Answering it
properly is far cheaper than revocation afterwards, so treat it as the most urgent
item in the engagement the moment one appears, regardless of what the user
originally asked for.

## Contents

- [The order of operations](#the-order-of-operations)
- [Finding the notice](#finding-the-notice)
- [Regularise first, then reply](#regularise-first-then-reply)
- [Drafting the reply](#drafting-the-reply)
- [Supporting documents](#supporting-documents)
- [Filing it](#filing-it)
- [After submission](#after-submission)

## The order of operations

This sequence matters more than the wording of the reply.

1. **Read the notice.** Reason for the proposed cancellation, the reply deadline
   (commonly 7 working days), and the notice reference.
2. **Diarise the deadline** and tell the user the days remaining, first, before
   anything else.
3. **Fix the underlying default.** For non-filing, that means filing the returns.
   A reply that promises compliance is weak; a reply that reports completed
   compliance with ARNs is strong, and often ends the matter.
4. **Draft the reply** against what has actually been done.
5. **Save it on the portal** as soon as the text is entered — do not draft, wander
   off, and come back.
6. **The user submits with EVC or DSC** (Tier 3).
7. **Capture the acknowledgement**, then monitor for the officer's order.

Steps 3 and 4 are the whole thing. The officer is deciding whether this registrant
is going to keep complying, and evidence beats assurance.

## Finding the notice

A REG-17 is a **registration** action, not a return action, so it may not surface
where people look for notices.

- Services → User Services → **View Notices and Orders**
- Services → User Services → **View Additional Notices and Orders**
- **Services → Registration → Application for Filing Clarifications** — this is the
  route that reliably shows a registration SCN and is where the reply is filed. If
  a user says they have a cancellation notice and the notices tabs show nothing,
  go here before concluding it does not exist.

Record the notice reference in the period state:

```text
work/period-state.md: notice.type=REG-17  notice.reference=<ref>
  notice.status=open  notice.deadline=<YYYY-MM-DD>
  next_action="file pending returns before drafting the REG-17 reply"
```

## Regularise first, then reply

Where the notice is for non-filing — much the most common reason — do this before
drafting anything:

1. List every unfiled period, oldest first.
2. Check the three-year bar. Anything barred cannot be filed and has to be
   addressed differently in the reply; say so plainly rather than being vague.
3. File each period completely — reconcile, compute, pay, file, **capture the ARN**
   — before starting the next. Returns are sequential and GSTR-2B will not generate
   for a period until the previous GSTR-3B is filed.
4. Build the compliance table that goes into the reply: period, return, ARN, date
   filed, tax paid, late fee paid.

Verify from the portal that nothing remains pending before drafting. A reply
claiming full compliance that the officer can immediately disprove is worse than
no reply.

## Drafting the reply

Use `assets/reg17-response-template.md`. What makes a reply work:

- **Answer the specific ground stated in the notice.** Not compliance in general —
  the thing they raised.
- **Lead with what has been done**, with ARNs and dates in a table. Verifiable
  facts, checkable on their own system.
- **Explain the cause briefly and without drama.** One or two sentences. A short,
  candid explanation reads better than an elaborate one.
- **Say what has changed** so it does not recur — a specific, modest, credible
  measure.
- **Request that the notice be dropped**, explicitly.
- **Keep it to one page.** Officers read many of these.

What to avoid:

- **Do not fabricate anything.** Not a medical emergency, not a hospitalisation,
  not a family bereavement, not a hardware failure. If the user offers a reason,
  ask whether documentary evidence exists and include it only if it genuinely does.
  Where there is no evidence, state the reason plainly as an unevidenced
  explanation, or leave it out. Inventing a ground in a statutory reply is a false
  statement to a tax authority, and it is not something to help with under any
  framing. If asked to, decline in one sentence, then offer the honest version —
  which is usually just as effective, because the compliance table is doing the
  work.
- Do not admit to anything not asked about.
- Do not dispute a ground that is factually correct — fix it and report the fix.
- Do not promise dates that will be missed.

## Supporting documents

The portal accepts a single supporting upload with a **size limit of about
0.976 MB** (1,024,000 bytes), typically PDF or JPEG.

So consolidate everything into **one PDF, one page if possible**: the compliance
table with ARNs, plus any genuine evidence. Practical ways to stay under the limit:

```bash
# Combine, then compress
pdfunite compliance.pdf evidence.pdf combined.pdf
gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.4 -dPDFSETTINGS=/ebook \
   -dNOPAUSE -dQUIET -dBATCH -sOutputFile=support.pdf combined.pdf
ls -l support.pdf     # must be under 1,024,000 bytes
```

If it will not compress far enough, drop screenshots before dropping the compliance
table — ARNs are checkable on the officer's own system, so a text table is worth
more per kilobyte than an image of the same thing.

Check the byte size before uploading. An oversized file is rejected at submission,
which on this form means re-entering the declaration block.

## Filing it

1. Navigate via **Services → Registration → Application for Filing Clarifications**
   and select the notice reference.
2. Enter the reply text yourself and verify it landed. This textarea is an Angular
   control that can silently drop pasted text: re-read the field after saving and
   check that **Save becomes enabled**.
3. **Screenshot the entered text** into `work/screenshots/` before saving. If the
   session resets, this is what lets it be re-entered exactly.
4. Upload the supporting PDF (Tier 1) and confirm the filename appears.
5. **Save** (Tier 2). Record `notice.status=saved_awaiting_evc` in the period state.
6. Complete the declaration block: **verification checkbox, authorised signatory,
   place.** Note that a session timeout **resets all three** while preserving the
   saved reply text — reopen via Dashboard → Saved Forms and set them again.
7. **The user submits with EVC or DSC (Tier 3).** The verification declaration is
   a legal statement by the taxpayer that the contents are true; reading and
   accepting it is theirs, not the agent's. Present the final text and let them
   confirm it before they sign.

If the reply is interrupted: Dashboard → **Saved Forms** → "Reply to Show Cause
Notice".

## After submission

- **Capture the acknowledgement / ARN immediately** and record it:

  ```text
  work/period-state.md: notice.status=submitted  notice.arn=<ARN>
  next_action="monitor for REG-20 (drop) or REG-19 (cancellation)"
  ```

- **Monitor for the order.** **REG-20** drops the proceedings and the registration
  continues. **REG-19** cancels it — at which point the revocation route applies
  (REG-21 within 90 days, all returns filed first) and
  `references/14-exception-flows.md` takes over.
- Registration is often **suspended while the SCN is pending**. Outward supplies
  should not be made under a suspended registration, and e-way bills may be
  blocked. Tell the user what that means operationally rather than leaving them to
  discover it at the warehouse.
- Keep filing on time. The single best protection against the order going the wrong
  way is a clean record between the reply and the decision.
