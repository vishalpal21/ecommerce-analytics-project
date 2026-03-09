import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

# Set styling
sns.set_style("whitegrid")
plt.rcParams['figure.figsize'] = (14, 8)
plt.rcParams['font.size'] = 10

print("="*70)
print("EXPLORATORY DATA ANALYSIS (EDA) - E-COMMERCE TRANSACTIONS")
print("="*70)

# ==============================================================================
# LOAD DATA
# ==============================================================================
print("\n[STEP 1] Loading Data...")

try:
    df = pd.read_csv("C:/Users/Vishal/Desktop/ecommerce-analytics-project/Data/cleaned_ecommerce_data.csv")
    df['Transaction_Date'] = pd.to_datetime(df['Transaction_Date'])
    print(f"✓ Loaded {len(df):,} transactions")
    print(f"  Date Range: {df['Transaction_Date'].min().date()} to {df['Transaction_Date'].max().date()}")
except FileNotFoundError:
    print("✗ Error: File not found. Run data cleaning script first.")
    exit()

# ==============================================================================
# UNIVARIATE ANALYSIS
# ==============================================================================
print("\n[STEP 2] Univariate Analysis")
print("-" * 70)

# Create visualization folder
import os
os.makedirs('visualizations', exist_ok=True)

# 2.1 Distribution of Purchase Amount
print("\n2.1 Purchase Amount Distribution:")
print(df['Purchase_Amount'].describe())

fig, axes = plt.subplots(1, 3, figsize=(18, 5))
fig.suptitle('Purchase Amount Analysis', fontsize=16, fontweight='bold')

# Histogram
axes[0].hist(df['Purchase_Amount'], bins=50, color='skyblue', edgecolor='black')
axes[0].set_xlabel('Purchase Amount ($)')
axes[0].set_ylabel('Frequency')
axes[0].set_title('Distribution of Purchase Amount')
axes[0].axvline(df['Purchase_Amount'].mean(), color='red', linestyle='--', label=f'Mean: ${df["Purchase_Amount"].mean():.2f}')
axes[0].axvline(df['Purchase_Amount'].median(), color='green', linestyle='--', label=f'Median: ${df["Purchase_Amount"].median():.2f}')
axes[0].legend()

# Box plot
axes[1].boxplot(df['Purchase_Amount'], vert=True)
axes[1].set_ylabel('Purchase Amount ($)')
axes[1].set_title('Box Plot of Purchase Amount')
axes[1].grid(axis='y', alpha=0.3)

# Violin plot by Purchase Category
if 'Purchase_Category' in df.columns:
    sns.violinplot(data=df, y='Purchase_Amount', x='Purchase_Category', ax=axes[2], palette='Set2')
    axes[2].set_title('Purchase Amount by Category')
    axes[2].set_xlabel('Purchase Category')
    axes[2].set_ylabel('Purchase Amount ($)')

plt.tight_layout()
plt.savefig('visualizations/01_purchase_amount_analysis.png', dpi=300, bbox_inches='tight')
print("✓ Saved: 01_purchase_amount_analysis.png")
plt.close()

# 2.2 Age Distribution
print("\n2.2 Age Distribution:")
print(df['Age'].describe())

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
fig.suptitle('Customer Age Analysis', fontsize=16, fontweight='bold')

# Age distribution
axes[0].hist(df['Age'], bins=30, color='lightcoral', edgecolor='black')
axes[0].set_xlabel('Age')
axes[0].set_ylabel('Frequency')
axes[0].set_title('Age Distribution')
axes[0].axvline(df['Age'].mean(), color='red', linestyle='--', label=f'Mean: {df["Age"].mean():.1f}')
axes[0].legend()

# Age group distribution
if 'Age_Group' in df.columns:
    age_group_counts = df['Age_Group'].value_counts().sort_index()
    axes[1].bar(age_group_counts.index, age_group_counts.values, color='lightgreen', edgecolor='black')
    axes[1].set_xlabel('Age Group')
    axes[1].set_ylabel('Number of Transactions')
    axes[1].set_title('Transactions by Age Group')
    axes[1].tick_params(axis='x', rotation=45)

plt.tight_layout()
plt.savefig('visualizations/02_age_analysis.png', dpi=300, bbox_inches='tight')
print("✓ Saved: 02_age_analysis.png")
plt.close()

# 2.3 Categorical Variables
print("\n2.3 Categorical Variable Analysis:")

fig, axes = plt.subplots(2, 2, figsize=(16, 12))
fig.suptitle('Categorical Variables Distribution', fontsize=16, fontweight='bold')

# Product Category
category_counts = df['Product_Category'].value_counts()
axes[0, 0].barh(category_counts.index, category_counts.values, color='steelblue')
axes[0, 0].set_xlabel('Number of Transactions')
axes[0, 0].set_title(f'Product Categories (Total: {len(category_counts)})')
for i, v in enumerate(category_counts.values):
    axes[0, 0].text(v, i, f' {v:,}', va='center')

# Country
country_counts = df['Country'].value_counts().head(10)
axes[0, 1].barh(country_counts.index, country_counts.values, color='coral')
axes[0, 1].set_xlabel('Number of Transactions')
axes[0, 1].set_title('Top 10 Countries by Transactions')
for i, v in enumerate(country_counts.values):
    axes[0, 1].text(v, i, f' {v:,}', va='center')

# Payment Method
payment_counts = df['Payment_Method'].value_counts()
colors = plt.cm.Set3(range(len(payment_counts)))
axes[1, 0].pie(payment_counts.values, labels=payment_counts.index, autopct='%1.1f%%',
               colors=colors, startangle=90)
axes[1, 0].set_title('Payment Method Distribution')

# Day of Week
if 'Day_of_Week' in df.columns:
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    day_counts = df['Day_of_Week'].value_counts().reindex(day_order)
    axes[1, 1].bar(range(len(day_counts)), day_counts.values, color='lightgreen', edgecolor='black')
    axes[1, 1].set_xticks(range(len(day_counts)))
    axes[1, 1].set_xticklabels(day_counts.index, rotation=45, ha='right')
    axes[1, 1].set_ylabel('Number of Transactions')
    axes[1, 1].set_title('Transactions by Day of Week')

plt.tight_layout()
plt.savefig('visualizations/03_categorical_analysis.png', dpi=300, bbox_inches='tight')
print("✓ Saved: 03_categorical_analysis.png")
plt.close()

# ==============================================================================
# TIME SERIES ANALYSIS
# ==============================================================================
print("\n[STEP 3] Time Series Analysis")
print("-" * 70)

# 3.1 Daily Transaction Trend
daily_transactions = df.groupby('Transaction_Date').agg({
    'Transaction_ID': 'count',
    'Purchase_Amount': 'sum'
}).rename(columns={'Transaction_ID': 'num_transactions', 'Purchase_Amount': 'total_revenue'})

fig, axes = plt.subplots(2, 1, figsize=(16, 10))
fig.suptitle('Daily Transaction Trends', fontsize=16, fontweight='bold')

# Daily transaction count
axes[0].plot(daily_transactions.index, daily_transactions['num_transactions'],
             color='blue', linewidth=1, alpha=0.7)
axes[0].set_ylabel('Number of Transactions')
axes[0].set_title('Daily Transaction Count')
axes[0].grid(alpha=0.3)

# Daily revenue
axes[1].plot(daily_transactions.index, daily_transactions['total_revenue'],
             color='green', linewidth=1, alpha=0.7)
axes[1].set_xlabel('Date')
axes[1].set_ylabel('Revenue ($)')
axes[1].set_title('Daily Revenue')
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.savefig('visualizations/04_daily_trends.png', dpi=300, bbox_inches='tight')
print("✓ Saved: 04_daily_trends.png")
plt.close()

# 3.2 Monthly Analysis
monthly_data = df.groupby(['Year', 'Month', 'Month_Name']).agg({
    'Transaction_ID': 'count',
    'Purchase_Amount': ['sum', 'mean'],
    'User_Name': 'nunique'
}).reset_index()

monthly_data.columns = ['Year', 'Month', 'Month_Name', 'num_transactions',
                        'total_revenue', 'avg_order_value', 'unique_customers']

print("\nMonthly Performance Summary:")
print(monthly_data[['Year', 'Month_Name', 'num_transactions', 'total_revenue', 'avg_order_value']].to_string(index=False))

fig, axes = plt.subplots(2, 2, figsize=(16, 10))
fig.suptitle('Monthly Performance Analysis', fontsize=16, fontweight='bold')

# Monthly revenue
axes[0, 0].bar(range(len(monthly_data)), monthly_data['total_revenue'], color='steelblue')
axes[0, 0].set_xticks(range(len(monthly_data)))
axes[0, 0].set_xticklabels([f"{row['Month_Name'][:3]}\n{row['Year']}" for _, row in monthly_data.iterrows()],
                            rotation=0, fontsize=8)
axes[0, 0].set_ylabel('Revenue ($)')
axes[0, 0].set_title('Monthly Revenue')

# Monthly transaction count
axes[0, 1].plot(range(len(monthly_data)), monthly_data['num_transactions'],
                marker='o', color='green', linewidth=2)
axes[0, 1].set_xticks(range(len(monthly_data)))
axes[0, 1].set_xticklabels([f"{row['Month_Name'][:3]}\n{row['Year']}" for _, row in monthly_data.iterrows()],
                            rotation=0, fontsize=8)
axes[0, 1].set_ylabel('Number of Transactions')
axes[0, 1].set_title('Monthly Transaction Count')
axes[0, 1].grid(alpha=0.3)

# Average order value
axes[1, 0].plot(range(len(monthly_data)), monthly_data['avg_order_value'],
                marker='s', color='coral', linewidth=2)
axes[1, 0].set_xticks(range(len(monthly_data)))
axes[1, 0].set_xticklabels([f"{row['Month_Name'][:3]}\n{row['Year']}" for _, row in monthly_data.iterrows()],
                            rotation=0, fontsize=8)
axes[1, 0].set_ylabel('Average Order Value ($)')
axes[1, 0].set_title('Monthly Average Order Value')
axes[1, 0].grid(alpha=0.3)

# Unique customers
axes[1, 1].bar(range(len(monthly_data)), monthly_data['unique_customers'], color='purple', alpha=0.7)
axes[1, 1].set_xticks(range(len(monthly_data)))
axes[1, 1].set_xticklabels([f"{row['Month_Name'][:3]}\n{row['Year']}" for _, row in monthly_data.iterrows()],
                            rotation=0, fontsize=8)
axes[1, 1].set_ylabel('Unique Customers')
axes[1, 1].set_title('Monthly Unique Customers')

plt.tight_layout()
plt.savefig('visualizations/05_monthly_analysis.png', dpi=300, bbox_inches='tight')
print("✓ Saved: 05_monthly_analysis.png")
plt.close()

# ==============================================================================
# BIVARIATE ANALYSIS
# ==============================================================================
print("\n[STEP 4] Bivariate Analysis")
print("-" * 70)

# 4.1 Revenue by Category and Country
category_country = df.groupby(['Product_Category', 'Country'])['Purchase_Amount'].sum().reset_index()
top_combinations = category_country.nlargest(15, 'Purchase_Amount')

fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle('Revenue Analysis: Category & Country', fontsize=16, fontweight='bold')

# Revenue by Product Category
category_revenue = df.groupby('Product_Category')['Purchase_Amount'].sum().sort_values(ascending=True)
axes[0].barh(category_revenue.index, category_revenue.values, color='teal')
axes[0].set_xlabel('Total Revenue ($)')
axes[0].set_title('Total Revenue by Product Category')
for i, v in enumerate(category_revenue.values):
    axes[0].text(v, i, f' ${v:,.0f}', va='center')

# Revenue by Country
country_revenue = df.groupby('Country')['Purchase_Amount'].sum().sort_values(ascending=False).head(10)
axes[1].bar(range(len(country_revenue)), country_revenue.values, color='orange')
axes[1].set_xticks(range(len(country_revenue)))
axes[1].set_xticklabels(country_revenue.index, rotation=45, ha='right')
axes[1].set_ylabel('Total Revenue ($)')
axes[1].set_title('Top 10 Countries by Revenue')

plt.tight_layout()
plt.savefig('visualizations/06_category_country_revenue.png', dpi=300, bbox_inches='tight')
print("✓ Saved: 06_category_country_revenue.png")
plt.close()

# 4.2 Age vs Purchase Amount
fig, axes = plt.subplots(1, 2, figsize=(16, 6))
fig.suptitle('Age vs Purchase Amount Analysis', fontsize=16, fontweight='bold')

# Scatter plot
axes[0].scatter(df['Age'], df['Purchase_Amount'], alpha=0.3, s=10, color='blue')
axes[0].set_xlabel('Age')
axes[0].set_ylabel('Purchase Amount ($)')
axes[0].set_title('Age vs Purchase Amount (Scatter)')
axes[0].grid(alpha=0.3)

# Box plot by Age Group
if 'Age_Group' in df.columns:
    df.boxplot(column='Purchase_Amount', by='Age_Group', ax=axes[1])
    axes[1].set_xlabel('Age Group')
    axes[1].set_ylabel('Purchase Amount ($)')
    axes[1].set_title('Purchase Amount Distribution by Age Group')
    plt.sca(axes[1])
    plt.xticks(rotation=45)

plt.tight_layout()
plt.savefig('visualizations/07_age_vs_purchase.png', dpi=300, bbox_inches='tight')
print("✓ Saved: 07_age_vs_purchase.png")
plt.close()

# 4.3 Heatmap: Category vs Payment Method
pivot_table = pd.crosstab(df['Product_Category'], df['Payment_Method'],
                           values=df['Purchase_Amount'], aggfunc='sum')

plt.figure(figsize=(12, 8))
sns.heatmap(pivot_table, annot=True, fmt='.0f', cmap='YlOrRd', linewidths=0.5)
plt.title('Revenue Heatmap: Product Category vs Payment Method', fontsize=16, fontweight='bold')
plt.xlabel('Payment Method')
plt.ylabel('Product Category')
plt.tight_layout()
plt.savefig('visualizations/08_category_payment_heatmap.png', dpi=300, bbox_inches='tight')
print("✓ Saved: 08_category_payment_heatmap.png")
plt.close()

# ==============================================================================
# KEY INSIGHTS SUMMARY
# ==============================================================================
print("\n[STEP 5] Key Insights Summary")
print("-" * 70)

insights = {
    'Total Transactions': f"{len(df):,}",
    'Total Revenue': f"${df['Purchase_Amount'].sum():,.2f}",
    'Average Order Value': f"${df['Purchase_Amount'].mean():.2f}",
    'Median Order Value': f"${df['Purchase_Amount'].median():.2f}",
    'Unique Customers': f"{df['User_Name'].nunique():,}",
    'Date Range': f"{df['Transaction_Date'].min().date()} to {df['Transaction_Date'].max().date()}",
    'Top Product Category': f"{df.groupby('Product_Category')['Purchase_Amount'].sum().idxmax()}",
    'Top Country': f"{df.groupby('Country')['Purchase_Amount'].sum().idxmax()}",
    'Most Popular Payment': f"{df['Payment_Method'].mode()[0]}",
    'Peak Transaction Day': f"{df['Day_of_Week'].mode()[0] if 'Day_of_Week' in df.columns else 'N/A'}"
}

print("\n📊 KEY BUSINESS METRICS:")
for key, value in insights.items():
    print(f"  • {key}: {value}")

# Save insights to file
with open('visualizations/eda_insights_summary.txt', 'w') as f:
    f.write("E-COMMERCE EDA - KEY INSIGHTS SUMMARY\n")
    f.write("="*70 + "\n\n")
    for key, value in insights.items():
        f.write(f"{key}: {value}\n")

print("\n✓ Insights saved: eda_insights_summary.txt")

# ==============================================================================
# COMPLETION
# ==============================================================================
print("\n" + "="*70)
print("EDA COMPLETED SUCCESSFULLY!")
print("="*70)
print("\n8 Visualizations created in 'visualizations/' folder:")
print("  1. Purchase Amount Analysis")
print("  2. Age Analysis")
print("  3. Categorical Variables")
print("  4. Daily Trends")
print("  5. Monthly Analysis")
print("  6. Category & Country Revenue")
print("  7. Age vs Purchase")
print("  8. Category-Payment Heatmap")
print("="*70)