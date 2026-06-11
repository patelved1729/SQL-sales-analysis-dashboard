# SQL Sales Analysis Setup Guide

This guide helps you set up and run SQL-based sales analysis on your sales data.

## 📁 Project Structure

```
sales_dashboard_project/
├── src/
│   ├── __init__.py
│   ├── sql_analyzer.py          # Main SQL analyzer module
│   ├── data_processor.py
│   ├── analytics.py
│   ├── visualizations.py
│   └── main.py
├── data/
│   └── sales_data.csv           # Source sales data
├── output/                       # Generated reports
├── requirements.txt
├── setup.py
├── SQL_QUERIES_REFERENCE.md     # SQL query reference guide
├── sql_analysis.py              # Main SQL analysis script
└── README.md
```

## ⚙️ Setup Instructions

### 1. Install Dependencies

No additional dependencies are needed! The project uses:
- **pandas** (for data manipulation) - already in requirements.txt
- **sqlite3** (built-in with Python)

If you haven't installed project dependencies, run:
```bash
pip install -r requirements.txt
```

### 2. Run SQL Analysis

#### Option A: Run the Analysis Script
```bash
python sql_analysis.py
```

This will:
- Create `sales_analysis.db` SQLite database
- Load CSV data into the database
- Run 12 comprehensive analysis reports
- Display formatted results in terminal

#### Option B: Use Jupyter Notebook
```bash
jupyter notebook SQL_Sales_Analysis.ipynb
```

This provides interactive SQL analysis with visualizations.

#### Option C: Use the SQL Analyzer Module in Python

```python
from src.sql_analyzer import SQLSalesAnalyzer

# Initialize
analyzer = SQLSalesAnalyzer("sales_analysis.db")

# Load data
analyzer.load_csv_data("data/sales_data.csv")

# Run pre-built queries
print(analyzer.total_revenue_by_region())
print(analyzer.sales_rep_performance())
print(analyzer.product_category_analysis())
print(analyzer.profitability_analysis())

# Run custom queries
result = analyzer.custom_query("""
    SELECT Region, SUM(Sales_Amount) as Revenue
    FROM sales
    GROUP BY Region
""")

# Close connection
analyzer.close()
```

## 📊 Available Analysis Reports

The SQL analyzer provides 13 pre-built analysis queries:

1. **total_revenue_by_region()** - Revenue breakdown by geographic region
2. **sales_rep_performance()** - Performance metrics for each sales representative
3. **product_category_analysis()** - Revenue and unit analysis by product category
4. **monthly_revenue_trend()** - Month-over-month revenue tracking
5. **customer_type_analysis()** - New vs. Returning customer comparison
6. **sales_channel_analysis()** - Online vs. Retail channel performance
7. **payment_method_analysis()** - Payment method distribution
8. **profitability_analysis()** - Profit margins by product category
9. **top_products()** - Top 10 products by revenue
10. **regional_and_rep_analysis()** - Cross-dimensional region/rep/category analysis
11. **discount_impact_analysis()** - Impact of discounts on sales volume
12. **seasonal_analysis()** - Quarterly performance patterns
13. **day_of_week_analysis()** - Sales patterns by day of week

## 🔍 Key SQL Queries Reference

All SQL queries are documented in `SQL_QUERIES_REFERENCE.md`. Some common queries:

### Total Revenue by Region
```sql
SELECT 
    Region,
    COUNT(*) as Transaction_Count,
    SUM(Sales_Amount) as Total_Revenue,
    AVG(Sales_Amount) as Avg_Sales
FROM sales
GROUP BY Region
ORDER BY Total_Revenue DESC
```

### Sales Rep Performance
```sql
SELECT 
    Sales_Rep,
    Region,
    COUNT(*) as Total_Transactions,
    SUM(Sales_Amount) as Total_Sales,
    AVG(Sales_Amount) as Avg_Transaction
FROM sales
GROUP BY Sales_Rep, Region
ORDER BY Total_Sales DESC
```

### Monthly Revenue Trend
```sql
SELECT 
    strftime('%Y-%m', Sale_Date) as Month,
    COUNT(*) as Transaction_Count,
    SUM(Sales_Amount) as Monthly_Revenue,
    AVG(Sales_Amount) as Avg_Transaction_Value
FROM sales
GROUP BY strftime('%Y-%m', Sale_Date)
ORDER BY Month
```

See `SQL_QUERIES_REFERENCE.md` for 23+ complete queries.

## 💾 Database Schema

The SQLite database contains a single `sales` table with:

- `Product_ID` - Unique product identifier
- `Sale_Date` - Date of sale (YYYY-MM-DD)
- `Sales_Rep` - Sales representative name
- `Region` - Geographic region
- `Sales_Amount` - Total sale amount
- `Quantity_Sold` - Units sold
- `Product_Category` - Product category
- `Unit_Cost` - Cost per unit
- `Unit_Price` - Selling price per unit
- `Customer_Type` - New or Returning
- `Discount` - Discount applied
- `Payment_Method` - Payment type
- `Sales_Channel` - Online or Retail

## 📈 Creating Visualizations

Using Pandas and Matplotlib:

```python
import pandas as pd
import matplotlib.pyplot as plt
from src.sql_analyzer import SQLSalesAnalyzer

analyzer = SQLSalesAnalyzer()
analyzer.load_csv_data("data/sales_data.csv")

# Get data
df_region = analyzer.total_revenue_by_region()

# Create visualization
plt.figure(figsize=(10, 6))
plt.barh(df_region['Region'], df_region['Total_Revenue'])
plt.xlabel('Total Revenue ($)')
plt.title('Revenue by Region')
plt.tight_layout()
plt.show()

analyzer.close()
```

## 📊 Jupyter Notebook Features

The `SQL_Sales_Analysis.ipynb` notebook includes:

1. **Data Loading** - Load CSV to SQLite
2. **Data Overview** - Schema and record count
3. **Product Analysis** - Category and top product analysis
4. **Time Series** - Monthly trends, seasonality, day-of-week patterns
5. **Performance** - Regional and sales rep metrics
6. **Customer Analysis** - Customer type and channel breakdown
7. **Metrics** - KPIs and profitability analysis
8. **Visualizations** - Charts and graphs
9. **Key Insights** - Summary statistics

Run cells individually or execute all with `Cell > Run All`.

## 🚀 Advanced Usage

### Export Results to CSV
```python
df_results = analyzer.sales_rep_performance()
df_results.to_csv("output/sales_rep_performance.csv", index=False)
```

### Filter Results in Python
```python
df_region = analyzer.total_revenue_by_region()
top_3_regions = df_region.head(3)
print(top_3_regions)
```

### Create Custom Queries
```python
custom_query = """
SELECT 
    Product_Category,
    Customer_Type,
    COUNT(*) as Count,
    SUM(Sales_Amount) as Revenue
FROM sales
WHERE Region = 'North'
GROUP BY Product_Category, Customer_Type
"""
df_custom = analyzer.custom_query(custom_query)
```

### Set Up Database Indexes for Performance
```python
analyzer.cursor.execute("CREATE INDEX idx_region ON sales(Region)")
analyzer.cursor.execute("CREATE INDEX idx_date ON sales(Sale_Date)")
analyzer.cursor.execute("CREATE INDEX idx_sales_rep ON sales(Sales_Rep)")
analyzer.conn.commit()
```

## 📝 Common Tasks

### Generate Monthly Revenue Report
```python
from src.sql_analyzer import SQLSalesAnalyzer

analyzer = SQLSalesAnalyzer()
analyzer.load_csv_data("data/sales_data.csv")

df = analyzer.monthly_revenue_trend()
df.to_csv("output/monthly_revenue.csv", index=False)
print(df)
analyzer.close()
```

### Analyze Top Performers
```python
df_reps = analyzer.sales_rep_performance()
top_10 = df_reps.head(10)
print(top_10)
```

### Calculate Profit Margins
```python
df_profit = analyzer.profitability_analysis()
print(df_profit[['Product_Category', 'Profit_Margin_Percent', 'Total_Profit']])
```

## ⚡ Performance Tips

1. **Use WHERE clauses** to filter before aggregating large datasets
2. **Create indexes** on frequently queried columns (Region, Sales_Rep, Date)
3. **Use LIMIT** for result sets to preview data before full export
4. **Materialized Views** for frequently used aggregations

## 🐛 Troubleshooting

**Issue**: "Table sales already exists"
- **Solution**: Delete `sales_analysis.db` and rerun

**Issue**: "CSV file not found"
- **Solution**: Ensure you're running from the project root directory

**Issue**: Slow queries on large datasets
- **Solution**: Create indexes or filter with WHERE clauses

## 📚 Additional Resources

- `SQL_QUERIES_REFERENCE.md` - 23+ SQL queries with explanations
- `sql_analyzer.py` - Source code with documentation
- `SQL_Sales_Analysis.ipynb` - Interactive Jupyter notebook
- SQLite Documentation: https://www.sqlite.org/docs.html
- Pandas Documentation: https://pandas.pydata.org/docs/

## ✅ Next Steps

1. Run `python sql_analysis.py` to generate your first reports
2. Open `SQL_Sales_Analysis.ipynb` for interactive analysis
3. Review `SQL_QUERIES_REFERENCE.md` for custom query examples
4. Export results to CSV for presentation or further analysis
5. Create visualization dashboards using Matplotlib or Seaborn

---

**Need help?** Check the notebook for examples or modify the queries to match your analysis needs!
