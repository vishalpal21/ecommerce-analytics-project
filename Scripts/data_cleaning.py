import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set display options for better readability
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)

print("="*70)
print("E-COMMERCE TRANSACTION DATA - LOADING & CLEANING SCRIPT")
print("="*70)

# ==============================================================================
# STEP 1: LOAD THE DATA
# ==============================================================================
print("\n[STEP 1] Loading the dataset...")

try:
    df = pd.read_csv('C:/Users\Vishal\Desktop\ecommerce-analytics-project\Data\ecommerce_transactions.csv')

    
    print(f"✓ Dataset loaded successfully!")
    print(f"  Rows: {df.shape[0]:,}")
    print(f"  Columns: {df.shape[1]}")
    
except FileNotFoundError:
    print("✗ Error: File not found. Please check the file path.")
    exit()

# ==============================================================================
# STEP 2: INITIAL DATA INSPECTION
# ==============================================================================
print("\n[STEP 2] Initial Data Inspection")
print("-" * 70)

print("\nFirst 5 rows:")
print(df.head())

print("\n\nDataset Info:")
print(df.info())

print("\n\nBasic Statistics:")
print(df.describe())

print("\n\nColumn Names:")
print(df.columns.tolist())

# ==============================================================================
# STEP 3: DATA CLEANING
# ==============================================================================
print("\n[STEP 3] Data Cleaning Process")
print("-" * 70)

# 3.1: Check for missing values
print("\n3.1 Missing Values Analysis:")
missing_values = df.isnull().sum()
missing_percent = (df.isnull().sum() / len(df)) * 100
missing_df = pd.DataFrame({
    'Missing_Count': missing_values,
    'Percentage': missing_percent
})
print(missing_df[missing_df['Missing_Count'] > 0])

if missing_values.sum() == 0:
    print("✓ No missing values found!")
else:
    # Handle missing values
    print("\nHandling missing values...")
    
    # For categorical columns, fill with mode
    categorical_cols = ['User_Name', 'Country', 'Product_Category', 'Payment_Method']
    for col in categorical_cols:
        if col in df.columns and df[col].isnull().sum() > 0:
            df[col].fillna(df[col].mode()[0], inplace=True)
    
    # For numerical columns, fill with median
    if 'Age' in df.columns and df['Age'].isnull().sum() > 0:
        df['Age'].fillna(df['Age'].median(), inplace=True)
    
    if 'Purchase_Amount' in df.columns and df['Purchase_Amount'].isnull().sum() > 0:
        df['Purchase_Amount'].fillna(df['Purchase_Amount'].median(), inplace=True)
    
    # For Transaction_Date, drop rows if missing (can't impute dates meaningfully)
    if 'Transaction_Date' in df.columns and df['Transaction_Date'].isnull().sum() > 0:
        df.dropna(subset=['Transaction_Date'], inplace=True)
    
    print("✓ Missing values handled!")

# 3.2: Remove duplicates
print("\n3.2 Checking for Duplicates:")
duplicates = df.duplicated().sum()
print(f"  Duplicate rows found: {duplicates}")

if duplicates > 0:
    # Keep first occurrence of duplicates
    df.drop_duplicates(keep='first', inplace=True)
    print(f"✓ Removed {duplicates} duplicate rows!")
else:
    print("✓ No duplicates found!")

# 3.3: Check for duplicate Transaction_IDs
if 'Transaction_ID' in df.columns:
    print("\n3.3 Checking Transaction_ID uniqueness:")
    duplicate_ids = df['Transaction_ID'].duplicated().sum()
    print(f"  Duplicate Transaction_IDs: {duplicate_ids}")
    
    if duplicate_ids > 0:
        df.drop_duplicates(subset=['Transaction_ID'], keep='first', inplace=True)
        print(f"✓ Removed {duplicate_ids} duplicate Transaction_IDs!")

# 3.4: Clean column names (remove spaces, standardize)
print("\n3.4 Standardizing Column Names:")
df.columns = df.columns.str.strip().str.replace(' ', '_')
print(f"✓ Column names standardized!")
print(f"  New columns: {df.columns.tolist()}")

# 3.5: Data Type Conversion
print("\n3.5 Converting Data Types:")

# Convert Transaction_Date to datetime
if 'Transaction_Date' in df.columns:
    df['Transaction_Date'] = pd.to_datetime(df['Transaction_Date'], errors='coerce')
    print("✓ Transaction_Date converted to datetime")

# Convert Age to integer
if 'Age' in df.columns:
    df['Age'] = df['Age'].astype(int)
    print("✓ Age converted to integer")

# Convert Purchase_Amount to float
if 'Purchase_Amount' in df.columns:
    df['Purchase_Amount'] = pd.to_numeric(df['Purchase_Amount'], errors='coerce')
    print("✓ Purchase_Amount converted to numeric")

# 3.6: Handle outliers in Age
print("\n3.6 Handling Outliers in Age:")
if 'Age' in df.columns:
    age_before = len(df)
    # Remove ages outside reasonable range (18-70 as per your description)
    df = df[(df['Age'] >= 18) & (df['Age'] <= 100)]
    age_removed = age_before - len(df)
    print(f"  Age range: {df['Age'].min()} to {df['Age'].max()}")
    print(f"✓ Removed {age_removed} rows with invalid ages")

# 3.7: Handle outliers in Purchase_Amount
print("\n3.7 Handling Outliers in Purchase_Amount:")
if 'Purchase_Amount' in df.columns:
    # Remove negative values
    purchase_before = len(df)
    df = df[df['Purchase_Amount'] > 0]
    
    # Optional: Remove extreme outliers using IQR method
    Q1 = df['Purchase_Amount'].quantile(0.25)
    Q3 = df['Purchase_Amount'].quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 3 * IQR  # Using 3*IQR for extreme outliers only
    upper_bound = Q3 + 3 * IQR
    
    df = df[(df['Purchase_Amount'] >= lower_bound) & (df['Purchase_Amount'] <= upper_bound)]
    purchase_removed = purchase_before - len(df)
    
    print(f"  Purchase Amount range: ${df['Purchase_Amount'].min():.2f} to ${df['Purchase_Amount'].max():.2f}")
    print(f"✓ Removed {purchase_removed} rows with invalid purchase amounts")

# 3.8: Standardize categorical values
print("\n3.8 Standardizing Categorical Values:")

# Standardize text columns (strip whitespace, title case)
text_columns = ['User_Name', 'Country', 'Product_Category', 'Payment_Method']
for col in text_columns:
    if col in df.columns:
        df[col] = df[col].str.strip().str.title()

print("✓ Categorical values standardized!")

# 3.9: Remove any remaining rows with NaN after conversions
print("\n3.9 Final NaN Check:")
final_nans = df.isnull().sum().sum()
if final_nans > 0:
    df.dropna(inplace=True)
    print(f"✓ Removed {final_nans} rows with remaining NaN values")
else:
    print("✓ No remaining NaN values!")

# ==============================================================================
# STEP 4: FEATURE ENGINEERING
# ==============================================================================
print("\n[STEP 4] Feature Engineering")
print("-" * 70)

if 'Transaction_Date' in df.columns:
    # Extract date components
    df['Year'] = df['Transaction_Date'].dt.year
    df['Month'] = df['Transaction_Date'].dt.month
    df['Month_Name'] = df['Transaction_Date'].dt.month_name()
    df['Quarter'] = df['Transaction_Date'].dt.quarter
    df['Day_of_Week'] = df['Transaction_Date'].dt.day_name()
    df['Week_of_Year'] = df['Transaction_Date'].dt.isocalendar().week
    df['Is_Weekend'] = df['Transaction_Date'].dt.dayofweek.isin([5, 6]).astype(int)
    
    print("✓ Created date-based features:")
    print("  - Year, Month, Month_Name, Quarter")
    print("  - Day_of_Week, Week_of_Year, Is_Weekend")

# Create Age Groups
if 'Age' in df.columns:
    df['Age_Group'] = pd.cut(df['Age'], 
                              bins=[0, 25, 35, 45, 55, 100], 
                              labels=['18-25', '26-35', '36-45', '46-55', '56+'])
    print("✓ Created Age_Group feature")

# Create Purchase Amount Categories
if 'Purchase_Amount' in df.columns:
    df['Purchase_Category'] = pd.cut(df['Purchase_Amount'],
                                      bins=[0, 50, 200, 500, 1000],
                                      labels=['Low', 'Medium', 'High', 'Very High'])
    print("✓ Created Purchase_Category feature")

# ==============================================================================
# STEP 5: DATA VALIDATION & SUMMARY
# ==============================================================================
print("\n[STEP 5] Data Validation & Summary")
print("-" * 70)

print(f"\nFinal Dataset Shape: {df.shape[0]:,} rows × {df.shape[1]} columns")

print("\n\nValue Counts for Categorical Columns:")
print("\nProduct Categories:")
print(df['Product_Category'].value_counts())

print("\nCountries:")
print(df['Country'].value_counts())

print("\nPayment Methods:")
print(df['Payment_Method'].value_counts())

print("\n\nNumerical Column Statistics:")
print(df[['Age', 'Purchase_Amount']].describe())

# ==============================================================================
# STEP 6: DATA QUALITY REPORT
# ==============================================================================
print("\n[STEP 6] Data Quality Report")
print("-" * 70)

quality_report = pd.DataFrame({
    'Column': df.columns,
    'Data_Type': df.dtypes,
    'Non_Null_Count': df.count(),
    'Null_Count': df.isnull().sum(),
    'Unique_Values': df.nunique()
})

print(quality_report.to_string(index=False))

# ==============================================================================
# STEP 7: SAVE CLEANED DATA
# ==============================================================================
print("\n[STEP 7] Saving Cleaned Data")
print("-" * 70)

try:
    # Save as CSV
    df.to_csv('cleaned_ecommerce_data.csv', index=False)
    print("✓ Cleaned data saved as 'cleaned_ecommerce_data.csv'")

      # Save data quality report
    quality_report.to_csv('data_quality_report.csv', index=False)
    print("✓ Data quality report saved as 'data_quality_report.csv'")
    
except Exception as e:
    print(f"✗ Error saving files: {e}")

# ==============================================================================
# STEP 8: GENERATE SIMPLE VISUALIZATIONS
# ==============================================================================
print("\n[STEP 8] Generating Data Visualizations")
print("-" * 70)

# Set style
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# Create a figure with multiple subplots
fig, axes = plt.subplots(2, 2, figsize=(15, 10))
fig.suptitle('E-Commerce Data - Overview', fontsize=16, fontweight='bold')

# 1. Purchase Amount Distribution
axes[0, 0].hist(df['Purchase_Amount'], bins=50, color='skyblue', edgecolor='black')
axes[0, 0].set_title('Purchase Amount Distribution')
axes[0, 0].set_xlabel('Purchase Amount ($)')
axes[0, 0].set_ylabel('Frequency')

# 2. Transactions by Product Category
category_counts = df['Product_Category'].value_counts()
axes[0, 1].bar(category_counts.index, category_counts.values, color='coral')
axes[0, 1].set_title('Transactions by Product Category')
axes[0, 1].set_xlabel('Category')
axes[0, 1].set_ylabel('Number of Transactions')
axes[0, 1].tick_params(axis='x', rotation=45)

# 3. Age Distribution
axes[1, 0].hist(df['Age'], bins=30, color='lightgreen', edgecolor='black')
axes[1, 0].set_title('Customer Age Distribution')
axes[1, 0].set_xlabel('Age')
axes[1, 0].set_ylabel('Frequency')

# 4. Payment Method Distribution
payment_counts = df['Payment_Method'].value_counts()
axes[1, 1].pie(payment_counts.values, labels=payment_counts.index, autopct='%1.1f%%', startangle=90)
axes[1, 1].set_title('Payment Method Distribution')

plt.tight_layout()
plt.savefig('data_overview_visualization.png', dpi=300, bbox_inches='tight')
print("✓ Visualization saved as 'data_overview_visualization.png'")
plt.show()

# ==============================================================================
# COMPLETION
# ==============================================================================
print("\n" + "="*70)
print("DATA CLEANING COMPLETED SUCCESSFULLY!")
print("="*70)
print(f"\nFinal Dataset: {df.shape[0]:,} rows × {df.shape[1]} columns")
print("\nFiles Created:")
print("  1. cleaned_ecommerce_data.csv - Cleaned dataset")
print("  2. data_quality_report.csv - Quality metrics")
print("  3. data_overview_visualization.png - Data visualizations")
print("\nYou can now proceed to the next phase of your project!")
print("="*70)