"""End-to-end local pipeline for the electronics sales analysis."""

from __future__ import annotations

import json
from pathlib import Path

import pandas as pd

from .cleaning import clean_orders
from .metrics import build_metrics, customer_summary


def _write_table(table: pd.DataFrame, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    table.to_csv(path, index=any(name is not None for name in table.index.names))


def run_pipeline(source_path: Path, output_root: Path) -> dict[str, object]:
    """Load one CSV, validate it, and write deterministic analysis artifacts."""

    if not source_path.is_file():
        raise FileNotFoundError(
            f"Source CSV not found: {source_path}. Download it from the documented source."
        )

    source = pd.read_csv(source_path, dtype={"Customer ID": "string"})
    orders = clean_orders(source)
    customers = customer_summary(orders)
    metrics = build_metrics(orders)

    processed_dir = output_root / "data" / "processed"
    tables_dir = output_root / "reports" / "tables"
    processed_dir.mkdir(parents=True, exist_ok=True)
    tables_dir.mkdir(parents=True, exist_ok=True)
    orders.to_csv(processed_dir / "orders_clean.csv", index=False)
    _write_table(customers, tables_dir / "customer_summary.csv")
    for name, table in metrics.items():
        _write_table(table, tables_dir / f"{name}.csv")

    cleaning_report = orders.attrs["cleaning_report"]
    _write_table(
        pd.Series(cleaning_report, name="rows").rename_axis("check").reset_index(),
        tables_dir / "cleaning_report.csv",
    )
    summary = {
        "source_rows": len(source),
        "retained_rows": len(orders),
        "customers": int(orders["customer_id"].nunique()),
        "total_revenue": float(orders["revenue"].sum()),
        "addon_revenue": float(orders["addons_total"].sum()),
        "period_start": (
            orders["purchase_date"].min().date().isoformat() if not orders.empty else None
        ),
        "period_end": (
            orders["purchase_date"].max().date().isoformat() if not orders.empty else None
        ),
    }
    (output_root / "reports").mkdir(parents=True, exist_ok=True)
    (output_root / "reports" / "summary.json").write_text(
        json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return summary
