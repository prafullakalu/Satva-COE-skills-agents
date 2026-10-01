"""SYNTHETIC fixtures only (no real client data): summary metrics/CSV + export-row normalizers."""
import sys, os, csv, tempfile, unittest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "scripts"))

from normalize import from_lw_export_rows, from_qbo_export_rows
from mapping_engine import match_product_identity, find_orphaned_products, detect_sku_key, data_gap_findings
from mapping_engine import _product_result
from summary import summary_metrics, save_summary_csv

LW = [{"SKU": "A1", "Product Name": "Alpha", "Qty": "10"}, {"ItemSKU": "B2", "Title": "Beta Coin", "Quantity": 5},
      {"Sku": "C3", "Name": "Gamma", "Stock": 1}]
QBO = [{"Sku": "1", "Name": "A1", "Qty On Hand": 3, "Id": "1"}, {"Sku": "2", "Name": "Beta Coin", "Qty": 5, "Id": "2"},
       {"Sku": "3", "Name": "Orphan", "Id": "3"}]


class TestSummary(unittest.TestCase):
    def test_export_row_aliases(self):
        s, t = from_lw_export_rows(LW), from_qbo_export_rows(QBO)
        self.assertEqual([x.sku for x in s], ["A1", "B2", "C3"])
        self.assertEqual(s[1].name, "Beta Coin"); self.assertEqual(s[1].qty, 5)
        self.assertEqual(t[0].qty, 3); self.assertEqual(t[0].target_id, "1")

    def test_metrics_shape_and_csv(self):
        s, t = from_lw_export_rows(LW), from_qbo_export_rows(QBO)
        info = detect_sku_key(s, t)
        self.assertEqual(info["sku_key_source"], "name")
        self.assertEqual(info["data_quality"][0]["gap"], "qbo_sku_column_is_item_id")
        res = [match_product_identity(x, t, sku_key="name") for x in s] + []
        res += find_orphaned_products(t, res)
        m = dict(summary_metrics("Synthetic scope", info, s, t, res, data_gap_findings(s, t)))
        self.assertEqual(m["Linnworks active products"], 3)
        self.assertEqual(m["QBO inventory items"], 3)
        self.assertEqual(m["SKU exact match: LW SKU = QBO Item Name (Matched)"], 1)
        self.assertEqual(m["   of which qty MISMATCH"], 1)
        self.assertEqual(m["Exact name match, SKU differs"], 1)  # B2 vs 'Beta Coin'
        self.assertEqual(m["Missing in QBO (UNMAPPED)"], 1)
        self.assertEqual(m["Missing in Linnworks (QBO orphan)"], 1)
        self.assertEqual(m["SKU match coverage (count)"], "33.3%")
        self.assertIn("Item IDs", m["Key finding"])
        with tempfile.TemporaryDirectory() as d:
            p = save_summary_csv(os.path.join(d, "s.csv"), summary_metrics("x", info, s, t, res))
            with open(p, encoding="utf-8-sig") as f:
                rows = list(csv.reader(f))
        self.assertEqual(rows[0], ["Metric", "Value"]); self.assertEqual(rows[1], ["Scope", "x"])

    def _run(self, approve=False):
        s, t = from_lw_export_rows(LW), from_qbo_export_rows(QBO)
        info = detect_sku_key(s, t)
        res = [match_product_identity(x, t, sku_key="name") for x in s]
        if approve:  # accountant approves C3 -> QBO item 3, as run_analysis does
            res[2] = _product_result(s[2], t[2], "MAPPED", "HIGH", ["approved by accountant"], "approved", False)
        res += find_orphaned_products(t, res)
        return info, s, t, res, data_gap_findings(s, t)

    def test_plain_wording_and_same_numbers(self):
        info, s, t, res, gaps = self._run()
        d = summary_metrics("x", info, s, t, res, gaps)
        p = summary_metrics("x", info, s, t, res, gaps, plain=True)
        text = " ".join(f"{a} {b}" for a, b in p)
        for bad in ("UNVERIFIED", "AMBIGUOUS", "UNMAPPED", "ORPHAN", "SKU", "QBO", "LW", "FBA", "Item IDs"):
            self.assertNotRegex(text, rf"\b{bad}\b", bad)
        pm, dm = dict(p), dict(d)
        self.assertEqual(pm["Products matched by product code"], dm["SKU exact match: LW SKU = QBO Item Name (Matched)"])
        self.assertEqual(pm["Products missing in QuickBooks"], dm["Missing in QBO (UNMAPPED)"])
        self.assertEqual(pm["Items only in QuickBooks (not part of the total above)"], dm["Missing in Linnworks (QBO orphan)"])
        self.assertEqual(pm["Products matched by name only - please confirm"], dm["Name overlap only - needs review (UNVERIFIED)"])
        self.assertEqual(pm["All Linnworks products counted above (equals Linnworks active products)"],
                         pm["Linnworks active products"])
        self.assertNotIn("Matched because you approved them", pm)
        self.assertNotIn("Approved by accountant (Matched)", dm)  # default unchanged when 0

    def test_approved_line_counted_in_both_modes(self):
        info, s, t, res, gaps = self._run(approve=True)
        d = dict(summary_metrics("x", info, s, t, res, gaps))
        p = dict(summary_metrics("x", info, s, t, res, gaps, plain=True))
        self.assertEqual(d["Approved by accountant (Matched)"], 1)
        self.assertEqual(p["Matched because you approved them"], 1)
        self.assertEqual(p["Products missing in QuickBooks"], 0)
        self.assertEqual(p["All Linnworks products counted above (equals Linnworks active products)"], 3)


if __name__ == "__main__":
    unittest.main()
