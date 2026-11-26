from __future__ import annotations

import json
import tempfile
import unittest
from pathlib import Path

from electronics_sales.pipeline import run_pipeline
from tests.fixtures import sample_orders


class PipelineTests(unittest.TestCase):
    def test_pipeline_writes_expected_artifacts(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source.csv"
            sample_orders().to_csv(source, index=False)

            summary = run_pipeline(source, root)

            self.assertEqual(summary["retained_rows"], 3)
            self.assertEqual(summary["customers"], 2)
            self.assertTrue((root / "data/processed/orders_clean.csv").is_file())
            self.assertTrue((root / "reports/tables/customer_summary.csv").is_file())
            self.assertTrue((root / "reports/tables/cohort_revenue.csv").is_file())
            saved = json.loads((root / "reports/summary.json").read_text())
            self.assertEqual(saved, summary)

    def test_missing_source_is_reported_clearly(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            with self.assertRaisesRegex(FileNotFoundError, "Source CSV not found"):
                run_pipeline(root / "missing.csv", root)


if __name__ == "__main__":
    unittest.main()
