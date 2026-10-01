# agents/

Claude Code subagents, grouped by department. Each file is a role: when to use it, which skills it leans on
(`skills:` in its frontmatter), how it works, and its rules. The generated [`CATALOG.md`](../CATALOG.md) lists every
agent beside the skills it uses.

**Which one do I use?** Start from the job.

| The job | Agent |
|---|---|
| Reconcile, categorise, process bills, chase invoices | `accounting-bookkeeper` |
| Close the month, explain variances, board pack, controls, audit support | `accounting-controller` |
| VAT / sales tax workings, 1099s, estimated tax, payroll reconciliation | `accounting-tax-support` |
| Set up a new client's books | `client-onboarding-accountant` |
| Non-US tax and payroll (India, Australia, Canada, UK, Ireland, Sweden, UAE, Israel, EU) | `international-tax-specialist` |
| Budget, forecast, runway, scenarios, treasury, fundraising readiness | `cfo-advisor` |
| Valuation, comps, LBO, M&A, quality of earnings, diligence lists | `deal-valuation-analyst` |
| The client's industry changes the accounting (SaaS, nonprofit, construction, real estate, ...) | `industry-accountant` |
| Run an accounting firm: engagement letters, onboarding SOPs, SOP audits | `accounting-practice-manager` |
| The system is QuickBooks / Xero / Zoho Books / Stripe | `quickbooks-specialist` · `xero-specialist` · `zoho-books-specialist` · `stripe-reconciliation-analyst` |
| Linnworks and Shopify: orders, payouts, stock vs ledger, marketplace posting | `ecommerce-accountant` |
| Positioning, ICP, competitors, launch plan, pricing | `marketing-strategist` |
| Write or edit content | `content-writer` |
| Email, ads, landing pages, tests, attribution | `growth-marketer` |
| Launch video | `launch-video-producer` |
| Audit a site, traffic drop, migration | `seo-technical-auditor` |
| Plan or improve search content, authority, AI-search visibility | `seo-content-strategist` |
| Satva-branded doc, guide or deck | `satva-document-producer` |

## Install

```sh
./install.sh --agents                    # skills + agents
./install.sh --agents --dept accounting  # one department
```

`.\install.ps1 -Agents -Dept accounting` on Windows. Agents go to `~/.claude/agents`.

## Adding an agent

1. Create `agents/<department>/<name>.md`; the file name must equal `name`.
2. Frontmatter: `name`, `description` (say when to use it), and `skills:` (comma-separated names that exist under `skills/`).
3. Anything that writes, sends or deletes must be draft-then-approve. Say so in the agent's rules.
4. Run `python scripts/validate.py --catalog`. CI fails on an unknown skill name or a stale catalog.
