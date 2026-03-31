import pandas as pd


def transform_orders(orders_df: pd.DataFrame, rates_df: pd.DataFrame) -> pd.DataFrame:
    """Clean and enrich orders with revenue and date dimensions."""

    # Revenue in USD
    orders_df["revenue_usd"] = (orders_df["price"] * orders_df["quantity"]).round(2)

    # Revenue in EUR
    eur_rate = rates_df.loc[rates_df["currency"] == "EUR", "rate"].values
    if len(eur_rate) > 0:
        orders_df["revenue_eur"] = (orders_df["revenue_usd"] * eur_rate[0]).round(2)
    else:
        orders_df["revenue_eur"] = None

    # Date dimensions
    orders_df["order_date"] = pd.to_datetime(orders_df["order_date"])
    orders_df["year"]       = orders_df["order_date"].dt.year
    orders_df["month"]      = orders_df["order_date"].dt.month
    orders_df["month_name"] = orders_df["order_date"].dt.strftime("%B")
    orders_df["quarter"]    = orders_df["order_date"].dt.quarter
    orders_df["week"]       = orders_df["order_date"].dt.isocalendar().week.astype(int)

    # Clean category names
    orders_df["category"] = orders_df["category"].str.title().str.strip()

    # Drop returned orders from revenue calc
    orders_df["revenue_usd"] = orders_df.apply(
        lambda r: 0 if r["status"] == "Returned" else r["revenue_usd"], axis=1
    )

    return orders_df


def transform_customers(customers_df: pd.DataFrame) -> pd.DataFrame:
    """Clean customers data."""
    customers_df["signup_date"] = pd.to_datetime(customers_df["signup_date"])
    customers_df["name"]        = customers_df["name"].str.strip().str.title()
    customers_df["email"]       = customers_df["email"].str.lower().str.strip()
    return customers_df


def transform_exchange_rates(rates_df: pd.DataFrame) -> pd.DataFrame:
    """Filter to major currencies only."""
    major = ["USD", "EUR", "GBP", "JPY", "AED", "SAR", "EGP", "CAD", "AUD"]
    return rates_df[rates_df["currency"].isin(major)].reset_index(drop=True)


if __name__ == "__main__":
    from extract import get_orders, get_exchange_rates, get_customers

    rates     = get_exchange_rates()
    orders    = get_orders(20)
    customers = get_customers(5)

    orders    = transform_orders(orders, rates)
    customers = transform_customers(customers)
    rates     = transform_exchange_rates(rates)

    print("✅ Orders transformed:\n", orders[["order_id","revenue_usd","revenue_eur","quarter"]].head())
    print("\n✅ Customers transformed:\n", customers.head())
    print("\n✅ Rates filtered:\n", rates)
