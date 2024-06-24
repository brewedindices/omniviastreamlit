import streamlit as st

def generate_summary(df):
    st.markdown("<div class='key-insights'>", unsafe_allow_html=True)
    best_combination = df.loc[df['Demand Score'].idxmax()]
    st.markdown(f"<p class='metric'>Best Combination: Feature - {best_combination['Feature']}, Tagline - {best_combination['Tagline']}, Price - ${best_combination['Price']}</p>", unsafe_allow_html=True)
    st.markdown(f"<p class='metric'>Highest Demand Score: {best_combination['Demand Score']:.1f}</p>", unsafe_allow_html=True)

    if df['Demand Score'].min() < 70:
        st.markdown("<p>Suggestions for Improvement:</p>", unsafe_allow_html=True)
        st.markdown("<ul><li>Consider revising features, taglines, or prices to boost demand.</li></ul>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
