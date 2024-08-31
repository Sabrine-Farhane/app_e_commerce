# amazon_bs4.py
import requests
from bs4 import BeautifulSoup
import pandas as pd

def fetch_amazon_data(url):
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Failed to fetch data: Status code {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, 'html.parser')
    data = []

    for item in soup.select('div.s-main-slot div.s-result-item'):
        try:
            title = item.select_one('span.a-text-normal').text
            price = item.select_one('span.a-price-whole').text
            data.append({'title': title, 'price': price})
        except AttributeError:
            print("Error extracting data from item.")
            continue

    if not data:
        print("No data found in the page content.")

    return data

def save_to_csv(data, file_path):
    if data:
        df = pd.DataFrame(data)
        df.to_csv(file_path, index=False)
        print(f"Data saved to {file_path}")
    else:
        print("No data to save.")
