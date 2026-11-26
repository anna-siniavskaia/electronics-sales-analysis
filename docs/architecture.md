# Architecture

```text
third-party CSV
      │
      ▼
schema and row validation ──► cleaning report
      │
      ▼
validated completed orders ──► data/processed/orders_clean.csv
      │
      ├──► customer summary
      ├──► revenue by shipping and product
      ├──► monthly and quarterly add-on revenue
      └──► four-month cohort matrices
                    │
                    ▼
            reports/tables + summary.json
```

The reusable logic lives in `src/electronics_sales`. The command-line interface calls the same functions exercised by the synthetic test suite. The notebook imports that package and is only a presentation layer; it does not contain a separate cleaning or metric implementation.

The raw third-party file and all generated artifacts remain outside version control. This keeps the repository small, avoids redistributing an unverified dataset, and makes every committed test independent of external data.
