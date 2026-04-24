import pandas as pd


def load_data(file_path):
    return pd.read_csv(file_path)


def analyze_sales(df):
    df["Revenue"] = df["Price"] * df["Quantity"]

    total_revenue = df["Revenue"].sum()
    best_product = df.groupby("Product")["Revenue"].sum().idxmax()
    top_category = df.groupby("Category")["Revenue"].sum().idxmax()
    average_order_value = df["Revenue"].mean()

    return total_revenue, best_product, top_category, average_order_value


def product_summary(df):
    return (
        df.groupby("Product")
        .agg(
            total_quantity=("Quantity", "sum"),
            total_revenue=("Revenue", "sum")
        )
        .sort_values(by="total_revenue", ascending=False)
    )


def main():
    df = load_data("sales.csv")

    total_revenue, best_product, top_category, average_order_value = analyze_sales(df)

    print("=== Sales Analysis Report ===")
    print(f"Total Revenue: ${total_revenue:,.2f}")
    print(f"Best Product: {best_product}")
    print(f"Top Category: {top_category}")
    print(f"Average Order Value: ${average_order_value:,.2f}")

    print("\n=== Product Summary ===")
    print(product_summary(df))


if __name__ == "__main__":
    main()
