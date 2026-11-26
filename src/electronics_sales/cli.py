"""Command-line entry point for the local analysis pipeline."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from .pipeline import run_pipeline


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Clean the electronics sales CSV and build analysis tables."
    )
    parser.add_argument(
        "--input",
        type=Path,
        default=Path("data/raw/Electronic_sales_Sep2023-Sep2024.csv"),
        help="Path to the source CSV.",
    )
    parser.add_argument(
        "--output-root",
        type=Path,
        default=Path.cwd(),
        help="Repository root where data/processed and reports are written.",
    )
    return parser


def main() -> None:
    args = build_parser().parse_args()
    summary = run_pipeline(args.input, args.output_root)
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
