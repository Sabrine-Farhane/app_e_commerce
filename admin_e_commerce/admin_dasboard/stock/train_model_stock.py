import pandas as pd
import numpy as np
from pymongo import MongoClient
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error
import joblib

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client.e_commerce
collection = db.stock

# Fetch data
data = list(collection.find())
df = pd.DataFrame(data)
df['date'] = pd.to_datetime(df['date'])

# Preprocessing
df = pd.get_dummies(df, columns=['category'], drop_first=True)
X = df[['quantity', 'price'] + [col for col in df.columns if 'category_' in col]]
y = df['quantity']

# Train-test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f'Mean Squared Error: {mse}')

# Save the model
joblib.dump(model, 'stock_model.pkl')
