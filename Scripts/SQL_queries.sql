-- ============================================================================
-- E-COMMERCE BUSINESS INTELLIGENCE SQL QUERIES
-- ============================================================================

USE ecommerce_db;

-- ============================================================================
-- 1. SALES PERFORMANCE QUERIES
-- ============================================================================

-- 1.1 Daily Sales Summary
SELECT 
    Transaction_Date,
    COUNT(*) as total_transactions,
    SUM(Purchase_Amount) as daily_revenue,
    AVG(Purchase_Amount) as avg_order_value,
    COUNT(DISTINCT User_Name) as unique_customers
FROM transactions
GROUP BY Transaction_Date
ORDER BY Transaction_Date DESC
LIMIT 30;

-- 1.2 Monthly Sales Performance
SELECT 
    Year,
    Month_Name,
    COUNT(*) as total_orders,
    SUM(Purchase_Amount) as total_revenue,
    AVG(Purchase_Amount) as avg_order_value,
    COUNT(DISTINCT User_Name) as unique_customers,
    SUM(Purchase_Amount) / COUNT(DISTINCT User_Name) as revenue_per_customer
FROM transactions
GROUP BY Year, Month, Month_Name
ORDER BY Year, Month;

-- 1.3 Year-over-Year Growth Analysis
SELECT 
    Year,
    SUM(Purchase_Amount) as annual_revenue,
    COUNT(*) as total_orders,
    LAG(SUM(Purchase_Amount)) OVER (ORDER BY Year) as previous_year_revenue,
    ROUND(
        ((SUM(Purchase_Amount) - LAG(SUM(Purchase_Amount)) OVER (ORDER BY Year)) / 
        LAG(SUM(Purchase_Amount)) OVER (ORDER BY Year)) * 100, 
        2
    ) as yoy_growth_percent
FROM transactions
GROUP BY Year
ORDER BY Year;

-- 1.4 Quarter Performance Comparison
SELECT 
    Year,
    Quarter,
    SUM(Purchase_Amount) as quarterly_revenue,
    COUNT(*) as total_orders,
    COUNT(DISTINCT User_Name) as unique_customers
FROM transactions
GROUP BY Year, Quarter
ORDER BY Year, Quarter;

-- ============================================================================
-- 2. PRODUCT ANALYSIS QUERIES
-- ============================================================================

-- 2.1 Top 10 Product Categories by Revenue
SELECT 
    Product_Category,
    COUNT(*) as total_orders,
    SUM(Purchase_Amount) as total_revenue,
    AVG(Purchase_Amount) as avg_order_value,
    ROUND(SUM(Purchase_Amount) / (SELECT SUM(Purchase_Amount) FROM transactions) * 100, 2) as revenue_percentage
FROM transactions
GROUP BY Product_Category
ORDER BY total_revenue DESC
LIMIT 10;

-- 2.2 Product Category Performance Trend (Last 6 Months)
SELECT 
    Product_Category,
    Month_Name,
    Year,
    SUM(Purchase_Amount) as monthly_revenue,
    COUNT(*) as order_count
FROM transactions
WHERE Transaction_Date >= DATE_SUB(CURDATE(), INTERVAL 6 MONTH)
GROUP BY Product_Category, Year, Month, Month_Name
ORDER BY Product_Category, Year, Month;

-- 2.3 Product Performance by Age Group
SELECT 
    Product_Category,
    Age_Group,
    COUNT(*) as purchases,
    SUM(Purchase_Amount) as total_revenue,
    AVG(Purchase_Amount) as avg_spent
FROM transactions
GROUP BY Product_Category, Age_Group
ORDER BY Product_Category, total_revenue DESC;

-- 2.4 Fastest Growing Categories (Last 3 Months)
SELECT 
    Product_Category,
    SUM(CASE WHEN Transaction_Date >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH) THEN Purchase_Amount ELSE 0 END) as last_month_revenue,
    SUM(CASE WHEN Transaction_Date >= DATE_SUB(CURDATE(), INTERVAL 2 MONTH) 
             AND Transaction_Date < DATE_SUB(CURDATE(), INTERVAL 1 MONTH) THEN Purchase_Amount ELSE 0 END) as prev_month_revenue,
    ROUND(
        ((SUM(CASE WHEN Transaction_Date >= DATE_SUB(CURDATE(), INTERVAL 1 MONTH) THEN Purchase_Amount ELSE 0 END) - 
          SUM(CASE WHEN Transaction_Date >= DATE_SUB(CURDATE(), INTERVAL 2 MONTH) 
             AND Transaction_Date < DATE_SUB(CURDATE(), INTERVAL 1 MONTH) THEN Purchase_Amount ELSE 0 END)) /
         NULLIF(SUM(CASE WHEN Transaction_Date >= DATE_SUB(CURDATE(), INTERVAL 2 MONTH) 
             AND Transaction_Date < DATE_SUB(CURDATE(), INTERVAL 1 MONTH) THEN Purchase_Amount ELSE 0 END), 0)) * 100,
        2
    ) as mom_growth_percent
FROM transactions
GROUP BY Product_Category
ORDER BY mom_growth_percent DESC;

-- ============================================================================
-- 3. CUSTOMER ANALYSIS QUERIES
-- ============================================================================

-- 3.1 Top 20 Customers by Revenue
SELECT 
    User_Name,
    COUNT(*) as total_purchases,
    SUM(Purchase_Amount) as total_spent,
    AVG(Purchase_Amount) as avg_order_value,
    MIN(Transaction_Date) as first_purchase,
    MAX(Transaction_Date) as last_purchase,
    DATEDIFF(MAX(Transaction_Date), MIN(Transaction_Date)) as customer_lifetime_days
FROM transactions
GROUP BY User_Name
ORDER BY total_spent DESC
LIMIT 20;

-- 3.2 Customer Segmentation by Purchase Frequency
SELECT 
    CASE 
        WHEN purchase_count = 1 THEN '1 Purchase (One-time)'
        WHEN purchase_count BETWEEN 2 AND 5 THEN '2-5 Purchases (Occasional)'
        WHEN purchase_count BETWEEN 6 AND 10 THEN '6-10 Purchases (Regular)'
        ELSE '11+ Purchases (Loyal)'
    END as customer_segment,
    COUNT(*) as num_customers,
    SUM(total_revenue) as segment_revenue,
    AVG(total_revenue) as avg_customer_value
FROM (
    SELECT 
        User_Name,
        COUNT(*) as purchase_count,
        SUM(Purchase_Amount) as total_revenue
    FROM transactions
    GROUP BY User_Name
) as customer_data
GROUP BY customer_segment
ORDER BY segment_revenue DESC;

-- 3.3 Customer Retention Analysis
SELECT 
    first_purchase_month,
    COUNT(DISTINCT User_Name) as customers,
    SUM(CASE WHEN months_since_first = 0 THEN 1 ELSE 0 END) as month_0,
    SUM(CASE WHEN months_since_first = 1 THEN 1 ELSE 0 END) as month_1,
    SUM(CASE WHEN months_since_first = 2 THEN 1 ELSE 0 END) as month_2,
    SUM(CASE WHEN months_since_first = 3 THEN 1 ELSE 0 END) as month_3
FROM (
    SELECT 
        User_Name,
        DATE_FORMAT(MIN(Transaction_Date), '%Y-%m') as first_purchase_month,
        DATE_FORMAT(Transaction_Date, '%Y-%m') as purchase_month,
        PERIOD_DIFF(
            EXTRACT(YEAR_MONTH FROM Transaction_Date),
            EXTRACT(YEAR_MONTH FROM MIN(Transaction_Date) OVER (PARTITION BY User_Name))
        ) as months_since_first
    FROM transactions
) as cohort_data
GROUP BY first_purchase_month
ORDER BY first_purchase_month;

-- 3.4 Customer Lifetime Value (CLV) Calculation
SELECT 
    User_Name,
    COUNT(*) as num_purchases,
    SUM(Purchase_Amount) as total_revenue,
    AVG(Purchase_Amount) as avg_order_value,
    MIN(Transaction_Date) as first_purchase_date,
    MAX(Transaction_Date) as last_purchase_date,
    DATEDIFF(MAX(Transaction_Date), MIN(Transaction_Date)) as lifespan_days,
    ROUND(
        COUNT(*) / NULLIF((DATEDIFF(MAX(Transaction_Date), MIN(Transaction_Date)) / 30), 0),
        2
    ) as purchases_per_month,
    ROUND(
        AVG(Purchase_Amount) * (COUNT(*) / NULLIF((DATEDIFF(MAX(Transaction_Date), MIN(Transaction_Date)) / 30), 0)) * 12,
        2
    ) as estimated_clv
FROM transactions
GROUP BY User_Name
HAVING num_purchases > 1
ORDER BY estimated_clv DESC
LIMIT 50;

-- 3.5 New vs Returning Customers by Month
SELECT 
    DATE_FORMAT(t.Transaction_Date, '%Y-%m') as month,
    COUNT(DISTINCT CASE WHEN customer_type = 'New' THEN t.User_Name END) as new_customers,
    COUNT(DISTINCT CASE WHEN customer_type = 'Returning' THEN t.User_Name END) as returning_customers,
    COUNT(DISTINCT t.User_Name) as total_customers
FROM transactions t
JOIN (
    SELECT 
        User_Name,
        MIN(Transaction_Date) as first_purchase_date
    FROM transactions
    GROUP BY User_Name
) first_purchase
ON t.User_Name = first_purchase.User_Name
CROSS APPLY(
    SELECT 
        CASE 
            WHEN DATE_FORMAT(t.Transaction_Date, '%Y-%m') = DATE_FORMAT(first_purchase.first_purchase_date, '%Y-%m') 
            THEN 'New'
            ELSE 'Returning'
        END as customer_type
) customer_classification
GROUP BY DATE_FORMAT(t.Transaction_Date, '%Y-%m')
ORDER BY month;

-- ============================================================================
-- 4. GEOGRAPHICAL ANALYSIS
-- ============================================================================

-- 4.1 Revenue by Country
SELECT 
    Country,
    COUNT(*) as total_orders,
    SUM(Purchase_Amount) as total_revenue,
    AVG(Purchase_Amount) as avg_order_value,
    COUNT(DISTINCT User_Name) as unique_customers,
    ROUND(SUM(Purchase_Amount) / (SELECT SUM(Purchase_Amount) FROM transactions) * 100, 2) as revenue_percentage
FROM transactions
GROUP BY Country
ORDER BY total_revenue DESC;

-- 4.2 Top Product Categories by Country
SELECT 
    Country,
    Product_Category,
    SUM(Purchase_Amount) as revenue,
    COUNT(*) as orders,
    ROW_NUMBER() OVER (PARTITION BY Country ORDER BY SUM(Purchase_Amount) DESC) as category_rank
FROM transactions
GROUP BY Country, Product_Category
HAVING category_rank <= 3
ORDER BY Country, category_rank;

-- 4.3 Country Performance Trend
SELECT 
    Country,
    Month_Name,
    Year,
    SUM(Purchase_Amount) as monthly_revenue,
    COUNT(*) as order_count
FROM transactions
WHERE Transaction_Date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)
GROUP BY Country, Year, Month, Month_Name
ORDER BY Country, Year, Month;

-- ============================================================================
-- 5. PAYMENT METHOD ANALYSIS
-- ============================================================================

-- 5.1 Payment Method Performance
SELECT 
    Payment_Method,
    COUNT(*) as transaction_count,
    SUM(Purchase_Amount) as total_revenue,
    AVG(Purchase_Amount) as avg_transaction_value,
    MIN(Purchase_Amount) as min_transaction,
    MAX(Purchase_Amount) as max_transaction,
    ROUND(COUNT(*) / (SELECT COUNT(*) FROM transactions) * 100, 2) as usage_percentage
FROM transactions
GROUP BY Payment_Method
ORDER BY total_revenue DESC;

-- 5.2 Payment Method by Age Group
SELECT 
    Age_Group,
    Payment_Method,
    COUNT(*) as usage_count,
    ROUND(COUNT(*) * 100.0 / SUM(COUNT(*)) OVER (PARTITION BY Age_Group), 2) as percentage_within_age_group
FROM transactions
GROUP BY Age_Group, Payment_Method
ORDER BY Age_Group, usage_count DESC;

-- 5.3 Payment Method Trend Over Time
SELECT 
    DATE_FORMAT(Transaction_Date, '%Y-%m') as month,
    Payment_Method,
    COUNT(*) as transactions,
    SUM(Purchase_Amount) as revenue
FROM transactions
WHERE Transaction_Date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)
GROUP BY DATE_FORMAT(Transaction_Date, '%Y-%m'), Payment_Method
ORDER BY month, Payment_Method;

-- ============================================================================
-- 6. TIME-BASED ANALYSIS
-- ============================================================================

-- 6.1 Sales by Day of Week
SELECT 
    Day_of_Week,
    COUNT(*) as total_transactions,
    SUM(Purchase_Amount) as total_revenue,
    AVG(Purchase_Amount) as avg_order_value,
    ROUND(AVG(Purchase_Amount), 2) as avg_transaction
FROM transactions
GROUP BY Day_of_Week,
    CASE Day_of_Week
        WHEN 'Monday' THEN 1
        WHEN 'Tuesday' THEN 2
        WHEN 'Wednesday' THEN 3
        WHEN 'Thursday' THEN 4
        WHEN 'Friday' THEN 5
        WHEN 'Saturday' THEN 6
        WHEN 'Sunday' THEN 7
    END
ORDER BY 
    CASE Day_of_Week
        WHEN 'Monday' THEN 1
        WHEN 'Tuesday' THEN 2
        WHEN 'Wednesday' THEN 3
        WHEN 'Thursday' THEN 4
        WHEN 'Friday' THEN 5
        WHEN 'Saturday' THEN 6
        WHEN 'Sunday' THEN 7
    END;

-- 6.2 Weekend vs Weekday Performance
SELECT 
    CASE 
        WHEN Is_Weekend = 1 THEN 'Weekend'
        ELSE 'Weekday'
    END as day_type,
    COUNT(*) as total_transactions,
    SUM(Purchase_Amount) as total_revenue,
    AVG(Purchase_Amount) as avg_order_value,
    COUNT(DISTINCT User_Name) as unique_customers
FROM transactions
GROUP BY Is_Weekend
ORDER BY Is_Weekend;

-- 6.3 Best Performing Day-Category Combinations
SELECT 
    Day_of_Week,
    Product_Category,
    COUNT(*) as transactions,
    SUM(Purchase_Amount) as revenue,
    ROW_NUMBER() OVER (PARTITION BY Day_of_Week ORDER BY SUM(Purchase_Amount) DESC) as rank_per_day
FROM transactions
GROUP BY Day_of_Week, Product_Category
HAVING rank_per_day <= 3
ORDER BY Day_of_Week, rank_per_day;

-- ============================================================================
-- 7. ADVANCED BUSINESS INSIGHTS
-- ============================================================================

-- 7.1 Market Basket Analysis - Which categories are often purchased together
SELECT 
    t1.Product_Category as category_1,
    t2.Product_Category as category_2,
    COUNT(DISTINCT t1.User_Name) as customers,
    COUNT(*) as co_purchases
FROM transactions t1
JOIN transactions t2 
    ON t1.User_Name = t2.User_Name 
    AND t1.Product_Category < t2.Product_Category
GROUP BY t1.Product_Category, t2.Product_Category
HAVING co_purchases >= 5
ORDER BY co_purchases DESC
LIMIT 20;

-- 7.2 Churn Risk Analysis - Customers who haven't purchased recently
SELECT 
    User_Name,
    MAX(Transaction_Date) as last_purchase_date,
    DATEDIFF(CURDATE(), MAX(Transaction_Date)) as days_since_purchase,
    COUNT(*) as total_purchases,
    SUM(Purchase_Amount) as lifetime_value,
    CASE 
        WHEN DATEDIFF(CURDATE(), MAX(Transaction_Date)) > 180 THEN 'High Risk'
        WHEN DATEDIFF(CURDATE(), MAX(Transaction_Date)) > 90 THEN 'Medium Risk'
        WHEN DATEDIFF(CURDATE(), MAX(Transaction_Date)) > 30 THEN 'Low Risk'
        ELSE 'Active'
    END as churn_risk
FROM transactions
GROUP BY User_Name
HAVING churn_risk IN ('High Risk', 'Medium Risk')
ORDER BY lifetime_value DESC;

-- 7.3 Revenue Concentration Analysis (Pareto Principle)
SELECT 
    customer_rank,
    COUNT(*) as num_customers,
    SUM(total_spent) as total_revenue,
    ROUND(SUM(total_spent) / (SELECT SUM(Purchase_Amount) FROM transactions) * 100, 2) as revenue_percentage,
    ROUND(SUM(SUM(total_spent)) OVER (ORDER BY customer_rank) / (SELECT SUM(Purchase_Amount) FROM transactions) * 100, 2) as cumulative_percentage
FROM (
    SELECT 
        User_Name,
        SUM(Purchase_Amount) as total_spent,
        NTILE(10) OVER (ORDER BY SUM(Purchase_Amount) DESC) as customer_rank
    FROM transactions
    GROUP BY User_Name
) ranked_customers
GROUP BY customer_rank
ORDER BY customer_rank;

-- 7.4 Customer Purchase Patterns - Time Between Purchases
SELECT 
    User_Name,
    COUNT(*) as num_purchases,
    MIN(Transaction_Date) as first_purchase,
    MAX(Transaction_Date) as last_purchase,
    AVG(days_between_purchases) as avg_days_between_purchases,
    CASE 
        WHEN AVG(days_between_purchases) <= 30 THEN 'Frequent Buyer'
        WHEN AVG(days_between_purchases) <= 60 THEN 'Regular Buyer'
        WHEN AVG(days_between_purchases) <= 90 THEN 'Occasional Buyer'
        ELSE 'Rare Buyer'
    END as purchase_frequency_segment
FROM (
    SELECT 
        User_Name,
        Transaction_Date,
        LAG(Transaction_Date) OVER (PARTITION BY User_Name ORDER BY Transaction_Date) as prev_purchase_date,
        DATEDIFF(Transaction_Date, LAG(Transaction_Date) OVER (PARTITION BY User_Name ORDER BY Transaction_Date)) as days_between_purchases
    FROM transactions
) purchase_intervals
WHERE days_between_purchases IS NOT NULL
GROUP BY User_Name
HAVING num_purchases > 1
ORDER BY avg_days_between_purchases;

-- ============================================================================
-- 8. EXECUTIVE SUMMARY QUERIES
-- ============================================================================

-- 8.1 Overall Business Health Dashboard
SELECT 
    COUNT(*) as total_transactions,
    COUNT(DISTINCT User_Name) as total_customers,
    SUM(Purchase_Amount) as total_revenue,
    AVG(Purchase_Amount) as avg_order_value,
    MIN(Transaction_Date) as business_start_date,
    MAX(Transaction_Date) as latest_transaction_date,
    COUNT(DISTINCT Product_Category) as num_product_categories,
    COUNT(DISTINCT Country) as num_countries_served
FROM transactions;

-- 8.2 Monthly KPI Summary
SELECT 
    DATE_FORMAT(Transaction_Date, '%Y-%m') as month,
    COUNT(*) as total_orders,
    COUNT(DISTINCT User_Name) as unique_customers,
    SUM(Purchase_Amount) as revenue,
    AVG(Purchase_Amount) as avg_order_value,
    SUM(Purchase_Amount) / COUNT(DISTINCT User_Name) as revenue_per_customer
FROM transactions
WHERE Transaction_Date >= DATE_SUB(CURDATE(), INTERVAL 12 MONTH)
GROUP BY DATE_FORMAT(Transaction_Date, '%Y-%m')
ORDER BY month DESC;

-- ============================================================================
-- END OF QUERIES
-- ============================================================================

