# Source data

Download `Electronic_sales_Sep2023-Sep2024.csv` from the [dataset page on Kaggle](https://www.kaggle.com/datasets/cameronseamons/electronic-sales-sep2023-sep2024) and place it in `data/raw/`. The source file is intentionally ignored by Git. Running the pipeline writes a validated order table to `data/processed/orders_clean.csv`; generated data is ignored as well.

The notebook expects these columns: `Customer ID`, `Payment Method`, `Total Price`, `Add-on Total`, `Unit Price`, `Quantity`, `Purchase Date`, `Shipping Type`, `Product Type`, and `Order Status`.

The dataset-specific license and redistribution terms have not been verified. Check the source terms before redistributing the CSV. Tests use synthetic rows and do not depend on this third-party file.
