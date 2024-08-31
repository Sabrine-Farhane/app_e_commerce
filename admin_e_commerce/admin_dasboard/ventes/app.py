import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from pymongo import MongoClient
import joblib
from datetime import datetime

def app():
    # MongoDB connection setup
    client = MongoClient("mongodb://localhost:27017/")
    db = client['e_commerce']
    collection = db['orders']

    # Load prediction model
    @st.cache_resource
    def load_model():
        return joblib.load('sales_model.pkl')  # Assurez-vous que le modèle de prévision est correctement chargé
    
    model = load_model()

    st.title('Sales Dashboard')

    # Fetch data from MongoDB
    def fetch_data():
        data = collection.find()
        df = pd.DataFrame(list(data))
        if '_id' in df.columns:
            df['_id'] = df['_id'].astype(str)
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
        df = df.dropna(subset=['date'])
        
        if 'items' in df.columns:
            # Expand items array into separate rows
            items_df = pd.json_normalize(df['items'].explode())
            items_df.columns = [f'item_{col}' for col in items_df.columns]  # Rename columns to avoid conflict
            df = df.drop(columns=['items']).join(items_df)
        
        required_columns = ['item_productName', 'item_quantity', 'item_price', 'total', 'date', 'user']
        missing_columns = [col for col in required_columns if col not in df.columns]
        if missing_columns:
            st.write(f"Les colonnes suivantes sont manquantes : {', '.join(missing_columns)}")
            return pd.DataFrame()
        return df

    df = fetch_data()

    if df.empty:
        st.write("No data found in the 'orders' collection.")
    else:
        st.write("### Sample Data")
        st.write(df.head())

        # Total Revenue by Product
        sales_by_product = df.groupby('item_productName')['total'].sum().reset_index()
        st.subheader('📈 Total Revenue by Product')
        st.bar_chart(sales_by_product.set_index('item_productName'))

        # Sales Trend Over Time
        sales_trend = df.groupby('date')['total'].sum().reset_index()
        st.subheader('📅 Sales Trend Over Time')
        st.line_chart(sales_trend.set_index('date'))

        # Units Sold by Product
        units_sold_by_product = df.groupby('item_productName')['item_quantity'].sum().reset_index()
        st.subheader('📊 Units Sold by Product')
        st.bar_chart(units_sold_by_product.set_index('item_productName'))

        # Total Revenue by Date
        revenue_by_date = df.groupby('date')['total'].sum().reset_index()
        st.subheader('💵 Total Revenue by Date')
        st.line_chart(revenue_by_date.set_index('date'))

        # Revenue Distribution by Region
        if 'region' in df.columns:
            revenue_by_region = df.groupby('region')['total'].sum().reset_index()
            st.subheader('🌍 Revenue Distribution by Region')
            st.bar_chart(revenue_by_region.set_index('region'))

        # Payment Methods Distribution
        if 'paymentMethod' in df.columns:
            payment_methods_distribution = df['paymentMethod'].value_counts().reset_index()
            payment_methods_distribution.columns = ['Payment Method', 'Count']
            st.subheader('💳 Payment Methods Distribution')
            st.bar_chart(payment_methods_distribution.set_index('Payment Method'))

        

if __name__ == "__main__":
    app()
