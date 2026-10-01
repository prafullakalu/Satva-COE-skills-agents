# Harvest h2-recon-apar: sources evaluated (stages: reconciliation, payables-receivables)

Licences below were read from the LICENSE file in a shallow clone made 2026-10-01. Verbatim texts of imported repos are in `LICENSES/`. The Anthropic repos ship an unfilled Apache-2.0 template (no copyright line); attribution is to the repository owner.

## Repositories evaluated

| Repo | Licence (read from file) | Verdict | Notes |
|---|---|---|---|
| https://github.com/anthropics/knowledge-work-plugins | Apache-2.0 | imported | small-business ap-processor and invoice-chase (with references); finance reconciliation |
| https://github.com/anthropics/financial-services | Apache-2.0 | imported (small) | gl-reconciler gl-recon and break-trace folded into a reference |
| https://github.com/Denymbird/accounts-receivable-skills | MIT (Paidnice) | imported | AR toolkit with tested local script; vendor promotion removed |
| https://github.com/Receiptor-AI/bookkeeping-skills | MIT | imported (reference) | bank-reconciliation tiers, rules and scenarios folded into our bank-reconciliation as a reference; its trivial summary script left out |
| https://github.com/panaversity/agentfactory-business-plugins | Apache-2.0 | imported | banking bank-reconciliation as nostro-and-suspense-reconciliation |
| https://github.com/GAJETOso/financeskills | MIT (KOMVIA) | imported | automated-reconciliation (with script, references, template); intercompany-accounting as a reference |
| https://github.com/ChipmunkRPA/bank-recon-skill | MIT | imported | bank-statement-to-gl-workbook with stdlib script; PDF path found fragile, documented |
| https://github.com/alirezarezvani/claude-skills | MIT | imported | business-operations vendor-management as vendor-performance-review (3 stdlib scripts) |
| https://github.com/grailautomation/claude-plugins | no LICENSE file | link-only | near copy of the Anthropic finance skills |
| https://github.com/MosoFin/finance-ops-skills-index | none read; published skills described as AGPL-3.0 | link-only | index of vendor skills (three-way match, expense report processor); AGPL, never copy |
| https://github.com/andrew-tao-li/ai-audit-skills (expense-audit-v2) | repo LICENSE Apache-2.0 template; skill frontmatter says MIT-0 | link-only | differing per-skill licence, Chinese-language, 1,800-line script; Satva wrote expense-report-review instead |
| https://github.com/claude-office-skills/skills (expense-report, expense-tracker, invoice-organizer) | MIT | skipped | generic templates, thin; no policy tests |
| https://github.com/openaccountant/skills (invoice-aging, venmo-reconciler) | MIT | skipped | 52 and 97 lines, tool-specific; superseded by the AR toolkit |
| https://github.com/harshith-vaddiparthy/finance-skills | MIT | skipped | 40-line stubs (ar-collections, dunning-emails, payment-reconciliation) |
| https://github.com/Denymbird/accounting-workflow-skills | MIT | skipped | accounting-practice workflows (fee scoping, onboarding, query chase), outside these stages |
| https://github.com/JoelLewis/finance_skills (client-operations reconciliation, settlement-clearing) | MIT | skipped | securities and custodian operations, not company accounting |
| https://github.com/himself65/finance-skills | MIT | skipped | market analysis and data readers, no AP/AR/reconciliation |
| https://github.com/Layer-Fi/bookkeeper-skill | no LICENSE file | link-only | |
| https://github.com/karbonhq/Public-Claude-Skills | MIT | skipped | practice management, not these topics |
| https://github.com/davidnumeric/generalaccountingskills | none; empty repository | skipped | |
| https://github.com/skills-il/accounting | not evaluated | skipped | Israel-specific |
| https://github.com/AIanumel2025/accounts-payable-agent | MIT (per listing, not cloned) | skipped | a software agent with a database, not a skill |

GitHub code and repository search was rate-limited (shared across parallel agents), so discovery relied on WebSearch, awesome-list style results and the repos already cloned by earlier passes. A wider sweep with `gh search` when the limit resets may find more.

## Per skill

| Our skill (path under skills/accounting) | Upstream path | Outcome |
|---|---|---|
| payables-receivables/ap-invoice-processing | anthropics/knowledge-work-plugins small-business/skills/ap-processor (+ reference/*) | replaced ours; our bank-detail, approval-matrix, discount and cut-off checks folded in |
| payables-receivables/ar-collections-dunning | anthropics/knowledge-work-plugins small-business/skills/invoice-chase (+ reference, examples) | replaced ours; our ladder, outcomes and write-off controls folded in |
| payables-receivables/ar-aging-analysis | Denymbird/accounts-receivable-skills skills/accounts-receivable (+ script, references, sample CSV) | replaced ours; our tie-out, concentration, AP and allowance notes folded in |
| payables-receivables/vendor-performance-review | alirezarezvani/claude-skills business-operations/skills/vendor-management | new |
| payables-receivables/ap-three-way-match | (ap-processor matching_and_exceptions, by pointer) | kept ours + added pointer |
| payables-receivables/vendor-setup-and-1099-data | none better found | kept ours |
| payables-receivables/ar-cash-application | none (original) | new, Satva-original |
| payables-receivables/customer-credit-control | none (original) | new, Satva-original |
| payables-receivables/bad-debt-and-credit-loss-allowance | none (original) | new, Satva-original |
| payables-receivables/expense-report-review | none (original); andrew-tao-li link-only | new, Satva-original |
| reconciliation/bank-reconciliation | Receiptor-AI/bookkeeping-skills skills/bank-reconciliation | kept ours + added references/matching-tiers-and-scenarios.md |
| reconciliation/bank-statement-to-gl-workbook | ChipmunkRPA/bank-recon-skill skill/ | new |
| reconciliation/automated-reconciliation | GAJETOso/financeskills skills/automated-reconciliation | new |
| reconciliation/nostro-and-suspense-reconciliation | panaversity banking/skills/bank-reconciliation | new |
| reconciliation/subledger-to-gl-reconciliation | anthropics knowledge-work-plugins finance/reconciliation; anthropics/financial-services gl-recon, break-trace | kept ours + added references/break-analysis-and-escalation.md |
| reconciliation/intercompany-tie-out | GAJETOso/financeskills skills/intercompany-accounting | kept ours + added references/framework-and-eliminations.md |
| reconciliation/credit-card-reconciliation | none better found | kept ours |
| reconciliation/account-reconciliation-certification | none (original) | new, Satva-original |
