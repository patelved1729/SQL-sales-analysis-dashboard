"""
SQL-based Sales Analysis Module
Provides SQL queries for comprehensive sales data analysis using SQLite
"""

import sqlite3
import pandas as pd
from pathlib import Path
from typing import List, Dict, Any, Tuple


class SQLSalesAnalyzer:
    """SQL-based analyzer for sales data using SQLite"""
    
    def __init__(self, db_path: str = "sales_analysis.db"):
        """
        Initialize SQL analyzer and create database connection
        
        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path
        self.conn = None
        self.cursor = None
        self._connect()
    
    def _connect(self):
        """Create database connection"""
        self.conn = sqlite3.connect(self.db_path)
        self.cursor = self.conn.cursor()
        self.conn.row_factory = sqlite3.Row
    
    def load_csv_data(self, csv_path: str, table_name: str = "sales"):
        """
        Load CSV data into database
        
        Args:
            csv_path: Path to CSV file
            table_name: Name of table to create
        """
        df = pd.read_csv(csv_path)
        df.to_sql(table_name, self.conn, if_exists='replace', index=False)
        self.conn.commit()
        print(f"✓ Loaded {len(df)} records into '{table_name}' table")
    
    def execute_query(self, query: str) -> pd.DataFrame:
        """
        Execute SQL query and return results as DataFrame
        
        Args:
            query: SQL query string
            
        Returns:
            DataFrame with query results
        """
        return pd.read_sql_query(query, self.conn)
    
    def close(self):
        """Close database connection"""
        if self.conn:
            self.conn.close()
    
    # ==================== ANALYSIS QUERIES ====================
    
    def total_revenue_by_region(self) -> pd.DataFrame:
        """Get total revenue by region"""
        query = """
        SELECT 
            Region,
            COUNT(*) as Transaction_Count,
            SUM(Sales_Amount) as Total_Revenue,
            AVG(Sales_Amount) as Avg_Sales,
            MIN(Sales_Amount) as Min_Sales,
            MAX(Sales_Amount) as Max_Sales
        FROM sales
        GROUP BY Region
        ORDER BY Total_Revenue DESC
        """
        return self.execute_query(query)
    
    def sales_rep_performance(self) -> pd.DataFrame:
        """Get performance metrics for each sales rep"""
        query = """
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
        ORDER BY Total_Sales DESC
        """
        return self.execute_query(query)
    
    def product_category_analysis(self) -> pd.DataFrame:
        """Get analysis by product category"""
        query = """
        SELECT 
            Product_Category,
            COUNT(*) as Sales_Count,
            SUM(Sales_Amount) as Total_Revenue,
            AVG(Sales_Amount) as Avg_Sale_Value,
            SUM(Quantity_Sold) as Total_Units_Sold,
            ROUND(SUM(Sales_Amount) * 100.0 / (SELECT SUM(Sales_Amount) FROM sales), 2) as Revenue_Percentage
        FROM sales
        GROUP BY Product_Category
        ORDER BY Total_Revenue DESC
        """
        return self.execute_query(query)
    
    def monthly_revenue_trend(self) -> pd.DataFrame:
        """Get monthly revenue trend"""
        query = """
        SELECT 
            strftime('%Y-%m', Sale_Date) as Month,
            COUNT(*) as Transaction_Count,
            SUM(Sales_Amount) as Monthly_Revenue,
            AVG(Sales_Amount) as Avg_Transaction_Value,
            SUM(Quantity_Sold) as Total_Units
        FROM sales
        GROUP BY strftime('%Y-%m', Sale_Date)
        ORDER BY Month
        """
        return self.execute_query(query)
    
    def customer_type_analysis(self) -> pd.DataFrame:
        """Analyze sales by customer type (New vs Returning)"""
        query = """
        SELECT 
            Customer_Type,
            COUNT(*) as Customer_Count,
            SUM(Sales_Amount) as Total_Revenue,
            AVG(Sales_Amount) as Avg_Purchase_Value,
            ROUND(AVG(Discount) * 100, 2) as Avg_Discount_Percent
        FROM sales
        GROUP BY Customer_Type
        ORDER BY Total_Revenue DESC
        """
        return self.execute_query(query)
    
    def sales_channel_analysis(self) -> pd.DataFrame:
        """Analyze sales by channel (Online vs Retail)"""
        query = """
        SELECT 
            Sales_Channel,
            COUNT(*) as Transaction_Count,
            SUM(Sales_Amount) as Total_Revenue,
            AVG(Sales_Amount) as Avg_Transaction,
            SUM(Quantity_Sold) as Total_Units,
            ROUND(SUM(Sales_Amount) * 100.0 / (SELECT SUM(Sales_Amount) FROM sales), 2) as Revenue_Share
        FROM sales
        GROUP BY Sales_Channel
        ORDER BY Total_Revenue DESC
        """
        return self.execute_query(query)
    
    def payment_method_analysis(self) -> pd.DataFrame:
        """Analyze sales by payment method"""
        query = """
        SELECT 
            Payment_Method,
            COUNT(*) as Transaction_Count,
            SUM(Sales_Amount) as Total_Revenue,
            AVG(Sales_Amount) as Avg_Amount,
            MIN(Sales_Amount) as Min_Amount,
            MAX(Sales_Amount) as Max_Amount
        FROM sales
        GROUP BY Payment_Method
        ORDER BY Total_Revenue DESC
        """
        return self.execute_query(query)
    
    def profitability_analysis(self) -> pd.DataFrame:
        """Analyze profit margins by product category"""
        query = """
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
        ORDER BY Total_Profit DESC
        """
        return self.execute_query(query)
    
    def top_products(self, limit: int = 10) -> pd.DataFrame:
        """Get top products by revenue"""
        query = f"""
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
        LIMIT {limit}
        """
        return self.execute_query(query)
    
    def regional_and_rep_analysis(self) -> pd.DataFrame:
        """Detailed analysis by region and sales rep combination"""
        query = """
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
        ORDER BY Total_Sales DESC
        """
        return self.execute_query(query)
    
    def discount_impact_analysis(self) -> pd.DataFrame:
        """Analyze impact of discounts on sales"""
        query = """
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
        ORDER BY Avg_Discount_Percent
        """
        return self.execute_query(query)
    
    def seasonal_analysis(self) -> pd.DataFrame:
        """Analyze sales by season/quarter"""
        query = """
        SELECT 
            strftime('%Y', Sale_Date) as Year,
            'Q' || CAST(((strftime('%m', Sale_Date) - 1) / 3) + 1 AS INTEGER) as Quarter,
            COUNT(*) as Transaction_Count,
            SUM(Sales_Amount) as Quarterly_Revenue,
            AVG(Sales_Amount) as Avg_Transaction
        FROM sales
        GROUP BY Year, Quarter
        ORDER BY Year, Quarter
        """
        return self.execute_query(query)
    
    def day_of_week_analysis(self) -> pd.DataFrame:
        """Analyze sales patterns by day of week"""
        query = """
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
        ORDER BY CAST(strftime('%w', Sale_Date) AS INTEGER)
        """
        return self.execute_query(query)
    
    # ==================== CUSTOM QUERY EXECUTION ====================
    
    def custom_query(self, sql_query: str) -> pd.DataFrame:
        """
        Execute custom SQL query
        
        Args:
            sql_query: Custom SQL query string
            
        Returns:
            DataFrame with results
        """
        try:
            return self.execute_query(sql_query)
        except Exception as e:
            print(f"Error executing query: {e}")
            return pd.DataFrame()
    
    def get_schema(self) -> Dict[str, List[str]]:
        """Get database schema information"""
        self.cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = self.cursor.fetchall()
        
        schema = {}
        for table in tables:
            table_name = table[0]
            self.cursor.execute(f"PRAGMA table_info({table_name})")
            columns = self.cursor.fetchall()
            schema[table_name] = [col[1] for col in columns]
        
        return schema
    
    def print_summary(self):
        """Print summary of database and available tables"""
        schema = self.get_schema()
        print("\n" + "="*60)
        print("DATABASE SCHEMA")
        print("="*60)
        for table_name, columns in schema.items():
            print(f"\n📊 Table: {table_name}")
            print(f"   Columns: {', '.join(columns)}")
            self.cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
            count = self.cursor.fetchone()[0]
            print(f"   Records: {count}")


if __name__ == "__main__":
    # Example usage
    analyzer = SQLSalesAnalyzer()
    analyzer.load_csv_data("data/sales_data.csv")
    
    print("\n" + "="*60)
    print("SALES ANALYSIS REPORTS")
    print("="*60)
    
    print("\n📍 Revenue by Region:")
    print(analyzer.total_revenue_by_region())
    
    print("\n👥 Sales Rep Performance:")
    print(analyzer.sales_rep_performance())
    
    print("\n🏷️ Product Category Analysis:")
    print(analyzer.product_category_analysis())
    
    print("\n📈 Monthly Revenue Trend:")
    print(analyzer.monthly_revenue_trend())
    
    print("\n💳 Customer Type Analysis:")
    print(analyzer.customer_type_analysis())
    
    print("\n🔗 Sales Channel Analysis:")
    print(analyzer.sales_channel_analysis())
    
    print("\n💰 Profitability Analysis:")
    print(analyzer.profitability_analysis())
    
    analyzer.close()
