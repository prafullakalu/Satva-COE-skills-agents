---
name: receipt-ocr-intake
description: >-
  Turn receipts, invoices and expense documents (photos, PDFs, email attachments) into validated, reviewable ledger entries using OCR extraction with confidence checks. Use for "process these receipts", "scan invoices", "OCR a bill", "expense receipts to bookkeeping", "attach receipt to transaction", or "missing receipt".
metadata:
  department: "accounting"
  domain: "transaction-capture"
  owner: "satva-coe"
  status: "beta"
  license: "Satva-original"
  source: "original"
---

# Receipt and document OCR intake

Extraction is a proposal. A document becomes a ledger entry only after the arithmetic ties and a person has confirmed anything low-confidence. The source image or PDF stays attached to the entry as audit evidence.

## 1. Classify the document first

Receipt (already paid), supplier invoice (payable), credit note, statement (not a bill; reconcile against it, do not post it), quote or purchase order (not an expense), duplicate or unreadable. Posting a statement or a quote as an expense is the most common intake error.

## 2. Extract these fields

| Field | Rule |
|---|---|
| Supplier legal name | As printed; map to an existing vendor, do not create near-duplicates |
| Supplier tax ID | Capture when printed; required for input tax claims in most regimes |
| Document number | Needed for duplicate detection |
| Document date and due date | Document date drives the period; ISO format |
| Currency | Never assume; symbols are ambiguous ($, kr, Rs) |
| Line items: description, quantity, unit price, line total | Needed for split coding |
| Subtotal, each tax amount and rate, total | See validation |
| Payment method and last four digits | Helps match the card or bank line |

## 3. Validate before proposing an entry

1. Sum of lines equals subtotal; subtotal plus tax equals total (tolerance: rounding of a few cents; beyond that, re-read).
2. Tax rate times taxable base is consistent with the printed tax within rounding. If tax is printed but no rate, derive and flag it.
3. Date is plausible: not in the future, not outside the open period without an explicit note, not older than the retention rule allows claiming.
4. Currency matches the supplier's norm or is explicitly foreign; foreign amounts need the rate and its source.
5. Duplicate check: same supplier, document number and total (or same supplier, date and total when no number) against posted and pending items.
6. Handwritten or blurred totals, crumpled thermal prints, mixed-language documents: lower confidence, always route to human review.

Confidence rule: any field below the confidence the team has agreed (default: treat anything the extractor flags uncertain, and every amount on a handwritten document, as unconfirmed) is shown to the reviewer next to the cropped region of the image.

## 4. Code the entry

- Choose the expense account from the line description, not the supplier name (an office-supplies store may sell furniture, a capital item).
- Split mixed receipts (groceries and office supplies, hotel room and meals) line by line. Non-deductible or partly deductible items (client entertainment, personal items) get separate lines so tax treatment is clean.
- Capital threshold: items above the client's capitalisation policy go to a fixed asset or prepaid review, not expense.
- Tip, shipping and service charges follow the item they relate to, or a stated default.
- Personal purchase on a business card: owner receivable or drawings, not an expense.

## 5. Match, then post

Preferred order: match the document to the bank or card line that already exists (so cash is not double-counted) and attach it; otherwise create a draft bill or expense claim. Posted entries link to the document ID. Nothing is auto-posted; the batch is shown for confirmation first.

## 6. Missing and late documents

Keep a missing-document list per month: bank lines over the client's threshold with no attachment. Request them in one batched message, state the amount and date, and do not invent supporting detail. For lost receipts, use the client's declaration process where the jurisdiction allows it, and keep it separate from real receipts.

## 7. Privacy and retention

Receipts carry card digits, names and addresses. Store them in the client's document system with access control, mask card numbers in notes, and follow the retention period set at onboarding.

## Output

A table per batch: document ID, supplier, date, currency, subtotal, tax, total, proposed account, confidence flags, duplicate result, match target. Then the list of items needing a human decision.

## Do not

- Post a document whose lines do not sum to the total.
- Create a vendor for every spelling variant.
- Trust OCR digits on a handwritten amount.
- Treat a statement or order confirmation as an invoice.
- Delete the source file after posting.
