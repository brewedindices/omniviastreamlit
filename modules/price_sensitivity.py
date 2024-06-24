import streamlit as st
import pandas as pd
import json

def run_price_sensitivity():
    """Runs the Price Sensitivity section of the app."""
    st.subheader("Price Sensitivity")
    st.write("**Analyze the impact of different prices on demand**")

    # --- Price Sensitivity Analysis ---
    price_points_str = st.text_input("Enter Price Points (comma-separated):")

    # Validate and parse price points
    try:
        price_points = [float(x.strip()) for x in price_points_str.split(',')] if price_points_str else []
        price_error = False
    except ValueError:
        price_error = True
        price_points = []

    if price_error:
        st.warning("Invalid price points. Please enter comma-separated numbers.")

    if st.button("Run Price Sensitivity Analysis") and not price_error:
        if not price_points:
            st.warning("Please enter price points.")
        else:
            st.write(f"**Price Points:** {price_points}")

            # Simulate retrieving responses from a database
            responses = []  # Replace with actual database call
            if responses:
                # Placeholder for actual price sensitivity analysis
                st.write("**Analysis Results:**")
                for point in price_points:
                    st.write(f"At ${point}, the demand is...")  # Placeholder for actual logic

                # Example of Van Westendorp Price Sensitivity Analysis
                st.write("**Van Westendorp Price Sensitivity Analysis:**")
                optimal_price_range = (min(price_points), max(price_points))  # Placeholder for actual analysis
                st.write(f"Optimal Price Range: {optimal_price_range}")

                # Example of Gabor-Granger Price Sensitivity Analysis
                st.write("**Gabor-Granger Price Sensitivity Analysis:**")
                demand_at_price = {point: random.randint(50, 100) for point in price_points}  # Placeholder
                st.write(f"Demand at Different Price Points: {demand_at_price}")

                # Chart for Gabor-Granger Results
                option = {
                    "title": {"text": "Gabor-Granger Price Sensitivity", "left": "center"},
                    "xAxis": {"type": "category", "data": price_points},
                    "yAxis": {"type": "value"},
                    "series": [
                        {"data": list(demand_at_price.values()), "type": "bar", "showBackground": True, "backgroundStyle": {"color": 'rgba(180, 180, 180, 0.2)'}}
                    ]
                }
                st.echarts(options=json.dumps(option), height="400px")
