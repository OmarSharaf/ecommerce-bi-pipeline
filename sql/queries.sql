-- ============================================
-- KPI Queries for Power BI
-- Author: Omar Sharafeldin Mohamed Abdelfatah
-- ============================================

-- 1. Total Revenue (USD)
SELECT ROUND(SUM(revenue_usd), 2) AS total_revenue_usd
FROM fact_orders
WHERE status = 'Completed';

-- 2. Total Orders
SELECT COUNT(*) AS total_orders
FROM fact_orders;

-- 3. Average Order Value
SELECT ROUND(AVG(revenue_usd), 2) AS avg_order_value
FROM fact_orders
WHERE status = 'Completed';

-- 4. Revenue by Category
SELECT
    category,
    COUNT(*)                    AS total_orders,
    ROUND(SUM(revenue_usd), 2)  AS total_revenue
FROM fact_orders
WHERE status = 'Completed'
GROUP BY category
ORDER BY total_revenue DESC;

-- 5. Monthly Revenue Trend
SELECT
    year,
    month,
    month_name,
    ROUND(SUM(revenue_usd), 2) AS monthly_revenue
FROM fact_orders
WHERE status = 'Completed'
GROUP BY year, month, month_name
ORDER BY year, month;

-- 6. Revenue by Region
SELECT
    region,
    ROUND(SUM(revenue_usd), 2) AS total_revenue,
    COUNT(*)                    AS total_orders
FROM fact_orders
WHERE status = 'Completed'
GROUP BY region
ORDER BY total_revenue DESC;

-- 7. Top 10 Products by Revenue
SELECT
    product_name,
    category,
    SUM(quantity)               AS units_sold,
    ROUND(SUM(revenue_usd), 2)  AS total_revenue
FROM fact_orders
WHERE status = 'Completed'
GROUP BY product_name, category
ORDER BY total_revenue DESC
LIMIT 10;

-- 8. Customer Segments Distribution
SELECT
    segment,
    COUNT(*) AS customer_count
FROM dim_customers
GROUP BY segment;

-- 9. Top 10 Customers by Revenue
SELECT
    c.name,
    c.segment,
    c.country,
    ROUND(SUM(o.revenue_usd), 2) AS total_spent
FROM fact_orders o
JOIN dim_customers c ON o.customer_id = c.customer_id
WHERE o.status = 'Completed'
GROUP BY c.name, c.segment, c.country
ORDER BY total_spent DESC
LIMIT 10;

-- 10. MoM Revenue Growth
WITH monthly AS (
    SELECT
        year, month,
        SUM(revenue_usd) AS revenue
    FROM fact_orders
    WHERE status = 'Completed'
    GROUP BY year, month
)
SELECT
    year, month, revenue,
    LAG(revenue) OVER (ORDER BY year, month) AS prev_month_revenue,
    ROUND(
        (revenue - LAG(revenue) OVER (ORDER BY year, month))
        / NULLIF(LAG(revenue) OVER (ORDER BY year, month), 0) * 100, 2
    ) AS mom_growth_pct
FROM monthly
ORDER BY year, month;
