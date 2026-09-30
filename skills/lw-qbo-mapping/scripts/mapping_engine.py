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


def _norm_sku(s: Optional[str]) -> str:
    """case/spacing/punctuation/leading-zero normalization for the 'near SKU' tier."""
    n = re.sub(r"[^a-z0-9]", "", (s or "").lower())
    return (n.lstrip("0") or "0") if n else ""


def _nm(s: Optional[str]) -> str:
    return " ".join((s or "").lower().split())


def _key(t: TargetRecord, sku_key: str) -> Optional[str]:
    return t.name if sku_key == "name" else (t.sku if sku_key == "sku" else None)


@dataclass
class ProductIndex:
    """Prebuilt lookups over item-type targets so match_product_identity is ~O(1) per source."""
    sku_key: str
    items: list
    exact: dict      # lowercased/stripped key -> [targets] (original order)
    near: dict       # _norm_sku(key) -> [targets]
    inverted: dict   # name token -> [item positions] (ascending)


def build_product_index(targets: list[TargetRecord], sku_key: str = "sku") -> ProductIndex:
    items = [t for t in targets if t.entity_type == "item"]
    exact: dict = {}
    near: dict = {}
    inverted: dict = {}
    for pos, t in enumerate(items):
        k = _key(t, sku_key)
        if k and sku_key in ("sku", "name"):
            exact.setdefault(k.strip().lower(), []).append(t)
            n = _norm_sku(k)
            if n:
                near.setdefault(n, []).append(t)
        for tok in _tokens(t.name):
            inverted.setdefault(tok, []).append(pos)
    return ProductIndex(sku_key, items, exact, near, inverted)


def match_product_identity(
    source: SourceRecord,
    targets: list[TargetRecord],
    price_tolerance_pct: float = PRICE_TOLERANCE_PCT,
    sku_key: str = "sku",
    index: Optional[ProductIndex] = None,
) -> MappingResult:
    """SKU (exact, then normalized) -> name -> price/qty, in that order. targets should be item-type.

    sku_key picks the QBO-side identifier compared with the Linnworks SKU: "sku" (QBO Sku field),
    "name" (QBO item Name holds the SKU) or "none" (skip SKU tiers). Use detect_sku_key() to choose.
    Returns status in {MAPPED, UNVERIFIED, AMBIGUOUS, INACTIVE, UNMAPPED}. UNVERIFIED is distinct
    from both AMBIGUOUS (multiple tied candidates) and UNMAPPED (no candidate at all): it means
    exactly one plausible candidate exists but the evidence isn't strong enough to confirm it
    without human review (see reference/gap-taxonomy.md). An exact-name hit with a different SKU
    stays UNVERIFIED but is tagged evidence 'exact_name_sku_differs'.
    """
    if index is None or index.sku_key != sku_key:
        index = build_product_index(targets, sku_key)
    items = index.items
    tag = f"sku_key_source={sku_key}"

    if source.sku and sku_key in ("sku", "name"):
        sku_matches = index.exact.get(source.sku.strip().lower(), [])
        if len(sku_matches) == 1:
            t = sku_matches[0]
            status = "MAPPED" if t.active else "INACTIVE"
            return _product_result(source, t, status, "HIGH", ["SKU exact match", tag],
                                    f"SKU '{source.sku}' matches QBO item '{t.name}' exactly",
                                    status != "MAPPED")
        if len(sku_matches) > 1:
            names = ", ".join(t.name for t in sku_matches)
            return _product_result(source, None, "AMBIGUOUS", "LOW",
                                    [f"{len(sku_matches)} QBO items share SKU '{source.sku}'", tag],
                                    f"Duplicate SKU in QBO item list: {names}", True, target_name=names)
        want = _norm_sku(source.sku)
        near = index.near.get(want, []) if want else []
        if len(near) == 1:
            t = near[0]
            return _product_result(source, t, "MAPPED" if t.active else "INACTIVE", "MEDIUM",
                                    ["near SKU match (normalized)", tag],
                                    f"SKU '{source.sku}' matches '{_key(t, sku_key)}' after normalization", True)
        if len(near) > 1:
            names = ", ".join(t.name for t in near)
            return _product_result(source, None, "AMBIGUOUS", "LOW",
                                    [f"{len(near)} QBO items near-match SKU '{source.sku}'", tag],
                                    f"Multiple normalized SKU matches: {names}", True, target_name=names)

    # Priority 2: name similarity (token overlap), constrained to item-type targets
    src_tokens = _tokens(source.name)
    counts: dict = {}
    for tok in src_tokens:
        for pos in index.inverted.get(tok, ()):
            counts[pos] = counts.get(pos, 0) + 1
    # ascending position + stable sort == original target order for ties
    candidates = [(items[pos], counts[pos]) for pos in sorted(counts)]
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
    exact_nm = ["exact_name_sku_differs"] if (
        source.sku and len(top) == 1 and _nm(source.name) and _nm(source.name) == _nm(top[0][0].name)) else []

    if len(top) == 1:
        t = top[0][0]
        if corroborated:
            status = "MAPPED" if t.active else "INACTIVE"
            return _product_result(source, t, status, "MEDIUM",
                                    [f"name overlap ({best_score} token(s))", "price corroborated within tolerance"] + exact_nm,
                                    f"Name match '{t.name}' corroborated by price", status != "MAPPED")
        return _product_result(source, t, "UNVERIFIED", "LOW",
                                [f"name overlap ({best_score} token(s)) only, price not corroborated"] + exact_nm,
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


# ---------------------------------------------------------------------------
# Data-source diagnostics (lessons from export-based runs: SKU column may be the Item ID, qty may be
# summed across mirrored locations, some gaps are structural)
# ---------------------------------------------------------------------------

MULTI_LOCATION_RATIO = 1.5  # LW/QBO total qty above this is implausible for one stock pool


def detect_sku_key(sources: list[SourceRecord], targets: list[TargetRecord]) -> dict:
    """Pick the QBO-side SKU key: "sku" if QBO Sku is populated and overlaps LW SKUs, else "name" if
    QBO item names overlap LW SKUs, else "none". Also returns data-quality findings, e.g. the QBO
    'SKU' column actually holding Item IDs. -> {"sku_key_source": str, "data_quality": [finding]}"""
    lw = {_norm_sku(s.sku) for s in sources if s.sku} - {""}
    items = [t for t in targets if t.entity_type == "item"]
    skus = [t for t in items if t.sku]
    if any(_norm_sku(t.sku) in lw for t in skus):
        key = "sku"
    elif any(_norm_sku(t.name) in lw for t in items):
        key = "name"
    else:
        key = "none"
    dq = []
    if skus and key != "sku" and (
            all(t.sku.strip() == str(t.target_id).strip() for t in skus) or all(t.sku.strip().isdigit() for t in skus)):
        dq.append({"gap": "qbo_sku_column_is_item_id", "severity": "HIGH",
                   "detail": "QBO 'SKU' values are Item IDs (equal to item ids / all numeric, no overlap with "
                             "Linnworks SKUs), not SKUs; items must be matched by "
                             + ("Name." if key == "name" else "another key.")})
    return {"sku_key_source": key, "data_quality": dq}


def inventory_totals_check(sources: list[SourceRecord], targets: list[TargetRecord]) -> dict:
    """Total qty per side + ratio. Flags possible_multi_location_sum when LW/QBO > 1.5x. Never sums
    locations itself: it only totals the qty values it is given."""
    lw = sum(s.qty for s in sources if s.qty is not None)
    qbo = sum(t.qty for t in targets if t.entity_type == "item" and t.qty is not None)
    ratio = round(lw / qbo, 2) if qbo else None
    flag = bool(ratio and ratio > MULTI_LOCATION_RATIO)
    return {"lw_total_qty": lw, "qbo_total_qty": qbo, "ratio": ratio, "possible_multi_location_sum": flag,
            "warning": (f"Linnworks qty is {ratio}x QBO: confirm it isn't summed across mirrored "
                        f"FBA/fulfilment locations.") if flag else ""}


def data_gap_findings(sources: list[SourceRecord], targets: list[TargetRecord],
                      account_results: Optional[list[MappingResult]] = None) -> list[dict]:
    """Deterministic data gaps -> [{"gap","severity","detail"}] (shape conclusions.derive_conclusions reads).
    account_results: channel/dimension->account MappingResults (from propose_mapping)."""
    out = []
    prods = [s for s in sources if s.entity_type == "sku"]
    items = [t for t in targets if t.entity_type == "item"]
    if prods and not any(s.amount for s in prods) and not any(t.unit_price for t in items):
        out.append({"gap": "no_price_data", "severity": "MEDIUM",
                    "detail": "No prices on either side: price can't corroborate name matches."})
    if not any(t.entity_type == "account" for t in targets):
        out.append({"gap": "no_chart_of_accounts", "severity": "HIGH",
                    "detail": "QBO chart of accounts not loaded: category -> account mapping can't be "
                              "proposed (an unmapped category can fail Sales Order sync)."})
    if not any(s.entity_type in ("marketplace_fee", "payment_processing_fee") for s in sources):
        out.append({"gap": "marketplace_fees_not_in_linnworks", "severity": "HIGH",
                    "detail": "Marketplace/payment fees aren't in Linnworks: they come from payout "
                              "statements (Amazon/eBay/Stripe)."})
    chans = sorted({r.source_name for r in (account_results or [])
                    if r.source_type == "channel" and r.status == "UNMAPPED"})
    if chans:
        out.append({"gap": "channel_no_clearing_account", "severity": "MEDIUM",
                    "detail": f"{' and '.join(chans) if len(chans) < 3 else ', '.join(chans)} "
                              f"have no clearing/income account in QBO."})
    chk = inventory_totals_check(prods, items)
    if chk["possible_multi_location_sum"]:
        out.append({"gap": "possible_multi_location_qty", "severity": "MEDIUM", "detail": chk["warning"]})
    return out
