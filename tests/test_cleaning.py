from __future__ import annotations

import unittest

from electronics_sales.cleaning import clean_orders
from tests.fixtures import sample_orders


class CleaningTests(unittest.TestCase):
    def test_cleaning_filters_and_reports_rows(self) -> None:
        source = sample_orders()
        original_columns = source.columns.tolist()
        result = clean_orders(source)

        self.assertEqual(len(result), 3)
        self.assertEqual(source.columns.tolist(), original_columns)
        self.assertEqual(result["quantity"].dtype.name, "int64")
        self.assertEqual(result.loc[result["customer_id"] == "B", "addons_total"].item(), 0)
        self.assertEqual(
            result.attrs["cleaning_report"],
            {
                "source_rows": 6,
                "not_completed_rows": 1,
                "invalid_completed_rows": 2,
                "missing_addon_totals_filled": 1,
                "retained_rows": 3,
            },
        )

    def test_missing_required_column_is_rejected(self) -> None:
        with self.assertRaisesRegex(ValueError, "Missing required columns: Customer ID"):
            clean_orders(sample_orders().drop(columns="Customer ID"))


if __name__ == "__main__":
    unittest.main()
