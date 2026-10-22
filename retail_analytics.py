"""Reusable cleaning, filtering, and summary functions for the dashboard."""

import pandas as pd


def filter_sales(
    sales: pd.DataFrame,
    start_date: object,
    end_date: object,
    categories: list[str],
    regions: list[str],
) -> pd.DataFrame:
    """Filter transactions by date, category, and region."""
    dates = pd.to_datetime(sales["date"])
    mask = dates.between(pd.Timestamp(start_date), pd.Timestamp(end_date))
    if categories:
        mask &= sales["category"].isin(categories)
    if regions:
        mask &= sales["region"].isin(regions)
    return sales.loc[mask].copy()


def summary_metrics(sales: pd.DataFrame) -> dict[str, float | int]:
    """Calculate headline measures for a filtered set of transactions."""
    order_count = int(sales["order_id"].nunique())
    revenue = float(sales["revenue"].sum())
    return {
        "revenue": revenue,
        "orders": order_count,
        "units": int(sales["units"].sum()),
        "average_order_value": revenue / order_count if order_count else 0.0,
    }


def monthly_revenue(sales: pd.DataFrame) -> pd.DataFrame:
    """Aggregate revenue by calendar month."""
    if sales.empty:
        return pd.DataFrame(columns=["month", "revenue"])
    monthly = sales.assign(month=pd.to_datetime(sales["date"]).dt.to_period("M").dt.to_timestamp())
    return monthly.groupby("month", as_index=False)["revenue"].sum().sort_values("month")


def top_products(sales: pd.DataFrame, limit: int = 10) -> pd.DataFrame:
    """Return products ranked by revenue."""
    return (
        sales.groupby("product", as_index=False)["revenue"]
        .sum()
        .sort_values("revenue", ascending=False)
        .head(limit)
    )


def build_insights(sales: pd.DataFrame) -> list[str]:
    """Create a few plain-language observations from the current selection."""
    if sales.empty:
        return ["No transactions match the selected filters."]

    category_sales = sales.groupby("category")["revenue"].sum()
    region_sales = sales.groupby("region")["revenue"].sum()
    monthly = monthly_revenue(sales)
    strongest_month = monthly.loc[monthly["revenue"].idxmax(), "month"].strftime("%B %Y")
    return [
        f"{category_sales.idxmax()} is the highest-revenue category.",
        f"{region_sales.idxmax()} is the highest-revenue region.",
        f"The strongest month by revenue is {strongest_month}.",
    ]