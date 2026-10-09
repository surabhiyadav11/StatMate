import streamlit as st
from styles import apply_styles

apply_styles()

st.title("Project Information")

st.header("Problem Statement")
st.markdown("""
Learning probability and statistics often involves abstract formulas and textbook examples. 
StatMate aims to bridge the gap between theory and practice by applying these mathematical concepts to real-world transportation data, providing an interactive, academic environment for exploration and learning.
""")

st.header("Dataset Details")
st.markdown("""
The dataset used in this application tracks the hourly passenger **entries** at various stations of the Bengaluru Namma Metro. 
- **Source**: Namma Metro Operational Data (Subset)
- **Granularity**: Hourly
- **Variables**: Date, Hour, Station, Ridership
""")

st.header("Methodology")
st.markdown("""
- **Data Validation**: Strict type checking and dropping of invalid/missing records to ensure mathematical accuracy.
- **Statistical Computation**: Core calculations are performed using robust Python libraries (`pandas`, `numpy`, `scipy.stats`).
- **Pedagogical Design**: Every concept is introduced with its formal definition, mathematical formula, component breakdown, and calculated result, followed by a plain-English interpretation.
""")

st.header("Assumptions and Limitations")
st.markdown("""
1. **Station Entries Only**: The dataset tracks passengers *entering* the station turnstiles. It does NOT track exits, nor does it measure the density or crowding *inside* the trains.
2. **Missing Data**: Hours with 0 entries or missing records might represent station closures or data collection failures, not necessarily zero demand.
3. **Distribution Fitting**: The theoretical probability distributions provided (Binomial, Poisson, etc.) are educational models. We do not claim that the metro data perfectly follows any of these theoretical distributions.
4. **Causation**: Correlation shown in this tool measures linear association only, not causal effects.
""")

st.header("Conclusion")
st.markdown("""
StatMate successfully demonstrates how foundational statistical measures, probability rules, distributions, and visualizations can be applied to real transportation data. 
The results describe the historical patterns of this specific dataset only and do not guarantee future passenger levels or represent official crowding metrics.
""")
