# Sources: platform-ecommerce (Linnworks and Shopify skills)

No third-party content was copied or adapted. All skills are Satva-original. Tool names, parameters and guard rails
were read from Satva-owned MCP server source code (internal; not redistributed).

| Source | Licence read | Verdict | Fed |
|---|---|---|---|
| Satva Linnworks read-only MCP, `linnworks_ro` (internal: tools/, services/, security/validator.py, client/connection.py, schema/registry.json, TOOLS.md) | Satva-owned, internal | reference only (facts, no text copied) | all `linnworks-*` skills, `ecommerce-multichannel-month-end` |
| Satva SyncTools read-only Shopify MCP (internal: src/tools, src/lib/read-only-guard.ts, shopify-scopes.ts, shop-rate-limit.ts, throttle-retry.ts; package.json declares MIT) | Satva-owned, internal | reference only | all `shopify-*` skills |
| Satva Shopify MCP catalog entry (internal: mcp-catalog/satva-shopify.yaml) | Satva-owned, internal | reference only (confirms the read-write server exists) | `shopify-mcp-operating-rules` |
| Existing client skill `lw-qbo-mapping` (this repo) | Satva-original | cross-referenced by name, never modified | `linnworks-to-ledger-posting-rules`, gap framing in `linnworks-channel-fees-and-refunds` |
| Shopify, Amazon, eBay public documentation | not consulted for copying | link-only, none used | platform behaviours not verifiable in code are tagged [Likely] in the skills |
