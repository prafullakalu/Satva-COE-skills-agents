# Sources: platform-other (Zoho Books, Stripe)

No third-party text was copied. All skills are Satva-original; the sources below were read for facts only.

| Source | Licence | Verdict | Fed |
|---|---|---|---|
| Zoho Books MCP connector tool schemas (connected in the authoring session): list_invoices, create_invoice, update_invoice, create_customer_payment, list_bank_accounts, list_expenses, create_expense, create_tax, list_contacts, list_chart_of_accounts, get_organization | Vendor connector (not redistributed) | link-only (tool names and field names referenced) | all zoho-books-* |
| Satva internal Zoho MCP research doc (mcp/docs/Zoho-MCP, 2026-09-16): OAuth, organization_id, rate limits, scopes | Satva-owned | original (facts) | zoho-books-operating-rules |
| https://www.zoho.com/books/api/v3/introduction | Vendor docs | link-only | zoho-books-* |
| https://docs.stripe.com/reports/payout-reconciliation | Vendor docs | link-only (facts: report types, columns, caveats) | stripe-payout-fee-reconciliation |
| https://docs.stripe.com/api/balance_transactions/object | Vendor docs | link-only | stripe-payout-fee-reconciliation, stripe-refunds-disputes-accounting |
| https://docs.stripe.com/disputes/how-disputes-work | Vendor docs | link-only (lifecycle, fees, timings) | stripe-refunds-disputes-accounting |
| ~/.claude sat plugin skill zoho-books-integration | Internal | not reused (developer-focused, thin) | none |

Not built (roadmap, no Satva connector and not enough grounded material for two excellent skills each): Sage, NetSuite, FreshBooks, Wave.
