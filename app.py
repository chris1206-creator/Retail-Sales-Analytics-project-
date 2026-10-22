from datetime import date

import pandas as pd
import streamlit as st

from generate_data import DATA_PATH, load_or_create_sales_data
from retail_analytics import build_insights, filter_sales, monthly_revenue, summary_metrics, top_products


st.set_page_config(page_title="Retail Sales Analytics", page_icon="📊", layout="wide")
st.title("Retail Sales Analytics")
st.caption("Explore two years of sample transactions by date, product category, and region.")

sales = load_or_create_sales_data()
minimum_date = sales["date"].min().date()
maximum_date = sales["date"].max().date()

with st.sidebar:
    st.header("Filters")
    selected_dates = st.date_input(
        "Date range",
        value=(minimum_date, maximum_date),
        min_value=minimum_date,
        max_value=maximum_date,
    )
    selected_categories = st.multiselect("Categories", sorted(sales["category"].unique()))
    selected_regions = st.multiselect("Regions", sorted(sales["region"].unique()))
    st.download_button(
        "Download sample CSV",
        data=DATA_PATH.read_bytes(),
        file_name="retail_sales.csv",
        mime="text/csv",
        use_container_width=True,
    )

if isinstance(selected_dates, tuple) and len(selected_dates) == 2:
    start_date, end_date = selected_dates
else:
    start_date = end_date = selected_dates if isinstance(selected_dates, date) else minimum_date

filtered = filter_sales(sales, start_date, end_date, selected_categories, selected_regions)
metrics = summary_metrics(filtered)

metric_columns = st.columns(4)
metric_columns[0].metric("Net revenue", f"${metrics['revenue']:,.2f}")
metric_columns[1].metric("Orders", f"{metrics['orders']:,}")
metric_columns[2].metric("Units sold", f"{metrics['units']:,}")
metric_columns[3].metric("Average order value", f"${metrics['average_order_value']:,.2f}")

st.divider()
left, right = st.columns([1.6, 1])

with left:
    st.subheader("Revenue over time")
    monthly = monthly_revenue(filtered)
    if monthly.empty:
        st.info("No data for these filters.")
    else:
        st.line_chart(monthly, x="month", y="revenue", color="#167d72")

with right:
    st.subheader("Revenue by region")
    region_revenue = filtered.groupby("region")["revenue"].sum().sort_values(ascending=False)
    if region_revenue.empty:
        st.info("No data for these filters.")
    else:
        st.bar_chart(region_revenue, color="#e38b42")

bottom_left, bottom_right = st.columns([1, 1])
with bottom_left:
    st.subheader("Top products")
    products = top_products(filtered)
    if products.empty:
        st.info("No data for these filters.")
    else:
        st.bar_chart(products.set_index("product")["revenue"], color="#4978a8")

with bottom_right:
    st.subheader("Key findings")
    for insight in build_insights(filtered):
        st.write(f"- {insight}")
    st.caption(f"Showing {len(filtered):,} of {len(sales):,} transactions.")

with st.expander("View filtered transactions"):
    st.dataframe(filtered, use_container_width=True, hide_index=True)