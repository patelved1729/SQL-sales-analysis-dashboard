# SQL Sales Analysis Dashboard

A comprehensive SQL-based sales analysis system using SQLite, Pandas, and Matplotlib. This project provides powerful SQL queries and analysis tools for sales data without requiring any external database setup.

## ✨ Features

- **SQL-Based Analysis** - Execute 13+ pre-built SQL queries for comprehensive sales insights
- **SQLite Database** - No external database needed; uses lightweight SQLite
- **Interactive Jupyter Notebook** - Run interactive analysis with visualizations
- **Pre-built Reports** - Generate professional reports with a single command
- **Custom Queries** - Write your own SQL queries for custom analysis
- **Data Visualization** - Beautiful charts using Matplotlib and Seaborn
- **Easy Export** - Export results to CSV for presentations
- **Comprehensive Documentation** - 23+ SQL query examples with explanations

## 📊 Analysis Included

1. Revenue Analysis - by region, category, and time period
2. Sales Rep Performance - individual and team metrics
3. Product Analysis - best-selling products and category performance
4. Customer Analysis - New vs. Returning customer breakdown
5. Channel Analysis - Online vs. Retail performance
6. Temporal Analysis - monthly trends, seasonal patterns
7. Profitability Analysis - profit margins by category
8. Discount Impact - how discounts affect sales volume
9. Payment Methods - distribution across payment types
10. Key Metrics - KPIs and business summary

## 🚀 Quick Start

### Installation

```bash
# Clone the repository
git clone https://github.com/patelved1729/SQL-sales-analysis-dashboard.git
cd SQL-sales-analysis-dashboard

# Install dependencies
pip install -r requirements.txt
```

### Run Analysis

**Command Line:**
```bash
python sql_analysis.py
```

**Jupyter Notebook:**
```bash
jupyter notebook notebooks/SQL_Sales_Analysis.ipynb
```

**Python Script:**
```python
from src.sql_analyzer import SQLSalesAnalyzer

analyzer = SQLSalesAnalyzer("sales_analysis.db")
analyzer.load_csv_data("data/sales_data.csv")
print(analyzer.total_revenue_by_region())
analyzer.close()
```

## 📂 Project Structure

```
SQL-sales-analysis-dashboard/
├── src/
│   ├── __init__.py
│   └── sql_analyzer.py           # Core SQL analyzer
├── data/
│   └── sales_data.csv            # Sales dataset
├── notebooks/
│   └── SQL_Sales_Analysis.ipynb  # Interactive notebook
├── output/                        # Reports directory
├── sql_analysis.py               # Analysis script
├── requirements.txt              # Dependencies
├── setup.py                      # Setup configuration
├── SQL_QUERIES_REFERENCE.md      # Query examples
├── SQL_SETUP_GUIDE.md            # Usage guide
└── README.md
```

## 📈 Key Methods

```python
analyzer.total_revenue_by_region()
analyzer.sales_rep_performance()
analyzer.product_category_analysis()
analyzer.monthly_revenue_trend()
analyzer.seasonal_analysis()
analyzer.customer_type_analysis()
analyzer.sales_channel_analysis()
analyzer.profitability_analysis()
analyzer.top_products(10)
analyzer.custom_query(sql_string)
```

## 📚 Documentation

- **SQL_SETUP_GUIDE.md** - Complete setup and usage guide
- **SQL_QUERIES_REFERENCE.md** - 23+ SQL query examples
- **notebooks/** - Interactive Jupyter notebooks

## 📄 License

MIT License - See LICENSE file for details

## 🤝 Contributing

Feel free to fork and submit pull requests!

---

**For detailed setup and usage instructions, see SQL_SETUP_GUIDE.md**
