import requests
import pandas as pd
from faker import Faker
import random
import os
from dotenv import load_dotenv

load_dotenv()
fake = Faker()


def get_products():
    """Fetch products from Fake Store API."""
    r = requests.get("https://fakestoreapi.com/products")
    r.raise_for_status()
    return pd.DataFrame(r.json())


def get_orders(n=500):
    """Generate synthetic orders based on real products."""
    products = get_products()
    orders = []
    for i in range(n):
        product = products.sample(1).iloc[0]
        orders.append({
            "order_id":     i + 1,
            "product_id":   product["id"],
            "product_name": product["title"],
            "category":     product["category"],
            "price":        product["price"],
            "quantity":     random.randint(1, 10),
            "customer_id":  random.randint(1, 100),
            "order_date":   fake.date_between("-1y", "today"),
            "region":       random.choice(["North", "South", "East", "West"]),
            "country":      fake.country(),
            "status":       random.choice(["Completed", "Pending", "Returned"])
        })
    return pd.DataFrame(orders)


def get_exchange_rates():
    """Fetch latest exchange rates from ExchangeRate API."""
    api_key = os.getenv("EXCHANGE_API_KEY", "")
    url = f"https://v6.exchangerate-api.com/v6/{api_key}/latest/USD"
    r = requests.get(url)
    r.raise_for_status()
    rates = r.json().get("conversion_rates", {})
    return pd.DataFrame(rates.items(), columns=["currency", "rate"])


def get_customers(n=100):
    """Generate synthetic customer data."""
    customers = []
    for i in range(n):
        customers.append({
            "customer_id":  i + 1,
            "name":         fake.name(),
            "email":        fake.email(),
            "phone":        fake.phone_number(),
            "country":      fake.country(),
            "segment":      random.choice(["VIP", "Regular", "New"]),
            "signup_date":  fake.date_between("-2y", "-6m")
        })
    return pd.DataFrame(customers)


if __name__ == "__main__":
    print("📦 Extracting products...")
    print(get_products().head())

    print("\n🛒 Extracting orders...")
    print(get_orders(10).head())

    print("\n💱 Extracting exchange rates...")
    print(get_exchange_rates().head())

    print("\n👤 Extracting customers...")
    print(get_customers(5).head())
