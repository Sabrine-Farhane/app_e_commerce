import streamlit as st
from pymongo import MongoClient
import pandas as pd
import plotly.express as px
from bson.objectid import ObjectId

# Set the page configuration at the top
st.set_page_config(page_title="Top 5 Products Per Month", layout="wide")

# MongoDB connection setup
client = MongoClient("mongodb://localhost:27017/")
db = client['e_commerce']
orders_collection = db['orders']

# Load and process data
def load_data():
    orders = list(orders_collection.find({}))
    data = []
    for order in orders:
        user = order.get('user', {})
        for item in order.get('items', []):
            data.append({
                'productName': item['productName'],
                'quantity': item['quantity'],
                'price': item['price'],
                'date': pd.to_datetime(order['date']).strftime('%Y-%m')
            })
    return pd.DataFrame(data)

df = load_data()

def display_top_products():
    # Group data by month and product, then find the top 5 products per month
    top_products_per_month = (
        df.groupby(['date', 'productName'])
        .agg({'quantity': 'sum'})
        .reset_index()
        .sort_values(['date', 'quantity'], ascending=[True, False])
        .groupby('date')
        .head(5)
    )

    # Display the results in Streamlit
    st.title("Top 5 Most Sold Products Per Month")
    st.write("This dashboard shows the top 5 most sold products for each month.")

    for month in top_products_per_month['date'].unique():
        st.subheader(f"Month: {month}")
        month_data = top_products_per_month[top_products_per_month['date'] == month]
        st.table(month_data[['productName', 'quantity']])

        # Plot
        fig = px.bar(
            month_data,
            x='productName',
            y='quantity',
            title=f"Top 5 Products for {month}",
            labels={'quantity': 'Units Sold'},
        )
        st.plotly_chart(fig)

if __name__ == "__main__":
    display_top_products()
