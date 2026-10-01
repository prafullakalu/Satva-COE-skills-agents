# Sources: platform-xero

All skills in `skills/accounting/platforms/xero/` are Satva-original. No third-party skill content was copied or adapted.

| Source | Licence (as read) | Verdict | Fed which skills |
|---|---|---|---|
| Satva `xero-mcp-server` source (`src/tools/**`, `src/helpers/xero-rate-limit.ts`, `src/consts/tool-scopes.ts`, `src/helpers/format-error.ts`, `TOOLS.md`), local clone, tool names and parameters read from code | Satva-owned (internal; fork of XeroAPI/xero-mcp-server, MIT) | ground truth for tool names, parameters, statuses and guard rails; no text copied | all |
| Satva `accounting-agent-skills/skills/live-ledger-ops` (local) | Satva-owned | consulted for the read-then-confirm-then-write pattern; not copied | xero-mcp-operating-rules |
| Xero developer documentation (rate limits 60/min, 5000/day; scopes) | Vendor docs, not reproduced | link-only knowledge: https://developer.xero.com/documentation/guides/oauth2/limits/ | xero-mcp-operating-rules |
| Other public Xero skill repositories | not evaluated (no clone made); skills naming other products' tools are excluded by policy | skipped | none |

Unverified against a live Xero org: Xero UI behaviours cited (merge semantics, period lock setting path, FX
revaluation, bank rule priority, two-category tracking limit). xero-multi-currency is marked beta for this reason.
