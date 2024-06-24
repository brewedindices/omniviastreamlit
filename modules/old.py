import streamlit as st
import pandas as pd
from itertools import product
from modules import utils, visualizations, narrative
from autogen import AssistantAgent, UserProxyAgent

def run_dashboard():
    st.title("Executive Dashboard - AI-Powered Demand Insights")

    product_name = st.text_input("Product Name:", placeholder="Enter the product name")
    product_features = st.text_area("Enter Product Features (comma-separated):", placeholder="Feature1, Feature2, Feature3")
    tagline_options = st.text_area("Enter Tagline Options (comma-separated):", placeholder="Tagline1, Tagline2, Tagline3")
    price_options_str = st.text_input("Enter Price Options (comma-separated):", placeholder="9.99, 19.99, 29.99")

    try:
        price_options = [float(x.strip()) for x in price_options_str.split(',')] if price_options_str else []
        price_error = False
    except ValueError:
        price_error = True
        price_options = []
        st.warning("Invalid price options. Please enter comma-separated numbers.")

    st.header("Simulation Configuration")
    num_bots = st.number_input("Enter number of bots for simulation:", min_value=1, max_value=1000, value=100)
    male_percentage = st.slider("Male Percentage", 0, 100, 50)
    income_range = st.slider("Income Range (in thousands)", 0, 500, (50, 150))
    interests = st.text_input("Enter Interests (comma-separated):", placeholder="Golf, Yoga, Basketball")
    interests_list = [i.strip() for i in interests.split(",")] if interests else []

    if interests_list:
        st.markdown("### Interests:")
        st.markdown(" ".join([f'<span style="background-color: #FF6F61; color: white; padding: 5px 10px; border-radius: 5px; margin: 5px;">{interest}</span>' for interest in interests_list]), unsafe_allow_html=True)

    if st.button("Calculate Demand") and not price_error:
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
                utils.log_error("Demand Meter", str(e))
                return

            if df.empty:
                st.error("No valid data was generated. Please check your inputs and try again.")
                return

            required_columns = ['Feature', 'Tagline', 'Price', 'Demand Score']
            if not all(col in df.columns for col in required_columns):
                st.error(f"Required columns are missing. Expected: {required_columns}. Found: {df.columns.tolist()}")
                return

            st.header("Executive Summary")
            narrative.generate_summary(df)

            st.header("Detailed Analysis")
            visualizations.plot_demand_distribution(df)
            visualizations.plot_demand_heatmap(df)

            st.header("User Feedback")
            feedback = st.text_area("Enter your feedback here:")
            if st.button("Submit Feedback"):
                utils.log_feedback(product_name, feedback)
                st.success("Thank you for your feedback!")

            st.header("Automated Insights")
            config_list = [{"model": "gpt-3.5-turbo"}]
            assistant = AssistantAgent(name="Assistant", llm_config={"config_list": config_list})
            user_proxy = UserProxyAgent(name="User_proxy", code_execution_config={"work_dir": "coding"})
            try:
                insights = utils.generate_insights(assistant, user_proxy, df.to_dict(orient='records'))
                st.write(insights)
            except Exception as e:
                st.error(f"Failed to generate insights: {e}")

if __name__ == "__main__":
    run_dashboard()
