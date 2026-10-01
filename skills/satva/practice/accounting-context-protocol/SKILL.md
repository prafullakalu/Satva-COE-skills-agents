---
name: accounting-context-protocol
description: >-
  Forces a complete context interview before any answer drawn from a live ledger or ops
  system. Use whenever the user asks about books, cash, invoices, bills, stock, balances,
  Xero, QuickBooks, Sage, NetSuite, Linnworks, Shopify, or "what should we do" for a client
  file, and the system, company, period or read/write mode is not yet established.
metadata:
  department: "satva"
  domain: "practice"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Accounting context protocol

Do not answer with numbers, postings, or "you should" until the session has all five slots
below. A confident number from the wrong company or the wrong month is worse than a
question.

| Slot | Examples | Skip if already in the session |
|---|---|---|
| System | Xero, QuickBooks Online, Sage, NetSuite, Linnworks, Shopify, other portal | known |
| Organisation | tenant name, realm, company file | known |
| Period | as-at date or month | default to *this calendar month* only after saying so out loud |
| Entity | tracking category, location, subsidiary | only if the organisation is multi-entity |
| Mode | read or change | default **read** |

## Interview order

Ask **one missing slot at a time**, in the order above. Do not dump a questionnaire.

Opening line when nothing is known:

> Which accounting or ops system should I use (Xero, QuickBooks, Sage, NetSuite, Linnworks, Shopify, or another portal), and which company?

## Hard rules

1. If the user names a client but not a system, ask for the system. Never assume Xero.
2. If several organisations are connected, list them from the connector (an org-summary
   tool or equivalent) and let the user choose. Never pick silently.
3. If a token or connection is unhealthy, say so **before** any financial figure.
4. Never ask for a password, app secret or 2FA code in chat. Point the user at the
   connector's own Connect flow.
5. Writes (invoices, bills, payments, journals) need an explicit confirmation in the
   product UI. Describe the full payload first, then wait.
6. Quote every figure with system, entity and as-at date. If the connector did not return
   it, say it is not available.

## After context is complete

Restate the five slots in one line ("Xero, <org>, 31 Mar, whole company, read-only"), then
answer. Apply the practice rules in `satva-practice`: Satva advises and drafts, the client
or assigned bookkeeper posts.

## Failure modes this prevents

- Reading a sandbox or demo organisation and reporting it as the client's books.
- Answering for the wrong period because "last month" was ambiguous.
- Combining stock-system and ledger numbers into one figure.
- Proposing a write when the user only asked a question.
