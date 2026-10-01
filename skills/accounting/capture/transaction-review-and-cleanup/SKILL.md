---
name: transaction-review-and-cleanup
description: >-
  Period transaction review and cleanup before close: sweep uncategorised or suspense items, scan for miscoded transactions, match transfers between own accounts, and hunt duplicates, producing a cleanup list that waits on approval. Use for "clean up the books", "uncategorised transactions", "suspense account cleanup", "find duplicate transactions", "unmatched transfers", "check coding before close", or "miscoded expenses".
metadata:
  department: "accounting"
  domain: "transaction-capture"
  owner: "satva-coe"
  status: "beta"
  license: "MIT"
  source: "https://github.com/hazlijohar95/skills/tree/main/skills/financial-close/categorize"
---

<!-- Adapted from hazlijohar95/skills skills/financial-close/categorize (MIT, Copyright (c) 2026 Hazli Johar). Modified by Satva: plugin paths, question-tool and house-style tooling removed; wording made tool-agnostic. -->

# Transaction review and cleanup

Sweep the period's transactions so every one sits in the right account exactly once. The artifact is a cleanup list of proposed recategorisations, matched transfers and suspected duplicates, each waiting on the user's approval. Nothing is fixed silently. For rule design and substance traps see `transaction-categorisation-rules`; for statement import see `bank-feed-import-and-capture`.

## Inputs

- GL detail export for the period.
- The client profile (`client-close-profile`) for materiality, risk areas and category conventions, if it exists.
- Prior-period GL detail where available: precedent for how this client codes things.

Inside a close, take scope from the close context and file the list with the workpapers. Standalone, sweep whatever export the user provides.

## Workflow

1. **Uncategorised sweep.** List every transaction in a suspense, uncategorised or "ask my accountant" account. Propose a category for each, sourced from this client's own precedent (same vendor, same amount pattern in prior periods) before any generic rule. The no-precedent rule: below materiality with an unambiguous description (a known vendor whose category is obvious), propose it marked low confidence and let batch approval handle it; ambiguous or above materiality goes to the question queue.
2. **Miscoding scan.** For each expense and income account flag transactions that break the account's own pattern: a vendor that always posts elsewhere, an amount an order of magnitude off the normal range, personal-looking spend in business accounts. Profile-flagged risk areas get a line-by-line read, not sampling.
3. **Transfer matching.** Pair each transfer out with its transfer in across accounts: equal amounts, dates within a few business days. Both legs must exist and both be coded as transfers, never income or expense. An unmatched leg is an exception with a proposed resolution.
4. **Duplicate detection.** Same vendor, same amount, dates within a few days. Show each candidate pair side by side in full. Never resolve a duplicate yourself; the user says which record survives. Two identical real transactions on one day are legitimate.
5. **Assemble the cleanup list** (format below), get approval item by item or as a batch, and record decisions. Approved fixes become a recategorisation list where the live system allows direct recoding, or entries routed to `adjusting-entries-register` where a journal is the only way to move the amount. In a file-only workspace, a journal is always the way.
6. **Record the outcome**: the dispositioned list is the record. Log every item questioned or dispositioned on the exceptions list too, so the adjustments step builds on it instead of re-asking.

## Degradation

| Missing input | Fallback |
|---|---|
| Prior-period GL | No precedent: apply the no-precedent rule from step 1 |
| Vendor or memo fields | Match on amount and date only; raise the duplicate threshold to exact-amount matches |
| Client profile | Use default materiality and treat no account as a flagged risk area |

## When to ask versus proceed

- **Fact**: the data settles it. Derive it, never ask.
- **Precedent**: this client's prior coding settles it. Follow and note.
- **Judgment**: more than one defensible category. Below materiality propose the conservative one and disclose. Above materiality, or in a flagged risk area, queue a question.

Write a question down the moment it is queued; a question held only in working memory will be silently answered. Track the running total of proceed-and-disclose judgments: when their aggregate crosses materiality, convert the open ones to questions and say the aggregate out loud. Twenty immaterial guesses are one material guess. Raise queued questions once, with the assembled list. Running unattended, leave unresolved proposals as disclosed exceptions; never auto-approve your own proposals.

## Anti-patterns

- **The confident guess**: a category proposed from a vague memo reads as authoritative. Every proposal names its source: precedent, vendor default or judgment.
- **Transfer income**: a transfer in coded as revenue inflates the P&L. Tell: an income transaction whose counterparty is the client's own account.

## Completion criteria

- [ ] Zero transactions remain uncategorised without an approved category or a place on the exceptions list.
- [ ] Every flagged miscoding is approved, declined by the user, or on the list.
- [ ] Every transfer leg is matched, or its missing counterpart is listed with a proposed resolution.
- [ ] Every duplicate candidate was shown side by side and dispositioned by the user.

## Guardrails

- Propose, never apply. The user approves each fix; unapproved proposals die with the run.
- Duplicates are dispositioned by the user only, with both records shown in full.
- Recategorisations above materiality are itemised individually; batch approval is for the small items.
- Never recode locked or reconciled periods directly; use a reclass journal.

## Output

```
Cleanup list: <client>, <period>
Uncategorised (n): txn, amount, proposed category, source: precedent/default/judgment
Suspected miscodings (n): txn, current account, proposed account, why
Transfers: matched pairs count; unmatched legs with proposed resolution
Duplicate candidates (n): each pair side by side
Approved / declined / open: counts, and where approved fixes went
```
