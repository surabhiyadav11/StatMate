import streamlit as st
import pandas as pd
from data_loader import load_data
from styles import apply_styles
from utils import render_formula, format_number, show_dataset_context_note
from stats_functions import calculate_central_tendency, calculate_range_measures

apply_styles()

st.title("Descriptive Statistics")
show_dataset_context_note()

df, error = load_data()
if error:
    st.error(error)
    st.stop()

# Use filtered dataframe from session state if available
if "filtered_df" in st.session_state:
    f_df = st.session_state.filtered_df
    st.info(f"Using filtered dataset with {len(f_df)} observations.")
else:
    f_df = df
    st.info(f"Using full dataset with {len(f_df)} observations. Go to Home to apply filters.")

if f_df.empty:
    st.warning("Dataset is empty. Cannot calculate statistics.")
    st.stop()

series = f_df['Ridership']
mean, median, modes = calculate_central_tendency(series)
min_val, max_val, range_val = calculate_range_measures(series)

st.header("1. Central Tendency")

st.subheader("Mean (Average)")
st.markdown("The mean is the sum of all values divided by the number of observations. It is sensitive to extreme values (outliers).")
render_formula(
    r"\bar{x} = \frac{\sum x_i}{n}", 
    {
        r"\bar{x}": "Sample mean",
        r"\sum x_i": "Sum of all observations (total ridership)",
        r"n": "Total number of observations"
    }
)
st.markdown(f"**Calculation**: Summing all {len(series)} hourly ridership entries and dividing by {len(series)}.")
st.success(f"**Result**: {format_number(mean)} passengers per hour")
st.markdown(f"**Interpretation**: On average, {format_number(mean)} passengers entered a station during a given hour in this dataset.")

st.divider()

st.subheader("Median")
st.markdown("The median is the middle value when the data is sorted. It is a robust measure that is not skewed by extreme values.")
st.markdown(f"**Result**: {format_number(median)} passengers per hour")
st.markdown(f"**Interpretation**: 50% of the hourly entries are below {format_number(median)}, and 50% are above.")
st.info("**Comparison**: If the mean is much higher than the median, it indicates the data is right-skewed (a few hours with very high ridership pull the average up).")

st.divider()

st.subheader("Mode")
st.markdown("The mode is the most frequently occurring value in the dataset. A dataset can have one mode, multiple modes, or no mode.")
mode_str = ", ".join(map(str, modes)) if modes else "None"
st.markdown(f"**Result**: {mode_str}")
st.markdown("**Interpretation**: This represents the most common hourly entry count.")

st.header("2. Range Measures")

st.subheader("Minimum, Maximum, and Range")
st.markdown("The range gives a quick sense of the spread of the data by looking at the extremes.")
render_formula(
    r"\text{Range} = \text{Max} - \text{Min}",
    {
        "Max": "Highest observed value",
        "Min": "Lowest observed value"
    }
)

st.markdown(f"- **Minimum (Min)**: {format_number(min_val)}")
st.markdown(f"- **Maximum (Max)**: {format_number(max_val)}")
st.markdown(f"- **Range**: {format_number(range_val)}")
st.markdown(f"**Interpretation**: The hourly passenger entries vary by {format_number(range_val)}, from a low of {format_number(min_val)} to a high of {format_number(max_val)}.")
