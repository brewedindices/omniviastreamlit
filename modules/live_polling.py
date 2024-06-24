import streamlit as st
import pandas as pd
import random
import concurrent.futures
import math
from modules import utils, results, analytics
import time  # Ensure the time module is imported

def run_live_polling():
    """Runs the Live Polling section of the app."""
    st.subheader("Live Polling")
    st.write("**Real-time Results and Interactive Visualizations**")

    # --- Live Polling Input ---
    st.sidebar.subheader("Create Survey")
    survey_question = st.sidebar.text_input("Enter your survey question:", "")
    options = {f"option_{chr(65+i)}": st.sidebar.text_input(f"Enter option {chr(65+i)}:", "") for i in range(4)}
    followups = [st.sidebar.text_input(f"Enter follow-up question {i+1}:", "") for i in range(2)]

    # --- Live Polling Logic and Display ---
    votes = {key: 0 for key in options.keys()}
    if st.button("Start Poll"):
        if not survey_question or not any(options.values()):
            st.warning("Please enter a question and options.")
        else:
            selected_option = st.selectbox("Choose your option:", options.values())
            if st.button("Vote"):
                votes[selected_option] += 1

            st.write(f"**Poll Results:**")
            for option, count in votes.items():
                st.write(f"- {option}: {count} votes")

            # Simple timer (You'll likely replace this with real-time updates)
            start_time = time.time()
            while time.time() - start_time < 10: # 10 seconds for example
                st.write(f"Time remaining: {10 - int(time.time() - start_time)} seconds")
                st.experimental_rerun()

    # --- Live Polling Input (Demographics) ---
    st.sidebar.subheader("Specify Demographics")
    male_percentage = st.sidebar.slider("Male Percentage", 0, 100, 50)
    female_percentage = 100 - male_percentage
    income_range = st.sidebar.slider("Income Range (in thousands)", 0, 500, (50, 150))

    # Interest badges
    interests = st.sidebar.text_input("Enter Interests (comma-separated):", placeholder="Golf, Yoga, Basketball")
    interests_list = interests.split(",") if interests else []

    if interests_list:
        st.sidebar.markdown("### Interests:")
        for interest in interests_list:
            st.sidebar.markdown(
                f"""<span style="background-color: #FF6F61; color: white; padding: 5px 10px; border-radius: 5px; margin: 5px;">{interest.strip()}</span>""",
                unsafe_allow_html=True
            )

    num_bots = st.sidebar.number_input("Enter number of bots:", min_value=1, max_value=1000, value=100)

    # Start button
    start_button = st.sidebar.button("Start Survey Simulation")

    # Simulation settings
    MAX_CONCURRENT_THREADS = 25
    batch_size = 25
    num_batches = math.ceil(num_bots / batch_size)

    # Survey simulation logic
    if start_button:
        bot_data = utils.generate_survey_data(int(num_bots), male_percentage, income_range, interests_list)

        # Sentiment Analysis
        sentiment_results = analytics.analyze_sentiment([data['persona'] for data in bot_data.values()])
        st.write("### Sentiment Analysis")
        sentiment_df = pd.DataFrame(sentiment_results)
        st.dataframe(sentiment_df)

        # Display Results
        results.display_survey_results(bot_data)