### --- Data Visualization --- ###

# Set the visual style
sns.set_theme(style="whitegrid")
plt.rcParams['figure.figsize'] = (12, 6)

# --- 1. SALES & FINANCIAL PERFORMANCE ---

# A. Pareto Analysis (80/20 Rule)
Inter_sales_rp_feature_revenue = Inter_sales_rp_feature.groupby('Style')['GROSS AMT'].sum().sort_values(ascending=False).reset_index()
Inter_sales_rp_feature_revenue['cum_pct'] = 100 * Inter_sales_rp_feature_revenue['GROSS AMT'].cumsum() / Inter_sales_rp_feature_revenue['GROSS AMT'].sum()

fig, ax1 = plt.subplots()
sns.barplot(x='Style', y='GROSS AMT', data=Inter_sales_rp_feature_revenue.head(15), ax=ax1, palette='Blues_r')
ax2 = ax1.twinx()
ax2.plot(Inter_sales_rp_feature_revenue['Style'].head(15), Inter_sales_rp_feature_revenue['cum_pct'].head(15), color='red', marker='o', linewidth=2)
ax1.set_title('Top 15 Styles: Revenue & Cumulative % (Pareto)')
plt.show()

# B. Seasonal Trends (Monthly Gross Amount)
# Ensure 'Date' or 'Month' column is sorted chronologically
sns.lineplot(x='Transaction_Month', y='GROSS AMT', data=Inter_sales_rp_feature, estimator=sum, ci=None, marker='o')
plt.title('Monthly Revenue Trend')
plt.xticks(rotation=45)
plt.show()

# --- 2. CUSTOMER & MARKET ANALYSIS ---

# A. Top 10 Customers by Revenue
top_customers = Inter_sales_rp_feature.groupby('CUSTOMER')['GROSS AMT'].sum().nlargest(10).reset_index()
sns.barplot(x='GROSS AMT', y='CUSTOMER', data=top_customers, palette='viridis')
plt.title('Top 10 High-Value Customers')
plt.show()

# B. Size Distribution (Demand by Size)
# Ordering sizes logically (S, M, L...) makes the visual easier to read
size_order = ['XS', 'S', 'M', 'L', 'XL', 'XXL', '3XL'] # Adjust based on your data
sns.countplot(x='Size', data=Inter_sales_rp_feature, order=[s for s in size_order if s in Inter_sales_rp_feature['Size'].unique()])
plt.title('Order Volume (PCS) by Size')
plt.show()

# C. Size Co-occurrence Heatmap (Customer Basket Analysis)
# Generate pairs of sizes found in the same 'basket'
size_pair_counts = Counter()

for sizes in transaction_sizes['Sizes_in_Basket']:
    if len(sizes) > 1:
        # Create unique combinations (A, B)
        pairs = list(combinations(sorted(sizes), 2))
        size_pair_counts.update(pairs)

# 2. Convert to a DataFrame for plotting
pair_df = pd.DataFrame(size_pair_counts.items(), columns=['Pair', 'Frequency'])
pair_df[['Size_A', 'Size_B']] = pd.DataFrame(pair_df['Pair'].tolist(), index=pair_df.index)

# 3. Create a Pivot Table for the Heatmap
heatmap_data = pair_df.pivot(index='Size_A', columns='Size_B', values='Frequency').fillna(0)

# 4. Plot
plt.figure(figsize=(10, 8))
sns.heatmap(heatmap_data, annot=True, cmap='YlGnBu', fmt='g')
plt.title('Size Co-occurrence Heatmap (Market Basket Analysis)')
plt.show()

# --- 3. PRODUCT & INVENTORY HEALTH ---

# A. Pricing Consistency (Rate Variance per SKU)
# We pick top 10 SKUs to avoid clutter
top_10_skus = Inter_sales_rp_feature['SKU'].value_counts().nlargest(10).index
Inter_sales_rp_feature_top_skus = Inter_sales_rp_feature[Inter_sales_rp_feature['SKU'].isin(top_10_skus)]

sns.stripplot(x='SKU', y='RATE', data=Inter_sales_rp_feature_top_skus, jitter=True, alpha=0.5)
plt.xticks(rotation=45)
plt.title('Pricing Consistency for Top 10 SKUs')
plt.show()

# B. Dead Stock Identification (< 50 PCS)
# Group and Filter
style_sales = Inter_sales_rp_feature.groupby('Style')['PCS'].sum().reset_index()
dead_stock = style_sales[style_sales['PCS'] < 50].sort_values(by='PCS', ascending=True)

# Limit to Bottom 20 to ensure the chart is readable
dead_stock_top20 = dead_stock.head(20)

# Create the Visual
plt.figure(figsize=(12, 8))
sns.set_theme(style="whitegrid")
# Using a color palette that fades to highlight the 'deadest' stock
ax = sns.barplot(
    x='PCS', 
    y='Style', 
    data=dead_stock_top20, 
    palette='Reds_r'
)
# Add labels for a professional finish
plt.title('Bottom 20 Underperforming Styles (Sales < 50 Units)', fontsize=16, fontweight='bold', pad=20)
plt.xlabel('Units Sold (PCS)', fontsize=12)
plt.ylabel('Product Style', fontsize=12)
# Optional: Add the actual number at the end of each bar for quick reading
for p in ax.patches:
    ax.annotate(f'{int(p.get_width())}', 
                (p.get_width(), p.get_y() + p.get_height() / 2), 
                ha='left', va='center', 
                xytext=(5, 0), 
                textcoords='offset points',
                fontsize=10)

plt.tight_layout()
plt.show()

# --- 4. DATA QUALITY (THE CLEANING PROOF) ---

# SKU Ambiguity Check (How many Middle Codes per Style?)
sku_check = Inter_sales_rp_feature.groupby('Style')['SKU'].nunique().reset_index().rename(columns={'SKU': 'Unique_SKU_Count'})
sns.histplot(sku_check['Unique_SKU_Count'], bins=10, kde=True)
plt.title('Data Quality: Number of Unique SKUs per Style')
plt.show()
