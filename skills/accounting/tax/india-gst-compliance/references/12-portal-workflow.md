# GST portal workflow and known quirks

LAST_VERIFIED: 2026-07-29

> **This is the manual route** and the default in this library: the agent prepares
> the figures and the click path, the user (or their CA) operates the portal. See
> `SKILL.md` for the authority tiers. It is also the reference for what each screen
> is supposed to contain.
>
> If something is blocked rather than merely manual — suspension, cancellation, a
> blocked ledger, blocked e-way bills, an open notice — go to
> `14-exception-flows.md` instead.

## The division of labour

**The agent prepares**: reconciled figures, table-by-table values, the difference
register, recommended IMS actions per invoice, offline-tool-ready JSON or CSV,
step-by-step portal instructions, and the checks to run on the portal's preview.

**The user does**: logging in, uploading, taking IMS actions, generating IRNs and
e-way bills, making payment, filing with DSC or EVC, and downloading the filed
return.

Say this explicitly at the start of a session, not at the end. A user who expects
you to file will otherwise assume it is done.

## Getting data out of the portal

Ask the user to download, and to save into `source/`:

| What | Where |
|---|---|
| GSTR-2B (JSON and Excel) | Returns Dashboard → the period → GSTR-2B → Download |
| GSTR-1 filed summary / JSON | Returns Dashboard → GSTR-1 → Download filed return |
| GSTR-3B filed summary | Returns Dashboard → GSTR-3B → Download filed return |
| IMS dashboard export | Services → Returns → Invoice Management System |
| Electronic cash / credit / liability ledgers | Services → Ledgers |
| E-invoice (IRN) list | einvoice.gst.gov.in → Reports, or the GSP/ERP |
| E-way bills | ewaybillgst.gov.in → Reports → Detailed |
| Notices and orders | Services → User Services → View Notices and Orders, **and** View Additional Notices and Orders |

**Check both notice tabs.** Notices routinely appear only under "Additional Notices
and Orders", and taxpayers miss reply deadlines because they only looked at the
first one. Make this an explicit intake question.

## The monthly sequence

```
1st–10th    Close books. Reconcile the sales register to e-invoices.
            Screen the expense ledger for RCM. Total everything independently.
11th/13th   User files GSTR-1 / IFF. Download the filed summary immediately.
11th–14th   IMS: review every record against the purchase register.
            Prepare a recommended action list; user executes it on the portal.
14th        GSTR-2B generates. Download it.
14th–19th   Reconcile 2B to the purchase register. If IMS actions were taken
            after generation, the user clicks Recompute GSTR-2B.
            Prepare GSTR-3B values. If GSTR-1 was wrong, prepare GSTR-1A now —
            it can be filed only once, so compile everything first.
            Check ledger balances and Rule 86B.
By 20th     Self-review, filing pack, sign-off. User pays and files.
```

For QRMP, the same sequence runs quarterly, with PMT-06 by the 25th in months 1
and 2 and the optional IFF by the 13th.

## Known portal behaviours worth planning around

- **Sessions time out** after a short idle period, and long uploads fail silently
  when they do. Tell the user to prepare offline and upload in one go.
- **The offline utility** (Returns Offline Tool) is more reliable than the online
  form for large GSTR-1 datasets. JSON schema versions change; download the current
  utility rather than reusing an old one.
- **Auto-population is not instant.** GSTR-1 to GSTR-3B, and e-invoice to GSTR-1,
  can lag by hours. A blank or partial table shortly after filing is usually
  latency, not data loss — refresh before re-entering anything.
- **"Proceed to File" recomputes.** Always review the summary generated at that
  point rather than the values entered earlier.
- **Locked tables cannot be overridden.** If the auto-populated 3.1/3.2 differs from
  your computation, your GSTR-1 is wrong, or your computation is. Investigate;
  never adjust another table to compensate. Compensating in 4B or 5.1 to make the
  net payable look right is the kind of fix that turns a small error into an
  allegation of suppression.
- **Negative values** are rejected in most tables. Excess credit notes over
  outward supplies in a period must be carried forward, not entered as negative.
- **GSTR-2B is static.** It does not update on its own after generation; only
  Recompute changes it.
- **DSC on Windows** needs emSigner running and the browser trusting localhost.
  EVC via OTP to the registered mobile and email is simpler where permitted —
  note that companies and LLPs generally must use DSC.
- **Peak-hour slowness** near the 11th, 13th and 20th is normal. Plan to be ready a
  day early rather than at 23:00 on the due date.

## Reviewing the portal preview before filing

Give the user a short, specific list rather than "check everything":

1. Does the total taxable value in the preview match the filing pack, to the rupee?
2. Does the tax head split (IGST / CGST / SGST / cess) match?
3. Does Table 4A ITC match the reconciled figure, and is the 2B date on the preview
   the recomputed one?
4. Is Table 3.1(d) RCM present, and is the cash payment sufficient for it?
5. Does the late fee and interest shown match the computed figure? If the portal's
   interest differs, understand why before accepting it.
6. Does the payment split between cash and credit respect Rule 86B?
7. Is the cash ledger balance sufficient? If not, the challan must be generated and
   paid first — and NEFT/RTGS challans can take time to reflect.

## After filing

- Download the filed return and the ARN acknowledgement into `output/`.
- Update the difference register: what was resolved, what was carried forward.
- Note anything to fix in the next period, especially credits deferred within
  §16(4) and IMS records left pending.
- Record any position taken that could be questioned later, with the reasoning. A
  year from now, nobody will remember why.
