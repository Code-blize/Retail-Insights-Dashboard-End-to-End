### --- Phase 6: Predictive Modeling --- ###

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import pickle

# 1. Feature Selection & Engineering
# We use 'Style', 'Size', and 'PCS' (Quantity) as primary drivers.
# 'Month' is included to capture seasonal trends Joseph mentioned.
features = ['Style', 'Size', 'PCS', 'Transaction_Month']
X = pd.get_dummies(Inter_sales_rp_feature[features], drop_first=True) # One-hot encoding for categories
y = Inter_sales_rp_feature['GROSS AMT']

# 2. Data Splitting (80% Train, 20% Test)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 3. Model Training
# Random Forest is excellent for capturing non-linear relationships in retail data.
model = RandomForestRegressor(n_estimators=100,max_depth=10, n_jobs=-1, random_state=42)
model.fit(X_train, y_train)

# 4. Evaluation
y_pred = model.predict(X_test)
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Absolute Error: ${mae:.2f}") # Average prediction error
print(f"Model Accuracy (R2): {r2:.2%}")   # % of variance explained

# 5. Save the model for Deployment
with open('amazon_sales_model.pkl', 'wb') as f:
    pickle.dump(model, f)

importances = pd.Series(model.feature_importances_, index=X.columns)
importances.nlargest(10).plot(kind='barh')
plt.title('Top 10 Drivers of Revenue')
plt.show()
