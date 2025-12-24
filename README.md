# 📦 Amazon International Apparel Sales: End-to-End Pipeline

> **A Data Science Challenge by Joseph Edet (Joebass)**

## 📌 Project Overview

This project addresses a real-world scenario involving extremely messy Amazon sales data. The goal was to build a robust pipeline that cleans "dirty" data, extracts actionable business insights through EDA, and deploys a machine learning model to predict future revenue.

### 🎯 Business Objectives

* **Revenue Optimization:** Identify the top 20% of SKUs driving 80% of sales.
* **Inventory Efficiency:** Highlight "Dead Stock" (Styles with < 50 units sold).
* **Predictive Analytics:** Build a model to estimate `Gross Amount` for future orders.

---

## 🏗️ Project Architecture

The project is structured to ensure scalability and reproducibility:

1. **Data Ingestion:** Loading raw, unformatted CSV/Excel files.
2. **Cleaning & Preprocessing:** Handling the complex null values in the `SKU` column using "Middle Code" logic.
3. **Feature Engineering:** Creating seasonal indicators and categorical encodings.
4. **Modeling:** Training a **Random Forest Regressor** for revenue prediction.
5. **Deployment:** A live web interface built with **Streamlit**.

---

## 🛠️ Technical Stack

* **Language:** Python 3.x
* **Libraries:** Pandas, NumPy, Scikit-learn, Seaborn, Matplotlib
* **Deployment:** Streamlit, Pickle
* **Version Control:** Git & GitHub

---

## 📊 Key Insights & Results

| Metric | Result |
| --- | --- |
| **Model Accuracy (R²)** | 85.4% (Sample) |
| **Mean Absolute Error** | $12.50 (Sample) |
| **Top Style** | Western Wear |
| **Top Size** | Large / XL |

### 🔍 Data Quality Highlight

A major win in this project was the **SKU Ambiguity Resolution**. By parsing strings in the SKU column, I was able to reconstruct missing data points for over [X]% of the null values, significantly improving the training data quality.

---

## 🚀 Installation & Usage

1. **Clone the Repository:**
```bash
git clone https://github.com/your-username/amazon-sales-pipeline.git
cd amazon-sales-pipeline

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

## 📜 Acknowledgments

Special thanks to **Joseph Edet** for providing the "extremely dirty" dataset and creating a challenge that pushes the boundaries of data cleaning and analytical thinking.

---
