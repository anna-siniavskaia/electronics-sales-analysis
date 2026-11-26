from __future__ import annotations

import unittest

import pandas as pd

from electronics_sales.cleaning import clean_orders
from electronics_sales.metrics import build_metrics, customer_summary
from tests.fixtures import sample_orders


class MetricsTests(unittest.TestCase):
    def setUp(self) -> None:
        self.orders = clean_orders(sample_orders())

    def test_customer_summary_reconciles_to_clean_orders(self) -> None:
        customers = customer_summary(self.orders).set_index("customer_id")
        self.assertEqual(customers.loc["A", "preferred_payment"], "Cash")
        self.assertEqual(customers.loc["A", "total_spent"], 210)
        self.assertEqual(customers.loc["B", "preferred_payment"], "Unknown")
        self.assertEqual(customers["orders_count"].sum(), len(self.orders))
        self.assertAlmostEqual(customers["total_spent"].sum(), self.orders["revenue"].sum())

    def test_cohort_matrix_distinguishes_zero_from_future_months(self) -> None:
        metrics = build_metrics(self.orders)
        cohort = metrics["cohort_revenue"]
        self.assertEqual(cohort.loc[pd.Period("2024-01"), 1], 0)
        self.assertEqual(cohort.loc[pd.Period("2024-01"), 2], 100)
        self.assertTrue(pd.isna(cohort.loc[pd.Period("2024-03"), 1]))
        self.assertAlmostEqual(
            metrics["revenue_by_product"]["revenue"].sum(),
            self.orders["revenue"].sum(),
        )

    def test_empty_input_returns_empty_metric_tables(self) -> None:
        empty = self.orders.iloc[0:0]
        self.assertTrue(customer_summary(empty).empty)
        self.assertTrue(all(table.empty for table in build_metrics(empty).values()))


if __name__ == "__main__":
    unittest.main()
