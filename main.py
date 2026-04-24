"""
Advanced Sales Data Analyzer
Author: Remas Alshahrani

This project analyzes sales data using Python and pandas.
It calculates revenue, identifies top-performing products/categories,
and prints a clean business summary.
"""

from __future__ import annotations

import pandas as pd


def load_data(file_path: str) -> pd.DataFrame:
    """Load sales data from a CSV file."""
    return pd.read_csv(file_path)


def prepare_data(df: pd.DataFrame) -> pd.DataFrame:
    """Clean and prepare data for analysis."""
    required_columns = {"OrderID", "Product", "Category", "Price", "Quantity"}
    missing_columns = required_columns - set(df.columns)

    if missing_columns:
        raise ValueError(f"Missing columns: {missing_columns}")

    df = df.copy()
    df["Price"] = pd.to_numeric(df["Price"], errors="coerce")
    df["Quantity"] = pd.to_numeric(df["Quantity"], errors="coerce")
    df = df.dropna(subset=["Price", "Quantity"])
    df = df[(df["Price"] > 0) & (df["Quantity"] > 0)]
    df["Revenue"] = df["Price"] * df["Quantity"]

    return df


def analyze_sales(df: pd.DataFrame) -> dict[str, object]:
    """Generate key business insights from the sales data."""
    return {
        "total_revenue": df["Revenue"].sum(),
        "best_product": df.groupby("Product")["Revenue"].sum().idxmax(),
        "top_category": df.groupby("Category")["Revenue"].sum().idxmax(),
        "average_order_value": df["Revenue"].mean(),
    }


def product_summary(df: pd.DataFrame) -> pd.DataFrame:
    """Create a product-level sales summary."""
    return (
        df.groupby("Product")
        .agg(
            total_quantity=("Quantity", "sum"),
            total_revenue=("Revenue", "sum"),
        )
        .sort_values(by="total_revenue", ascending=False)
    )


def main() -> None:
    df = load_data("sales.csv")
    df = prepare_data(df)
    insights = analyze_sales(df)
    summary = product_summary(df)

    print("\n=== Advanced Sales Data Analyzer ===")
    print(f"Total Revenue: ${insights['total_revenue']:,.2f}")
    print(f"Best Product: {insights['best_product']}")
    print(f"Top Category: {insights['top_category']}")
    print(f"Average Order Value: ${insights['average_order_value']:,.2f}")

    print("\n=== Product Summary ===")
    print(summary)


if __name__ == "__main__":
    main()
