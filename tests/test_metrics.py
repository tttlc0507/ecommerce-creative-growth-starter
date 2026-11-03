import importlib.util
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

SCRIPT = Path(__file__).resolve().parents[1] / "skills/ecommerce-creative-growth-starter/scripts/metrics.py"
spec = importlib.util.spec_from_file_location("public_metrics", SCRIPT)
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class MetricsBehavior(unittest.TestCase):
    def run_csv(self, text):
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "sample.csv"
            path.write_text(text, encoding="utf-8-sig")
            return module.compute_csv(path)

    def test_ctr_and_cpc_use_counts(self):
        row = self.run_csv("creative_id,impressions,clicks,spend\nfictional,900,45,90\n")["rows"][0]
        self.assertEqual(row["ctr_pct"], 5)
        self.assertEqual(row["cpc"], 2)

    def test_zero_clicks_are_not_missing_impressions(self):
        row = self.run_csv("creative_id,impressions,clicks,spend\nfictional,100,0,12\n")["rows"][0]
        self.assertEqual(row["ctr_pct"], 0)
        self.assertIsNone(row["cpc"])

    def test_zero_and_missing_denominators_remain_null(self):
        rows = self.run_csv("creative_id,impressions,clicks,spend\nfictional-a,0,0,0\nfictional-b,,8,16\n")["rows"]
        self.assertIsNone(rows[0]["ctr_pct"])
        self.assertIsNone(rows[0]["cpc"])
        self.assertIsNone(rows[1]["ctr_pct"])
        self.assertEqual(rows[1]["cpc"], 2)

    def test_rate_label_cannot_create_purchase_cvr(self):
        report = self.run_csv("creative_id,impressions,clicks,spend,CVR\nfictional,100,8,16,8%\n")
        self.assertEqual(report["rows"][0]["ctr_pct"], 8)
        self.assertNotIn("cvr", report["rows"][0])
        self.assertNotIn("cvr_pct", report["rows"][0])

    def test_nonfinite_negative_and_fractional_counts_fail(self):
        for raw in ("NaN", "Infinity", "-1", "3.5", "=A1/B1", "5%"):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                self.run_csv(f"creative_id,impressions,clicks,spend\nfictional,{raw},1,1\n")

    def test_chinese_headers(self):
        row = self.run_csv("素材ID,展现,点击,花费\n虚构,500,25,50\n")["rows"][0]
        self.assertEqual((row["ctr_pct"], row["cpc"]), (5, 2))

    def test_duplicate_aliases_fail(self):
        with self.assertRaises(ValueError):
            self.run_csv("creative_id,impressions,展现,clicks,spend\nfictional,100,200,8,16\n")

    def test_repeated_ids_are_not_merged(self):
        report = self.run_csv("creative_id,impressions,clicks,spend\nfictional,100,8,16\nfictional,200,4,12\n")
        self.assertEqual(len(report["rows"]), 2)
        self.assertTrue(report["rows"][1]["notes"])

    def test_bad_columns_and_empty_ids_fail(self):
        for text in ("creative_id,impressions,clicks,spend\n,100,8,16\n", "creative_id,impressions,clicks,spend\nfictional,100,8,16,extra\n"):
            with self.assertRaises(ValueError):
                self.run_csv(text)

    def test_empty_template_has_no_fabricated_rows(self):
        report = self.run_csv("creative_id,impressions,clicks,spend\n")
        self.assertEqual(report["rows"], [])

    def test_conversion_requires_explicit_event_definitions(self):
        row = self.run_csv("creative_id,impressions,clicks,spend,conversions,conversion_base_count\nfictional,100,10,30,3,60\n")["rows"][0]
        self.assertIsNone(row["conversion_rate_pct"])
        self.assertIsNone(row["cost_per_conversion"])
        self.assertTrue(row["notes"])

    def test_conversion_ratio_and_cost_preserve_context(self):
        row = self.run_csv("creative_id,impressions,clicks,spend,conversion_event,conversions,conversion_base_event,conversion_base_count,period,attribution_window\nfictional,100,10,30,add_to_cart_users,3,visitors,60,demo_period,demo_window\n")["rows"][0]
        self.assertEqual(row["conversion_rate_pct"], 5)
        self.assertEqual(row["cost_per_conversion"], 10)
        self.assertEqual(row["conversion_event"], "add_to_cart_users")
        self.assertEqual(row["conversion_base_event"], "visitors")
        self.assertEqual(row["context"]["attribution_window"], "demo_window")

    def test_zero_conversions_are_zero_rate_and_undefined_cost(self):
        row = self.run_csv("creative_id,impressions,clicks,spend,conversion_event,conversions,conversion_base_event,conversion_base_count\nfictional,100,10,30,paid_buyers,0,visitors,60\n")["rows"][0]
        self.assertEqual(row["conversion_rate_pct"], 0)
        self.assertIsNone(row["cost_per_conversion"])

    def test_conversion_counts_must_be_finite_integers(self):
        for raw in ("NaN", "3.5", "-1"):
            with self.subTest(raw=raw), self.assertRaises(ValueError):
                self.run_csv(f"creative_id,impressions,clicks,spend,conversions\nfictional,100,10,30,{raw}\n")

    def test_conversion_chinese_headers_and_inconsistent_units(self):
        row = self.run_csv("素材ID,曝光,点击,花费,转化事件,转化数,分母事件,分母计数\n虚构,100,10,30,orders,12,visitors,6\n")["rows"][0]
        self.assertEqual(row["conversion_rate_pct"], 200)
        self.assertTrue(row["notes"])

    def test_cli_preserves_existing_file(self):
        with tempfile.TemporaryDirectory() as temp:
            data, output = Path(temp) / "data.csv", Path(temp) / "result.json"
            data.write_text("creative_id,impressions,clicks,spend\nfictional,100,8,16\n")
            output.write_text("existing user report")
            result = subprocess.run([sys.executable, str(SCRIPT), str(data), "--output", str(output)], capture_output=True, text=True)
            self.assertEqual(result.returncode, 2)
            self.assertEqual(output.read_text(), "existing user report")


if __name__ == "__main__":
    unittest.main()
