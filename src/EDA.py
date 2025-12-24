### --- Phase 5: EDA --- ###

# ----  Sales & Financial Performance ---- #

  # 1. Revenue Drivers

print("\n--- Running Pareto Analysis on Styles ---\n")
total_revenue = Inter_sales_rp_feature['Net_Revenue'].sum()

# Group by Style and calculate total revenue per style
style_revenue = Inter_sales_rp_feature.groupby('Style')['Net_Revenue'].sum().reset_index()
style_revenue = style_revenue.sort_values(by='Net_Revenue', ascending=False)

# Calculate cumulative revenue and percentage
style_revenue['Cumulative_Revenue'] = style_revenue['Net_Revenue'].cumsum()
style_revenue['Cumulative_Percent'] = (style_revenue['Cumulative_Revenue'] / total_revenue ) * 100

# Identify the 80% cutoff point
eighty_percent_cutoff = style_revenue[style_revenue['Cumulative_Percent'] <= 80]
num_styles_for_80_percent = eighty_percent_cutoff.shape[0]

# Save the analysis result to a CSV file
style_revenue.to_csv('Style_Pareto_Analysis.csv', index=False)

print(f"\nTotal Number of Unique Styles: {Inter_sales_rp_feature['Style'].nunique()}")
print(f"Number of Styles accounting for the top 80% of revenue: {num_styles_for_80_percent}")
print("Style Pareto Analysis saved to: Style_Pareto_Analysis.csv")



   # 2. Profitability Index (Styles)

print("\n--- Profitability Index Analysis (Top 10 Styles) ---")

profit_index = Inter_sales_rp_feature.groupby('Style').agg(
    Avg_Rate=('RATE', 'mean'),             # Average Price per unit
    Avg_Gross_Amt=('GROSS AMT', 'mean'),   # Average Transaction Value
    Total_PCS=('PCS', 'sum')
).reset_index()

# Top 10 by Average RATE (Premium Products)
top_rate = profit_index.sort_values(by='Avg_Rate', ascending=False).head(10)
print("\nTop 10 Styles by Average Unit Rate (Premium Products):")
print(top_rate[['Style', 'Avg_Rate', 'Avg_Gross_Amt']].round(2))

# Top 10 by Average GROSS AMT (High Basket Value Transactions)
top_gross_amt = profit_index.sort_values(by='Avg_Gross_Amt', ascending=False).head(10)
print("\nTop 10 Styles by Average Transaction Value:")
print(top_gross_amt[['Style', 'Avg_Rate', 'Avg_Gross_Amt']].round(2))

# Add category labels
top_rate['Category'] = 'Top by Avg Rate'
top_gross_amt['Category'] = 'Top by Avg Gross Amount'

# Combine both tables
profitability_index = pd.concat(
    [top_rate, top_gross_amt],
    ignore_index=True
)

# Save to CSV
profitability_index.to_csv('Profitability_Index.csv', index=False)

print("Profitability_Index.csv saved successfully.")



   # 3. Seasonal Trend Analysis 

print("\n--- Running Seasonal Trend Analysis ---")

# Group by Year and Month and calculate total GROSS AMT
monthly_sales = Inter_sales_rp_feature.groupby(['Transaction_Year', 'Transaction_Month'])['GROSS AMT'].sum().reset_index()

# Create a clean date for sorting and plotting
# Use string concatenation and conversion for a standard YYYY-MM format
monthly_sales['Year_Month'] = monthly_sales['Transaction_Year'].astype(int).astype(str) + '-' + \
                              monthly_sales['Transaction_Month'].astype(int).astype(str).str.zfill(2)

# Sort the results chronologically
monthly_sales = monthly_sales.sort_values('Year_Month')

# Save the result to a CSV file for detailed analysis
monthly_sales.to_csv('Monthly_Sales_Trend.csv', index=False)

print("Monthly Sales Trend Analysis saved to: Monthly_Sales_Trend.csv")
print("\nFirst 5 rows of the Monthly Sales Trend:")
print(monthly_sales.head())



# 4. Sales Velocity
print("\n--- Sales Velocity Analysis (Top 10 SKUs) ---")

# Identify Top 10 Best-Selling SKUs by total PCS
top_10_skus_list = Inter_sales_rp_feature.groupby('SKU')['PCS'].sum().nlargest(10).index.tolist()

# Calculate the duration of the data in months
min_date = Inter_sales_rp_feature['DATE'].min()
max_date = Inter_sales_rp_feature['DATE'].max()
# Calculate difference in months: use the floor of the difference (e.g., 2021-06 to 2022-03 is 10 months)
total_months = (max_date.year - min_date.year) * 12 + (max_date.month - min_date.month) + 1

# Calculate the total PCS sold for these top 10 SKUs
top_10_sales = Inter_sales_rp_feature[Inter_sales_rp_feature['SKU'].isin(top_10_skus_list)].groupby('SKU')['PCS'].sum().reset_index()
top_10_sales = top_10_sales.rename(columns={'PCS': 'Total_PCS'})

# Calculate Average Monthly Sales Volume
top_10_sales['Avg_Monthly_PCS'] = top_10_sales['Total_PCS'] / total_months
top_10_sales = top_10_sales.sort_values(by='Avg_Monthly_PCS', ascending=False)
top_10_sales.to_csv('Sales_Velocity.csv', index=False)
print(f"Data period covers approximately {total_months} months ({min_date.strftime('%Y-%m')} to {max_date.strftime('%Y-%m')}).")
print("\nTop 10 SKUs by Average Monthly Sales Volume (PCS):")
print(top_10_sales[['SKU', 'Total_PCS', 'Avg_Monthly_PCS']].round(2))



# --- Customer and Market Analysis --- #


# 1. Top Tier Customers & Product Profile 

print("\n--- Top Tier Customers Analysis ---")

# Identify Top 10 Customers by Revenue
customer_revenue = Inter_sales_rp_feature.groupby('CUSTOMER')['Net_Revenue'].sum().reset_index()
top_10_customers = customer_revenue.sort_values(by='Net_Revenue', ascending=False).head(10)
top_10_names = top_10_customers['CUSTOMER'].tolist()

print(f"\nTop 10 Customers by Net Revenue:\n{top_10_customers.round(2)}")

# Analyze Product Profile of Top 10
top_10_transactions = Inter_sales_rp_feature[Inter_sales_rp_feature['CUSTOMER'].isin(top_10_names)]

# Find the most frequent Style and Size among these transactions (The Mode)
most_frequent_style = top_10_transactions['Style'].mode().iloc[0] if not top_10_transactions['Style'].mode().empty else "N/A"
most_frequent_size = top_10_transactions['Size'].mode().iloc[0] if not top_10_transactions['Size'].mode().empty else "N/A"
print(f"\nProduct Profile of Top 10 Customers:")
print(f"Most Frequent Style: {most_frequent_style}")
print(f"Most Frequent Size: {most_frequent_size}")



# 2.  Customer Concentration 

print("\n--- Customer Concentration Analysis ---")

total_revenue = Inter_sales_rp_feature['Net_Revenue'].sum()
total_customers = Inter_sales_rp_feature['CUSTOMER'].nunique()
top_5_percent_count = int(total_customers * 0.05)
print(f"Total Unique Customers: {total_customers}")
print(f"Number of customers in the top 5% concentration: {top_5_percent_count}")

# Get the revenue of the top 5% of customers
top_customers_revenue = customer_revenue.sort_values(by='Net_Revenue', ascending=False).head(top_5_percent_count)
revenue_from_top = top_customers_revenue['Net_Revenue'].sum()
concentration_percentage = (revenue_from_top / total_revenue) * 100

print(f"\nRevenue contributed by the top {top_5_percent_count} customers (5%): {revenue_from_top:,.2f}")
print(f"Customer Concentration: {concentration_percentage:.2f}% of total revenue")



# 3. Customer Basket Analysis (Size Co-occurrence) 

print("\n--- Customer Basket Analysis (Co-occurrence of Sizes) ---")

# Identify Top 10 Sizes by total PCS (to focus on the most common sizes, including the numerical ones)
top_sizes_list = Inter_sales_rp_feature.groupby('Size')['PCS'].sum().nlargest(10).index.tolist()

# Create the missing column (Crucial Step)
    # This combines Date and Customer to represent a single "basket"
Inter_sales_rp_feature['Transaction_ID'] = Inter_sales_rp_feature['DATE'].astype(str) + '_' + Inter_sales_rp_feature['CUSTOMER']

# Identify Top 10 Sizes
top_sizes_list = Inter_sales_rp_feature.groupby('Size')['PCS'].sum().nlargest(10).index.tolist()

#  Now run the GroupBy (This should work now!)
transaction_sizes = Inter_sales_rp_feature[Inter_sales_rp_feature['PCS'] > 0].groupby('Transaction_ID')['Size'].apply(lambda x: list(set(x))).reset_index(name='Sizes_in_Basket')
# Generate pairs
size_pair_counts = Counter()

for sizes in transaction_sizes['Sizes_in_Basket']:
    valid_sizes = [s for s in sizes if s in top_sizes_list]
    for pair in combinations(sorted(valid_sizes), 2):
        size_pair_counts[pair] += 1

# Convert to DataFrame and format
top_size_pairs = pd.DataFrame(size_pair_counts.items(), 
                              columns=['Size_Pair', 'Co_occurrence_Count'])
top_size_pairs[['Size_A', 'Size_B']] = pd.DataFrame(top_size_pairs['Size_Pair'].tolist(), index=top_size_pairs.index)
top_size_pairs = top_size_pairs.drop(columns='Size_Pair')
top_size_pairs = top_size_pairs.sort_values(by='Co_occurrence_Count', ascending=False).head(10)

print("\nTop 10 Most Frequently Co-Purchased Sizes (Based on Top 10 Selling Sizes):")
print(top_size_pairs)




# ----  Product & Inventory Management ---- #


# 1.  Dead Stock/Underperforming Products 

print("\n--- Dead Stock Analysis (Styles < 50 PCS) ---")

# Calculate total PCS sold per style
style_total_pcs = Inter_sales_rp_feature.groupby('Style')['PCS'].sum().reset_index(name='Total_PCS')

# Filter for underperforming products
dead_stock_threshold = 50
underperforming_styles = style_total_pcs[style_total_pcs['Total_PCS'] < dead_stock_threshold]

# Sort by lowest PCS first
underperforming_styles = underperforming_styles.sort_values(by='Total_PCS', ascending=True)

# Save the list to CSV for easy inspection
underperforming_styles.to_csv('Underperforming_Styles.csv', index=False)

print(f"Total Unique Styles: {Inter_sales_rp['Style'].nunique()}")
print(f"Number of Underperforming Styles (< {dead_stock_threshold} PCS): {underperforming_styles.shape[0]}")
print("Top 10 Least Selling Styles:")
print(underperforming_styles.head(10))



# 2.  Popular Size Distribution 

print("\n--- Popular Size Distribution Analysis ---")

# Calculate total PCS sold per size
size_distribution =Inter_sales_rp.groupby('Size')['PCS'].sum().reset_index(name='Total_PCS')
total_pcs_sum = size_distribution['Total_PCS'].sum()
size_distribution['Percentage'] = (size_distribution['Total_PCS'] / total_pcs_sum) * 100

# Sort and display the top 10 sizes
size_distribution = size_distribution.sort_values(by='Percentage', ascending=False)

size_distribution.to_csv("Popular Size Distribution.csv", index=False)

print("Top 10 Sizes by Sales Volume (PCS):")
print(size_distribution.head(10).round(2))



# 3. SKU Ambiguity (Data Quality Revisit) ---

print("\n--- SKU Ambiguity Analysis ---")

# Define a function to extract the 'Middle Code' from the SKU
    # Example: 'men5004-kr-l' -> 'kr'
def parse_sku(sku):
    if not isinstance(sku, str):
        return None, None
    
    parts = sku.split('-')
    
    style = parts[0] if len(parts) > 0 else None
    middle_code = parts[1] if len(parts) > 1 else None
    
    return style, middle_code

# Creating Style and Middle Code columns
Inter_sales_rp_feature[['Style', 'Middle_Code']] = (
    Inter_sales_rp_feature['SKU']
    .apply(lambda x: pd.Series(parse_sku(x)))
)

# Removing invalid role ( Important for data Quality)
df_sku_clean = Inter_sales_rp_feature.dropna(subset=['Style', 'Middle_Code'])

# identifying SKU ambiguity 
sku_ambiguity = (
    df_sku_clean
    .groupby('Style')['Middle_Code']
    .nunique()
    .reset_index(name='Distinct_Middle_Code_Count')
)

# Filtering ambuigious styles 
ambiguous_styles = sku_ambiguity[
    sku_ambiguity['Distinct_Middle_Code_Count'] > 1
]

# showing the particular codes that causes SKU ambiguity
ambiguous_details = (
    df_sku_clean
    .groupby('Style')['Middle_Code']
    .unique()
    .reset_index(name='Middle_Codes_Used')
)
Inter_sales_rp_feature['SKU_Ambiguous'] = Inter_sales_rp_feature['Style'].isin(
    ambiguous_styles['Style']
)
ambiguous_details.to_csv('SKU_Ambiguity_Styles.csv', index= False)

print(f"Total Styles checked: {df_sku_clean['Style'].nunique()}")
print(f"Number of Styles with Ambiguous Middle Codes: {ambiguous_styles.shape[0]}")
print("\nTop 10 Styles with Highest SKU Ambiguity:")
print(ambiguous_styles.head(10))



# 4. Pricing Consistency Check 

print("\n--- Pricing Consistency Check (SKU Level Rate Variance) ---")

# Aggregate RATE statistics by SKU
pricing_variance =Inter_sales_rp_feature.groupby('SKU')['RATE'].agg(
    Max_Rate='max',
    Min_Rate='min',
    Std_Rate='std',
    Count='count'
).reset_index()

# Calculate the Price Range (Max - Min)
pricing_variance['Rate_Range'] = pricing_variance['Max_Rate'] - pricing_variance['Min_Rate']

# Filter for SKUs where the price is not perfectly consistent (Rate_Range > 0)
# Filter out single-transaction SKUs as they cannot show variance
inconsistent_skus = pricing_variance[
    (pricing_variance['Rate_Range'] > 0.01) & 
    (pricing_variance['Count'] > 1)
]

# Sort by the largest standard deviation to find the most erratic pricing
inconsistent_skus = inconsistent_skus.sort_values(by='Std_Rate', ascending=False)

# Filter out non-product anomalies
inconsistent_skus = inconsistent_skus[~inconsistent_skus['SKU'].str.contains('shipping|tag')]
inconsistent_skus.to_csv('Price_Consistensy_Check', index=False)

print(f"Total Unique SKUs with > 1 transaction: {pricing_variance[pricing_variance['Count'] > 1].shape[0]}")
print(f"Number of SKUs with Inconsistent Pricing (Rate Range > $0.01): {inconsistent_skus.shape[0]}")
print("Top 10 SKUs with the Highest Price Variance:")
print(inconsistent_skus[['SKU', 'Count', 'Max_Rate', 'Min_Rate', 'Rate_Range', 'Std_Rate']].head(10).round(2))
