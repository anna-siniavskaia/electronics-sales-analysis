"""Synthetic source rows used by the test suite."""

from __future__ import annotations

import pandas as pd


def sample_orders() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "Customer ID": ["A", "A", "B", "C", "D", "E"],
            "Payment Method": ["Cash", "Credit Card", None, "Cash", "Cash", "Cash"],
            "Total Price": [100, 100, 50, -1, 20, 10],
            "Add-on Total": [10, 0, None, 0, 5, 0],
            "Unit Price": [100, 100, 50, 1, 20, 10],
            "Quantity": [1, 1, 1, 1, 1, 1],
            "Purchase Date": [
                "2024-01-10",
                "2024-03-10",
                "2024-03-11",
                "2024-02-01",
                "2024-02-02",
                "bad-date",
            ],
            "Shipping Type": [
                "Standard", "Express", "Standard", "Standard", "Pickup", "Standard"
            ],
            "Product Type": ["Laptop", "Laptop", "Phone", "Phone", "Tablet", "Laptop"],
            "Order Status": [
                "Completed", "Completed", "Completed", "Completed", "Cancelled", "Completed"
            ],
        }
    )
