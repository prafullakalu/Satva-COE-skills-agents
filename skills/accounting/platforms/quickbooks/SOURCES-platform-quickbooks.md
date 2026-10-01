# Sources: platform-quickbooks

All skills in `skills/accounting/platforms/quickbooks/` are Satva-original. Nothing third-party was copied or adapted.

| Source | Licence (as read) | Verdict | Fed which skills |
|---|---|---|---|
| Satva QuickBooks Online MCP server, local clone `mcp/accounting/quickbooks-online-mcp-server` (src/tools, src/helpers, src/server, docs/TOOL-GAP-ANALYSIS.md) | Satva-owned code (repo LICENSE not relied on; behaviour read, nothing copied) | read for ground truth: tool names, parameters, read/write split, entity catalog, error formatting | all |
| Satva `accounting-agent-skills` repo: `skills/live-ledger-ops`, `marketing/proof-of-run/REPORT.md` | Satva-owned | read for house conventions (read-first, confirm, echo ids) | qbo-mcp-operating-rules |
| Intuit QuickBooks Online Accounting API documentation (entities, reports, batch, CDC, minor versions) | Intuit terms; not copied | link-only knowledge; facts restated in own words where the server source confirmed them | all |
| Composio `qbo_accounting_*` style skills | not evaluated for copying: they name another product's tools (brief rule) | link-only, excluded | none |
| Satva `accounting/core/month-end-close` (sibling skill in this repo) | Satva-original | referenced, not copied | qbo-month-end-close |
