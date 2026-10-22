# Retail Sales Analytics

A beginner-friendly Big Data Analytics project that explores retail sales across products, categories, regions, and time. It generates a reproducible sample dataset and displays interactive summaries in a Streamlit dashboard.

## Run it

1. Create and activate a Python virtual environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Start the dashboard with `streamlit run app.py`.

The app creates `data/retail_sales.csv` the first time it runs. It contains 5,000 reproducible sample transactions covering 2024 and 2025. Use the sidebar to filter results and download the CSV.

## What it analyzes

- Net revenue, order count, units sold, and average order value
- Monthly revenue trends
- Revenue by region and top products
- Short insights for the currently selected filters

## Validate the analysis

Run `python -m unittest` to check data generation, filtering, and monthly totals.

## Big-data extension

The bundled dataset is intentionally small enough for a laptop. For a course extension, generate a larger CSV by changing the `rows` argument in `generate_data.py`, then read it with PySpark using `spark.read.csv(...)` and reproduce the monthly/category aggregations with `groupBy`. The dashboard's analysis functions are kept separate so they can be compared with Spark results.