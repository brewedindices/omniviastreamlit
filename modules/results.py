import streamlit as st
import pandas as pd
import random

def display_survey_results(bot_data):
    """Displays the survey results in a structured format."""
    df = pd.DataFrame(bot_data)
    response_tally = df['response'].value_counts()
    st.write("### Survey Results")
    st.bar_chart(response_tally)

    # Key Insights
    st.write("### Key Insights")
    most_popular = response_tally.idxmax()
    st.write(f"**Most popular option**: {most_popular} ({options[f'option_{most_popular.lower()}']})")
    st.write(f"**Average score for '{followups[0]}'**: {df['followups'].apply(lambda x: x[0]).mean():.2f}/10")
    st.write(f"**Most common response to '{followups[1]}'**: {df['followups'].apply(lambda x: x[1]).mode()[0]}")

    # Sample Personas
    st.write("### Sample Personas")
    for i, (bot, data) in enumerate(random.sample(list(bot_data.items()), 5)):
        with st.expander(f"Persona {i+1}"):
            st.write(data['persona'])
            st.write(f"Response: {data['response']}")