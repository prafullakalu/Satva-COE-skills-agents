# Harvest sources: setup, capture, journals (tag h1)

Licences read from each LICENSE file in a local shallow clone.

## Repositories evaluated

| Repo | Licence (read from file) | Verdict | Notes |
|---|---|---|---|
| https://github.com/anthropics/knowledge-work-plugins | Apache-2.0 (no NOTICE) | imported | finance/skills/journal-entry and journal-entry-prep fed journal-entry-controls and accruals-deferrals-prepaids references. smb-onboard skipped: tied to Cowork connectors and memory. |
| https://github.com/hazlijohar95/skills | MIT, Copyright (c) 2026 Hazli Johar | imported | financial-close adjust, journal-entry, categorize, setup-client. Strongest source found. closekit script not copied. |
| https://github.com/Receiptor-AI/bookkeeping-skills | MIT, Copyright (c) 2026 Receiptor AI | imported | bookkeeping-setup, expense-categorization, receipt-processing: references and two pure-local scripts. US tax mapping not imported. |
| https://github.com/openaccountant/skills | MIT, Copyright (c) 2026 Open Accountant | skipped | import-transactions, smart-categorize, bank-sync: thin and bound to the vendor's "Wilson" tools; bank-specific header notes US-only. |
| https://github.com/claude-office-skills/skills | MIT, Copyright (c) 2026 Claude Office Skills Contributors | skipped | smart-ocr, pdf-ocr, invoice-organizer: library tutorials (PaddleOCR) and filler; not accounting practice. |
| https://github.com/karbonhq/Public-Claude-Skills | MIT, Copyright (c) 2026 Karbon | skipped | payroll-journal-entry-skill-builder is payroll (other stage) and Karbon-specific. |
| https://github.com/alirezarezvani/claude-skills | MIT, Copyright (c) 2025 Alireza Rezvani | skipped | no bookkeeping, setup, capture or journal skills in my stages. |
| https://github.com/panaversity/agentfactory-business-plugins | Apache-2.0 | skipped | banking regulation focus; bank-reconciliation belongs to another stage. |
| https://github.com/anthropics/financial-services-plugins | Apache-2.0 | skipped | accrual-schedule and roll-forward are 33-37 line fund-admin stubs; ours is deeper. |
| https://github.com/vpodugu/startup-bookkeeper | MIT, Copyright (c) 2026 Q3 Learners LLC | skipped | single 435-line app-style skill coupled to artifact storage keys and dashboards. |
| https://github.com/GAJETOso/financeskills | MIT, Copyright (c) 2026 KOMVIA | skipped | journal-entry is 94 lines; covered by the Apache and MIT imports above. |
| https://github.com/harshith-vaddiparthy/finance-skills | MIT, Copyright (c) 2026 Loopfour | skipped | 39-47 line stubs, AR and revenue focus. |
| https://github.com/sickn33/agentic-awesome-skills | MIT root plus separate LICENSE-CONTENT (not adopted) | link-only | aggregator of 2,500 skills with mixed provenance; accounting entries are Nepal-specific registers (PAN, VAT, TDS). |
| https://github.com/Layer-Fi/bookkeeper-skill | no LICENSE file | link-only | journal entry skill bound to the Layer API; cannot copy. |
| https://github.com/Denymbird/accounts-receivable-skills | MIT, Copyright (c) 2026 Paidnice | skipped | accounts receivable, another stage. |
| https://github.com/ugbodagadave/Isabella | MIT, Copyright (c) 2024 Ugbodaga Dave | skipped | application code, no skills in my stages. |
| https://github.com/openaccountants/claude-code-plugin | MIT, Copyright (c) 2026 Glimpse Ltd | skipped | tax skills over a hosted MCP; tax stage. |

## Per-skill mapping

| Our skill | Upstream path | Outcome |
|---|---|---|
| journals/journal-entry-controls | knowledge-work-plugins finance/skills/journal-entry, journal-entry-prep; hazlijohar95/skills financial-close/journal-entry (+ je-csv-format reference) | replaced ours, ours folded in |
| journals/adjusting-entries-register | hazlijohar95/skills financial-close/adjust (+ schedule-formats reference) | new |
| journals/accruals-deferrals-prepaids | knowledge-work-plugins finance/skills/journal-entry-prep | kept ours + added reference |
| setup/client-close-profile | hazlijohar95/skills financial-close/setup-client | new |
| setup/client-books-onboarding | Receiptor-AI/bookkeeping-skills bookkeeping-setup | kept ours + added reference |
| capture/transaction-review-and-cleanup | hazlijohar95/skills financial-close/categorize | new |
| capture/transaction-categorisation-rules | Receiptor-AI/bookkeeping-skills expense-categorization | kept ours + added references and script |
| capture/receipt-ocr-intake | Receiptor-AI/bookkeeping-skills receipt-processing | kept ours + added references and script |
| setup/chart-of-accounts-design, capture/bank-feed-import-and-capture | none better found | kept ours |
