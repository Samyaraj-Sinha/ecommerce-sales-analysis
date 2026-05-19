# ecommerce_analysis.py
# This Python project uses Pandas and Seaborn to clean raw e-commerce sales logs and track retail business performance.
# The script fixes missing entries using data averages and calculates total store revenue, top product categories, and peak sales months.
# It saves a clean, multi-plot dark dashboard panel comparing metrics to help teams optimize inventory and marketing budgets.

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# Apply a professional dark thematic layout
plt.style.use('dark_background')
sns.set_theme(style="darkgrid", rc={"axes.facecolor": "#1A1A1A", "figure.facecolor": "#121212"})

print("Generating synthetic retail data rows...")
np.random.seed(42)
rows = 800

data = {
    'OrderID': range(1001, 1001 + rows),
    'ProductCategory': np.random.choice(['Electronics', 'Clothing', 'Home & Kitchen', 'Books'], rows, p=[0.25, 0.35, 0.20, 0.20]),
    'SalesAmount': np.random.uniform(15.0, 750.0, rows).round(2),
    'QuantityOrdered': np.random.randint(1, 8, rows),
    'OrderMonth': np.random.choice(['January', 'February', 'March', 'April', 'May', 'June'], rows)
}

df = pd.DataFrame(data)
df.loc[df.sample(25, random_state=42).index, 'SalesAmount'] = np.nan

print("Executing basic missing value imputation...")
average_sales = df['SalesAmount'].mean()
df['SalesAmount'] = df['SalesAmount'].fillna(average_sales)

# --- Core Business Data Aggregations ---
category_revenue = df.groupby('ProductCategory')['SalesAmount'].sum().sort_values(ascending=False).reset_index()
category_quantity = df.groupby('ProductCategory')['QuantityOrdered'].sum().sort_values(ascending=False).reset_index()

month_order = ['January', 'February', 'March', 'April', 'May', 'June']
monthly_revenue = df.groupby('OrderMonth')['SalesAmount'].sum().reindex(month_order).reset_index()

# =======================================================
# BUILDING THE PROFESSIONAL MULTI-PLOT DASHBOARD PANEL
# =======================================================
print("Building the executive dashboard canvas panel...")
fig, axes = plt.subplots(1, 3, figsize=(18, 6), sharey=False)
fig.suptitle('E-Commerce Store Analytics & Operational KPI Dashboard', fontsize=16, weight='bold', color='#FFFFFF', y=1.02)

# --- PLOT 1: Revenue Generation Mix (Vertical Bar Chart) ---
sns.barplot(ax=axes[0], data=category_revenue, x='ProductCategory', y='SalesAmount', palette='icefire')
axes[0].set_title('Gross Revenue Mix by Category', fontsize=12, pad=10, weight='bold', color='#E0E0E0')
axes[0].set_xlabel('Product Category', fontsize=10)
axes[0].set_ylabel('Total Cumulative Sales ($)', fontsize=10)

# Inject data value labels right on top of the bars
for bar in axes[0].patches:
    axes[0].annotate(f"${bar.get_height():,.0f}", 
                     (bar.get_x() + bar.get_width() / 2., bar.get_height()), 
                     ha='center', va='center', xytext=(0, 8), 
                     textcoords='offset points', fontsize=9, color='#FFFFFF', weight='bold')

# --- PLOT 2: Monthly Financial Momentum (Line Chart) ---
sns.lineplot(ax=axes[1], data=monthly_revenue, x='OrderMonth', y='SalesAmount', marker='o', color='#00ADB5', linewidth=2.5, markersize=8)
axes[1].set_title('Monthly Revenue Tracking Velocity', fontsize=12, pad=10, weight='bold', color='#E0E0E0')
axes[1].set_xlabel('Operating Month', fontsize=10)
axes[1].set_ylabel('Monthly Total Sales ($)', fontsize=10)
axes[1].tick_params(axis='x', rotation=15)

# --- PLOT 3: Product Volume Demands (Horizontal Bar Chart) ---
sns.barplot(ax=axes[3-1], data=category_quantity, x='QuantityOrdered', y='ProductCategory', palette='rocket')
axes[2].set_title('Total Units Demanded by Category', fontsize=12, pad=10, weight='bold', color='#E0E0E0')
axes[2].set_xlabel('Total Physical Quantities Sold (Units)', fontsize=10)
axes[2].set_ylabel('', fontsize=10) # Remove vertical label to prevent cluttering

# Adjust the layout elements cleanly
plt.tight_layout()

# Save the dashboard image file cleanly to your local path
plt.savefig('ecommerce_dashboard_panel.png', dpi=300, bbox_inches='tight')
print("[✔] Dashboard panel successfully saved as 'ecommerce_dashboard_panel.png'.")

# Display the panel window directly on your monitor screen
plt.show()