# SQL Sales Analysis - Query Reference Guide

This guide provides SQL queries for comprehensive sales data analysis using SQLite.

## Database Schema

### sales table
- `Product_ID` - Unique product identifier
- `Sale_Date` - Date of sale
- `Sales_Rep` - Name of sales representative
- `Region` - Geographic region (North, South, East, West)
- `Sales_Amount` - Total sale amount
- `Quantity_Sold` - Number of units sold
- `Product_Category` - Product category (Furniture, Food, Clothing, Electronics)
- `Unit_Cost` - Cost per unit
- `Unit_Price` - Selling price per unit
- `Customer_Type` - New or Returning customer
- `Discount` - Discount applied (as decimal)
- `Payment_Method` - Payment type (Cash, Credit Card, Bank Transfer)
- `Sales_Channel` - Sales channel (Online, Retail)

---

## Core Analysis Queries

### 1. Revenue Analysis by Region
```sql
SELECT 
    Region,
    COUNT(*) as Transaction_Count,
    SUM(Sales_Amount) as Total_Revenue,
    AVG(Sales_Amount) as Avg_Sales,
    MIN(Sales_Amount) as Min_Sales,
    MAX(Sales_Amount) as Max_Sales
FROM sales
GROUP BY Region
ORDER BY Total_Revenue DESC;
```

### 2. Sales Representative Performance
```sql
SELECT 
    Sales_Rep,
    Region,
    COUNT(*) as Total_Transactions,
    SUM(Sales_Amount) as Total_Sales,
    AVG(Sales_Amount) as Avg_Transaction,
    SUM(Quantity_Sold) as Total_Items_Sold,
    ROUND(AVG(Discount) * 100, 2) as Avg_Discount_Percent
FROM sales
GROUP BY Sales_Rep, Region
ORDER BY Total_Sales DESC;
```

### 3. Product Category Revenue Breakdown
```sql
SELECT 
    Product_Category,
    COUNT(*) as Sales_Count,
    SUM(Sales_Amount) as Total_Revenue,
    AVG(Sales_Amount) as Avg_Sale_Value,
    SUM(Quantity_Sold) as Total_Units_Sold,
    ROUND(SUM(Sales_Amount) * 100.0 / (SELECT SUM(Sales_Amount) FROM sales), 2) as Revenue_Percentage
FROM sales
GROUP BY Product_Category
ORDER BY Total_Revenue DESC;
```

### 4. Monthly Revenue Trend
```sql
SELECT 
    strftime('%Y-%m', Sale_Date) as Month,
    COUNT(*) as Transaction_Count,
    SUM(Sales_Amount) as Monthly_Revenue,
    AVG(Sales_Amount) as Avg_Transaction_Value,
    SUM(Quantity_Sold) as Total_Units
FROM sales
GROUP BY strftime('%Y-%m', Sale_Date)
ORDER BY Month;
```

### 5. Customer Type Analysis
```sql
SELECT 
    Customer_Type,
    COUNT(*) as Customer_Count,
    SUM(Sales_Amount) as Total_Revenue,
    AVG(Sales_Amount) as Avg_Purchase_Value,
    ROUND(AVG(Discount) * 100, 2) as Avg_Discount_Percent
FROM sales
GROUP BY Customer_Type
ORDER BY Total_Revenue DESC;
```

### 6. Sales Channel Comparison (Online vs Retail)
```sql
SELECT 
    Sales_Channel,
    COUNT(*) as Transaction_Count,
    SUM(Sales_Amount) as Total_Revenue,
    AVG(Sales_Amount) as Avg_Transaction,
    SUM(Quantity_Sold) as Total_Units,
    ROUND(SUM(Sales_Amount) * 100.0 / (SELECT SUM(Sales_Amount) FROM sales), 2) as Revenue_Share
FROM sales
GROUP BY Sales_Channel
ORDER BY Total_Revenue DESC;
```

### 7. Payment Method Analysis
```sql
SELECT 
    Payment_Method,
    COUNT(*) as Transaction_Count,
    SUM(Sales_Amount) as Total_Revenue,
    AVG(Sales_Amount) as Avg_Amount,
    MIN(Sales_Amount) as Min_Amount,
    MAX(Sales_Amount) as Max_Amount
FROM sales
GROUP BY Payment_Method
ORDER BY Total_Revenue DESC;
```

---

## Profitability Analysis

### 8. Profit Margin Analysis by Category
```sql
SELECT 
    Product_Category,
    COUNT(*) as Sales_Count,
    ROUND(AVG(Unit_Cost), 2) as Avg_Cost,
    ROUND(AVG(Unit_Price), 2) as Avg_Price,
    ROUND(AVG(Unit_Price - Unit_Cost), 2) as Avg_Profit_Per_Unit,
    ROUND(AVG((Unit_Price - Unit_Cost) / Unit_Price * 100), 2) as Profit_Margin_Percent,
    SUM(Quantity_Sold * (Unit_Price - Unit_Cost)) as Total_Profit
FROM sales
GROUP BY Product_Category
ORDER BY Total_Profit DESC;
```

### 9. Top 10 Products by Revenue
```sql
SELECT 
    Product_ID,
    Product_Category,
    COUNT(*) as Sales_Count,
    SUM(Sales_Amount) as Total_Revenue,
    SUM(Quantity_Sold) as Units_Sold,
    ROUND(AVG(Sales_Amount), 2) as Avg_Sale_Value
FROM sales
GROUP BY Product_ID, Product_Category
ORDER BY Total_Revenue DESC
LIMIT 10;
```

### 10. Profit by Region
```sql
SELECT 
    Region,
    COUNT(*) as Transaction_Count,
    SUM(Sales_Amount) as Total_Revenue,
    ROUND(SUM(Quantity_Sold * (Unit_Price - Unit_Cost)), 2) as Total_Profit,
    ROUND(SUM(Quantity_Sold * (Unit_Price - Unit_Cost)) / SUM(Sales_Amount) * 100, 2) as Profit_Margin_Percent
FROM sales
GROUP BY Region
ORDER BY Total_Profit DESC;
```

---

## Temporal Analysis

### 11. Seasonal Analysis (Quarterly)
```sql
SELECT 
    strftime('%Y', Sale_Date) as Year,
    'Q' || CAST(((strftime('%m', Sale_Date) - 1) / 3) + 1 AS INTEGER) as Quarter,
    COUNT(*) as Transaction_Count,
    SUM(Sales_Amount) as Quarterly_Revenue,
    AVG(Sales_Amount) as Avg_Transaction
FROM sales
GROUP BY Year, Quarter
ORDER BY Year, Quarter;
```

### 12. Day of Week Analysis
```sql
SELECT 
    CASE CAST(strftime('%w', Sale_Date) AS INTEGER)
        WHEN 0 THEN 'Sunday'
        WHEN 1 THEN 'Monday'
        WHEN 2 THEN 'Tuesday'
        WHEN 3 THEN 'Wednesday'
        WHEN 4 THEN 'Thursday'
        WHEN 5 THEN 'Friday'
        WHEN 6 THEN 'Saturday'
    END as Day_of_Week,
    COUNT(*) as Transaction_Count,
    SUM(Sales_Amount) as Total_Sales,
    AVG(Sales_Amount) as Avg_Sale,
    SUM(Quantity_Sold) as Total_Units
FROM sales
GROUP BY strftime('%w', Sale_Date)
ORDER BY CAST(strftime('%w', Sale_Date) AS INTEGER);
```

### 13. Daily Sales Trend
```sql
SELECT 
    Sale_Date,
    COUNT(*) as Transaction_Count,
    SUM(Sales_Amount) as Daily_Revenue,
    AVG(Sales_Amount) as Avg_Transaction,
    SUM(Quantity_Sold) as Total_Units
FROM sales
GROUP BY Sale_Date
ORDER BY Sale_Date;
```

---

## Discount Analysis

### 14. Discount Impact on Sales
```sql
SELECT 
    CASE 
        WHEN Discount = 0 THEN 'No Discount'
        WHEN Discount < 0.1 THEN '0-10%'
        WHEN Discount < 0.2 THEN '10-20%'
        ELSE '20%+'
    END as Discount_Range,
    COUNT(*) as Transaction_Count,
    ROUND(AVG(Discount) * 100, 2) as Avg_Discount_Percent,
    SUM(Sales_Amount) as Total_Sales,
    AVG(Sales_Amount) as Avg_Sale_Amount,
    AVG(Quantity_Sold) as Avg_Quantity
FROM sales
GROUP BY Discount_Range
ORDER BY Avg_Discount_Percent;
```

### 15. Discount Revenue Lost
```sql
SELECT 
    SUM(Sales_Amount) as Total_Sales_After_Discount,
    ROUND(SUM(Sales_Amount / (1 - Discount)) - SUM(Sales_Amount), 2) as Revenue_Lost_To_Discounts,
    ROUND(SUM(Sales_Amount / (1 - Discount)), 2) as Original_Revenue,
    ROUND((1 - SUM(Sales_Amount) / SUM(Sales_Amount / (1 - Discount))) * 100, 2) as Discount_Percentage
FROM sales
WHERE Discount > 0;
```

---

## Cross-Dimensional Analysis

### 16. Region and Sales Rep Performance Matrix
```sql
SELECT 
    Region,
    Sales_Rep,
    Product_Category,
    COUNT(*) as Transactions,
    SUM(Sales_Amount) as Total_Sales,
    AVG(Sales_Amount) as Avg_Sale,
    SUM(Quantity_Sold) as Units_Sold
FROM sales
GROUP BY Region, Sales_Rep, Product_Category
ORDER BY Total_Sales DESC;
```

### 17. Customer Type by Channel
```sql
SELECT 
    Customer_Type,
    Sales_Channel,
    COUNT(*) as Transaction_Count,
    SUM(Sales_Amount) as Total_Revenue,
    AVG(Sales_Amount) as Avg_Transaction,
    ROUND(AVG(Discount) * 100, 2) as Avg_Discount
FROM sales
GROUP BY Customer_Type, Sales_Channel
ORDER BY Total_Revenue DESC;
```

### 18. Product Category Performance by Channel
```sql
SELECT 
    Product_Category,
    Sales_Channel,
    COUNT(*) as Sales_Count,
    SUM(Sales_Amount) as Total_Revenue,
    AVG(Sales_Amount) as Avg_Sale,
    SUM(Quantity_Sold) as Units_Sold,
    ROUND(SUM(Sales_Amount) * 100.0 / 
        (SELECT SUM(Sales_Amount) FROM sales WHERE Sales_Channel = s.Sales_Channel), 2) as Channel_Share
FROM sales s
GROUP BY Product_Category, Sales_Channel
ORDER BY Total_Revenue DESC;
```

---

## Advanced Analytics

### 19. Sales Ranking Within Region
```sql
SELECT 
    Region,
    Sales_Rep,
    SUM(Sales_Amount) as Total_Sales,
    RANK() OVER (PARTITION BY Region ORDER BY SUM(Sales_Amount) DESC) as Region_Rank
FROM sales
GROUP BY Region, Sales_Rep
ORDER BY Region, Region_Rank;
```

### 20. Running Total (Month over Month)
```sql
SELECT 
    strftime('%Y-%m', Sale_Date) as Month,
    SUM(Sales_Amount) as Monthly_Revenue,
    SUM(SUM(Sales_Amount)) OVER (ORDER BY strftime('%Y-%m', Sale_Date)) as Cumulative_Revenue
FROM sales
GROUP BY strftime('%Y-%m', Sale_Date)
ORDER BY Month;
```

### 21. Year-over-Year Comparison
```sql
SELECT 
    strftime('%m', Sale_Date) as Month,
    strftime('%Y', Sale_Date) as Year,
    SUM(Sales_Amount) as Monthly_Revenue,
    SUM(Quantity_Sold) as Units_Sold
FROM sales
GROUP BY Year, Month
ORDER BY Year, Month;
```

### 22. Top Performing Combinations
```sql
SELECT 
    Region,
    Sales_Rep,
    Product_Category,
    Customer_Type,
    COUNT(*) as Transactions,
    SUM(Sales_Amount) as Total_Sales,
    ROUND(AVG(Sales_Amount), 2) as Avg_Sale
FROM sales
GROUP BY Region, Sales_Rep, Product_Category, Customer_Type
HAVING COUNT(*) > 2
ORDER BY Total_Sales DESC
LIMIT 20;
```

---

## Summary Statistics

### 23. Overall Business Summary
```sql
SELECT 
    COUNT(*) as Total_Transactions,
    ROUND(SUM(Sales_Amount), 2) as Total_Revenue,
    ROUND(AVG(Sales_Amount), 2) as Avg_Transaction_Value,
    ROUND(MIN(Sales_Amount), 2) as Min_Transaction,
    ROUND(MAX(Sales_Amount), 2) as Max_Transaction,
    SUM(Quantity_Sold) as Total_Units_Sold,
    COUNT(DISTINCT Sales_Rep) as Total_Sales_Reps,
    COUNT(DISTINCT Region) as Total_Regions,
    COUNT(DISTINCT Product_Category) as Total_Categories
FROM sales;
```

---

## Performance Tips

1. **Indexing**: For large datasets, create indexes on frequently queried columns:
   ```sql
   CREATE INDEX idx_region ON sales(Region);
   CREATE INDEX idx_sales_rep ON sales(Sales_Rep);
   CREATE INDEX idx_category ON sales(Product_Category);
   CREATE INDEX idx_date ON sales(Sale_Date);
   ```

2. **Query Optimization**: Use WHERE clauses to filter before aggregating
   ```sql
   SELECT Region, SUM(Sales_Amount)
   FROM sales
   WHERE Sale_Date >= '2023-01-01'
   GROUP BY Region;
   ```

3. **Materialized Views**: For frequently used aggregations, create views:
   ```sql
   CREATE VIEW monthly_revenue AS
   SELECT 
       strftime('%Y-%m', Sale_Date) as Month,
       SUM(Sales_Amount) as Revenue
   FROM sales
   GROUP BY Month;
   ```

---

## Using the SQL Analyzer in Python

```python
from sql_analyzer import SQLSalesAnalyzer

# Initialize
analyzer = SQLSalesAnalyzer("sales_analysis.db")

# Load data
analyzer.load_csv_data("data/sales_data.csv")

# Run pre-built queries
print(analyzer.total_revenue_by_region())
print(analyzer.sales_rep_performance())
print(analyzer.product_category_analysis())

# Run custom query
custom_result = analyzer.custom_query("""
    SELECT Region, SUM(Sales_Amount) 
    FROM sales 
    GROUP BY Region
""")

# Close connection
analyzer.close()
```

---

## Export Results to CSV

```python
df = analyzer.total_revenue_by_region()
df.to_csv("revenue_by_region.csv", index=False)
```

