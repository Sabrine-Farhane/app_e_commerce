# amazon_selenium.py
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def fetch_amazon_data_selenium(url):
    data = []
    try:
        options = Options()
        options.add_argument("--headless")  # Exécute le navigateur en arrière-plan
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        driver.get(url)

        # Attente pour s'assurer que la page est complètement chargée
        WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'div.s-main-slot div.s-result-item'))
        )

        products = driver.find_elements(By.CSS_SELECTOR, 'div.s-main-slot div.s-result-item')
        
        if not products:
            print("No products found on the page.")

        for product in products:
            try:
                title = product.find_element(By.CSS_SELECTOR, 'span.a-text-normal').text
                price = product.find_element(By.CSS_SELECTOR, 'span.a-price-whole').text
                data.append({'title': title, 'price': price})
            except Exception as e:
                print(f"Error extracting product data: {e}")
                continue

        driver.quit()
    except Exception as e:
        print(f"Error: {e}")
        return []

    return data

def save_to_csv(data, file_path):
    if data:
        df = pd.DataFrame(data)
        df.to_csv(file_path, index=False)
        print(f"Data saved to {file_path}")
    else:
        print("No data to save.")
