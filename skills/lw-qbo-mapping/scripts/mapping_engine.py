"""
Deterministic mapping engine: SourceRecord + TargetRecord[] -> MappingResult.

Steps 1-7 of reference/confidence-model.md are implemented here, deterministically, no LLM calls.
Step 8 (LLM semantic reasoning) is NOT implemented here on purpose — spec #18 says the LLM is used
for semantic reasoning, not folded into a deterministic helper script. The calling skill invokes
the LLM only when propose_mapping() returns confidence=UNRESOLVED and entity_type has enough source
information to plausibly be mapped (i.e. not a STRUCTURAL_DATA_GAP) — then calls
apply_llm_proposal() below to fold the LLM's answer back in, always at review_required=True.
"""
from __future__ import annotations
import re
from dataclasses import dataclass, field
from typing import Optional
from normalize import SourceRecord, TargetRecord

# entity_type -> accounting concept -> compatible QBO account_type(s).
# This is the ecommerce-dimension -> accounting-concept translation coa-mapper-mcp does not have.
CONCEPT_RULES = {
    "channel": {"concept": "sales_income", "account_types": {"Income"}},
    "refund": {"concept": "refund_contra_income", "account_types": {"Income"}},
    "return": {"concept": "refund_contra_income", "account_types": {"Income"}},
    "shipping": {"concept": "shipping_income", "account_types": {"Income"}},
    "tax": {"concept": "sales_tax_liability", "account_types": {"Other Current Liabilities", "Other Current Liability"}},
    "discount": {"concept": "discount_contra_income", "account_types": {"Income"}},
    "cogs": {"concept": "cogs", "account_types": {"Cost of Goods Sold"}},
    "sku": {"concept": "cogs", "account_types": {"Cost of Goods Sold"}},
    "inventory_adjustment": {"concept": "inventory_asset", "account_types": {"Current assets", "Other Current Assets"}},
    "marketplace_fee": {"concept": "marketplace_fee_expense", "account_types": {"Expenses", "Cost of Goods Sold"}},
    "payment_processing_fee": {"concept": "payment_processing_fee_expense", "account_types": {"Expenses", "Cost of Goods Sold"}},
    "purchase_order": {"concept": "supplier_payable", "account_types": {"Accounts payable (A/P)"}},
}

STOPWORDS = {"the", "a", "an", "of", "and", "-", "sales", "income"}


def _tokens(name: str) -> set[str]:
    return {t for t in re.split(r"[^a-z0-9]+", name.lower()) if t and t not in STOPWORDS}


def _concept_for(source: SourceRecord) -> dict:
    return CONCEPT_RULES.get(source.entity_type, {"concept": "undetermined", "account_types": None})


@dataclass
class MappingResult:
    source_id: str
    source_type: str
    source_name: str
    source_value: Optional[float]
    currency: Optional[str]
    target_id: Optional[str]
    target_name: Optional[str]
    target_type: Optional[str]
    status: str
    confidence: str
    evidence: list = field(default_factory=list)
    reason: str = ""
    review_required: bool = True

    def to_row(self) -> dict:
        return {
            "linnworks_source": self.source_name,
            "source_type": self.source_type,
            "qbo_target": self.target_name,
            "target_type": self.target_type,
            "status": self.status,
            "confidence": self.confidence,
            "evidence": "; ".join(self.evidence),
        }


def propose_mapping(
    source: SourceRecord,
    targets: list[TargetRecord],
    explicit_rules: Optional[dict[str, str]] = None,
) -> MappingResult:
    """Run steps 1-6 of the ordered pipeline. explicit_rules maps source_id -> target_id (step 1)."""
    explicit_rules = explicit_rules or {}
    concept = _concept_for(source)
    compatible_types = concept["account_types"]

    def compatible(t: TargetRecord) -> bool:
        return compatible_types is None or t.account_type in compatible_types

    # Step 1: explicit rule
    if source.source_id in explicit_rules:
        tid = explicit_rules[source.source_id]
        target = next((t for t in targets if t.target_id == tid), None)
        if target is None:
            return _unresolved(source, "explicit rule points at a target_id that no longer exists")
        if not target.active:
            return _result(source, target, "INACTIVE", "HIGH",
                            ["explicit rule"], "Explicit mapping rule target is inactive in QBO", True)
        if not compatible(target):
            return _result(source, target, "INVALID", "HIGH",
                            ["explicit rule"], f"Explicit rule target type {target.account_type} incompatible with concept {concept['concept']}", True)
        return _result(source, target, "MAPPED", "HIGH", ["explicit rule"], "Explicit mapping rule", False)

    # Step 2: exact identifier/code match (source_id equals target_id or a target metadata code)
    exact = [t for t in targets if t.target_id == source.source_id or t.name.strip().lower() == source.source_id.strip().lower()]
    if len(exact) == 1:
        t = exact[0]
        status = "MAPPED" if (t.active and compatible(t)) else ("INACTIVE" if not t.active else "INVALID")
        return _result(source, t, status, "HIGH", ["exact identifier match"], "Exact id/name match", status != "MAPPED")

    # Steps 3-5: name/keyword match constrained by account-type compatibility
    src_tokens = _tokens(source.name) | _tokens(source.channel or "")
    candidates = []
    for t in targets:
        if not compatible(t):
            continue
        overlap = src_tokens & _tokens(t.name)
        if overlap:
            candidates.append((t, len(overlap)))
    candidates.sort(key=lambda x: -x[1])

    if candidates:
        best_score = candidates[0][1]
        top = [c for c in candidates if c[1] == best_score]
        if len(top) == 1:
            t = top[0][0]
            conf = "HIGH" if best_score >= 2 else "MEDIUM"
            status = "MAPPED" if t.active else "INACTIVE"
            return _result(source, t, status, conf if status == "MAPPED" else "HIGH",
                            [f"keyword match ({best_score} token(s) overlap)"],
                            f"Name overlap with '{t.name}'", conf != "HIGH" or status != "MAPPED")
        else:
            # Step 4 fallback: type-compatible but no unique winner -> AMBIGUOUS
            names = ", ".join(c[0].name for c in top)
            return MappingResult(
                source_id=source.source_id, source_type=source.entity_type, source_name=source.name,
                source_value=source.amount, currency=source.currency,
                target_id=None, target_name=names, target_type=None,
                status="AMBIGUOUS", confidence="LOW",
                evidence=[f"{len(top)} tied candidates at {best_score} token overlap"],
                reason=f"Multiple equally-plausible targets: {names}", review_required=True,
            )

    # No keyword evidence at all. Account-type compatibility alone is NEVER enough to auto-confirm
    # a mapping (spec #6: don't guess) -- it only tells us how many plausible-but-unevidenced
    # candidates exist, which changes UNMAPPED vs AMBIGUOUS but never produces a MAPPED result here.
    if concept["concept"] == "undetermined":
        return _unresolved(source, "no accounting concept could be derived from this Linnworks dimension without further context")

    type_only = [t for t in targets if compatible(t)]
    if len(type_only) >= 2:
        names = ", ".join(t.name for t in type_only)
        return MappingResult(
            source_id=source.source_id, source_type=source.entity_type, source_name=source.name,
            source_value=source.amount, currency=source.currency,
            target_id=None, target_name=names, target_type=None,
            status="AMBIGUOUS", confidence="LOW",
            evidence=[f"{len(type_only)} type-compatible candidates, no name evidence to break the tie"],
            reason=f"Multiple equally-plausible targets by account type alone: {names}", review_required=True,
        )

    return MappingResult(
        source_id=source.source_id, source_type=source.entity_type, source_name=source.name,
        source_value=source.amount, currency=source.currency,
        target_id=None, target_name=None, target_type=None,
        status="UNMAPPED", confidence="UNRESOLVED",
        evidence=["no QBO target with supporting evidence (identifier, rule, or name overlap) exists"],
        reason=f"No evidenced QBO account/item found for concept '{concept['concept']}'"
               + (f" (compatible type(s) {compatible_types} has only {len(type_only)} candidate, but no name evidence to confirm it)" if type_only else ""),
        review_required=True,
    )


def apply_llm_proposal(source: SourceRecord, target: TargetRecord, llm_reason: str) -> MappingResult:
    """Fold an LLM semantic-reasoning proposal (pipeline step 8) into a MappingResult.
    Always review_required=True, confidence capped at MEDIUM per spec #6 — an LLM guess never
    becomes a confirmed HIGH mapping automatically.
    """
    status = "MAPPED" if target.active else "INACTIVE"
    return _result(source, target, status, "MEDIUM", ["LLM semantic reasoning"], llm_reason, True)


def find_orphaned_targets(targets: list[TargetRecord], results: list[MappingResult]) -> list[MappingResult]:
    """Any active QBO target never chosen as a MappingResult.target_id is ORPHANED (spec #4E)."""
    used = {r.target_id for r in results if r.target_id}
    out = []
    for t in targets:
        if t.target_id not in used and t.active:
            out.append(MappingResult(
                source_id="", source_type="", source_name="(no Linnworks source)",
                source_value=None, currency=None,
                target_id=t.target_id, target_name=t.name, target_type=t.account_type,
                status="ORPHANED", confidence="HIGH",
                evidence=["no MappingResult ever selected this target"],
                reason="QBO account/item with no corresponding Linnworks source dimension",
                review_required=True,
            ))
    return out


def _result(source, target, status, confidence, evidence, reason, review_required) -> MappingResult:
    return MappingResult(
        source_id=source.source_id, source_type=source.entity_type, source_name=source.name,
        source_value=source.amount, currency=source.currency,
        target_id=target.target_id, target_name=target.name, target_type=target.account_type,
        status=status, confidence=confidence, evidence=evidence, reason=reason,
        review_required=review_required,
    )


def _unresolved(source, reason) -> MappingResult:
    return MappingResult(
        source_id=source.source_id, source_type=source.entity_type, source_name=source.name,
        source_value=source.amount, currency=source.currency,
        target_id=None, target_name=None, target_type=None,
        status="UNMAPPED", confidence="UNRESOLVED", evidence=["ordered pipeline exhausted"],
        reason=reason, review_required=True,
    )


# ---------------------------------------------------------------------------
# Product / SKU identity matching (Linnworks StockItem <-> QBO Item)
#
# This is a DIFFERENT matching problem from propose_mapping() above: propose_mapping() maps an
# ecommerce dimension to an accounting-concept-compatible ACCOUNT (channel -> Income account,
# refund -> contra-income account, etc). match_product_identity() instead asks "does this
# Linnworks product exist, correctly, as a QBO Item?" -- product master-data reconciliation.
#
# Priority order per user request: SKU first (strongest signal, near-zero false-positive rate),
# then name similarity, then price/qty as CORROBORATION (never the primary signal -- two unrelated
# products can share a price by coincidence, so price/qty alone never promotes a match to MAPPED).
# ---------------------------------------------------------------------------

PRICE_TOLERANCE_PCT = 5.0  # price within this % is treated as corroborating evidence, not proof


def _price_close(a: Optional[float], b: Optional[float], tolerance_pct: float = PRICE_TOLERANCE_PCT) -> bool:
    if a is None or b is None:
        return False
    base = max(abs(a), abs(b))
    if base == 0:
        return a == b
    return abs(a - b) / base * 100 <= tolerance_pct


def match_product_identity(
    source: SourceRecord,
    targets: list[TargetRecord],
    price_tolerance_pct: float = PRICE_TOLERANCE_PCT,
) -> MappingResult:
    """SKU -> name -> price/qty, in that order. targets should be entity_type == 'item'.

    Returns status in {MAPPED, UNVERIFIED, AMBIGUOUS, INACTIVE, UNMAPPED}. UNVERIFIED is distinct
    from both AMBIGUOUS (multiple tied candidates) and UNMAPPED (no candidate at all): it means
    exactly one plausible candidate exists but the evidence isn't strong enough to confirm it
    without human review (see reference/gap-taxonomy.md).
    """
    items = [t for t in targets if t.entity_type == "item"]

    # Priority 1: SKU exact match (case-insensitive)
    if source.sku:
        sku_matches = [t for t in items if t.sku and t.sku.strip().lower() == source.sku.strip().lower()]
        if len(sku_matches) == 1:
            t = sku_matches[0]
            status = "MAPPED" if t.active else "INACTIVE"
            return _product_result(source, t, status, "HIGH", ["SKU exact match"],
                                    f"SKU '{source.sku}' matches QBO item '{t.name}' exactly",
                                    status != "MAPPED")
        if len(sku_matches) > 1:
            names = ", ".join(t.name for t in sku_matches)
            return _product_result(source, None, "AMBIGUOUS", "LOW",
                                    [f"{len(sku_matches)} QBO items share SKU '{source.sku}'"],
                                    f"Duplicate SKU in QBO item list: {names}", True, target_name=names)

    # Priority 2: name similarity (token overlap), constrained to item-type targets
    src_tokens = _tokens(source.name)
    candidates = []
    for t in items:
        overlap = src_tokens & _tokens(t.name)
        if overlap:
            candidates.append((t, len(overlap)))
    candidates.sort(key=lambda x: -x[1])

    if not candidates:
        if items:
            return _product_result(source, None, "UNMAPPED", "UNRESOLVED",
                                    ["no SKU match, no name overlap with any QBO item"],
                                    "No corresponding QBO item found by SKU or name", True)
        return _product_result(source, None, "UNMAPPED", "UNRESOLVED",
                                ["no QBO items available to match against"],
                                "No QBO items in scope", True)

    best_score = candidates[0][1]
    top = [c for c in candidates if c[1] == best_score]

    # Priority 3: price/qty corroborates a name match, or breaks a name-overlap tie.
    # Price/qty NEVER promotes a match on its own -- it only corroborates or disambiguates a
    # name-overlap candidate that already exists.
    corroborated = [c for c in top if _price_close(source.amount, c[0].unit_price, price_tolerance_pct)]

    if len(top) == 1:
        t = top[0][0]
        if corroborated:
            status = "MAPPED" if t.active else "INACTIVE"
            return _product_result(source, t, status, "MEDIUM",
                                    [f"name overlap ({best_score} token(s))", "price corroborated within tolerance"],
                                    f"Name match '{t.name}' corroborated by price", status != "MAPPED")
        return _product_result(source, t, "UNVERIFIED", "LOW",
                                [f"name overlap ({best_score} token(s)) only, price not corroborated"],
                                f"Name overlap with '{t.name}' but price/qty could not confirm it", True)

    if len(corroborated) == 1:
        t = corroborated[0][0]
        status = "MAPPED" if t.active else "INACTIVE"
        return _product_result(source, t, status, "MEDIUM",
                                [f"{len(top)} tied name candidates, price corroboration broke the tie"],
                                f"Price corroboration selected '{t.name}' among {len(top)} name-tied candidates",
                                status != "MAPPED")

    names = ", ".join(c[0].name for c in top)
    return _product_result(source, None, "AMBIGUOUS", "LOW",
                            [f"{len(top)} tied name candidates, price did not break the tie"],
                            f"Multiple equally-plausible product matches: {names}", True, target_name=names)


def _product_result(source, target, status, confidence, evidence, reason, review_required, target_name=None) -> MappingResult:
    return MappingResult(
        source_id=source.source_id, source_type=source.entity_type, source_name=source.name,
        source_value=source.amount, currency=source.currency,
        target_id=(target.target_id if target else None),
        target_name=(target.name if target else target_name),
        target_type=(target.entity_type if target else None),
        status=status, confidence=confidence, evidence=evidence, reason=reason,
        review_required=review_required,
    )


def find_orphaned_products(targets: list[TargetRecord], results: list[MappingResult]) -> list[MappingResult]:
    """Active QBO items never selected by any product-identity MappingResult -> ORPHANED."""
    items = [t for t in targets if t.entity_type == "item"]
    used = {r.target_id for r in results if r.target_id}
    out = []
    for t in items:
        if t.target_id not in used and t.active:
            out.append(_product_result(
                SourceRecord(source_system="linnworks", entity_type="sku", source_id="", name="(no Linnworks source)"),
                t, "ORPHANED", "HIGH", ["no MappingResult ever selected this QBO item"],
                "QBO item with no corresponding Linnworks SKU", True,
            ))
    return out
