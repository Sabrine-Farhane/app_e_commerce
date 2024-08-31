import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import joblib

# Load data
data = pd.read_csv(r'C:\Users\dell\Downloads\Online Sales Data.csv')

# Data preprocessing
data['Date'] = pd.to_datetime(data['Date'])
data['Year'] = data['Date'].dt.year
data['Month'] = data['Date'].dt.month

# Features and target
features = ['Units Sold', 'Unit Price', 'Year', 'Month']
target = 'Total Revenue'

X = data[features]
y = data[target]

# Split the data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

# Save the model
joblib.dump(model, 'sales_model.pkl')
print("Model saved as sales_model.pkl")

