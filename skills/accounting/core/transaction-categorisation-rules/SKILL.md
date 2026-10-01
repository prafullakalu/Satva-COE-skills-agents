---
name: transaction-categorisation-rules
description: >-
  Categorise bank and card transactions accurately and build safe, auditable bank rules: rule precedence, split rules, confidence tiers, transfers, owner items and a review queue. Use for "categorise these transactions", "create bank rules", "auto-categorise", "uncategorised items", "miscellaneous is too big", or "why was this coded wrong".
metadata:
  department: "accounting"
  domain: "transaction-capture"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Transaction categorisation and bank rules

Categorisation is a judgement about economic substance, not about the payee's name. A rule is a standing judgement applied to future money, so it needs the same care as a journal.

## 1. Order of evaluation

For each uncategorised transaction, test in this order and stop at the first that applies:

1. **Transfer between own accounts** (matching opposite leg in another own account within a few days): post as a transfer.
2. **Matches an open bill or invoice** (amount and counterparty): record as a payment or receipt against it, not as a new expense or income.
3. **Processor or marketplace payout**: clear against processor clearing, see `bank-feed-import-and-capture`.
4. **Loan, tax, payroll, owner or capital movement**: balance-sheet accounts, never expense or revenue.
5. **Ordinary income or expense**: categorise from description, amount pattern and history for that counterparty.

## 2. Substance traps

| Looks like | Usually is |
|---|---|
| Payment to tax authority | Liability settlement (sales tax, payroll tax) or income tax, not expense, except penalties and interest |
| Loan repayment | Split principal (liability) and interest (expense) |
| Credit card payment | Transfer to the card liability |
| Cash withdrawal | Owner draw, petty cash or an expense: ask |
| Large round-sum deposit | Loan, owner contribution, customer deposit (liability) or revenue: ask |
| Annual software or insurance | Prepaid asset amortised over the term, see `accruals-deferrals-prepaids` |
| Equipment purchase | Fixed asset above the capitalisation threshold |
| Refund from supplier | Reduces the original expense, not income |
| Payment to a contractor | Expense plus 1099 or equivalent data, see `vendor-setup-and-1099-data` |

## 3. Confidence tiers

- **High** (repeat counterparty, one historical account, consistent amount range): propose and allow bulk confirmation.
- **Medium** (known counterparty, multiple historical accounts, or unusual amount): propose with reason, one-by-one confirm.
- **Low or unknown**: leave in the review queue with a question. Do not guess to empty the queue. A suspense balance with honest questions is better than a clean-looking wrong ledger.

## 4. Writing rules

A good rule has: an explicit condition, one outcome, a name, an owner and a review date.

- Match on stable text (normalised payee or bank memo) and, where needed, direction and an amount band. Avoid single-word matches ("AMAZON" can be inventory, software, office, or personal).
- One counterparty, multiple natures: use separate rules by amount band or memo pattern, or no rule.
- **Split rules** only for fixed patterns (for example monthly invoice: 80 percent hosting, 20 percent support). Remainder lines must sum to the whole.
- Precedence: most specific first; the first matching rule wins; keep a catch-all only to route to review, never to a real expense account.
- Rules never create transfers or tax postings by themselves; those need matching logic.
- Test a new rule against the last 12 months of history in preview. A rule that would have changed more than a handful of already-correct lines is too broad.
- Rules fire on new transactions only; do not silently recode reconciled or locked-period history.

## 5. Rule hygiene

Quarterly: list rules by hit count and last-hit date; retire dead rules; check the review-queue rate (target under a few percent of lines needing manual coding after the first quarter); sample 20 auto-coded lines and verify against documents. Record every rule creation or change with date and approver.

## 6. Mixed personal and business

Where the entity cannot be cleanly separated, do not infer. Code to owner's drawings or an owner receivable pending a decision, and recommend a dedicated business account and card.

## Output

For a batch: transaction, proposed account, tax code, tier, reason, rule hit (if any), question (if unresolved). For rules: condition, outcome, preview impact, owner.

## Do not

- Post to "miscellaneous" or "ask my accountant" as a permanent home.
- Create a rule from one example.
- Let a rule override a match to an open bill.
- Recode locked or reconciled periods; use a reclass journal.
