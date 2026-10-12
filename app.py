import streamlit as st

st.set_page_config(
    page_title="StatMate — Probability & Statistics Analyzer",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sidebar setup
st.sidebar.title("StatMate")
st.sidebar.markdown("Probability & Statistics Analyzer")

pages = {
    "Home": [
        st.Page("pages/01_home.py", title="Overview & Dataset Explorer")
    ],
    "Descriptive Statistics": [
        st.Page("pages/02_descriptive_statistics.py", title="Central Tendency & Range")
    ],
    "Measures of Dispersion": [
        st.Page("pages/03_measures_of_dispersion.py", title="Variance, SD, IQR & Outliers")
    ],
    "Probability": [
        st.Page("pages/04_probability.py", title="Empirical, Classification & Conditional")
    ],
    "Probability Distributions": [
        st.Page("pages/05_probability_distributions.py", title="Theoretical Distributions")
    ],
    "Data Visualization": [
        st.Page("pages/06_data_visualization.py", title="Charts & Plots")
    ],
    "Correlation": [
        st.Page("pages/07_correlation.py", title="Relationship Analysis")
    ],
    "Information": [
        st.Page("pages/08_project_information.py", title="Project Information")
    ]
}

pg = st.navigation(pages)
pg.run()
