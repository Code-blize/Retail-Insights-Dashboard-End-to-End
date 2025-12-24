### --- Phase 3: Feature Engineering - Part 1 --- ###
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

Inter_sales_rp_feature = Inter_sales_rp.copy()

# --- Step 3.1: Handling the SKU Null Values ---
 
  # Create a Series containing non-null SKU values
non_null_skus = Inter_sales_rp_feature.dropna(subset=['SKU'])
 
  # Group by Style and Size, and find the mode ( the most frequent SKU)
    # If a (Style, Size) pair only maps to one SKU, this will be the unique SKU.
sku_mapping = non_null_skus.groupby(['Style', 'Size'])['SKU'].agg(lambda x: x.mode().iloc[0] 
                                                                  if not x.mode().empty 
                                                                  else None).reset_index()

  # Convvert the result to a dictionary for faster lookup
sku_dict = sku_mapping.set_index(['Style', 'Size'])['SKU'].to_dict()

# --- Step 3.2: Apply imputations ---

  # Fill missing SKU values
def impute_sku(row):
    # Only try to fill if the SKU is NaN
    if pd.isna(row['SKU']):
        # look up the corresponding SKU using the Style and Size from the mapping dictionary
        key = (row['Style'], row['Size'])

        if key in sku_dict:
            # If a mapping is found, mark it as ambiguous/unknown
            return f"{row['Style']}_SKU_AMBIGUOUS"
        return row['SKU'] # Keep the original SKU if it was not NaN
    
  # Apply the function to the Dataframe
Inter_sales_rp_feature['SKU'] = Inter_sales_rp_feature.apply(impute_sku, axis=1)

  # Report the success
print(f"SKU NaNs remaining after imputation: {Inter_sales_rp_feature['SKU'].isnull().sum()}")


### --- Phase 4: Feature Engineering - Part 2 (Analytical Features) --- ###

# --- Step 4.1: Revenue and Return Flags ---

  # Net Revenue (The actual money from the transaction)
"""
This is a critical feature for the 'Revenue Drivers' and 
'Profitability Index' questions.
"""
Inter_sales_rp_feature['Net_Revenue'] = Inter_sales_rp_feature['PCS'] * Inter_sales_rp_feature['RATE']

  # Is Return Flag (essential for seperating sales from returns)
"""
Since minimum PCS was 1.0, we will assume this data does not explicitly contain returns
represented by negative PCS values. However, we'll create the column defensively.
"""
Inter_sales_rp_feature['Is_Return'] = (Inter_sales_rp_feature['PCS'] < 0).astype(int)

  # Sales Velocity Measure (Transaction Size)
    # Although we have PCS, sometimes categorizing transaction size is helpful for EDA

  # We calculate the bins first, then apply labels based on how many unique bins exist
bins = pd.qcut(Inter_sales_rp_feature['PCS'], q=3, duplicates='drop')
n_bins = len(bins.cat.categories)

  # Only apply as many labels as there are bins
labels = ['Small', 'Medium', 'Large'][:n_bins]
Inter_sales_rp_feature['Sale_volume_category'] = pd.qcut(
    Inter_sales_rp_feature['PCS'], 
    q=3, 
    labels=labels, 
    duplicates='drop'
)

  # Price Segment Categorization
    # Calculate the unique bin edges first
price_bins = pd.qcut(Inter_sales_rp_feature['RATE'], q=4, duplicates='drop')

  # Check how many unique categories actually survived
n_unique_bins = len(price_bins.cat.categories)

  # Create a matching list of labels
price_labels = ['Low', 'Mid-Low', 'Mid-High', 'High'][:n_unique_bins]

  # Apply qcut again with the correct number of labels
Inter_sales_rp_feature['Price_Segment'] = pd.qcut(
    Inter_sales_rp_feature['RATE'], 
    q=4, 
    labels=price_labels, 
    duplicates='drop'
)
print("\n--- Final Feature Set Preview (head and dtypes) ---")
print(Inter_sales_rp_feature.head())
print(Inter_sales_rp_feature.dtypes)

Inter_sales_rp_feature.to_csv(
    "feature_engineered_sales_data.csv",
    index=False
)
