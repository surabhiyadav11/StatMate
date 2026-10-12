# Architecture

The StatMate project is a modular Python Streamlit application built for teaching Probability and Statistics.

## Directory Structure
- `app.py`: Main entry point configuring the Streamlit page layout and sidebar navigation.
- `data_loader.py`: Handles CSV loading, parsing, validation, and caching.
- `utils.py`: Helpers for input validation and text formatting.
- `styles.py`: Custom CSS for enforcing the academic white theme.
- `stats_functions.py`: Pure functions for Descriptive Statistics and Measures of Dispersion.
- `probability_functions.py`: Pure functions for probabilities (empirical, classification, conditional).
- `distribution_functions.py`: Logic for probability distributions (Binomial, Poisson, Normal, Exponential, Uniform).
- `charts.py`: Plotly functions for data visualization.
- `pages/`: Individual Streamlit views. Each view explains theory and handles UI state.
- `tests/`: Pytest/unittest file verifying calculations.

## State Management
User inputs are handled using Streamlit forms (`st.form`). Recalculation only occurs upon explicitly clicking "Calculate" or "Apply Filters".

## Dependencies
- `streamlit`: Web framework
- `pandas`: Data manipulation
- `numpy`: Numerical operations
- `scipy`: Probability distributions
- `plotly`: Interactive charting
