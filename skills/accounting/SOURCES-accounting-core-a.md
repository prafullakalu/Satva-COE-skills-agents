# Sources evaluated: accounting-core-a (setup, capture, journals, reconciliation, AP/AR)

All 16 skills in `skills/accounting/core/` for this tag are Satva-original, written from practitioner expertise. Upstream repos were cloned and their LICENSE files read (shallow clones, 2026-10-01). Where licence allowed, they were read for topic coverage only; no text was copied.

| Upstream | Licence (read from LICENSE) | Verdict | Fed which skills |
|---|---|---|---|
| https://github.com/anthropics/knowledge-work-plugins (finance/reconciliation, journal-entry, journal-entry-prep; small-business/ap-processor, invoice-chase, pay-the-bills) | Apache-2.0 | Permissive; consulted as topic reference, not copied | bank-reconciliation, subledger-to-gl-reconciliation, journal-entry-controls, ap-invoice-processing, ar-collections-dunning |
| https://github.com/panaversity/agentfactory-business-plugins (banking/bank-reconciliation) | Apache-2.0 | Permissive; consulted (matching hierarchy idea), banking-specific so not copied | bank-reconciliation, intercompany-tie-out |
| https://github.com/openaccountant/skills (shared/bank-sync, import-transactions, smart-categorize, business/invoice-aging) | MIT | Permissive; consulted, not copied (tool-specific) | bank-feed-import-and-capture, transaction-categorisation-rules, ar-aging-analysis |
| https://github.com/Receiptor-AI/bookkeeping-skills (receipt-processing, bank-reconciliation, contractor-1099) | MIT | Permissive; consulted, not copied | receipt-ocr-intake, bank-reconciliation, vendor-setup-and-1099-data |
| https://github.com/claude-office-skills/skills (invoice-automation, expense-tracker, expense-report) | MIT | Permissive; consulted, not copied | ap-invoice-processing, receipt-ocr-intake |
| https://github.com/grailautomation/claude-plugins (finance/reconciliation, journal-entry, journal-entry-prep) | No LICENSE file | link-only, never copied | none |
| Satva in-house `accounting-agent-skills/skills` (accounting-fundamentals, ar-ap-aging) | Satva-original | Ideas adapted (three-way match methods, aging netting caveat); product tool names removed | ap-three-way-match, ar-aging-analysis |
