import sys, os, re, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))
import plain

STATUSES = ["MAPPED", "UNMAPPED", "AMBIGUOUS", "INVALID", "ORPHANED", "INACTIVE",
            "UNVERIFIED", "STRUCTURAL_DATA_GAP", "exact_name_sku_differs", "near_sku_match"]
BAD = re.compile(r"MAPPED|AMBIGUOUS|INVALID|ORPHANED|INACTIVE|UNVERIFIED|STRUCTURAL|"
                 r"exact_name|near_sku|entity_type|confidence|\bSKU\b|\bHIGH\b|\bLOW\b")
KINDS = ["missing_item", "missing_account", "inactive_account", "item_mismatch", "quantity_mismatch",
         "tax_account", "refund_account", "shipping_account", "marketplace_fees"]


class T(unittest.TestCase):
    def test_every_status(self):
        for s in STATUSES:
            e = plain.STATUS_PLAIN[s]
            self.assertIn(e["urgency"], ("high", "medium", "low"))
            for k in ("label", "sentence"):
                self.assertFalse(BAD.search(e[k]), (s, e[k]))

    def test_reason_no_jargon(self):
        for s in STATUSES[:8]:
            r = plain.plain_reason({"linnworks_source": "TIKTOK", "qbo_target": "Sales", "status": s,
                                    "confidence": "HIGH", "evidence": "x"})
            self.assertFalse(BAD.search(r), r)

    def test_steps(self):
        for k in KINDS:
            st = plain.fix_steps(k, name="Widget", sku="A1", qty=5, channel="WALMART")
            self.assertTrue(st and st[0].startswith("1. "), k)
            self.assertFalse(BAD.search(" ".join(st)), k)
        self.assertIn("A1", " ".join(plain.fix_steps("missing_item", name="W", sku="A1", qty=5)))
        self.assertIn("warehouse", " ".join(plain.fix_steps("quantity_mismatch")))
        with self.assertRaises(ValueError):
            plain.fix_steps("nope")

    def test_rank(self):
        f = [{"key": "a", "status": "ORPHANED", "money": 5}, {"key": "b", "status": "UNMAPPED", "money": 500},
             {"key": "c", "status": "UNMAPPED", "money": 5}, {"key": "d", "status": "UNVERIFIED", "money": 500}]
        self.assertEqual([x["key"] for x in plain.rank_findings(f)], ["b", "d", "c", "a"])

    def test_headline(self):
        self.assertEqual(plain.headline({"decisions": 42, "urgent": 3}), "42 things need your decision, 3 are urgent.")
        self.assertEqual(plain.headline({"decisions": 1, "urgent": 1}), "1 thing needs your decision, 1 is urgent.")
        self.assertEqual(plain.headline({"decisions": 0, "urgent": 0}), "Nothing needs your decision.")

    def test_glossary(self):
        self.assertGreaterEqual(len(plain.GLOSSARY), 15)
        self.assertFalse(BAD.search(" ".join(m for _, m in plain.GLOSSARY)))


if __name__ == "__main__":
    unittest.main()
