import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
from itertools import product
from modules import utils, narrative  # Ensure you have the utils and narrative modules defined
import logging
from openai import OpenAI
import os

# Configure logging
logging.basicConfig(level=logging.INFO)

# Custom CSS for better visuals and modern look
st.markdown("""
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #1E1E1E;
            color: #D4D4D4;
        }
        .report-title {
            font-size: 2.5rem;
            color: #FFC300;
            margin-top: 20px;
            margin-bottom: 20px;
        }
        .section-header {
            font-size: 1.8rem;
            color: #FFD700;
            margin-top: 20px;
            margin-bottom: 10px;
        }
        .key-insights {
            font-size: 1.2rem;
            color: #E0E0E0;
            background-color: #333333;
            padding: 20px;
            border-radius: 10px;
            margin-top: 20px;
        }
        .metric {
            font-size: 1.5rem;
            font-weight: bold;
            color: #FFD700;
            margin: 10px 0;
        }
        .sidebar .sidebar-content {
            background-color: #333333;
            padding: 20px;
            border-radius: 10px;
        }
        .sidebar .sidebar-content input, .sidebar .sidebar-content select {
            background-color: #444444;
            color: #D4D4D4;
            border: none;
            border-radius: 5px;
            padding: 10px;
        }
        .sidebar .sidebar-content button {
            background-color: #FFC300;
            color: #1E1E1E;
            border: none;
            border-radius: 5px;
            padding: 10px 20px;
            margin-top: 10px;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize OpenAI client
openai_client = OpenAI()
openai_client.api_key = os.getenv('OPENAI_API_KEY')
if not openai_client.api_key:
    st.error("OpenAI API key is missing. Please set the OPENAI_API_KEY environment variable.")

# Function to generate narrative summary using OpenAI GPT
def generate_narrative_summary(df):
    prompt = f"Generate an executive summary for the following data:\n{df.to_string(index=False)}"

    try:
        response = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=200
        )

        # Check if the response has a 'choices' field and if it's not empty
        if response.choices:
            summary = response.choices[0].message.content.strip()
            return summary
        else:
            st.warning("OpenAI response did not contain a summary. Please try again later.")
            return ""  # Return an empty string if there's no summary

    except Exception as e:
        logging.error(f"Error generating narrative summary: {str(e)}")
        st.error(f"Error generating narrative summary. Please try again later.")
        return "" 

# Function to generate predictive analytics 
def generate_predictive_analytics(df):
    df['Predicted_Demand_Score'] = df['Demand Score'] * 1.05  # Mock prediction logic
    return df[['Feature', 'Tagline', 'Price', 'Predicted_Demand_Score']]

# Function to personalize dashboard based on user preferences
def personalized_insights(user_preferences):
    insights = f"Personalized insights based on preferences: {user_preferences}"
    return insights

# Function to set up alerts and notifications
def setup_alerts():
    st.sidebar.header("Alerts and Notifications")
    st.sidebar.text_input("Enter Alert Criteria", key="alert_criteria")
    if st.sidebar.button("Set Alert"):
        st.sidebar.success("Alert set successfully!")

# Run the main dashboard application
def run_dashboard():
    try:
        st.markdown("<h1 class='report-title'>Executive Dashboard - AI-Powered Demand Insights</h1>", unsafe_allow_html=True)

        st.sidebar.markdown("<div class='sidebar-content'>", unsafe_allow_html=True)
        product_name = st.sidebar.text_input("Product Name:", placeholder="Enter the product name")
        product_features = st.sidebar.text_area("Enter Product Features (comma-separated):", placeholder="Feature1, Feature2, Feature3")
        tagline_options = st.sidebar.text_area("Enter Tagline Options (comma-separated):", placeholder="Tagline1, Tagline2, Tagline3")
        price_options_str = st.sidebar.text_input("Enter Price Options (comma-separated):", placeholder="9.99, 19.99, 29.99")

        try:
            price_options = [float(x.strip()) for x in price_options_str.split(',')] if price_options_str else []
            price_error = False
        except ValueError:
            price_error = True
            price_options = []
            st.sidebar.warning("Invalid price options. Please enter comma-separated numbers.")

        st.sidebar.markdown("<h3 class='section-header'>Simulation Configuration</h3>", unsafe_allow_html=True)
        num_bots = st.sidebar.number_input("Enter number of bots for simulation:", min_value=1, max_value=1000, value=100)
        male_percentage = st.sidebar.slider("Male Percentage", 0, 100, 50)
        income_range = st.sidebar.slider("Income Range (in thousands)", 0, 500, (50, 150))
        interests = st.sidebar.text_input("Enter Interests (comma-separated):", placeholder="Golf, Yoga, Basketball")
        interests_list = [i.strip() for i in interests.split(",")] if interests else []

        if interests_list:
            st.sidebar.markdown("<h3 class='section-header'>Interests:</h3>", unsafe_allow_html=True)
            st.sidebar.markdown(" ".join([f'<span style="background-color: #FFD700; color: #1E1E1E; padding: 5px 10px; border-radius: 5px; margin: 5px;">{interest}</span>' for interest in interests_list]), unsafe_allow_html=True)

        # Initialize df outside the conditional block
        df = pd.DataFrame() 

        if st.sidebar.button("Calculate Demand") and not price_error:
            if not all([product_name, product_features, tagline_options, price_options]):
                st.warning("Please fill in all product details.")
            else:
                features = [x.strip() for x in product_features.split(',')]
                taglines = [x.strip() for x in tagline_options.split(',')]
                st.write(f"**Product Name:** {product_name}")
                st.write(f"**Features:** {features}")
                st.write(f"**Taglines:** {taglines}")
                st.write(f"**Prices:** {price_options}")
                st.write(f"**Number of Bots:** {num_bots}")
                combinations = list(product(features, taglines, price_options))
                st.write(f"**Combinations:** {combinations}")

                progress_placeholder = st.empty()
                try:
                    df = utils.process_simulation(combinations, num_bots, male_percentage, income_range, interests_list, progress_placeholder)
                except Exception as e:
                    st.error(f"Error during simulation: {str(e)}")
                    logging.error(f"Error during simulation: {str(e)}")
                    utils.log_error("Demand Meter", str(e))

                if not df.empty:
                    required_columns = ['Feature', 'Tagline', 'Price', 'Demand Score']
                    if not all(col in df.columns for col in required_columns):
                        st.error(f"Required columns are missing. Expected: {required_columns}. Found: {df.columns.tolist()}")
                        return

                    st.markdown("<h2 class='section-header'>Executive Summary</h2>", unsafe_allow_html=True)
                    summary = generate_narrative_summary(df)
                    st.markdown(f"<div class='key-insights'>{summary}</div>", unsafe_allow_html=True)

                    st.markdown("<h2 class='section-header'>Detailed Analysis</h2>", unsafe_allow_html=True)
                    fig = px.scatter(df, x='Price', y='Demand Score', color='Feature', hover_data=['Tagline'])
                    st.plotly_chart(fig, use_container_width=True)

                    heatmap_data = df.pivot_table(index="Feature", columns="Tagline", values="Demand Score")
                    fig = go.Figure(data=go.Heatmap(z=heatmap_data.values, x=heatmap_data.columns, y=heatmap_data.index))
                    st.plotly_chart(fig, use_container_width=True)

                    # User Feedback
                    st.markdown("<h2 class='section-header'>User Feedback</h2>", unsafe_allow_html=True)
                    feedback = st.text_area("Enter your feedback here:")
                    if st.button("Submit Feedback"):
                        utils.log_feedback(product_name, feedback)
                        st.success("Thank you for your feedback!")

        # Predictive Analytics (Now uses df even if not calculated)
        st.markdown("<h2 class='section-header'>Predictive Analytics</h2>", unsafe_allow_html=True)
        if not df.empty:  # Check if df is populated
            predictions = generate_predictive_analytics(df)
            st.write(predictions)
        else:
            st.info("Please run a simulation to view predictive analytics.")

        # Personalized Insights (Now uses df even if not calculated)
        st.markdown("<h2 class='section-header'>Personalized Insights</h2>", unsafe_allow_html=True)
        user_preferences = st.text_input("Enter your preferences (comma-separated):", placeholder="Preference1, Preference2")
        if user_preferences and not df.empty:  # Check for both preferences and data
            insights = personalized_insights(user_preferences)
            st.write(insights)
        else:
            st.info("Please run a simulation to view personalized insights.")

        # Set up Alerts
        setup_alerts()

    except Exception as e:
        logging.error(f"Error in run_dashboard: {str(e)}")
        st.error(f"Error in run_dashboard: {str(e)}")

if __name__ == "__main__":
    run_dashboard()