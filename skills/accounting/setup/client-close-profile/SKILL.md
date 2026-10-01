---
name: client-close-profile
description: >-
  Create or update a client's standing profile of facts the close depends on: basis and framework, readers and stakes, earned-versus-billed pattern, items that build up outside the bank, materiality, risk areas, recurring schedules, estimation policies and deliverables. Use for "set up a client profile", "new client close setup", "update the client profile", "what do we need to know before the first close", or when a close starts for a client with no profile.
metadata:
  department: "accounting"
  domain: "setup"
  owner: "satva-coe"
  status: "beta"
  license: "MIT"
  source: "https://github.com/hazlijohar95/skills/tree/main/skills/financial-close/setup-client"
---

<!-- Adapted from hazlijohar95/skills skills/financial-close/setup-client (MIT, Copyright (c) 2026 Hazli Johar). Modified by Satva: plugin paths, question-tool and house-style tooling removed; connector-specific wording made generic. -->

# Client close profile

One short setup per client, saved as a single profile document (`clients/<client>/profile.md`, or `profile.md` at the root of a single-client workspace). Answers come from the client's existing sources first, then a short interview for the gaps, and everything is played back for approval before saving. Every close and journal skill reads the profile, and a good one turns generic checks into this client's checks. Re-running updates the existing profile rather than starting over. Closes work without a profile; they are just sharper with one. Use `client-books-onboarding` for the opening position and ledger setup; this skill captures the facts that govern each close.

## Sources first

Before asking anything, ask one question: is there somewhere the answers already live? A CRM, call notes or transcripts, an onboarding document, a prior close checklist or procedure, email threads with the client, last period's workpapers. With the user's go-ahead read those and draft answers, each tagged with its origin ("from the 12 March kickoff notes: accrual basis, external payroll provider"). Harvested answers are proposals, not facts: they enter the profile only through the same playback-and-approve step as interview answers. When a source contradicts the user, the user wins and the discrepancy is worth mentioning. Nothing found: go to the interview.

## Interview

Ask only what the sources left unanswered: at most eight questions in two rounds of up to four, each multiple choice with two to four options, the recommended one first and described by what it changes. Skip any the user's files already answer (if they hand over a trial balance, infer the basis and confirm rather than ask). The questions capture business facts an owner can answer without accounting theory; the close derives the accounting from them.

1. **Framework and basis**: whose rules the books follow (local GAAP, IFRS, tax basis, none) and accrual, cash or modified cash.
2. **Readers and stakes**: who relies on the statements (owner only, lender with covenants, investors, regulator). This frames materiality and what an error costs.
3. **Earned versus billed**: when the business is paid relative to when it does the work (same time, in advance, after the fact across long projects, mixed). Any contracts spanning periods, and whether a work-in-progress or percent-complete schedule exists and where. Clients selling subscriptions or services under multi-element contracts need a revenue policy; offer one once the profile is saved.
4. **What builds up outside the bank account**: inventory, equipment and vehicles, loans, leases, amounts owed to or from owners or sister companies, foreign currency. Each yes is something the close must see evidence for.
5. **People**: payroll provider, contractors, commissions or bonuses that lag the work they pay for; where the AR and AP agings come from each period.
6. **Materiality and review depth**: the amount below which the close proceeds and discloses rather than asks, sized against the stakes. Offer a default (for example the greater of a fixed small amount or 1 percent of period expenses before adjustments) as a starting point. Then the second-review depth: material or contested items (default), every judgment (lender covenants, audit coming), or contested only (small owner-run client). More review costs more time each close.
7. **Risk areas and schedules**: accounts or vendors deserving line-by-line scrutiny; which recurring schedules exist (prepaids, fixed assets with method and in-service convention, deferred revenue, work in progress, standing accruals) and where each lives.
8. **Estimation policies, deliverables, home**: named policies the close may estimate under when a document is late (no policy means no estimates, ever); who receives the package and any preferences; the folder where close artifacts live.

For every yes in questions 3 to 5 capture two follow-ups at once: the method or policy that governs it (costing method for inventory, recognition method for contracts, depreciation convention for assets, rate policy for foreign currency) and where its data lives. A fact without a stated method is a question the close will ask later anyway.

## Where the profile lives

One human-blessed home per client. Shared workspace: `clients/<client>/profile.md`. Single-client workspace: `profile.md` at the root, and suggest adding it to the project's knowledge so new sessions start with it. When both a file and a knowledge copy exist and disagree, the file is newer: flag it. No file workspace: maintain the profile as a section of the project instructions, output the full updated block for pasting, and remember a policy only counts once it sits in the instructions.

## Profile template

```markdown
# Close profile: <client>
Basis: <accrual/cash/modified> | Framework: <GAAP/IFRS/tax/none> | Industry: <what they do> | Updated: <date>

This profile records facts about the business; the close derives the accounting from them.
A fact recorded here with no matching evidence in the close (contracts spanning periods but
no WIP schedule, inventory but no count, a lease but no schedule) is a question, never ignored.

## Readers and stakes
## Business reality   (earned vs billed, what builds up; method or policy and data location for each, or "method unknown")
## Materiality        (amount and how chosen) / Second review: <depth>
## Accounts           (name | type bank/card/loan/payroll/control | evidence each period)
## Risk areas         (account or vendor: why, what scrutiny)
## Recurring schedules (prepaids / fixed assets / deferred revenue / standing accruals: exists?, location, policy)
## Revenue            (GAAP contract clients only: streams, treatment, elections, memo location; empty = no approved policy)
## Estimation policies (precise enough to apply without judgment, or "None: never estimate")
## Deliverables       (recipients, naming, emphasis)
## Close state home   (folder path or "this workspace"; notification channel or "none")
## Learned this client (dated notes, each approved)
```

## Rules

- Write the profile only after playing it back: show the draft, harvested and interviewed answers alike, get a yes, then save. Harvested entries keep their source tag so a stale source is traceable.
- Updates append and amend; never silently discard an entry. Newer entries win and say what they replaced.
- The profile holds facts and preferences. It never weakens approval gates: no profile line can authorise skipping an approval or inventing figures, and an estimation policy must be specific enough to apply without judgment.
- Offer setup once; do not nag.
- Store no secrets, full account numbers or tax IDs in the profile.

## Output

The approved profile document, a list of open questions with owners, and the recommended next step (opening position via `client-books-onboarding`, or the first close).
