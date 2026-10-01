---
name: ap-three-way-match
description: >-
  Match supplier invoices to purchase orders and goods receipts (two-way and three-way match), apply price and quantity tolerances, and resolve exceptions and goods-received-not-invoiced accruals. Use for "three-way match", "PO does not match invoice", "price variance", "quantity variance", "invoice received without receipt", "GRNI", or "match bills to POs".
metadata:
  department: "accounting"
  domain: "ap-ar"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# AP three-way match

The match proves three independent facts agree: the business ordered it (purchase order), the business received it (goods receipt or service acceptance), and the supplier billed for it (invoice). Pay only what all three support.

## 1. When to use which match

| Match | Documents | Use for |
|---|---|---|
| Two-way | Invoice and PO | Services and low-risk purchases where a receipt is not practical |
| Three-way | Invoice, PO, goods receipt | Stock and physical goods, high-value items |
| Four-way | plus inspection or quality acceptance | Regulated, project or specification-critical goods |
| No PO | Invoice and approval only | Utilities, rent, subscriptions under a contract, small recurring |

Set the policy per category and threshold, then enforce it. A no-PO exception list reviewed monthly stops PO circumvention.

## 2. Procedure

For each invoice line, compare:

| Test | Compare | Formula |
|---|---|---|
| Item | Description or SKU on invoice vs PO line | Same item |
| Quantity | Invoiced vs received (not vs ordered) | Invoice qty <= cumulative received qty not yet billed |
| Price | Invoice unit price vs PO unit price | |invoice - PO| / PO within tolerance |
| Extension | qty x price | Arithmetic ties |
| Tax and charges | Freight, duties, surcharges | Authorised on PO or contract |
| Totals | Invoice total vs PO remaining open value | Not over-billing the PO |

Tolerances (set per client and category, record them): for example price within 2 percent or a small absolute amount, quantity within 0 for high-value items, and a larger band for bulk goods. An item inside tolerance posts and the variance goes to the purchase price variance (or the expense) account; outside tolerance it holds.

## 3. Exception handling

| Exception | Meaning | Action |
|---|---|---|
| Invoice before receipt | Goods not received or receipt not logged | Hold; ask receiving; do not pay |
| Quantity over received | Over-billing or short delivery | Pay received quantity if the vendor permits partials, else hold; request credit or delivery |
| Price above PO | Price change not authorised | Buyer confirms; amend PO with approval or request a credit note |
| No PO | Unauthorised purchase | Route to budget owner for retrospective approval and log as a control exception |
| Partial deliveries | Several receipts and invoices on one PO | Track cumulative received and cumulative invoiced per line |
| Duplicate invoice | Same supplier and number | Block |
| PO closed or expired | Over-delivery or late billing | Reopen only with approval |

Each exception has an owner (buyer, receiver, AP) and a target resolution date; ageing is reported.

## 4. Goods received not invoiced

At period end, receipts without a matched invoice are a liability that must be accrued:

```
Dr Inventory or expense        (received qty x PO price)
  Cr GRNI (accrued liabilities)
```

Reverse on day one; the matched invoice then posts normally. The GRNI account is reconciled to the open-receipts report (`subledger-to-gl-reconciliation`), and old items (over 60 to 90 days) are investigated: wrong receipt, vendor never billed, return not recorded.

## 5. Variances in stock accounts

Under standard costing, price variance goes to a variance account; under actual costing it adjusts inventory cost. Choose per client and keep consistent. Inventory costing mechanics are outside this skill; this tracks the AP side.

## 6. Controls

The buyer, the receiver and the AP processor are different people for material purchases. Receipt is entered by whoever physically receives, not by purchasing. Changes to PO price or quantity after issue need approval and a version trail. Matching overrides are logged with reason and approver.

## Output

Match worksheet per invoice (PO, receipt, invoice, variances, result), exception list with owner and age, GRNI listing and proposed accrual journal in draft.

## Do not

- Pay on the invoice alone when the policy requires a receipt.
- Widen tolerances to clear a backlog.
- Let AP edit PO prices to make a match pass.
- Leave GRNI items indefinitely.
