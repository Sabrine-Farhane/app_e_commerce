import streamlit as st
import pandas as pd
from pymongo import MongoClient
from datetime import datetime

# Connexion à MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client.e_commerce
stock_collection = db.stock
products_collection = db.products

@st.cache_data
def fetch_stock_data():
    """Récupérer les données de la collection stock"""
    data = list(stock_collection.find())
    df = pd.DataFrame(data)
    return df

def add_to_products(product, description, quantity):
    """Ajouter un produit à la collection products, décrémenter la quantité dans stock, et supprimer si quantité = 0"""
    # Convertir la série Pandas en dictionnaire
    product = product.to_dict()

    # Vérifier que la quantité est valide
    if quantity > product['quantity'] or quantity <= 0:
        st.error("Quantité invalide")
        return
    
    # Augmenter le prix de 30%
    product['price'] *= 1.3

    # Ajouter la description personnalisée
    product['description'] = description

    # Ajouter la date d'achat
    product['date_achat'] = datetime.now().isoformat()

    # Modifier la quantité
    product['quantity'] = quantity

    # Supprimer les champs inutiles pour la collection products
    product.pop('_id', None)
    product.pop('seuil', None)

    # Insérer dans la collection products
    products_collection.insert_one(product)

    # Décrémenter la quantité dans stock
    stock_collection.update_one({'name': product['name']}, {'$inc': {'quantity': -quantity}})

    # Vérifier si la quantité restante est 0 et supprimer le produit de la collection stock si c'est le cas
    updated_product = stock_collection.find_one({'name': product['name']})
    if updated_product['quantity'] <= 0:
        stock_collection.delete_one({'name': product['name']})

def add_products():
    st.title('📦 Gestion des Stocks')

    # Récupérer les données de la collection stock
    df = fetch_stock_data()
    
    if df.empty:
        st.warning("Aucun stock disponible.")
        return

    # Afficher les produits du stock avec leurs quantités et prix dans un tableau
    st.subheader('Produits en Stock')
    
    # Styling options
    st.markdown("""
        <style>
            .stock-table {
                margin-bottom: 20px;
                border: 1px solid #e0e0e0;
                border-radius: 10px;
                background-color: #f8f9fa;
                padding: 15px;
            }
            .product-name {
                font-weight: bold;
                color: #2b2b2b;
            }
            .quantity-label {
                color: #007bff;
            }
            .price-label {
                color: #28a745;
            }
            .form-container {
                margin-top: 10px;
            }
        </style>
    """, unsafe_allow_html=True)

    for _, row in df.iterrows():
        with st.form(f"form_{row['name']}"):
            st.markdown(f"<div class='stock-table'>", unsafe_allow_html=True)
            st.markdown(f"<span class='product-name'>{row['name']}</span>", unsafe_allow_html=True)
            st.markdown(f"<div class='quantity-label'>Quantité disponible: {row['quantity']}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='price-label'>Prix: {row['price']} $</div>", unsafe_allow_html=True)

            # Champs pour ajouter une description personnalisée et une quantité
            description = st.text_input(f"Description pour {row['name']}", "")
            quantity = st.number_input(f"Quantité pour {row['name']}", min_value=1, max_value=row['quantity'], step=1)

            submitted = st.form_submit_button(f"Ajouter {row['name']} au produit")
            if submitted:
                add_to_products(row, description, quantity)
                st.success(f"{row['name']} ajouté à la collection products avec {quantity} unités!")
            
            st.markdown("</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    add_products()
