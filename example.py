import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Set page configuration
st.set_page_config(
    page_title="Executive Report",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Navigation Tabs
tabs = ['Overview', 'Price & Performance', 'Portfolio & Management', 'Fees & Minimums', 'Distributions', 'News & Reviews']
tab = st.sidebar.radio("Navigation", tabs)

# Dummy data
def generate_dummy_data():
    dates = pd.date_range(start="2023-01-01", periods=100, freq="D")
    values = np.random.randn(100).cumsum()
    return pd.DataFrame({"Date": dates, "Value": values})

# Header
st.title("Executive Report")
st.markdown("""
A comprehensive report highlighting key financial metrics, market trends, and potential risks for 
**PSS World Medical, Inc. (PSSI)**.
""")

# Main content based on selected tab
if tab == "Overview":
    st.header("Company Overview")
    st.markdown("""
    **PSS World Medical, Inc. (PSSI)**

    - **Sector**: Healthcare
    - **Industry**: Medical Distribution
    - **Market Cap**: $2.3B
    """)
    st.image("https://via.placeholder.com/600x400", caption="Company Headquarters", use_column_width=True)
    st.subheader("Key Highlights")
    st.markdown("""
    - Strong market position
    - Consistent revenue growth
    - Expanding product lines
    """)

elif tab == "Price & Performance":
    st.header("Price & Performance")

    st.subheader("Current Prices")
    current_prices = {
        "Price as of 02/27/2018": "$254.07",
        "Change": "-$3.23 (-1.26%)",
        "SEC Yield": "1.67%",
        "52-week high 01/26/2018": "$265.42",
        "52-week low 04/13/2017": "$215.11",
        "Range": "$50.31 (23.39%)"
    }
    st.table(pd.DataFrame.from_dict(current_prices, orient='index', columns=['Value']).reset_index().rename(columns={"index": "Metric"}))

    st.subheader("Historical Prices")
    historical_prices = pd.DataFrame({
        "Date": ["02/22/2018", "02/23/2018", "02/26/2018", "02/27/2018", "02/28/2018"],
        "Price": ["$250.26", "$254.29", "$257.30", "$254.07", "$251.27"]
    })
    st.table(historical_prices)

    st.subheader("Performance")
    data = generate_dummy_data()
    fig = px.line(data, x="Date", y="Value", title="Performance Over Time", labels={"Date": "Date", "Value": "Value"})
    fig.update_layout(height=400)
    st.plotly_chart(fig)

    st.subheader("Average Annual Returns")
    annual_returns = pd.DataFrame({
        "Metric": ["500 Index Fund Inv", "S&P 500 Index"],
        "1 Year": ["16.94%", "17.01%"],
        "3 Year": ["11.00%", "11.14%"],
        "5 Year": ["14.57%", "14.73%"],
        "10 Year": ["9.60%", "9.73%"],
        "Since Inception": ["11.12%", "-"]
    })
    st.table(annual_returns)

    st.subheader("After-tax Returns")
    after_tax_returns = pd.DataFrame({
        "Metric": ["500 Index Fund Inv", "Returns after taxes on distributions", "Returns after taxes on distributions and sale of fund shares"],
        "1 Year": ["21.67%", "12.64%", "20.44%"],
        "3 Year": ["11.26%", "8.71%", "9.70%"],
        "5 Year": ["15.62%", "12.51%", "14.24%"],
        "10 Year": ["8.37%", "6.75%", "7.61%"],
        "Since Inception": ["11.11%", "-", "-"]
    })
    st.table(after_tax_returns)

elif tab == "Portfolio & Management":
    st.header("Portfolio & Management")
    st.markdown("Details about the portfolio and management team go here.")

elif tab == "Fees & Minimums":
    st.header("Fees & Minimums")
    st.markdown("Details about the fees and minimums go here.")

elif tab == "Distributions":
    st.header("Distributions")
    st.markdown("Details about the distributions go here.")

elif tab == "News & Reviews":
    st.header("News & Reviews")
    st.markdown("Details about the latest news and reviews go here.")

# Custom CSS for styling
st.markdown("""
    <style>
    .report-container { max-width: 1200px; margin: 0 auto; }
    .header { background-color: #f0f2f6; padding: 20px; border-radius: 5px; margin-bottom: 20px; text-align: center; }
    .header h1 { font-size: 2.5em; margin-bottom: 0; }
    .header p { font-size: 1.2em; color: #666; }
    .main { background-color: #fff; padding: 20px; border-radius: 5px; margin-bottom: 20px; }
    .section-title { font-size: 1.8em; margin-bottom: 20px; border-bottom: 2px solid #e0e0e0; padding-bottom: 10px; }
    .metric-box { text-align: center; background-color: #f9fafb; padding: 10px; border-radius: 5px; margin-bottom: 20px; }
    .metric-box h2 { font-size: 1.5em; margin: 0; }
    .metric-box p { font-size: 1.2em; color: #666; margin: 0; }
    .visual-card { background-color: #f9fafb; padding: 10px; border-radius: 5px; margin-bottom: 20px; }
    </style>
""", unsafe_allow_html=True)
