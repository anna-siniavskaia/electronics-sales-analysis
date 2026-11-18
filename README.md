# Electronic Sales Analysis

A customer-level and revenue analysis of the public [Electronic Sales Sep 2023–Sep 2024 dataset](https://www.kaggle.com/datasets/cameronseamons/electronic-sales-sep2023-sep2024). The notebook uses pandas for cleaning, aggregation, customer summaries, monthly and quarterly add-on revenue, cohort tables, and visualizations.

## Questions explored

- Which customers have the highest completed-order spend, and which payment method do they use most often?
- How does revenue vary by shipping method and product type?
- How do monthly and quarterly add-on sales change over time?
- What does revenue look like during each cohort's first four observed months?

## Method choices

- Only completed orders are included in spending and revenue metrics.
- Each row is treated as one order because the source has no separate order ID; duplicate-looking rows are retained.
- Total revenue is calculated as `Total Price + Add-on Total`; the source does not specify a currency.
- Cohorts are based on each customer's first valid completed order in this file, not necessarily their first purchase ever.
- Missing add-on totals are treated as zero; invalid dates, non-positive prices or quantities, fractional quantities, and negative add-on totals are excluded.
- Cohort cells use zero for observed months without orders and blank values for months outside the observation window.

These choices are documented in the notebook so the calculations can be reviewed and changed. The cleaner also checks that every required source column is present before processing.

## Run in Google Colab

1. Download the source CSV from Kaggle under its terms.
2. Open `notebooks/electronic_sales_analysis.ipynb` in Google Colab.
3. Run all cells and upload the CSV when prompted.

The notebook requires these source columns: `Customer ID`, `Payment Method`, `Total Price`, `Add-on Total`, `Unit Price`, `Quantity`, `Purchase Date`, `Shipping Type`, `Product Type`, and `Order Status`. It stops with a list of missing columns if the uploaded file does not match this schema.

The source dataset is not included in this repository. Its current dataset-specific license and redistribution terms have not been verified; check the license shown on Kaggle before bundling or redistributing the CSV. Notebook outputs were removed from the portfolio copy, so it contains no embedded customer rows or previously rendered results.

## Limitations

The source data covers one year and does not specify a currency or a unique order identifier. Cohort revenue is not a direct retention metric, and later cohorts have shorter observation windows. The first and last calendar months may be incomplete. The notebook has not been re-executed during portfolio preparation.
