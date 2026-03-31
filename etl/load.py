import os
import pandas as pd
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

from extract import get_orders, get_exchange_rates, get_customers
from transform import transform_orders, transform_customers, transform_exchange_rates

load_dotenv()

DB_URL = (
    f"postgresql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}"
    f"@{os.getenv('DB_HOST', 'localhost')}:{os.getenv('DB_PORT', '5432')}"
    f"/{os.getenv('DB_NAME')}"
)


def load_to_db(df: pd.DataFrame, table_name: str, engine):
    """Load a DataFrame into PostgreSQL."""
    df.to_sql(table_name, engine, if_exists="replace", index=False)
    print(f"  ✅ {len(df):,} rows → '{table_name}'")


def run_pipeline():
    print("🚀 Starting ETL Pipeline...\n")

    # --- Extract ---
    print("📥 Extracting data...")
    rates     = get_exchange_rates()
    orders    = get_orders(500)
    customers = get_customers(100)

    # --- Transform ---
    print("\n🔄 Transforming data...")
    orders    = transform_orders(orders, rates)
    customers = transform_customers(customers)
    rates     = transform_exchange_rates(rates)

    # --- Load ---
    print("\n📤 Loading to PostgreSQL...")
    engine = create_engine(DB_URL)

    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
        print("  🔗 DB connection successful")

    load_to_db(orders,    "fact_orders",         engine)
    load_to_db(customers, "dim_customers",        engine)
    load_to_db(rates,     "dim_exchange_rates",   engine)

    print("\n✅ Pipeline completed successfully!")


if __name__ == "__main__":
    run_pipeline()
