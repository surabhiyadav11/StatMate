import streamlit as st
import pandas as pd
from data_loader import load_data
from styles import apply_styles
from utils import render_formula, format_number, show_dataset_context_note
from stats_functions import calculate_dispersion

apply_styles()

st.title("Measures of Dispersion")
show_dataset_context_note()

df, error = load_data()
if error:
    st.error(error)
    st.stop()

if "filtered_df" in st.session_state:
    f_df = st.session_state.filtered_df
    st.info(f"Using filtered dataset with {len(f_df)} observations.")
else:
    f_df = df

if f_df.empty:
    st.warning("Dataset is empty. Cannot calculate dispersion.")
    st.stop()

series = f_df['Ridership']
disp = calculate_dispersion(series)

st.header("1. Variance and Standard Deviation")
st.markdown("These measure how spread out the numbers are from the mean. The standard deviation is the square root of the variance and is in the same units as the data.")

st.subheader("Population vs Sample")
st.markdown("""
- **Population**: Use when your dataset is the *entire* population you care about.
- **Sample**: Use when your dataset is a sample representing a larger population. We divide by `n-1` instead of `N` (Bessel's correction) to get an unbiased estimate.
""")

col1, col2 = st.columns(2)
with col1:
    st.markdown("**Population Standard Deviation**")
    render_formula(
        r"\sigma = \sqrt{\frac{\sum (x_i - \mu)^2}{N}}",
        {r"\sigma": "Population SD", r"\mu": "Population Mean", "N": "Total population size"}
    )
    st.success(f"**Pop SD**: {format_number(disp['pop_std'])}")
    st.markdown(f"**Pop Variance**: {format_number(disp['pop_var'])}")

with col2:
    st.markdown("**Sample Standard Deviation**")
    render_formula(
        r"s = \sqrt{\frac{\sum (x_i - \bar{x})^2}{n-1}}",
        {"s": "Sample SD", r"\bar{x}": "Sample Mean", "n": "Sample size"}
    )
    if disp['samp_std'] is not None:
        st.success(f"**Sample SD**: {format_number(disp['samp_std'])}")
        st.markdown(f"**Sample Variance**: {format_number(disp['samp_var'])}")
    else:
        st.warning("Cannot calculate sample SD with n=1")

st.divider()

st.header("2. Coefficient of Variation (CV)")
st.markdown("The ratio of the standard deviation to the mean. It shows the extent of variability in relation to the mean of the population.")
render_formula(r"CV = \frac{\sigma}{\mu} \times 100", {"CV": "Coefficient of Variation", r"\sigma": "Standard Deviation", r"\mu": "Mean"})

if disp['cv'] is not None:
    st.success(f"**Result**: {format_number(disp['cv'])}%")
else:
    st.warning("CV is undefined because the mean is 0.")

st.divider()

st.header("3. Quartiles, IQR, and Outliers")
st.markdown("Quartiles divide the sorted dataset into four equal parts. The Interquartile Range (IQR) represents the middle 50% of the data.")

render_formula(
    r"\text{IQR} = Q3 - Q1",
    {"Q3": "75th Percentile", "Q1": "25th Percentile"}
)

st.markdown(f"- **Q1 (25th Percentile)**: {format_number(disp['q1'])}")
st.markdown(f"- **Q2 (Median, 50th Percentile)**: {format_number(disp['q2'])}")
st.markdown(f"- **Q3 (75th Percentile)**: {format_number(disp['q3'])}")
st.success(f"**IQR**: {format_number(disp['iqr'])}")

st.subheader("Outlier Detection (1.5 × IQR Rule)")
st.markdown("Values falling below `Q1 - 1.5*IQR` or above `Q3 + 1.5*IQR` are considered potential outliers.")
st.markdown(f"- **Lower Bound**: {format_number(disp['lower_bound'])}")
st.markdown(f"- **Upper Bound**: {format_number(disp['upper_bound'])}")
st.markdown(f"**Outliers Found**: {disp['outlier_count']} ({(disp['outlier_count']/disp['n']*100):.2f}% of data)")

if disp['outlier_count'] > 0:
    with st.expander("View Outliers"):
        # only show up to 100 to not crash browser
        st.write(disp['outliers'][:100])
        if disp['outlier_count'] > 100:
            st.write("*(Showing first 100 outliers)*")
