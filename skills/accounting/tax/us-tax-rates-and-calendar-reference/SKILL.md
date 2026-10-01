---
name: us-tax-rates-and-calendar-reference
description: >-
  Dated reference for US federal and Illinois tax: 2025-2026 brackets, limits and thresholds, the post-OBBBA changes, filing and estimated-payment calendar, multi-state nexus and apportionment notes, Illinois PTE and replacement tax, plus routing to the right tax skill. Use for 'what is the current bracket/limit', 'tax deadlines', 'when is the 1099 due', 'what changed with OBBBA', 'multi-state filing'. Always state the tax year of a figure; verify against IRS and state sources.
metadata:
  department: "accounting"
  domain: "tax"
  owner: "satva-coe"
  status: "beta"
  license: "MIT"
  source: "https://github.com/davidjelinekk/tax-skills-claude-code/tree/main/skills/tax"
---
<!-- Adapted from davidjelinekk/tax-skills-claude-code skills/tax (MIT, Copyright (c) 2025-2026; the LICENSE file names no holder). Modified by Satva: orchestrator reduced to a routing and reference skill, slash-command routing replaced by skill names, currency caveat added. -->

> **Tax year and jurisdiction.** Upstream targets US federal tax for tax years 2025 and 2026 (post-OBBBA, P.L. 119-21, signed 4 July 2025) with Illinois as the default state. Figures, thresholds and sunset dates change: verify against current IRS and state guidance. Illinois-specific material applies only to Illinois taxpayers. Educational guidance, not tax advice; a licensed CPA or tax attorney makes the binding call.

# US tax rates, limits and calendar reference (2025-2026)

Look-up skill: it holds dated reference tables and routes tax questions to the right skill. It computes nothing itself.

## When to use

Use to answer "what is the current bracket / limit / threshold", "when is this due", "what changed with OBBBA", or to pick the right sibling skill. Always state the tax year of every figure you quote.

## Routing

| Question | Skill |
|---|---|
| Categorise expenses, chart of accounts, records | `tax-aligned-bookkeeping`, `schedule-c-expense-categories` |
| Reduce tax, entity choice, retirement plans | `tax-optimization-strategies` |
| Which forms, document checklist, extensions | `us-return-forms-and-filing-checklist`, `tax-prep-package` |
| Audit risk, red flags, penalties | `tax-audit-risk-assessment` |
| Quarterly estimates | `estimated-tax-and-tax-prep-organiser` |
| 1099 and W-9 | `contractor-1099-reporting` |

## Context intake (ask once, in a single message)

Filing status; state of residence; income sources (W-2, Schedule C, K-1, investments, rental, crypto); entity types; dependents; approximate AGI range (phase-outs); the specific question. Extract what the user already gave; do not re-ask.

## Key legislative context (post-OBBBA, signed 4 July 2025)

QBI deduction (Section 199A) made permanent; 100% bonus depreciation restored for property acquired after 19 January 2025; SALT cap raised to $40,000 for 2025-2029 with phase-down above $500K AGI; Section 179 limit $2,500,000 (2025); Child Tax Credit $2,200 per child; standard deduction increased; new deductions for tips, overtime and auto-loan interest; estate exemption $15M per person; interest-deduction limit back to 30% of EBITDA. Verify each against current law and note sunset years.

## Quality gates

- Include the not-professional-advice disclaimer.
- Cite the IRC section or IRS publication for any position; flag audit-risk implications (`tax-audit-risk-assessment`).
- Note where Illinois rules differ from federal.
- Use post-OBBBA numbers for 2025 and later; flag sunset provisions.
- Never recommend a filing position without noting its documentation requirement.

## Reference files (load on demand)

- `references/current-rates.md`: 2025-2026 rates, brackets, limits, thresholds.
- `references/tax-calendar.md`: federal and Illinois deadlines, estimated payment dates.
- `references/multi-state-guide.md`: multi-state nexus, apportionment, state filing.
- `references/il-tax-guide.md`: Illinois PTE election, replacement tax, Chicago and Cook County taxes.
