"""Validation and cleaning for the source electronics sales table."""

from __future__ import annotations

import numpy as np
import pandas as pd


COLUMN_MAP = {
    "Customer ID": "customer_id",
    "Payment Method": "payment_method",
    "Total Price": "product_total",
    "Add-on Total": "addons_total",
    "Unit Price": "unit_price",
    "Quantity": "quantity",
    "Purchase Date": "purchase_date",
    "Shipping Type": "shipping_method",
    "Product Type": "product_type",
    "Order Status": "order_status",
}
REQUIRED_COLUMNS = tuple(COLUMN_MAP)
TEXT_COLUMNS = (
    "customer_id",
    "payment_method",
    "shipping_method",
    "product_type",
    "order_status",
)
NUMERIC_COLUMNS = ("product_total", "addons_total", "unit_price", "quantity")


def clean_orders(source: pd.DataFrame) -> pd.DataFrame:
    """Return valid completed orders without mutating ``source``.

    The cleaning report is stored in ``result.attrs['cleaning_report']``. Rows
    with missing or invalid core values are rejected; genuinely missing add-on
    totals are interpreted as zero before validation.
    """

    missing = sorted(set(REQUIRED_COLUMNS) - set(source.columns))
    if missing:
        raise ValueError(f"Missing required columns: {', '.join(missing)}")

    frame = (
        source.rename(columns=COLUMN_MAP)
        .reindex(columns=list(COLUMN_MAP.values()))
        .copy()
    )
    for column in TEXT_COLUMNS:
        frame[column] = frame[column].astype("string").str.strip().replace("", pd.NA)

    frame["payment_method"] = frame["payment_method"].replace({"Paypal": "PayPal"})
    frame["purchase_date"] = pd.to_datetime(
        frame["purchase_date"], format="%Y-%m-%d", errors="coerce"
    )

    add_on_text = frame["addons_total"].astype("string").str.strip()
    add_on_missing = add_on_text.isna() | add_on_text.eq("")
    for column in NUMERIC_COLUMNS:
        frame[column] = pd.to_numeric(frame[column], errors="coerce").astype(float)
    frame.loc[add_on_missing, "addons_total"] = 0.0

    finite = np.isfinite(frame[list(NUMERIC_COLUMNS)]).all(axis=1)
    valid = (
        frame["customer_id"].notna()
        & frame["purchase_date"].notna()
        & finite
        & frame["product_total"].gt(0)
        & frame["unit_price"].gt(0)
        & frame["quantity"].gt(0)
        & frame["quantity"].mod(1).eq(0)
        & frame["addons_total"].ge(0)
    )
    completed = frame["order_status"].str.casefold().eq("completed").fillna(False)

    report = {
        "source_rows": len(frame),
        "not_completed_rows": int((~completed).sum()),
        "invalid_completed_rows": int((completed & ~valid).sum()),
        "missing_addon_totals_filled": int(add_on_missing.sum()),
    }
    result = frame.loc[valid & completed].copy()
    result[["shipping_method", "product_type"]] = result[
        ["shipping_method", "product_type"]
    ].fillna("Unknown")
    result["quantity"] = result["quantity"].astype("int64")
    result["revenue"] = result["product_total"] + result["addons_total"]
    result["month"] = result["purchase_date"].dt.to_period("M")
    result = result.reset_index(drop=True)
    report["retained_rows"] = len(result)
    result.attrs["cleaning_report"] = report
    return result
