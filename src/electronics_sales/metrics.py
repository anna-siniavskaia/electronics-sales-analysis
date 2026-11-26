"""Business metrics computed from cleaned completed orders."""

from __future__ import annotations

import numpy as np
import pandas as pd


def customer_summary(orders: pd.DataFrame) -> pd.DataFrame:
    """Aggregate spend, add-ons, order count, and preferred payment method."""

    columns = [
        "customer_id",
        "preferred_payment",
        "total_spent",
        "addons_spent",
        "orders_count",
    ]
    if orders.empty:
        return pd.DataFrame(columns=columns)

    totals = orders.groupby("customer_id", as_index=False).agg(
        total_spent=("revenue", "sum"),
        addons_spent=("addons_total", "sum"),
        orders_count=("customer_id", "size"),
    )
    frequencies = (
        orders.dropna(subset=["payment_method"])
        .groupby(["customer_id", "payment_method"])
        .size()
        .rename("frequency")
        .reset_index()
    )
    preferred = (
        frequencies.sort_values(
            ["customer_id", "frequency", "payment_method"],
            ascending=[True, False, True],
        )
        .drop_duplicates("customer_id")
        .rename(columns={"payment_method": "preferred_payment"})
    )
    result = totals.merge(
        preferred[["customer_id", "preferred_payment"]],
        on="customer_id",
        how="left",
    )
    result["preferred_payment"] = result["preferred_payment"].fillna("Unknown")
    return (
        result[columns]
        .sort_values(["total_spent", "customer_id"], ascending=[False, True])
        .reset_index(drop=True)
    )


def _empty_metrics() -> dict[str, pd.DataFrame]:
    cohorts = pd.PeriodIndex([], freq="M", name="cohort")
    ages = pd.Index(range(4), name="age")
    return {
        "revenue_by_shipping": pd.DataFrame(columns=["shipping_method", "revenue"]),
        "revenue_by_product": pd.DataFrame(columns=["product_type", "revenue"]),
        "addons_by_month": pd.DataFrame(columns=["month", "addons_revenue"]),
        "addons_by_quarter": pd.DataFrame(columns=["quarter", "addons_revenue"]),
        "cohort_revenue": pd.DataFrame(index=cohorts, columns=ages, dtype=float),
        "cohort_customers": pd.DataFrame(index=cohorts, columns=ages, dtype="Int64"),
    }


def build_metrics(orders: pd.DataFrame) -> dict[str, pd.DataFrame]:
    """Build revenue, add-on, and first-four-month cohort tables."""

    if orders.empty:
        return _empty_metrics()

    shipping = (
        orders.groupby("shipping_method", as_index=False)["revenue"]
        .sum()
        .sort_values("revenue", ascending=False)
        .reset_index(drop=True)
    )
    products = (
        orders.groupby("product_type", as_index=False)["revenue"]
        .sum()
        .sort_values("revenue", ascending=False)
        .reset_index(drop=True)
    )

    months = pd.period_range(
        orders["month"].min(), orders["month"].max(), freq="M", name="month"
    )
    monthly = (
        orders.groupby("month")["addons_total"]
        .sum()
        .reindex(months, fill_value=0)
        .rename("addons_revenue")
        .reset_index()
    )
    quarterly = (
        monthly.assign(quarter=monthly["month"].dt.asfreq("Q"))
        .groupby("quarter", as_index=False)["addons_revenue"]
        .sum()
    )

    cohort_orders = orders.copy()
    cohort_orders["cohort"] = cohort_orders.groupby("customer_id")["month"].transform("min")
    cohort_orders["age"] = (
        cohort_orders["month"].astype("int64")
        - cohort_orders["cohort"].astype("int64")
    )
    grouped = (
        cohort_orders.loc[cohort_orders["age"].between(0, 3)]
        .groupby(["cohort", "age"])
        .agg(revenue=("revenue", "sum"), customers=("customer_id", "nunique"))
    )
    cohorts = pd.PeriodIndex(
        cohort_orders["cohort"].unique(), freq="M", name="cohort"
    ).sort_values()
    ages = pd.Index(range(4), name="age")
    observed = pd.DataFrame(
        cohorts.asi8[:, None] + np.arange(4)[None, :]
        <= cohort_orders["month"].max().ordinal,
        index=cohorts,
        columns=ages,
    )
    cohort_revenue = (
        grouped["revenue"]
        .unstack("age")
        .reindex(index=cohorts, columns=ages)
        .fillna(0)
        .where(observed)
    )
    cohort_customers = (
        grouped["customers"]
        .unstack("age")
        .reindex(index=cohorts, columns=ages)
        .fillna(0)
        .where(observed)
        .astype("Int64")
    )
    return {
        "revenue_by_shipping": shipping,
        "revenue_by_product": products,
        "addons_by_month": monthly,
        "addons_by_quarter": quarterly,
        "cohort_revenue": cohort_revenue,
        "cohort_customers": cohort_customers,
    }
