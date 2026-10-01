<!-- Adapted from anthropics/knowledge-work-plugins small-business/skills/invoice-chase/reference/tone-matching.md (Apache-2.0). Modified by Satva: ledger-neutral wording. -->
# Tone matching

Scoring logic and tone guidelines for overdue-invoice reminders.

## Scoring

Score each customer from the ledger's payment history for the last 12 months. Require at least 3 invoices to score; fewer than 3 defaults to `occasionally-late`.

| Score | Criteria |
|---|---|
| `good-payer` | Paid on time or early in 75 percent or more of invoices |
| `occasionally-late` | Paid late in 25 to 50 percent of invoices, or fewer than 3 invoices on record |
| `repeat-late` | Paid late in more than 50 percent of invoices |

"On time" means payment received on or before the invoice due date. Use the payment date, not the date it was recorded.

## Tone by score

| Score | Tone | Character |
|---|---|---|
| `good-payer` | Gentle | Friendly, assumes oversight. Opens with grace. |
| `occasionally-late` | Neutral | Professional, no judgment. Factual follow-up. |
| `repeat-late` | Firm | Direct, states a deadline. No warmth, no accusation. |

Score sets the starting tone. Days overdue and the escalation ladder in SKILL.md can raise it: a good payer 60 days late is no longer a gentle case, and a broken promise to pay raises the tone one level and cites the promise and its date.

## Subject lines

- Gentle: `Quick reminder: Invoice #[N] for [amount]`
- Neutral: `Following up: Invoice #[N] - [amount] past due`
- Firm: `Past due notice: Invoice #[N] - [amount] ([X] days overdue)`

## Body structure (all tones)

Every reminder includes invoice number(s), total amount due, original due date, days overdue, and how to pay (link or remittance details).

Tone-specific additions:
- **Gentle**: one acknowledgment sentence ("I know things get busy")
- **Neutral**: none, facts only
- **Firm**: one deadline sentence ("Please remit by [date]")

One call to action per email, never two. Under about 120 words up to the firm level.

## Consolidation rule

A customer with several overdue invoices gets one email: list each invoice (number, amount, due date), then the combined total. Use the customer's score, not the most overdue invoice's score.
