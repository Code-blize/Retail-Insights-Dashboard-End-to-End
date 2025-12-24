### --- Phase 1: Initial Data Inspection (The Basics) --- ###

# --- Step 1: Loading the data ---

import pandas as pd
import numpy as np
from itertools import combinations
from collections import Counter
import seaborn as sns
import matplotlib.pyplot as plt


Inter_sales_rp = pd.read_csv(r'c:\Users\obasi\Downloads\International sale Report.csv', encoding= 'latin1' )

# --- Step 2: Getting the Dimensions ---
print(f'The dataset has {Inter_sales_rp.shape[0]} rows and {Inter_sales_rp.shape[1]} columns')

# --- Step 3: Inspecting the Data Types and Missing Values ---
print(Inter_sales_rp.info())



### --- Phase 2: Targeted Data Cleaning --- ###

# --- Step 2.1: Drop Redundant and Useless rows --- #

  # Drop the redundant 'index' columns
try:
    Inter_sales_rp = Inter_sales_rp.drop('index', axis=1)
except KeyError:
    pass

  # Drop rows where key columns are nulls. We can use the 'style' column as a proxy
     # since 6 different columns are null for the same 1040 rows.
Inter_sales_rp.dropna(subset=['Style'], inplace=True)

# --- Step 2.2: Robust Numerical Conversion ---

numerical_cols = ['PCS', 'RATE', 'GROSS AMT']

for col in numerical_cols:
    # Use pd.to_numeric with errors='coerce' to turn bad strings (like 'RATE') into NaN
    Inter_sales_rp[col] = pd.to_numeric(Inter_sales_rp[col], errors='coerce')
    """ 
    The errors='coerce' parameter tells Panda: "Try to convert the value to a value
    to a number. If you fail, don't crash the code; instead, change the problematic value
    into NaN ( Not a Number).
    """ 

print("\n --- Mininum Value Check --- \n")
print("Minimum PCS:", Inter_sales_rp['PCS'].min())
print("Minimum Rate:", Inter_sales_rp['RATE'].min())
print("Minimum GROSS AMT:", Inter_sales_rp['GROSS AMT'].min())

# --- Step 2.3: Date Type Conversion ---

  # convert the 'DATE' column to datetime format
    # Pandas is usually smart, but specifying the format ('%m-%d-%y) is better
Inter_sales_rp['DATE'] = pd.to_datetime(Inter_sales_rp['DATE'], format='%m-%d-%y', errors='coerce')

# --- Step 2.4: Feature engineering - Create new columns for Month and Year

Inter_sales_rp['Transaction_Month'] = Inter_sales_rp['DATE'].dt.month
Inter_sales_rp['Transaction_Year'] = Inter_sales_rp['DATE'].dt.year

# --- Step 2.5: Drop the redundant 'Months' ---
try: 
    Inter_sales_rp = Inter_sales_rp.drop('Months', axis=1)
except KeyError:
    pass

  # List of columns to standardize
text_cols = ['CUSTOMER', 'Style', 'SKU', 'Size']


# --- Step 2.6: Standarding Text ---

 # lists of column to standardize
for col in text_cols:
    # Convert to string (to handle any potential non-string object types gracefully)
    # Convert to lowercase
    # Strip leading/trailing whitespace
    Inter_sales_rp[col] = Inter_sales_rp[col].astype(str).str.lower().str.strip()

print("--- Data Structure After Date Cleaning & Feature Creation ---")
print(Inter_sales_rp.head())
print("\n--- Check Data Types Again ---")
print(Inter_sales_rp.dtypes)

Inter_sales_rp_cleaned = Inter_sales_rp.copy()
Inter_sales_rp_cleaned.to_csv("cleaned_sales_data.csv", index=False)
