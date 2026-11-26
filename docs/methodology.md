# Methodology

## Cleaning

- Keep completed orders only.
- Keep duplicate-looking rows: the source lacks an order identifier, so their status cannot be resolved reliably.
- Treat missing add-on totals as zero.
- Exclude rows with invalid dates, non-positive prices or quantities, fractional quantities, or negative add-on totals.
- Check for every required source column before processing.

## Metrics

- Order revenue is `Total Price + Add-on Total`; the source does not specify a currency.
- Customer spend and revenue by shipping method and product type sum order revenue.
- Monthly and quarterly add-on totals sum `Add-on Total` for completed, valid orders.
- A customer's cohort is the month of their first valid completed order in this file. It is not necessarily their first purchase ever.
- Cohort cells use zero for observed months with no orders and blank values for months outside the observation window.

## Interpretation limits

The file covers about one year. Later cohorts have less follow-up time, and the first and last calendar months may be incomplete. Cohort revenue is not a direct measure of retention. Without an order ID, duplicate-looking records cannot be verified. The source CSV is not bundled with the project, so repository checks use a synthetic fixture. The full pipeline can be reproduced locally after downloading the documented source file.
