import streamlit as st
from app_top_products import display_top_products
from ventes.app import app as app_ventes
from stock.app_stock import app_stock
from commandes.commande import app_commande
from scraping.app_scrapp import main as display_scraping_results
from add_products import add_products
from client_fidele import display_loyal_customers

# Appliquer des styles personnalisés
st.markdown(
    """
    <style>
    .css-1d391kg {width: 280px; padding-top: 0px;}
    .css-1d391kg {background-color: #f8f9fa; border-right: 1px solid #e0e0e0;}
    .sidebar-header {
        display: flex;
        align-items: center;
        padding: 10px;
        border-bottom: 1px solid #e0e0e0; /* Ajouter une ligne fine sous l'en-tête */
    }
    .ecostore-title {
        font-family: 'Arial', sans-serif;
        font-size: 28px;
        font-weight: bold;
        color: #007BFF;
        margin-left: 10px; /* Ajouter un peu d'espace entre le logo et le texte */
        flex: 1;
        text-align: left; /* Alignement du texte à gauche */
    }
    
    .ecostore-text {
        font-family: 'Arial', sans-serif;
        color: #6c757d;
        font-size: 14px;
        text-align: center;
        margin-bottom: 20px;
    }
    .stButton button {
        width: 100%;
        padding: 10px;
        font-size: 16px;
        background-color: transparent;
        color: #000000;
        border: none;
        border-radius: 8px;
        transition: background-color 0.3s ease, transform 0.2s ease;
        box-shadow: none;
        border-bottom: 1px solid #e0e0e0; /* Ajouter une ligne fine sous chaque bouton */
    }
    .stButton button:hover {
        background-color: #e0e0e0;
        transform: scale(1.02);
    }
    .stButton.active button {
        background-color: #cccccc;
    }
    .stButton {
        margin-bottom: 0; /* Supprimer la marge en bas des boutons pour éviter des espaces supplémentaires */
    }
    </style>
    """,
    unsafe_allow_html=True
)

def main():
    # Initialiser la clé de session si elle n'existe pas
    if 'page' not in st.session_state:
        st.session_state.page = 'Sales Dashboard'

    # Configuration de la barre latérale
    st.sidebar.markdown(
        '<div class="sidebar-header">'
        
        '<div class="ecostore-title">Ecostore</div>'
        '</div>',
        unsafe_allow_html=True
    )
    
    st.sidebar.markdown('<div class="ecostore-text">Navigate to sections</div>', unsafe_allow_html=True)

    # Ajouter des boutons avec des icônes et des styles
    buttons = {
        "Sales Dashboard": "📊",
        "Stock Prediction": "📈",
        "Top Products": "🏆",
        "Orders": "📋",
        "Scraping Results": "🔍",
        "Manage Stock": "📦",
        "Loyal Customers": "💎"
    }

    # Affichage des boutons avec des icônes
    for button_text, icon in buttons.items():
        button_key = button_text.replace(" ", "_")  # Créer une clé unique pour chaque bouton
        button_class = 'active' if st.session_state.page == button_text else ''
        if st.sidebar.button(f"{icon} {button_text}", key=button_key):
            st.session_state.page = button_text

    # Logique pour afficher la page en fonction du bouton sélectionné
    if st.session_state.page == "Sales Dashboard":
        app_ventes()
    elif st.session_state.page == "Stock Prediction":
        app_stock()
    elif st.session_state.page == "Top Products":
        display_top_products()
    elif st.session_state.page == "Orders":
        app_commande()
    elif st.session_state.page == "Scraping Results":
        display_scraping_results()
    elif st.session_state.page == "Manage Stock":
        add_products()
    elif st.session_state.page == "Loyal Customers":
        display_loyal_customers()

if __name__ == "__main__":
    main()
