import streamlit as st
from pymongo import MongoClient
import pandas as pd
from bson.objectid import ObjectId

def app_commande():
    # Connect to MongoDB
    client = MongoClient("mongodb://localhost:27017/")
    db = client["e_commerce"]
    collection = db["orders"]

    # Fetch all orders from the database
    orders = collection.find()

    # Convert orders to a DataFrame
    orders_list = []
    for order in orders:
        # Ensure correct field names and types
        items = order.get("items", [])
        for item in items:
            orders_list.append({
                "_id": str(order.get("_id", "")),  # Convert ObjectId to string
                "Date": order.get("date", "No Date"),
                "ProductName": item.get("productName", "No Product Name"),
                "Client": order.get("user", {}).get("name", "No Client"),
                "Com-pere": order.get("user", {}).get("email", "No Com-pere"),
                "Quantity": item.get("quantity", 0),
                "Total": order.get("total", 0),
                "Status": order.get("status", "Not Viewed")  # Added status field
            })

    df = pd.DataFrame(orders_list)

    # Set up the Streamlit app
    st.title("Order Management Dashboard")

    # Style the DataFrame
    def style_status(val):
        color = 'green' if val == 'Viewed' else 'red'
        return f'color: {color};'

    # Display the orders in a table with styled Status column
    styled_df = df.style.applymap(style_status, subset=['Status'])
    
    # Display the styled DataFrame
    st.write(styled_df.to_html(escape=False, index=False), unsafe_allow_html=True)

    # Optionally, add an "OK" button for each non-viewed order
    for index, row in df.iterrows():
        # Generate a unique key for each button
        unique_key = f"ok_{row['_id']}_{index}"
        if row["Status"] == "Not Viewed":
            if st.button(f"Mark as Viewed {row['_id']}", key=unique_key):
                # Update the order status in the database
                collection.update_one(
                    {"_id": ObjectId(row['_id'])},
                    {"$set": {"status": "Viewed"}}
                )
                st.success(f"Order {row['_id']} marked as viewed.")
                st.experimental_rerun()  # Refresh the page after updating

if __name__ == "__main__":
    app_commande()
