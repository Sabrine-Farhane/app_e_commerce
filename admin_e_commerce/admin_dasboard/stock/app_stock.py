import streamlit as st
import pandas as pd
import joblib
from pymongo import MongoClient
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
from datetime import datetime, timedelta

@st.cache_resource
def load_model():
    return joblib.load('stock_model.pkl')

@st.cache_data
def fetch_data():
    client = MongoClient("mongodb://localhost:27017/")
    db = client.e_commerce
    collection = db.stock
    data = list(collection.find())
    df = pd.DataFrame(data)
    if '_id' in df.columns:
        df['_id'] = df['_id'].astype(str)
    df['date_de_validite'] = pd.to_datetime(df['date_de_validite'], errors='coerce')
    return df

def app_stock():
    # Load the prediction model
    model = load_model()

    st.title('📊 Stock Prediction and Analysis Dashboard')

    # Fetch and display data from MongoDB
    df = fetch_data()
    st.write("Data from MongoDB:", df.head())

    # Check for products with expiration dates within 2 months
    today = datetime.now()
    alert_threshold = today + timedelta(days=60)
    expiring_soon = df[df['date_de_validite'] <= alert_threshold]

    if not expiring_soon.empty:
        st.warning("⚠️ The following products will expire within the next 2 months:")
        st.write(expiring_soon[['name', 'date_de_validite', 'quantity', 'category']])
    else:
        st.success("✅ No products are expiring within the next 2 months.")

    # New: Check for products below their threshold quantity
    below_threshold = df[df['quantity'] <= df['seuil']]
    if not below_threshold.empty:
        st.error("🚨 The following products are below their threshold quantity:")
        st.write(below_threshold[['name', 'quantity', 'seuil', 'category']])
    else:
        st.success("✅ All products have sufficient stock.")

    # Sidebar for user inputs
    st.sidebar.header('🔍 Filter Products')
    product_name = st.sidebar.selectbox("Product", df['name'].unique() if 'name' in df.columns else [])
    quantity = st.sidebar.number_input("Quantity", min_value=0, value=10)
    price = st.sidebar.number_input("Price", min_value=0.0, value=1125.0)
    category = st.sidebar.selectbox("Category", df['category'].unique() if 'category' in df.columns else [])

    start_date = st.sidebar.date_input("Start Date", pd.to_datetime(df['date_de_validite'].min()).date() if not df['date_de_validite'].empty else pd.to_datetime('today').date())
    end_date = st.sidebar.date_input("End Date", pd.to_datetime(df['date_de_validite'].max()).date() if not df['date_de_validite'].empty else pd.to_datetime('today').date())

    # Filter data based on user selection
    filtered_df = df[(pd.to_datetime(df['date_de_validite']) >= pd.to_datetime(start_date)) & (pd.to_datetime(df['date_de_validite']) <= pd.to_datetime(end_date))]

    # Display filtered data
    st.write(f"📅 Data from {start_date} to {end_date}", filtered_df)

    # Data Visualizations
    st.subheader('📈 Quantity Trends Over Time')
    if not df.empty:
        df_sorted = df.sort_values(by='date_de_validite')
        st.line_chart(df_sorted.set_index('date_de_validite')['quantity'])

    st.subheader('💰 Price Distribution')
    if 'price' in df.columns:
        fig, ax = plt.subplots()
        ax.hist(df['price'].dropna(), bins=30, edgecolor='k', alpha=0.7)
        ax.set_title('Price Distribution')
        ax.set_xlabel('Price')
        ax.set_ylabel('Frequency')
        st.pyplot(fig)

    st.subheader('🔍 Correlation Heatmap')
    if 'quantity' in df.columns and 'price' in df.columns:
        corr_matrix = df[['quantity', 'price']].corr()
        fig, ax = plt.subplots()
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', ax=ax)
        st.pyplot(fig)

    st.subheader('🛒 Interactive Scatter Plot')
    if 'category' in df.columns:
        fig = px.scatter(df, x='price', y='quantity', color='category', title='Price vs Quantity by Category')
        st.plotly_chart(fig)

    # Prepare input data for prediction
    input_data = {
        'quantity': [quantity],
        'price': [price]
    }
    if 'category' in df.columns:
        for cat in df['category'].unique():
            input_data[f'category_{cat}'] = [1 if cat == category else 0]
    input_df = pd.DataFrame(input_data)

    # Make a prediction
    if st.sidebar.button("Predict"):
        try:
            prediction = model.predict(input_df)[0]
            st.sidebar.write(f"Predicted Quantity: {prediction}")
        except Exception as e:
            st.sidebar.error(f"Error in prediction: {e}")

    # Statistical Summary
    st.subheader('📊 Statistical Summary')
    st.write(df.describe())

if __name__ == "__main__":
    app_stock()
