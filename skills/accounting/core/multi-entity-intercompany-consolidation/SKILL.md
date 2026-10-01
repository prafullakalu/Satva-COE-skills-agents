---
name: multi-entity-intercompany-consolidation
description: >-
  Multi-entity accounting: intercompany transactions and balances, matching and elimination, currency translation, consolidation workflow and cost allocations across entities. Use for "intercompany reconciliation", "consolidate these entities", "eliminate intercompany", "translate subsidiary to USD", "allocate shared costs between entities", "intercompany loan".
metadata:
  department: "accounting"
  domain: "multi-entity"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Multi-entity, intercompany and consolidation

## Entity set-up checklist
Per entity: legal name, jurisdiction, functional currency, fiscal year-end, ownership %, chart of accounts mapped to the group chart, intercompany accounts (one receivable and one payable per counterparty), tax registration. Keep each entity's books separate; combine only in consolidation.

## Intercompany transaction types
Management fees and cost recharges, goods sales (inventory in transit), loans and interest, cash pooling/sweeps, expense paid on behalf, dividends, capital contributions.

Rules:
1. Both entities record the same transaction on the same date, same currency, same amount (invoice-currency basis), with a shared reference number.
2. Use dedicated intercompany accounts; never run intercompany through trade AR/AP or revenue-only accounts that cannot be eliminated.
3. Transfer pricing: charges priced at arm's length with documented method. Flag to tax advisers; policy owner is tax/legal.

## Intercompany matching (every month)
For each pair: Entity A receivable from B (in A's functional currency) vs B payable to A (translated). Differences come from: timing (in-transit invoice or cash), FX, one-sided entries, wrong counterparty, different dates. Process: matrix of pairs, difference column, resolution owner. Tolerance: zero before elimination (or immaterial FX rounding with documented policy). Settle or accrue the other side; never eliminate with a plug beyond FX.

## Consolidation workflow
1. Close each entity (month-end-close); lock.
2. Map subsidiary TB to group chart; confirm TBs balance.
3. **Translate** foreign-currency entities (IAS 21 / ASC 830 pattern): assets and liabilities at closing rate; income and expenses at average rate for the period (or transaction-date rates); equity at historical rates; translation difference to Other Comprehensive Income (cumulative translation adjustment). Remeasure monetary items in a currency other than functional through P&L first.
4. **Aggregate** all entities line by line.
5. **Eliminate:**
   - Intercompany receivable/payable balances.
   - Intercompany revenue and expense (sales vs purchases, fees, interest).
   - Unrealised profit in inventory: unsold intercompany goods x seller's margin %. Entry: Dr COGS (or consolidated reserve) / Cr Inventory.
   - Investment in subsidiary against subsidiary equity: difference goes to goodwill (purchase consideration + non-controlling interest - fair value of net assets) or a gain on bargain purchase.
   - Intercompany dividends against dividend income.
6. **Non-controlling interest:** NCI % x subsidiary net assets (and its share of profit) shown separately in equity and P&L.
7. Checks: consolidated TB balances; intercompany accounts net to zero; consolidated cash agrees to the sum of entity cash; CTA roll-forward (opening + movement = closing); consolidated equity = parent equity + post-acquisition reserves + NCI.
8. Produce consolidated statements (financial-statement-preparation) plus entity-level bridge (entity contribution to revenue, EBITDA, net income).

## Cost allocations
Define pools (shared payroll, IT, rent) and drivers (headcount, revenue, square metres, usage); allocation = pool x entity driver / total driver; document the method annually; post as intercompany charges so they eliminate. Re-run when drivers change; do not re-allocate retrospectively without approval.

## Common failures
Intercompany loans in different currencies revalued on one side only; sale recognised by seller in March and received in inventory in April; cash sweeps recorded as revenue; elimination journals not reversed and re-posted monthly; changing the account mapping mid-year without restating comparatives; one-off consolidations in spreadsheets that are not repeatable (keep a locked elimination template).

## Do not
Do not net intercompany balances against third-party balances; do not eliminate a difference you have not understood; do not consolidate entities the group does not control without evaluating (equity method, joint arrangements).

## Output
Intercompany matrix, elimination journals with support, translation workings and rates used (source and date), consolidated TB/statements, list of unresolved differences.

See also: `intercompany-tie-out` (overlapping topic; this skill covers its own scope, that one covers the other side).
