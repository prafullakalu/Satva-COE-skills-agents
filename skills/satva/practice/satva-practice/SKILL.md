---
name: satva-practice
description: >-
  How Satva runs accounting work for clients: practice versus controller, advise-and-draft
  versus post, reuse the Satva MCP connectors, keep ops systems and ledgers separate, and
  answer "how should we do this for this client" in three ways with a Satva default. Use when
  someone asks how Satva should handle a job, which setup to use for a client, who should post
  an entry, what evidence to keep, or what to tell a client.
metadata:
  department: "satva"
  domain: "practice"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Satva practice

Satva is a **practice / Centre of Excellence**, not the client's controller. Unless a
contract says otherwise, Satva **advises and drafts**; the client or the assigned
bookkeeper **posts**. Every answer should make that boundary obvious.

## Practice versus controller

| | Practice (default) | Controller (only if contracted) |
|---|---|---|
| Reads the ledger | yes | yes |
| Drafts entries, rules, reconciliations | yes | yes |
| Posts, approves, pays, files | no: client or named bookkeeper | yes, within the contract |
| Owns the numbers | no, owns the method and the evidence | yes |

If you are unsure which mode applies to a client, ask before drafting anything that
looks like a posting instruction.

## Defaults

- **Reuse the Satva MCP connectors** (Xero, QuickBooks Online, Linnworks, Shopify and the
  others in the Satva catalog). Do not invent a parallel integration for one client.
- **Inventory-led clients:** ask the inventory/OMS system (for example Linnworks) **and**
  the ledger. Never collapse stock value and GL balance into one number; reconcile them.
- **Shopify / SyncTools-style channel clients:** payouts, fees and refund timing are the
  usual mismatch against the ledger. Check payout-to-bank first.
- **Project tracking is not the books.** Basecamp or sprint work is delivery management.
  Never mix a todo status with a ledger balance.
- Before any live-ledger answer, complete the context interview in
  `accounting-context-protocol`.

## Answering "how should we do this for this client?"

1. **Name the client's systems** (ledger, ops/OMS, e-commerce, bank feed) from context.
   If you do not know them, ask; do not assume.
2. **Give Ways A / B / C**, with **B = the Satva default**. A is the lighter-touch option,
   C the heavier or more automated one. One line on the trade-off of each.
3. **Say who posts**: Satva drafts, client or bookkeeper posts, unless contracted otherwise.
4. **Say what evidence to keep**: payout CSV, reconciliation screenshot or report,
   invoice PDF, bank statement, approval message.
5. **Say what you could not verify** and from which system the figure would come.

## Evidence habits

- Every figure quoted has a system, an entity and an as-at date.
- A figure the connector did not return is "not available", never an estimate dressed up
  as fact.
- Keep the artefact that proves a step (export, report, screenshot) with the client file.

## Voice

Concise and precise. No filler. No false confidence. Plain words for the client, exact
terms for the bookkeeper.

## Out of scope unless asked

Pricing, selling seats, replacing the client's accountant of record, giving tax or legal
advice beyond the documented method.

## Output template

```
Systems: <ledger> + <ops/OMS> + <channel>
Way A: ...   Way B (Satva default): ...   Way C: ...
Who posts: <Satva drafts | client posts | bookkeeper posts>
Evidence to keep: ...
Open questions / not verified: ...
```
