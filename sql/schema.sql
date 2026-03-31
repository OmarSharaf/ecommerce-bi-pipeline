-- ============================================
-- Unified Sales Intelligence Dashboard
-- Schema Definition
-- Author: Omar Sharafeldin Mohamed Abdelfatah
-- ============================================

-- Customers Dimension
CREATE TABLE IF NOT EXISTS dim_customers (
    customer_id   SERIAL PRIMARY KEY,
    name          VARCHAR(100),
    email         VARCHAR(150) UNIQUE,
    phone         VARCHAR(50),
    country       VARCHAR(100),
    segment       VARCHAR(20) CHECK (segment IN ('VIP', 'Regular', 'New')),
    signup_date   DATE
);

-- Exchange Rates Dimension
CREATE TABLE IF NOT EXISTS dim_exchange_rates (
    currency      VARCHAR(10) PRIMARY KEY,
    rate          NUMERIC(12, 6)
);

-- Orders Fact Table
CREATE TABLE IF NOT EXISTS fact_orders (
    order_id      SERIAL PRIMARY KEY,
    product_id    INT,
    product_name  VARCHAR(255),
    category      VARCHAR(100),
    price         NUMERIC(10, 2),
    quantity      INT,
    customer_id   INT REFERENCES dim_customers(customer_id),
    order_date    DATE,
    region        VARCHAR(50),
    country       VARCHAR(100),
    status        VARCHAR(20) CHECK (status IN ('Completed', 'Pending', 'Returned')),
    revenue_usd   NUMERIC(12, 2),
    revenue_eur   NUMERIC(12, 2),
    year          INT,
    month         INT,
    month_name    VARCHAR(20),
    quarter       INT,
    week          INT
);

-- Indexes for Power BI performance
CREATE INDEX IF NOT EXISTS idx_orders_date     ON fact_orders(order_date);
CREATE INDEX IF NOT EXISTS idx_orders_category ON fact_orders(category);
CREATE INDEX IF NOT EXISTS idx_orders_region   ON fact_orders(region);
CREATE INDEX IF NOT EXISTS idx_orders_customer ON fact_orders(customer_id);
