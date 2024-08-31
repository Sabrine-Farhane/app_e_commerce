import streamlit as st
import pandas as pd
from pymongo import MongoClient
from bson import ObjectId

# Connexion à MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client.e_commerce
orders_collection = db.orders

@st.cache_data
def fetch_orders_data():
    """Récupérer les données de la collection orders"""
    data = list(orders_collection.find())
    df = pd.DataFrame(data)
    
    # Convertir les ObjectId en chaînes de caractères
    df['_id'] = df['_id'].astype(str)
    if 'items' in df.columns:
        df['items'] = df['items'].apply(lambda x: [{k: str(v) if isinstance(v, ObjectId) else v for k, v in item.items()} for item in x])
    if 'user' in df.columns:
        df['user'] = df['user'].apply(lambda x: {k: str(v) if isinstance(v, ObjectId) else v for k, v in x.items()} if isinstance(x, dict) else x)
    
    return df

def get_most_loyal_customers(df):
    """Retourner les clients les plus fidèles en fonction du nombre de commandes passées"""
    if 'user' in df.columns:
        # Extraire les informations utilisateur du champ 'user'
        df['user_name'] = df['user'].apply(lambda x: x.get('name') if isinstance(x, dict) else None)
        df['user_email'] = df['user'].apply(lambda x: x.get('email') if isinstance(x, dict) else None)
        
        # Compter le nombre de commandes par client
        loyal_customers = df.groupby(['user_name', 'user_email']).size().reset_index(name='order_count')
        loyal_customers = loyal_customers.sort_values(by='order_count', ascending=False)
        return loyal_customers
    else:
        st.error("Les informations utilisateur ne sont pas disponibles dans les données.")
        return pd.DataFrame()

def display_loyal_customers():
    st.title("📊 Clients les plus fidèles")

    # Récupérer les données de la collection orders
    df = fetch_orders_data()

    if df.empty:
        st.warning("Aucune commande disponible.")
        return

    # Obtenir les clients les plus fidèles
    loyal_customers = get_most_loyal_customers(df)

    if not loyal_customers.empty:
        st.subheader("Top clients les plus fidèles")
        st.dataframe(loyal_customers)

        # Afficher un graphique
        st.subheader("Graphique des clients les plus fidèles")
        st.bar_chart(loyal_customers.set_index('user_name')['order_count'])

if __name__ == "__main__":
    display_loyal_customers()
