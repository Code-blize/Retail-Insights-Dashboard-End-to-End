import streamlit as st
import pandas as pd
import pickle
import seaborn as sns
import matplotlib.pyplot as plt
import os

# 1. Load the Model
with open('amazon_sales_model.pkl', 'rb') as f:
    model = pickle.load(f)

# 2. Setup the UI
st.set_page_config(page_title="Amazon Revenue Predictor", page_icon="📦")
st.title("📦 Amazon Sales Revenue Predictor")
st.markdown("Enter the transaction details below to predict the **Gross Revenue**.")

# 3. User Inputs
col1, col2 = st.columns(2)

with col1:
    style = st.selectbox("Select Style", ['Western Wear', 'Ethnic Wear', 'Modern']) # Add your actual styles
    size = st.selectbox("Select Size", ['S', 'M', 'L', 'XL', 'XXL', '3XL'])
    
with col2:
    month = st.selectbox("Month", ['January', 'February', 'March', 'April', 'May', 'June', 
                                   'July', 'August', 'September', 'October', 'November', 'December'])
    pcs = st.number_input("Quantity (PCS)", min_value=1, max_value=100, value=1)

# 4. Handle Prediction Logic
if st.button("Predict Revenue"):
    # Create a dataframe for the input
    input_data = pd.DataFrame([[style, size, pcs, month]], 
                              columns=['Style', 'Size', 'PCS', 'Month'])
    
    # APPLY ONE-HOT ENCODING (Must match your training columns)
    # Pro Tip: It's safer to save your training column names to a list and re-apply them here.
    input_encoded = pd.get_dummies(input_data)
    
    # (Simplified for this example)
    # In a real app, you would align input_encoded with your model's X_train.columns
    try:
        prediction = model.predict(input_encoded)[0]
        st.success(f"### Predicted Gross Revenue: ${prediction:,.2f}")
    except Exception as e:
        st.error("Model input mismatch. Ensure the Styles and Sizes match the training data exactly.")