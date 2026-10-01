# REG-17 reply — working draft

Draft here, get it confirmed, then enter it on the portal yourself (long text
fields on the portal can silently drop pasted text: re-read the field after saving). Keep the final text to roughly one page.

Everything in angle brackets must be replaced with a verified fact. **Do not leave
a placeholder in, and do not fill one with something plausible that has not been
checked** — this is a statutory reply and the taxpayer signs a declaration that its
contents are true.

---

## Notice details (fill before drafting)

| | |
|---|---|
| Notice reference | |
| Notice date | |
| Reply deadline | |
| **Days remaining as at today** | |
| Ground stated in the notice | |
| Registration status now | Active / Suspended |
| Jurisdictional officer / ward | |

## Compliance position (complete BEFORE drafting)

Every pending return filed, verified from the portal:

| Period | Return | ARN | Filed on | Tax paid ₹ | Late fee ₹ |
|---|---|---|---|---|---|
| | | | | | |

- [ ] Every period listed in the notice is now filed
- [ ] Verified from the portal, not from memory or from this table
- [ ] Any period that **cannot** be filed (three-year bar) is identified below,
      with what is being done about it instead
- [ ] Nothing else is outstanding that the officer could immediately point to

Periods that cannot be filed, and why:

---

## Reply text

> To,
> The Proper Officer / Superintendent,
> <ward / jurisdiction>
>
> **Subject: Reply to show cause notice for cancellation of registration —
> Notice Reference <reference> dated <date>**
>
> Sir / Madam,
>
> This is in response to the show cause notice referenced above, which proposed
> cancellation of GSTIN <GSTIN> on the ground of <ground exactly as stated in the
> notice>.
>
> **The default has been made good.** All returns referred to in the notice have
> been filed, with tax, interest and late fee paid in full:
>
> | Period | Return | ARN | Filed on |
> |---|---|---|---|
> | | | | |
>
> **Reason for the delay.** <One or two plain sentences. State only what is true.
> If there is documentary evidence, refer to it and attach it. If there is none,
> say so plainly — an unevidenced but honest explanation reads better than an
> elaborate one, and the compliance table above is what actually persuades.>
>
> **Steps taken to prevent recurrence.** <One specific, modest, credible measure —
> a named person responsible, a monthly reminder, an accountant engaged. Do not
> promise a system that will not exist.>
>
> The registration is active and the business is continuing to operate. There is no
> outstanding liability as at the date of this reply.
>
> In the circumstances, I respectfully request that the proposed cancellation be
> dropped and the registration be continued.
>
> Supporting document attached: <filename> — <one line describing it>.
>
> Yours faithfully,
> <Name>
> <Designation — Proprietor / Partner / Director / Authorised Signatory>
> <Legal name of the business>
> GSTIN <GSTIN>
> <Date>

---

## Honesty check before this goes anywhere

- [ ] Every factual statement is verified, including every ARN
- [ ] **No reason has been invented.** No medical, bereavement, hardware or family
      ground appears unless it is genuine *and* evidenced, or is clearly stated as
      an unevidenced explanation
- [ ] Nothing is promised that will not happen
- [ ] Nothing is admitted that the notice did not ask about
- [ ] The compliance table matches the portal exactly

If the user asks for a fabricated ground, decline in one sentence and offer the
honest version. A false statement in a statutory reply is not a drafting choice.

## Supporting PDF

- [ ] Single file, one page if possible
- [ ] Contains the compliance table with ARNs
- [ ] Contains only genuine evidence
- [ ] **Under 1,024,000 bytes** — checked with `ls -l`, not estimated
- [ ] Filename is meaningful

## Portal submission

- [ ] Route: Services → Registration → Application for Filing Clarifications
- [ ] Reply text entered on the portal and re-read after saving
- [ ] Save button became enabled (proof the text landed)
- [ ] Screenshot of the entered text saved to `work/screenshots/`
- [ ] Supporting PDF uploaded, filename confirmed on screen
- [ ] **Saved** on the portal — logged as Tier 2
- [ ] Period state updated to `notice.status=saved_awaiting_evc`
- [ ] Declaration block completed: verification checkbox, authorised signatory,
      place — **re-check these if the session timed out; they reset while the
      saved text survives**
- [ ] Final text read and accepted by the taxpayer
- [ ] **Submitted by the taxpayer with EVC or DSC** (Tier 3 — the verification
      declaration is their legal statement, not the agent's)
- [ ] Acknowledgement / ARN captured immediately
- [ ] Period state updated to `notice.status=submitted` with the ARN

## Afterwards

- [ ] Diarised to watch for **REG-20** (dropped) or **REG-19** (cancelled)
- [ ] User told what suspension means operationally in the meantime
- [ ] Ongoing returns kept current — the record between reply and order matters
