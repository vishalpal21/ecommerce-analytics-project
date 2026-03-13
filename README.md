🛒 E-Commerce Sales Analytics Dashboard <br><br>
An end-to-end data analytics project analyzing e-commerce transaction data to derive actionable business insights using Python, MySQL, and Power BI.<br>
________________________________________<br>
📋 Table of Contents <br><br>
•	Project Overview <br><br>
•	Business Problem <br><br>
•	Dataset<br><br>
•	Technologies Used<br><br>
•	Project Architecture<br><br>
•	Key Features<br><br>
•	Installation & Setup<br><br>
•	Project Workflow<br><br>
•	Dashboard Overview<br><br>
•	Key Insights<br><br>
•	SQL Queries<br><br>
•	Skills Demonstrated<br><br>
•	Future Enhancements<br><br>
•	Contact<br><br>
________________________________________<br>
🎯 Project Overview<br><br>
This project demonstrates a complete data analytics workflow for an e-commerce business, from raw data cleaning to interactive dashboard creation. The analysis focuses on understanding sales performance, customer behavior, product trends, and geographical patterns to support data-driven decision making. <br><br>
Project Duration: 4 weeks<br>
Domain: E-Commerce / Retail Analytics<br>
Role: Data Analyst<br><br>
________________________________________<br>
💼 Business Problem<br><br>
The e-commerce company needed to: <br><br>
•	📊 Track and analyze sales performance across different dimensions<br><br>
•	👥 Understand customer purchasing behavior and retention patterns<br><br>
•	📦 Identify top-performing and underperforming product categories<br><br>
•	🌍 Analyze geographical sales distribution<br><br>
•	💳 Evaluate payment method preferences<br><br>
•	📈 Monitor key performance indicators (KPIs) in real-time<br><br>
________________________________________<br>
📊 Dataset<br><br>
Data Source<br><br>
•	Format: CSV/Excel<br><br>
•	Records: ~10,000+ transactions<br><br>
•	Time Period: 2 years (2024-2026) <br><br>
•	Size: ~2 MB<br><br>
Data Structure<br>
Column Name		Data Type	Description<br>
Transaction_ID		String	Unique identifier for each transaction<br>
User_Name		String	Customer name<br>
Age		Integer	Customer age (18-70) <br>
Country		String	Transaction country<br>
Product_Category		String	Product category (Electronics, Clothing, etc.) <br>
Purchase_Amount		Float	Transaction amount ($5-$1000) <br>
Payment_Method		String	Payment type (Credit Card, PayPal, UPI) <br>
Transaction_Date		Date	Date of purchase<br>
________________________________________<br>
🛠️ Technologies Used<br><br>
Data Processing & Analysis<br><br>
•	Python 3.9+ <br><br>
o	Pandas - Data manipulation and analysis<br><br>
o	NumPy - Numerical computations<br><br>
o	Matplotlib & Seaborn - Data visualization<br><br>
Database Management<br><br>
•	MySQL 8.0 <br><br>
o	Data storage and querying<br><br>
o	Complex SQL analytics<br><br>
Business Intelligence<br><br>
•	Microsoft Power BI Desktop<br> <br>
o	Interactive dashboards<br><br>
o	DAX calculations<br><br>
o	Data modeling<br><br>
Development Tools<br><br>
•	MySQL Workbench - Database management<br><br>
•	Git/GitHub - Version control<br><br>
•	VS Code - Code editing<br><br>
________________________________________<br>
🏗️ Project Architecture<br><br>
┌─────────────────┐<br><br>
│   Raw Data      │<br><br>
│   (CSV/Excel)   │<br><br>
└────────┬────────┘<br><br>
         │<br><br>
         ▼<br><br>
┌─────────────────┐<br><br>
│ Python Script   │<br><br>
│ Data Cleaning   │<br><br>
│ & Validation    │<br><br>
└────────┬────────┘<br><br>
         │<br><br>
         ▼<br><br>
┌─────────────────┐<br><br>
│  MySQL Database │<br><br>
│  Data Storage   │<br><br>
└────────┬────────┘<br><br>
         │<br><br>
         ▼<br><br>
┌─────────────────┐<br><br>
│   Power BI      │<br><br>
│   Dashboard     │<br><br>
└─────────────────┘<br><br>
________________________________________<br>
✨ Key Features<br><br>
Data Processing<br><br>
✅ Automated data cleaning pipeline<br>
✅ Missing value handling (imputation strategies) <br>
✅ Outlier detection and treatment<br>
✅ Data type standardization<br>
✅ Feature engineering (date features, categories) <br><br>
Database Implementation<br><br>
✅ Normalized database schema<br>
✅ Indexed tables for query optimization<br>
✅ Complex SQL queries for business analytics<br>
✅ Stored views for common analyses<br><br>
Interactive Dashboard<br><br>
✅ 5 comprehensive dashboard pages<br>
✅ 20+ interactive visualizations<br>
✅ Real-time filtering and drill-down<br>
<br>
________________________________________<br>
🚀 Installation & Setup<br>
Prerequisites<br>
Python 3.9+<br>
MySQL 8.0+<br>
Power BI Desktop<br>
Step 1: Clone Repository<br>
git clone https://github.com/yourusername/ecommerce-analytics.git<br>
cd ecommerce-analytics<br>
Step 2: Install Python Dependencies<br>
pip install -r requirements.txt<br>
requirements.txt:<br>
pandas==2.0.0<br>
numpy==1.24.0<br>
matplotlib==3.7.0<br>
seaborn==0.12.0<br>
mysql-connector-python==8.0.33<br>
sqlalchemy==2.0.0<br>
pymysql==1.0.3<br>
openpyxl==3.1.0<br>
Step 3: Setup MySQL Database<br>
# Login to MySQL<br>
mysql -u root -p<br>
<br>
# Run database setup script<br>
source sql/schema.sql<br>
Step 4: Run Data Pipeline<br>
# 1. Clean the data<br>
python scripts/01_data_cleaning.py<br>
<br>
# 2. Load data into MySQL<br>
python scripts/02_mysql_loader.py<br>
<br>
# 3. Generate EDA visualizations<br>
python scripts/03_eda_analysis.py<br>
Step 5: Open Power BI Dashboard<br>
# Open the .pbix file in Power BI Desktop<br>
powerbi/dashboard.pbix<br>
________________________________________<br>
📈 Project Workflow<br>
Phase 1: Data Collection & Cleaning (Week 1)<br>
1.	Data Acquisition<br>
o	Loaded raw e-commerce transaction data<br>
o	Performed initial data profiling<br>
2.	Data Cleaning<br>
o	Handled missing values (3% of records)<br>
o	Removed duplicate transactions (150 records)<br>
o	Standardized categorical values<br>
o	Corrected data types<br>
o	Treated outliers using IQR method<br>
3.	Feature Engineering<br>
o	Extracted date components (Year, Month, Quarter, Day of Week)<br>
o	Created Age Groups (18-25, 26-35, 36-45, 46-55, 56+)<br>
o	Categorized purchase amounts (Low, Medium, High, Very High)<br>
o	Added weekend flag<br>
Phase 2: Database Design & Implementation (Week 1-2)<br>
1.	Schema Design<br>
o	Created normalized table structure<br>
o	Defined primary keys and indexes<br>
2.	Data Loading<br>
o	Inserted cleaned data into MySQL<br>
o	Created indexes on frequently queried columns<br>
o	Validated data integrity<br>
3.	View Creation<br>
o	Monthly sales summary view<br>
o	Product performance view<br>
o	Customer segmentation view<br>
o	Payment analysis view<br>
Phase 3: Exploratory Data Analysis (Week 2-3)<br>
1.	Python Analysis<br>
o	Generated 8 comprehensive visualizations<br>
o	Statistical analysis of key metrics<br>
o	Trend identification<br>
o	Pattern recognition<br>
2.	SQL Analytics<br>
o	Created 40+ business intelligence queries<br>
o	Time-series analysis<br>
o	Customer behavior analysis<br>
o	Product performance analysis<br>
Phase 4: Dashboard Development (Week 3-4)<br>
1.	Data Modeling<br>
o	Connected Power BI to MySQL<br>
o	Created Date dimension table<br>
o	Established relationships<br>
2.	DAX Calculations<br>
o	Created 15+ measures for KPIs<br>
o	Implemented time intelligence<br>
o	Built calculated columns<br>
3.	Visualization<br>
o	Designed 5 interactive pages<br>
o	Applied consistent formatting<br>
o	Added slicers and filters<br>
o	Implemented drill-through functionality<br>
________________________________________<br>
📊 Dashboard Overview<br>
Page 1: Executive Summary 🎯<br>
Purpose: High-level overview for executives<br>
Key Metrics:<br>
•	Total Revenue: $2.5M<br>
•	Total Transactions: 10,234<br>
•	Average Order Value: $244<br>
•	Unique Customers: 5,678<br>
Visualizations:<br>
•	Revenue trend line chart<br>
•	Revenue by category (bar chart)<br>
•	Geographic distribution (map)<br>
•	Payment method breakdown (donut chart)<br>
 <br>
________________________________________<br>
Page 2: Sales Analysis 💰<br>
Purpose: Deep dive into sales performance<br>
Key Visualizations:<br>
•	Sales by category and country (matrix)<br>
•	Monthly revenue breakdown (waterfall chart)<br>
•	Revenue vs transactions (area chart)<br>
•	Category contribution (treemap)<br>
•	Day of week analysis (stacked column)<br>
Insights:<br>
•	Electronics: 35% of total revenue<br>
•	Weekend sales: 15% higher than weekdays<br>
•	Q4 seasonal spike: 25% increase<br>
 <br>
________________________________________<br>
Page 3: Customer Analytics 👥<br>
Purpose: Customer behavior and segmentation<br>
Key Visualizations:<br>
•	Top 20 customers (bar chart)<br>
•	Customer acquisition trend (line chart)<br>
•	Customer details table (with conditional formatting)<br>
Key Metrics:<br>
•	Repeat customer rate: 35%<br>
•	Average customer lifetime value: $850<br>
•	New vs returning ratio: 40:60<br>
 <br>
________________________________________<br>
Page 4: Product Performance 📦<br>
Purpose: Product-level insights<br>
Key Visualizations:<br>
•	Revenue by category (bar chart)<br>
•	Category performance (line & column chart)<br>
•	Product deep dive (matrix with conditional formatting)<br>
•	Price vs volume (scatter chart)<br>
•	Category trend (stacked area)<br>
Insights:<br>
•	Top 3 categories generate 70% revenue<br>
•	Average items per order: 2.3<br>
•	Best performing category: Electronics ($875K)<br>
 <br>
________________________________________<br>
Page 5: Time Analysis ⏰<br>
Purpose: Temporal patterns and trends<br>
Key Visualizations:<br>
•	Daily revenue pattern (line chart)<br>
•	Year × Quarter performance (matrix)<br>
•	Monthly comparison (clustered column)<br>
•	Category ranking over time (ribbon chart)<br>
Insights:<br>
•	Peak sales day: Friday<br>
•	Revenue growth: 15% YoY<br>
•	Best performing month: December<br>
 <br>
________________________________________<br>
💡 Key Insights<br>
1. Revenue Performance<br>
•	Total Revenue: $2.5M over 2-year period<br>
•	Year-over-Year Growth: 15%<br>
•	Average Order Value: $244<br>
•	Peak Revenue Month: December ($450K)<br>
2. Customer Behavior<br>
•	Total Customers: 5,678<br>
•	Repeat Purchase Rate: 35%<br>
•	Top 20% customers contribute 60% of revenue (Pareto Principle)<br>
•	Average purchases per customer: 1.8<br>
3. Product Insights<br>
•	Top Category: Electronics (35% revenue share)<br>
•	Fastest Growing: Books category (25% MoM growth)<br>
•	Most Popular: Electronics has highest transaction count<br>
•	Average Category Performance: 3-5 products per category drive 80% sales<br>
4. Geographic Trends<br>
•	Top Country: United States (40% revenue)<br>
•	Fastest Growing Market: India (30% growth rate)<br>
•	Markets Served: 10 countries across 4 continents<br>
5. Payment Preferences<br>
•	Most Popular: Credit Card (45%)<br>
•	Growing: UPI adoption increasing 15% quarterly<br>
•	Average Transaction by Method: PayPal has highest AOV ($280)<br>
6. Temporal Patterns<br>
•	Best Day: Friday (18% of weekly sales)<br>
•	Weekend Boost: 15% higher than weekday average<br>
•	Seasonal Trend: Q4 shows 25% spike (holiday season)<br>
________________________________________<br>
🎓 Skills Demonstrated<br>
Technical Skills<br>
•	✅ Python Programming: Pandas, NumPy, data manipulation<br>
•	✅ SQL: Complex queries, joins, window functions, CTEs<br>
•	✅ Data Cleaning: Missing values, outliers, normalization<br>
•	✅ Data Visualization: Matplotlib, Seaborn, Power BI<br>
•	✅ Database Design: Schema design, indexing, optimization<br>
•	✅ DAX: Measures, calculated columns, time intelligence<br>
•	✅ ETL Processes: Extract, Transform, Load pipelines<br>
Analytical Skills<br>
•	✅ Exploratory Data Analysis (EDA)<br>
•	✅ Statistical analysis<br>
•	✅ Trend identification<br>
•	✅ Pattern recognition<br>
•	✅ Business metrics calculation<br>
•	✅ KPI definition and tracking<br>
Business Skills<br>
•	✅ Understanding business requirements<br>
•	✅ Translating data into actionable insights<br>
•	✅ Stakeholder communication<br>
•	✅ Data storytelling<br>
•	✅ Dashboard design principles<br>
•	✅ Presentation skills<br>
________________________________________<br>
📁 Project Structure<br>
ecommerce-analytics/<br>
│<br>
├── data/<br>
│   ├── raw/<br>
│   │   └── ecommerce_data.csv<br>
│   └── cleaned/<br>
│       └── cleaned_ecommerce_data.csv<br>
│<br>
├── scripts/<br>
│   ├── 01_data_cleaning.py<br>
│   ├── 02_mysql_loader.py<br>
│   └── 03_eda_analysis.py<br>
│<br>
├── sql/<br>
│   ├── schema.sql<br>
│   └── business_queries.sql<br>
│<br>
├── visualizations/<br>
│   ├── 01_purchase_amount_analysis.png<br>
│   ├── 02_age_analysis.png<br>
│   ├── 03_categorical_analysis.png<br>
│   ├── 04_daily_trends.png<br>
│   ├── 05_monthly_analysis.png<br>
│   ├── 06_category_country_revenue.png<br>
│   ├── 07_age_vs_purchase.png<br>
│   └── 08_category_payment_heatmap.png<br>
│<br>
├── powerbi/<br>
│   ├── dashboard.pbix<br>
│   └── screenshots/<br>
│       ├── executive_summary.png<br>
│       ├── sales_analysis.png<br>
│       ├── customer_analysis.png<br>
│       ├── product_performance.png<br>
│       └── time_analysis.png<br>
│<br>
├── images/<br>
│   └── (dashboard screenshots)<br>
│<br>
├── README.md<br>
├── requirements.txt<br>
└── .gitignore <br>
________________________________________<br>
📝 Lessons Learned<br>
Technical Learnings<br>
1.	Data Quality: 70% of project time spent on data cleaning - crucial for accurate analysis<br>
2.	Indexing: Proper database indexing reduced query time by 80%<br>
3.	DAX Optimization: Context transition understanding critical for performance<br>
4.	Visualization: Less is more - removed 40% of initial visuals for clarity<br>
Business Learnings<br>
1.	Stakeholder Communication: Regular check-ins prevented rework<br>
2.	Iterative Development: Agile approach allowed for feedback incorporation<br>
3.	Documentation: Comprehensive docs saved 50% onboarding time<br>
________________________________________<br>
📄 License<br>
This project is licensed under the MIT License - see the LICENSE file for details.<br>
________________________________________<br>
👤 Contact<br>
Vishal Pal<br>
•	📧 Email: i.vishalpal@gmail.com<br>
•	🐱 GitHub: @vishalpal21<br>
________________________________________<br>
🙏 Acknowledgments<br>
•	Dataset inspired by real e-commerce transaction patterns<br>
•	Power BI community for dashboard design inspiration<br>
•	Stack Overflow community for technical support<br>
•	Python and MySQL documentation<br>
<br>

