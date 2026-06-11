"""
SQL Sales Analysis Runner
Execute and display comprehensive SQL-based sales analysis reports
"""

import pandas as pd
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from sql_analyzer import SQLSalesAnalyzer


def format_currency(value):
    """Format value as currency"""
    if isinstance(value, (int, float)):
        return f"${value:,.2f}"
    return value


def print_section(title: str):
    """Print formatted section header"""
    print("\n" + "=" * 80)
    print(f"  {title}")
    print("=" * 80 + "\n")


def display_dataframe(df, title: str = "", currency_columns=None):
    """Display DataFrame with formatting"""
    if title:
        print(f"📊 {title}\n")
    
    # Apply currency formatting if specified
    if currency_columns:
        df_display = df.copy()
        for col in currency_columns:
            if col in df_display.columns:
                df_display[col] = df_display[col].apply(format_currency)
        print(df_display.to_string(index=False))
    else:
        print(df.to_string(index=False))
    print()


def main():
    """Run SQL-based sales analysis"""
    
    # Initialize analyzer
    print("\n🚀 Initializing SQL Sales Analyzer...\n")
    analyzer = SQLSalesAnalyzer("sales_analysis.db")
    
    # Load data
    data_path = Path(__file__).parent / "data" / "sales_data.csv"
    if not data_path.exists():
        print(f"❌ Error: Data file not found at {data_path}")
        return
    
    print(f"📁 Loading data from: {data_path}")
    analyzer.load_csv_data(str(data_path))
    
    # Print schema
    analyzer.print_summary()
    
    # ==================== ANALYSIS REPORTS ====================
    
    print_section("1️⃣  REVENUE BY REGION")
    display_dataframe(
        analyzer.total_revenue_by_region(),
        currency_columns=['Total_Revenue', 'Avg_Sales', 'Min_Sales', 'Max_Sales']
    )
    
    print_section("2️⃣  SALES REP PERFORMANCE")
    df_reps = analyzer.sales_rep_performance()
    display_dataframe(
        df_reps,
        currency_columns=['Total_Sales', 'Avg_Transaction']
    )
    
    print_section("3️⃣  PRODUCT CATEGORY ANALYSIS")
    df_category = analyzer.product_category_analysis()
    display_dataframe(
        df_category,
        currency_columns=['Total_Revenue', 'Avg_Sale_Value']
    )
    
    print_section("4️⃣  MONTHLY REVENUE TREND")
    df_monthly = analyzer.monthly_revenue_trend()
    display_dataframe(
        df_monthly,
        currency_columns=['Monthly_Revenue', 'Avg_Transaction_Value']
    )
    
    print_section("5️⃣  CUSTOMER TYPE ANALYSIS")
    df_customer = analyzer.customer_type_analysis()
    display_dataframe(
        df_customer,
        currency_columns=['Total_Revenue', 'Avg_Purchase_Value']
    )
    
    print_section("6️⃣  SALES CHANNEL ANALYSIS (Online vs Retail)")
    df_channel = analyzer.sales_channel_analysis()
    display_dataframe(
        df_channel,
        currency_columns=['Total_Revenue', 'Avg_Transaction']
    )
    
    print_section("7️⃣  PAYMENT METHOD ANALYSIS")
    df_payment = analyzer.payment_method_analysis()
    display_dataframe(
        df_payment,
        currency_columns=['Total_Revenue', 'Avg_Amount', 'Min_Amount', 'Max_Amount']
    )
    
    print_section("8️⃣  PROFITABILITY ANALYSIS")
    df_profit = analyzer.profitability_analysis()
    display_dataframe(
        df_profit,
        currency_columns=['Avg_Cost', 'Avg_Price', 'Avg_Profit_Per_Unit', 'Total_Profit']
    )
    
    print_section("9️⃣  TOP 10 PRODUCTS BY REVENUE")
    df_top = analyzer.top_products(10)
    display_dataframe(
        df_top,
        currency_columns=['Total_Revenue', 'Avg_Sale_Value']
    )
    
    print_section("🔟  DISCOUNT IMPACT ANALYSIS")
    df_discount = analyzer.discount_impact_analysis()
    display_dataframe(
        df_discount,
        currency_columns=['Total_Sales', 'Avg_Sale_Amount']
    )
    
    print_section("1️⃣1️⃣  SEASONAL ANALYSIS (By Quarter)")
    df_seasonal = analyzer.seasonal_analysis()
    display_dataframe(
        df_seasonal,
        currency_columns=['Quarterly_Revenue', 'Avg_Transaction']
    )
    
    print_section("1️⃣2️⃣  DAY OF WEEK ANALYSIS")
    df_dow = analyzer.day_of_week_analysis()
    display_dataframe(
        df_dow,
        currency_columns=['Total_Sales', 'Avg_Sale']
    )
    
    # ==================== SUMMARY STATISTICS ====================
    
    print_section("📈 OVERALL SUMMARY STATISTICS")
    
    query = """
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
    FROM sales
    """
    
    summary = analyzer.execute_query(query)
    print(summary.to_string(index=False))
    
    # Close connection
    analyzer.close()
    
    print("\n✅ SQL Analysis Complete!\n")


if __name__ == "__main__":
    main()
