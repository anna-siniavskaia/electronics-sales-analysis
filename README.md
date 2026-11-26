# Electronic Sales Analysis

A reproducible Python pipeline for cleaning customer orders and producing revenue, add-on, and cohort tables from the [Electronic Sales Sep 2023–Sep 2024 dataset](https://www.kaggle.com/datasets/cameronseamons/electronic-sales-sep2023-sep2024).

The command-line pipeline is the primary interface. The notebook is optional and contains no Google Colab setup, uploads, mounts, or Colab-specific metadata.

## Project structure

```text
electronics-sales-analysis/
├── data/
│   ├── raw/                       # downloaded source CSV; ignored by Git
│   └── processed/                 # generated validated orders
├── docs/
│   ├── architecture.md            # pipeline and ownership boundaries
│   └── methodology.md             # cleaning and metric definitions
├── notebooks/
│   └── electronic_sales_analysis.ipynb  # optional exploration
├── reports/
│   ├── figures/                   # generated charts
│   ├── tables/                    # generated metric CSV files
│   └── summary.json               # generated run summary
├── src/electronics_sales/
│   ├── cleaning.py                # schema checks and row-level validation
│   ├── metrics.py                 # customer, revenue, add-on, cohort metrics
│   ├── pipeline.py                # end-to-end artifact generation
│   └── cli.py                     # command-line interface
├── tests/                         # synthetic, dataset-independent checks
├── pyproject.toml
└── requirements.txt
```

## What the pipeline answers

- Which customers have the highest completed-order spend?
- How does revenue vary by shipping method and product type?
- How do add-on sales change by month and quarter?
- What is the revenue pattern in each cohort's first four observed months?

## Run locally

1. Download the CSV under its source terms and save it as:

   ```text
   data/raw/Electronic_sales_Sep2023-Sep2024.csv
   ```

2. Create an environment and install the project:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   python -m pip install -r requirements.txt
   ```

3. Run the tested command-line pipeline:

   ```bash
   electronics-sales
   ```

   It writes the cleaned order table to `data/processed/`, metric tables to `reports/tables/`, and a machine-readable run summary to `reports/summary.json`.

4. Run the dataset-independent test suite:

   ```bash
   python -m unittest discover -s tests -v
   ```

The optional notebook can be opened with `jupyter lab`; it is not required to execute the pipeline.

## Method and limits

Only valid completed orders enter revenue metrics. Each row is treated as one order because the source has no separate order ID. Revenue is `Total Price + Add-on Total`; the source does not specify a currency. Cohorts start at each customer's first valid completed order observed in this file, which may not be their first purchase ever.

The CSV is not committed. Its exact dataset-specific license and redistribution terms have not been verified, so obtain it from the source and check the current terms before sharing a copy. See [the architecture](docs/architecture.md) for the execution flow and [the methodology](docs/methodology.md) for all cleaning rules and interpretation limits.
