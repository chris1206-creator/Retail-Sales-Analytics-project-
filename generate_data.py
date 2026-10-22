"""Create a reproducible sample retail transactions dataset."""

from pathlib import Path

import numpy as np
import pandas as pd


DATA_PATH = Path(__file__).parent / "data" / "retail_sales.csv"


def create_sales_data(rows: int = 5000, seed: int = 42) -> pd.DataFrame:
    """Return synthetic retail transactions spanning two years."""
    if rows < 1:
        raise ValueError("rows must be greater than zero")

    rng = np.random.default_rng(seed)
    products = {
        "Electronics": ["Wireless Mouse", "Headphones", "Keyboard", "USB Hub"],
        "Home": ["Desk Lamp", "Storage Box", "Water Bottle", "Throw Blanket"],
        "Clothing": ["T-Shirt", "Hoodie", "Socks", "Baseball Cap"],
        "Books": ["Cookbook", "Mystery Novel", "Travel Guide", "Sketchbook"],
    }
    prices = {
        "Wireless Mouse": 24.99,
        "Headphones": 59.99,
        "Keyboard": 44.99,
        "USB Hub": 19.99,
        "Desk Lamp": 34.99,
        "Storage Box": 14.99,
        "Water Bottle": 18.99,
        "Throw Blanket": 39.99,
        "T-Shirt": 22.99,
        "Hoodie": 49.99,
        "Socks": 9.99,
        "Baseball Cap": 17.99,
        "Cookbook": 27.99,
        "Mystery Novel": 16.99,
        "Travel Guide": 21.99,
        "Sketchbook": 12.99,
    }

    categories = list(products)
    category = rng.choice(categories, size=rows, p=[0.31, 0.27, 0.24, 0.18])
    product = [rng.choice(products[item]) for item in category]
    units = rng.integers(1, 6, size=rows)
    discount = rng.choice([0.0, 0.05, 0.10, 0.15, 0.20], size=rows, p=[0.48, 0.18, 0.17, 0.11, 0.06])
    unit_price = np.array([prices[item] for item in product])

    sales = pd.DataFrame(
        {
            "date": rng.choice(pd.date_range("2024-01-01", "2025-12-31"), size=rows),
            "order_id": [f"ORD-{number:05d}" for number in range(1, rows + 1)],
            "product": product,
            "category": category,
            "region": rng.choice(
                ["North", "South", "East", "West"],
                size=rows,
                p=[0.28, 0.23, 0.25, 0.24],
            ),
            "units": units,
            "unit_price": unit_price,
            "discount": discount,
        }
    )
    sales["date"] = pd.to_datetime(sales["date"])
    sales["revenue"] = (sales["units"] * sales["unit_price"] * (1 - sales["discount"])).round(2)
    return sales.sort_values("date").reset_index(drop=True)


def load_or_create_sales_data(path: Path = DATA_PATH) -> pd.DataFrame:
    """Load the CSV if present; otherwise generate and save it."""
    if path.exists():
        return pd.read_csv(path, parse_dates=["date"])

    sales = create_sales_data()
    path.parent.mkdir(parents=True, exist_ok=True)
    sales.to_csv(path, index=False)
    return sales


if __name__ == "__main__":
    sales = load_or_create_sales_data()
    print(f"Created {len(sales):,} transactions at {DATA_PATH}")