# Sources: satva-house

All content below is Satva-written (`Satva-original`); no third-party licences involved.
Every item was sanitised for a public repo before inclusion.

| Source (internal location) | Verdict | Fed skill | Sanitising notes |
|---|---|---|---|
| `satva-ppt` skill (personal skills folder) | adapted | `presentations/satva-ppt` | Copied the 4 helper scripts (python and PowerShell); dropped the Session-3 build script, in-place-update sample, caches and metrics; removed laptop paths and deck file names; template deck must be requested from the CoE (background image is not shipped) |
| `satva-mcp` skill (personal skills folder) | adapted | `engineering/satva-mcp` | Removed Coolify host/IP, project, environment, server and app UUIDs, secrets-file location, internal domains, catalog repo name, commit hashes, dated audit findings and local paths; deploy.md and catalog.md rewritten generically; kept workflow, gates, tenancy tree, read-only patterns, fixing method |
| `satva-mcp-template` (internal repo under the mcp tooling folder) | link-only | referenced by `satva-mcp` | Source tree with dependencies, internal scaffolding and domains; not copied. Skill says to ask the CoE for access |
| `satva-practice` (accounting-agent-skills POC) | adapted | `practice/satva-practice` | Expanded into a standalone skill; removed internal product name and references to sibling POC skills not in this repo |
| `accounting-context-protocol` (accounting-agent-skills POC) | adapted | `practice/accounting-context-protocol` | Made standalone; sibling-skill references replaced with `satva-practice` |

## Evaluated and withheld

| Item | Reason |
|---|---|
| `satva-doc`, `satva-guide-gif`, `feature-launch-video` | already in the repo under `skills/satva` and `skills/marketing` (owned by other work) |
| `grill-me`, `grill-with-docs` | stubs that delegate to external `/grilling` and `/domain-modeling` skills not in the repo; not Satva-original |
| `learned`, `synced` | personal/synced state folders, not skills |
| gstack, hyperframes, ponytail, godmode, graphify, remotion, ios-*, plan-*, etc. | third-party tools |
| Other POC skills in accounting-agent-skills (`live-ledger-ops`, `accounting-domain`, `desk-agent`, `bank-sync`, ...) | outside this assignment; `live-ledger-ops` and `accounting-domain` are referenced by the originals but belong to the accounting owners |


## Withheld by the lead before publishing

- `satva-mcp` (Satva MCP server build/test/deploy/publish): withheld from this public repo. Its `references/tenancy.md` documents Satva's access-control layering, including which layers are configuration-only and a default-off gateway layer. That is internal security architecture; publishing it needs an explicit decision by the CoE owner. Held outside the repo; republish (or a sanitised version) once approved.
