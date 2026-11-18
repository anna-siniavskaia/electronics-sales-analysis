# Electronic Sales Analysis

Customer, revenue, and cohort analysis of the [Electronic Sales Sep 2023–Sep 2024 dataset](https://www.kaggle.com/datasets/cameronseamons/electronic-sales-sep2023-sep2024). The project keeps the analysis notebook separate from the data and documents the assumptions behind each metric.

## Project layout

```text
electronic-sales-analysis/
├── data/
│   ├── README.md                 # data source and expected schema
│   └── raw/                      # place the downloaded CSV here; ignored by Git
├── docs/
│   └── methodology.md            # cleaning rules and metric definitions
├── notebooks/
│   └── electronic_sales_analysis.ipynb
├── requirements.txt
└── README.md
```

## Questions

- Which customers have the highest completed-order spend?
- How does revenue vary by shipping method and product type?
- How do add-on sales change by month and quarter?
- What is the revenue pattern in each cohort's first four observed months?

## Run locally

1. Download the CSV from Kaggle under its terms and save it as `data/raw/Electronic_sales_Sep2023-Sep2024.csv`.
2. From the repository root, create an environment and install dependencies:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   python -m pip install -r requirements.txt
   jupyter lab
   ```

3. Open `notebooks/electronic_sales_analysis.ipynb` and run its cells in order. The notebook checks the source path and required columns before analysis.

The CSV is not included. The exact dataset-specific license and redistribution terms have not been verified, so obtain it from the source and check its terms before sharing a copy. Notebook outputs were removed from this repository, and the notebook has not been re-executed during portfolio preparation.

## Method and limits

Only completed orders enter the revenue metrics. Each row is treated as one order because the source has no separate order ID. Revenue is `Total Price + Add-on Total`; the source does not specify a currency. Cohorts start at each customer's first valid completed order *in this file*, which may not be their first purchase ever.

The full cleaning rules, metric definitions, and limits are in [docs/methodology.md](docs/methodology.md). The one-year observation period means later cohorts have shorter windows, and the first or last calendar month may be incomplete.
