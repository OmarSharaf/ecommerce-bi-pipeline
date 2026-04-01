import pytest
import pandas as pd
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'etl'))

from extract import get_products, get_orders, get_customers
from transform import transform_orders, transform_customers, transform_exchange_rates


# ─── Extract Tests ────────────────────────────────────────────

class TestExtract:

    def test_get_products_returns_dataframe(self):
        df = get_products()
        assert isinstance(df, pd.DataFrame)
        assert len(df) > 0

    def test_get_products_has_required_columns(self):
        df = get_products()
        for col in ["id", "title", "price", "category"]:
            assert col in df.columns

    def test_get_orders_returns_correct_count(self):
        df = get_orders(10)
        assert len(df) == 10

    def test_get_orders_has_required_columns(self):
        df = get_orders(5)
        for col in ["order_id", "product_id", "price", "quantity", "customer_id", "order_date", "region", "status"]:
            assert col in df.columns

    def test_get_orders_status_values(self):
        df = get_orders(50)
        valid = {"Completed", "Pending", "Returned"}
        assert set(df["status"].unique()).issubset(valid)

    def test_get_customers_returns_correct_count(self):
        df = get_customers(20)
        assert len(df) == 20

    def test_get_customers_has_required_columns(self):
        df = get_customers(5)
        for col in ["customer_id", "name", "email", "segment", "signup_date"]:
            assert col in df.columns

    def test_get_customers_segment_values(self):
        df = get_customers(50)
        valid = {"VIP", "Regular", "New"}
        assert set(df["segment"].unique()).issubset(valid)


# ─── Transform Tests ──────────────────────────────────────────

class TestTransform:

    @pytest.fixture
    def sample_rates(self):
        return pd.DataFrame({
            "currency": ["USD", "EUR", "GBP", "EGP"],
            "rate":     [1.0,   0.92,  0.79,  48.5]
        })

    @pytest.fixture
    def sample_orders(self):
        return pd.DataFrame({
            "order_id":     [1, 2, 3],
            "product_id":   [10, 11, 12],
            "product_name": ["Prod A", "Prod B", "Prod C"],
            "category":     ["electronics", "jewelery", "men's clothing"],
            "price":        [100.0, 50.0, 75.0],
            "quantity":     [2, 1, 3],
            "customer_id":  [1, 2, 3],
            "order_date":   ["2024-01-15", "2024-03-20", "2024-06-10"],
            "region":       ["North", "South", "East"],
            "country":      ["Egypt", "USA", "UK"],
            "status":       ["Completed", "Returned", "Completed"]
        })

    def test_transform_orders_adds_revenue(self, sample_orders, sample_rates):
        df = transform_orders(sample_orders, sample_rates)
        assert "revenue_usd" in df.columns
        assert "revenue_eur" in df.columns

    def test_transform_orders_returned_revenue_is_zero(self, sample_orders, sample_rates):
        df = transform_orders(sample_orders, sample_rates)
        returned = df[df["status"] == "Returned"]["revenue_usd"]
        assert (returned == 0).all()

    def test_transform_orders_adds_date_dimensions(self, sample_orders, sample_rates):
        df = transform_orders(sample_orders, sample_rates)
        for col in ["year", "month", "quarter", "month_name"]:
            assert col in df.columns

    def test_transform_orders_category_is_title_case(self, sample_orders, sample_rates):
        df = transform_orders(sample_orders, sample_rates)
        assert df["category"].iloc[0] == "Electronics"

    def test_transform_customers_email_is_lowercase(self):
        customers = pd.DataFrame({
            "customer_id": [1],
            "name":        ["omar SHARAFELDIN"],
            "email":       ["OMAR@EXAMPLE.COM"],
            "phone":       ["123"],
            "country":     ["Egypt"],
            "segment":     ["VIP"],
            "signup_date": ["2023-01-01"]
        })
        df = transform_customers(customers)
        assert df["email"].iloc[0] == "omar@example.com"

    def test_transform_exchange_rates_filters_major(self, sample_rates):
        df = transform_exchange_rates(sample_rates)
        assert "USD" in df["currency"].values
        assert "EUR" in df["currency"].values
