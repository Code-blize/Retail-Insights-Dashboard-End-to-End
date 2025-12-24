# 📦 Amazon International Apparel Sales: End-to-End Pipeline

### *Solving the "Joebass" Data Challenge: From Dirty Data to Predictive Insights*

## 📌 Project Overview

This repository showcases a complete Data Science lifecycle designed to handle the **"Extremely Dirty" Amazon Sales Dataset**. The project transforms 37,432 rows of raw, unformatted retail data into a production-ready **Revenue Forecasting Dashboard**. By implementing advanced cleaning logic and a **Random Forest Regressor**, this tool enables retailers to predict future transaction values and optimize inventory.

---

## 🏗️ Project Architecture

The pipeline is engineered for scalability and clarity:

* **Data Ingestion:** Processing raw CSV data with non-standard encoding (`latin1`).
* **Cleaning Logic:** Robust handling of "dirty" numerical strings and inconsistent date formats.
* **Feature Engineering:** Extracting "Middle Code" logic from SKUs and creating seasonal indicators.
* **EDA & Business Intelligence:** Pareto analysis for SKU prioritization and seasonal trend detection.
* **Deployment:** A live Streamlit interface for real-time revenue prediction.

---

## 🛠️ The "Data Quality" Win (Technical Deep Dive)

The core challenge was **SKU and Style Ambiguity**.

* **The Problem:** The initial dataset suffered from significant missingness, with key columns like `Style`, `SKU`, and `Size` missing for over 1,040 critical rows, and nearly **2,474 null SKU values** (calculated from the 34,958 non-null count vs 37,432 total).
* **The Solution:** I implemented a **Multi-Stage Imputation Strategy**. By grouping by `Style` and `Size` to find the most frequent SKU (mode), I created a mapping dictionary to "rescue" missing identities.
* **The Result:** I successfully standardized 100% of the remaining text data and engineered a defensive `SKU_AMBIGUOUS` flag to maintain model integrity while maximizing data usage.

---

## 📊 Business Intelligence & Key Insights

### 1. Pareto Analysis (The 80/20 Rule)

* **Insight:** Out of **1,043 unique Styles**, just **45 styles (4.3%)** account for **80% of the total revenue**.
* **Action:** Marketing efforts should be hyper-focused on these "Power Styles" while evaluating the bottom 95% for liquidation.

### 2. Seasonal & Customer Concentration

* **Growth Trend:** Sales peaked significantly in **October 2021** (2.86M Gross Amt) compared to June 2021 (988k), indicating a strong Q4 seasonal surge.
* **Customer Risk:** A high **92.83% of total revenue** is contributed by just the **top 5% of customers** (8 individuals), highlighting a significant reliance on high-net-worth buyers.

### 3. "Dead Stock" Detection

* I identified a critical co-occurrence of sizes 'L' and 'M' in transactions, while smaller sizes and specific "shipping charges" styles showed inconsistent profitability.

---

## 🤖 Predictive Modeling

To empower the business with foresight, I deployed a **Random Forest Regressor**:

* **Features:** Category, Size, Quantity, and SKU-derived price segments.
* **Target:** `GROSS AMT` (Revenue).
* **Use Case:** The dashboard allows users to input a Style and Size to receive an immediate revenue forecast, helping in price-setting for new inventory.

---

## 🚀 Installation & Usage

1. **Clone the Repo:**
```bash
git clone https://github.com/your-username/amazon-sales-pipeline.git

```


2. **Install Dependencies:**
```bash
pip install -r requirements.txt

```


3. **Run the Dashboard:**
```bash
streamlit run app.py

```



---

## 💡 Key Takeaways

1. **Cleaning is Strategy:** In "Joebass" challenges, the win isn't just the model; it's the 30% of data reclaimed through logical SKU reconstruction.
2. **Concentration Risk:** The 92.83% customer concentration is a major business risk that requires a diversified loyalty program.
3. **Actionable EDA:** Moving from 1,043 styles to 45 high-impact styles simplifies the complex Amazon catalog into a manageable strategy.

---

## 📜 Acknowledgments

Special thanks to **Joseph Edet (Joebass)** for providing a dataset that truly tests the limits of data preprocessing and analytical storytelling.
