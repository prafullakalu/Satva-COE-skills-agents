---
name: shopify-mcp-operating-rules
description: >-
  Operating rules for the Satva read-only Shopify MCP (SyncTools, 33 GraphQL query tools): the three guard rails,
  which accounting data it can and cannot return (no payouts, balance transactions, fees, gift-card or store-credit
  balances), truncated nested lists, cursor paging, per-shop rate limits, multi-store targeting and the 60-day order
  window. Load first for any Shopify accounting task. Trigger on "pull Shopify orders", "Shopify MCP", "get-orders
  returns too few", "Shopify rate limit", "can the MCP refund or edit orders", "which Shopify tools can I use".
metadata:
  department: "accounting"
  domain: "ecommerce-operations"
  platform: "shopify"
  owner: "satva-coe"
  status: "stable"
  license: "Satva-original"
  source: "original"
---

# Shopify MCP: operating rules

Verified against the `synctools-shopify-mcp` source (the read-only server). Satva also runs a *read-write* Shopify MCP
(`satva-shopify`) that can edit products, refund and adjust inventory. **These skills use read-only tools only.** If the
connected server exposes write tools, do not call them from any skill in this library; hand the recommendation to a
human.

## 1. Guard rails (enforced in code, not by convention)

1. **No mutations.** Every GraphQL document passes `assertReadOnlyDocument`; a `mutation` or `subscription` throws
   `ReadOnlyViolationError` before leaving the process.
2. **Scope check.** Each tool declares required scopes (`TOOL_SCOPES`); a tool whose scopes the store did not grant is
   refused locally, not sent to Shopify.
3. **GraphQL only**, never the REST Admin API.
Granted scopes: read_products, read_orders, read_draft_orders, read_customers, read_inventory, read_locations,
read_fulfillments, read_merchant_managed_fulfillment_orders, read_assigned_fulfillment_orders, read_returns,
read_discounts, read_markets, read_companies.

## 2. The 33 tools

- Orders: `get-orders`, `get-order-by-id`, `get-order-transactions`, `get-order-refund-details`,
  `get-fulfillment-orders`, `get-draft-orders`, `get-draft-order-by-id`, `get-returns`, `get-return-by-id`
- Catalog and stock: `get-products`, `get-product-by-id`, `get-product-variants-detailed`, `get-inventory-items`,
  `get-inventory-levels`, `get-locations`, `get-collections`, `get-collection-by-id`, `get-price-lists`
- Customers/B2B: `get-customers`, `get-customer-by-id`, `get-customer-orders`, `get-segments`, `get-companies`,
  `get-company-by-id`
- Config: `get-shop-info`, `get-markets`, `get-discounts`, `get-metafields`, `get-metafield-definitions`, `search-shop`
- Stores: `list-stores`, `list-stores-summary`, `set-active-store` (sets only the dashboard default, not store data)

## 3. What it cannot give an accountant (scope list proves it)

- **No payouts, balance transactions or processing fees.** The `read_shopify_payments_*` scopes are not requested,
  and no payout tool exists. Payout reconciliation needs the user's Shopify Payments export (see
  `shopify-payout-reconciliation`).
- **No gift card balances or liabilities, no store-credit accounts.** `get-shop-info` only reports whether the
  gift-card feature is enabled (`features.giftCards`).
- **No order older than 60 days unless the app has `read_all_orders`**, which is not in the scope list. Treat any
  period older than about two months as possibly incomplete on `get-orders` and check against the Shopify admin export
  [Likely: Shopify platform behaviour, confirm on the store].
- Unit cost exists per variant (`get-inventory-items`, `get-product-variants-detailed`: `unitCost`) but is a merchant-
  entered field, not a ledger cost.

## 4. Truncated nested lists: the silent-error trap

Nested connections are capped inside the tool queries. A figure built from them is wrong without any error:

| Tool | Nested cap |
|---|---|
| `get-orders` line items | first 10 lines per order (no cursor for lines) |
| `get-order-by-id` line items | first 20 |
| `get-order-refund-details` | first 25 refunds, 50 refund lines each, 10 transactions each |
| `get-inventory-levels` | first 50 locations |
| `get-inventory-items` | first 100 variants per product |

Rule: if a nested list is at its cap, treat the order or product as **incomplete** and flag it. Header totals
(`totalPriceSet`, `totalTaxSet`, `totalShippingPriceSet`, `subtotalPriceSet`) are complete; line-level sums may not
be. Reconcile line sum to header; a mismatch means truncation or discounts.

## 5. Paging

- `get-orders`, `get-products`, `get-customer-orders`: `limit` (default 10), `after` cursor from `pageInfo.endCursor`,
  `status` (any/open/closed/cancelled), `sortKey`, `reverse`, raw `query` string. Page until `hasNextPage` is false.
  Shopify caps a page at 250.
- Date window via `query`, e.g. `created_at:>=2026-03-01 created_at:<2026-04-01`, combined with
  `financial_status:paid` etc. Quote the exact string you used on the deliverable.
- `get-draft-orders`, `get-discounts`, `get-returns`, `get-segments`, `get-companies`: `first` (1 to 50, default 20)
  and `after`.
- `get-order-by-id` accepts a GID, a long numeric id, or a short number or `#name`, which is resolved by name search.

## 6. Rate limits and throttling

- Per shop: at most 2 concurrent calls and 30 requests per minute by default (the MCP shares the Partner app's API
  bucket with the SyncTools product). When the per-minute window is exhausted the call is refused with a
  `ShopRateLimitError`; wait and repeat. A refused call is not an empty result.
- Shopify `THROTTLED` responses are retried automatically after 1s, 2s and 4s; beyond that the error surfaces.
- Budget: at 30 calls per minute, a per-order loop over 2,000 orders is over an hour. Prefer `get-orders` pages (many
  orders per call) and fetch `get-order-transactions` / `get-order-refund-details` only for the orders that need it.

## 7. Stores and money

- Every tool takes an optional `store` (domain or name). Call `list-stores` first; with several stores, always pass
  `store` explicitly and put the store name on every output.
- Order amounts are requested as `shopMoney` (the store's currency) and sometimes also `presentmentMoney` (customer
  currency). Reconcile in `shopMoney`; a multi-currency store has one shop currency (`get-shop-info.currencyCode`).
- `get-shop-info`: `taxesIncluded`, `taxShipping`, `ianaTimezone`, `enabledPresentmentCurrencies`, `plan`.

## 8. Data protection

Orders and customers expose names, emails, phones and addresses (protected customer data). Keep them out of outputs:
use order names and ids. Never paste a customer's details into a deliverable or ticket unless the task needs it.

## Do not

- Do not total line items from a capped list.
- Do not call a missing payout tool "no payouts"; say the MCP cannot see payouts.
- Do not run the per-order tools in a large unthrottled loop.
