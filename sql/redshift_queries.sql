-- 1. Daily revenue

SELECT 
    order_date,
    COUNT(order_id) AS total_orders,
    SUM(total_amount) AS total_revenue
FROM ecommerce_lakehouse.curated_orders
GROUP BY order_date
ORDER BY order_date;


-- 2. Revenue per product

SELECT 
    product_id,
    COUNT(order_id) AS total_orders,
    SUM(total_amount) AS total_revenue
FROM ecommerce_lakehouse.curated_orders
GROUP BY product_id
ORDER BY total_revenue DESC;


-- 3. Top 10 products by revenue

SELECT 
    product_id,
    COUNT(order_id) AS total_orders,
    SUM(total_amount) AS total_revenue
FROM ecommerce_lakehouse.curated_orders
GROUP BY product_id
ORDER BY total_revenue DESC
LIMIT 10;


-- 4. Revenue by hour of day

SELECT 
    hour_of_day,
    COUNT(order_id) AS total_orders,
    SUM(total_amount) AS total_revenue
FROM ecommerce_lakehouse.curated_orders
GROUP BY hour_of_day
ORDER BY hour_of_day;


-- 5. Orders and revenue by status

SELECT 
    status,
    COUNT(order_id) AS total_orders,
    SUM(total_amount) AS total_revenue,
    ROUND(100.0 * COUNT(order_id) / SUM(COUNT(order_id)) OVER (), 2) AS pct_of_total_orders
FROM ecommerce_lakehouse.curated_orders
GROUP BY status
ORDER BY total_revenue DESC;


-- 6. Top 5 customers by total revenue

SELECT 
    customer_id,
    COUNT(order_id) AS total_orders,
    SUM(total_amount) AS total_revenue
FROM ecommerce_lakehouse.curated_orders
GROUP BY customer_id
ORDER BY total_revenue DESC
LIMIT 5;


-- 7. Average order value (AOV) per day

SELECT 
    order_date,
    COUNT(order_id) AS total_orders,
    ROUND(SUM(total_amount), 2) AS total_revenue,
    ROUND(SUM(total_amount) / COUNT(order_id), 2) AS avg_order_value
FROM ecommerce_lakehouse.curated_orders
GROUP BY order_date
ORDER BY order_date;


-- 8. Orders and revenue by day of week

SELECT 
    EXTRACT(DOW FROM order_timestamp) AS day_of_week,  -- 0 = Sunday, 1 = Monday, ..., 6 = Saturday
    COUNT(order_id) AS total_orders,
    SUM(total_amount) AS total_revenue
FROM ecommerce_lakehouse.curated_orders
GROUP BY day_of_week
ORDER BY day_of_week;