import streamlit as st
import pandas as pd
from scraping.amazon_selenium import fetch_amazon_data_selenium, save_to_csv as save_selenium_to_csv
from .amazon_bs4 import fetch_amazon_data, save_to_csv as save_bs4_to_csv

def main():
    st.title('Amazon Data Extraction Dashboard')

    menu = ["Selenium Data Extraction", "BeautifulSoup Data Extraction"]
    choice = st.sidebar.selectbox("Select Option", menu)

    if choice == "Selenium Data Extraction":
        st.subheader("Extract Data using Selenium")
        
        url = st.text_input("Amazon URL", "https://www.amazon.com/s?k=laptops")
        if st.button("Fetch Data"):
            with st.spinner('Fetching data...'):
                data = fetch_amazon_data_selenium(url)
                if data:
                    st.write("Extracted Data (Selenium):", data)  # Afficher les données extraites
                    save_selenium_to_csv(data, 'amazon_products_selenium.csv')
                    st.success("Data fetched and saved successfully using Selenium.")
                    st.dataframe(pd.DataFrame(data))  # Display data in the app
                else:
                    st.error("No data found or error occurred during extraction.")

    elif choice == "BeautifulSoup Data Extraction":
        st.subheader("Extract Data using BeautifulSoup")
        
        url = st.text_input("Amazon URL", "https://www.amazon.com/s?k=laptops")
        if st.button("Fetch Data"):
            with st.spinner('Fetching data...'):
                data = fetch_amazon_data(url)
                if data:
                    st.write("Extracted Data (BeautifulSoup):", data)  # Afficher les données extraites
                    save_bs4_to_csv(data, 'amazon_products_bs4.csv')
                    st.success("Data fetched and saved successfully using BeautifulSoup.")
                    st.dataframe(pd.DataFrame(data))  # Display data in the app
                else:
                    st.error("No data found or error occurred during extraction.")

if __name__ == "__main__":
    main()
