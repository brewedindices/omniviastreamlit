import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt

def plot_demand_distribution(df):
    st.write("### Demand Score Distribution")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.histplot(df['Demand Score'], bins=20, kde=True, ax=ax)
    st.pyplot(fig)

def plot_demand_heatmap(df):
    st.write("### Demand Score Heatmap")
    try:
        heatmap_data = df.pivot_table(values='Demand Score', index='Feature', columns='Tagline', aggfunc='mean')
        fig, ax = plt.subplots(figsize=(12, 8))
        sns.heatmap(heatmap_data, annot=True, cmap="YlGnBu", ax=ax)
        st.pyplot(fig)
    except Exception as e:
        st.error(f"Error creating heatmap: {str(e)}")
