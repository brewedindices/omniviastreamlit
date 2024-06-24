# app.py
import streamlit as st

# --- Streamlit Page Configuration ---
st.set_page_config(
    page_title="Omnivia Survey Platform",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon=":bar_chart:"
)

from modules import personas, questions, results, analytics, utils, dashboard, price_sensitivity, live_polling
from PIL import Image
from streamlit_option_menu import option_menu
import json
import requests
from pymongo import MongoClient
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG)

# --- Load Brand Assets ---
def load_brand_assets():
    logo_path = "logo.png"  # Replace with your logo path
    primary_color = "#FF6F61"
    try:
        logo = Image.open(logo_path)
        return logo, primary_color
    except FileNotFoundError:
        logging.error("Logo file not found.")
        return None, primary_color

logo_image, primary_color = load_brand_assets()

# --- Main App Logic ---
def main():
    with st.container():
        if logo_image:
            st.image(logo_image, use_column_width=True)
        st.title("Omnivia Survey Platform")

        # --- Navigation ---
        selected = option_menu(
            menu_title=None,
            options=["Demand Meter", "Price Sensitivity", "Live Polling"],
            icons=["bar-chart", "graph-up-arrow", "chat-dots"],
            menu_icon="cast",
            default_index=0,
            styles={
                "container": {"padding": "5!important", "background-color": "#2A2A2A"},
                "icon": {"color": "white"},
                "nav-link": {"font-size": "16px", "text-align": "left", "margin": "0px", "--hover-color": "#D65A50"},
                "nav-link-selected": {"background-color": "#D65A50"},
            }
        )

        # --- App Sections ---
        try:
            if selected == "Demand Meter":
                dashboard.run_dashboard()  # Call the module to run Demand Meter
            elif selected == "Price Sensitivity":
                price_sensitivity.run_price_sensitivity()  # Call the module to run Price Sensitivity
            elif selected == "Live Polling":
                live_polling.run_live_polling()  # Call the module to run Live Polling
        except Exception as e:
            st.error(f"Error running {selected}: {str(e)}")
            logging.error(f"Error running {selected}: {str(e)}")
            utils.log_error(selected, str(e))

if __name__ == "__main__":
    main()
