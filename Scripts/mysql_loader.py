import pandas as pd
import mysql.connector
from mysql.connector import Error
from sqlalchemy import create_engine
import warnings

warnings.filterwarnings('ignore')

print("=" * 70)
print("MYSQL DATABASE SETUP & DATA LOADING")
print("=" * 70)

# ==============================================================================
# CONFIGURATION - MYSQL CREDENTIALS
# ==============================================================================
MYSQL_CONFIG = {
    'host': 'localhost',
    'user': 'root',  # Change to your MySQL username
    'password': 'vishal',  # Change to your MySQL password
    'database': 'ecommerce_db'
}

# ==============================================================================
# STEP 1: DATABASE CREATION
# ==============================================================================
print("\n[STEP 1] Creating Database...")

try:
    connection = mysql.connector.connect(
        host=MYSQL_CONFIG['host'],
        user=MYSQL_CONFIG['user'],
        password=MYSQL_CONFIG['password']
    )

    cursor = connection.cursor()

    # Create database if not exists
    cursor.execute(f"CREATE DATABASE IF NOT EXISTS {MYSQL_CONFIG['database']}")
    print(f"✓ Database '{MYSQL_CONFIG['database']}' created/verified successfully!")

    cursor.close()
    connection.close()

except Error as e:
    print(f"✗ Error creating database: {e}")
    exit()

# ==============================================================================
# STEP 2: TABLES CREATION
# ==============================================================================
print("\n[STEP 2] Creating Tables...")

try:
    # Connect to the database
    connection = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = connection.cursor()

    # Drop existing tables (optional - comment out if you want to keep existing data)
    print("  Dropping existing tables if they exist...")
    cursor.execute("DROP TABLE IF EXISTS transactions")

    # Create transactions table
    create_table_query = """
                         CREATE TABLE IF NOT EXISTS transactions \
                         ( \
                             Transaction_ID \
                             VARCHAR \
                         ( \
                             50 \
                         ) PRIMARY KEY,
                             User_Name VARCHAR \
                         ( \
                             100 \
                         ),
                             Age INT,
                             Country VARCHAR \
                         ( \
                             50 \
                         ),
                             Product_Category VARCHAR \
                         ( \
                             100 \
                         ),
                             Purchase_Amount DECIMAL \
                         ( \
                             10, \
                             2 \
                         ),
                             Payment_Method VARCHAR \
                         ( \
                             50 \
                         ),
                             Transaction_Date DATE,
                             Year INT,
                             Month INT,
                             Month_Name VARCHAR \
                         ( \
                             20 \
                         ),
                             Quarter INT,
                             Day_of_Week VARCHAR \
                         ( \
                             20 \
                         ),
                             Week_of_Year INT,
                             Is_Weekend TINYINT,
                             Age_Group VARCHAR \
                         ( \
                             20 \
                         ),
                             Purchase_Category VARCHAR \
                         ( \
                             20 \
                         ),
                             INDEX idx_date \
                         ( \
                             Transaction_Date \
                         ),
                             INDEX idx_country \
                         ( \
                             Country \
                         ),
                             INDEX idx_category \
                         ( \
                             Product_Category \
                         ),
                             INDEX idx_payment \
                         ( \
                             Payment_Method \
                         )
                             ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4; \
                         """

    cursor.execute(create_table_query)
    print("✓ Table 'transactions' created successfully!")

    cursor.close()
    connection.close()

except Error as e:
    print(f"✗ Error creating tables: {e}")
    exit()

# ==============================================================================
# STEP 3: LOAD CLEANED DATA
# ==============================================================================
print("\n[STEP 3] Loading Data from CSV...")

try:
    # Read cleaned data
    df = pd.read_csv("C:/Users/Vishal/Desktop/ecommerce-analytics-project/Data/cleaned_ecommerce_data.csv")
    print(f"✓ Loaded {len(df):,} records from CSV")

    # Convert Transaction_Date to proper format
    df['Transaction_Date'] = pd.to_datetime(df['Transaction_Date'])

    # Display sample
    print("\nSample data to be loaded:")
    print(df.head(3))

except FileNotFoundError:
    print("✗ Error: 'cleaned_ecommerce_data.csv' not found!")
    print("  Please run the data cleaning script first.")
    exit()

# ==============================================================================
# STEP 4: INSERT DATA INTO MYSQL
# ==============================================================================
print("\n[STEP 4] Inserting Data into MySQL...")

try:
    # Create SQLAlchemy engine
    engine = create_engine(
        f"mysql+pymysql://{MYSQL_CONFIG['user']}:{MYSQL_CONFIG['password']}@{MYSQL_CONFIG['host']}/{MYSQL_CONFIG['database']}"
    )

    # Insert data
    df.to_sql(
        name='transactions',
        con=engine,
        if_exists='append',  # Use 'replace' to overwrite existing data
        index=False,
        chunksize=1000  # Insert in batches
    )

    print(f"✓ Successfully inserted {len(df):,} records into 'transactions' table!")

except Exception as e:
    print(f"✗ Error inserting data: {e}")
    exit()

# ==============================================================================
# STEP 5: VERIFY DATA LOAD
# ==============================================================================
print("\n[STEP 5] Verifying Data Load...")

try:
    connection = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = connection.cursor()

    # Count records
    cursor.execute("SELECT COUNT(*) FROM transactions")
    count = cursor.fetchone()[0]
    print(f"✓ Total records in database: {count:,}")

    # Show sample records
    cursor.execute("SELECT * FROM transactions LIMIT 5")
    print("\nSample records from database:")
    columns = [desc[0] for desc in cursor.description]
    print(f"\nColumns: {columns}")

    for row in cursor.fetchall():
        print(row)

    # Show date range
    cursor.execute("SELECT MIN(Transaction_Date), MAX(Transaction_Date) FROM transactions")
    date_range = cursor.fetchone()
    print(f"\nDate Range: {date_range[0]} to {date_range[1]}")

    # Show categories
    cursor.execute("SELECT Product_Category, COUNT(*) as count FROM transactions GROUP BY Product_Category")
    print("\nTransactions by Category:")
    for row in cursor.fetchall():
        print(f"  {row[0]}: {row[1]:,}")

    cursor.close()
    connection.close()

except Error as e:
    print(f"✗ Error verifying data: {e}")

# ==============================================================================
# STEP 6: CREATE USEFUL VIEWS FOR ANALYSIS
# ==============================================================================
print("\n[STEP 6] Creating Database Views...")

try:
    connection = mysql.connector.connect(**MYSQL_CONFIG)
    cursor = connection.cursor()

    # View 1: Monthly Sales Summary
    cursor.execute("DROP VIEW IF EXISTS monthly_sales_summary")
    monthly_view = """
                   CREATE VIEW monthly_sales_summary AS
                   SELECT
                           Year,
                           Month,
                           Month_Name,
                           COUNT(*) as total_transactions,
                           SUM(Purchase_Amount) as total_revenue,
                           AVG(Purchase_Amount) as avg_order_value,
                           COUNT(DISTINCT User_Name) as unique_customers
                           FROM transactions
                           GROUP BY Year, Month, Month_Name
                           ORDER BY Year, Month; 
                   """
    cursor.execute(monthly_view)
    print("✓ Created view: monthly_sales_summary")

    # View 2: Product Performance
    cursor.execute("DROP VIEW IF EXISTS product_performance")
    product_view = """
                   CREATE VIEW product_performance AS
                   SELECT Product_Category, 
                          COUNT(*) as total_orders, 
                          SUM(Purchase_Amount) as total_revenue, 
                          AVG(Purchase_Amount) as avg_order_value, 
                          MIN(Purchase_Amount) as min_purchase, 
                          MAX(Purchase_Amount) as max_purchase
                   FROM transactions
                   GROUP BY Product_Category
                   ORDER BY total_revenue DESC; 
                   """
    cursor.execute(product_view)
    print("✓ Created view: product_performance")

    # View 3: Customer Segmentation
    cursor.execute("DROP VIEW IF EXISTS customer_segments")
    customer_view = """
                    CREATE VIEW customer_segments AS
                    SELECT Age_Group, 
                           Country, 
                           COUNT(*) as transaction_count, 
                           SUM(Purchase_Amount) as total_spent, 
                           AVG(Purchase_Amount) as avg_spent
                    FROM transactions
                    GROUP BY Age_Group, Country
                    ORDER BY total_spent DESC; 
                    """
    cursor.execute(customer_view)
    print("✓ Created view: customer_segments")

    # View 4: Payment Method Analysis
    cursor.execute("DROP VIEW IF EXISTS payment_analysis")
    payment_view = """
                   CREATE VIEW payment_analysis AS
                   SELECT Payment_Method, 
                          COUNT(*) as transaction_count, 
                          SUM(Purchase_Amount) as total_amount, 
                          AVG(Purchase_Amount) as avg_amount, 
                          ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM transactions), 2) as percentage
                   FROM transactions
                   GROUP BY Payment_Method
                   ORDER BY transaction_count DESC; 
                   """
    cursor.execute(payment_view)
    print("✓ Created view: payment_analysis")

    connection.commit()
    cursor.close()
    connection.close()

except Error as e:
    print(f"✗ Error creating views: {e}")

# ==============================================================================
# COMPLETION
# ==============================================================================
print("\n" + "=" * 70)
print("DATABASE SETUP COMPLETED SUCCESSFULLY!")
print("=" * 70)
print("\nDatabase Details:")
print(f"  Host: {MYSQL_CONFIG['host']}")
print(f"  Database: {MYSQL_CONFIG['database']}")
print(f"  Table: transactions")
print(f"  Records: {count:,}")
print("\nViews Created:")
print("  1. monthly_sales_summary")
print("  2. product_performance")
print("  3. customer_segments")
print("  4. payment_analysis")
print("=" * 70)