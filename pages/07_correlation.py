import streamlit as st
import pandas as pd
from data_loader import load_data
from styles import apply_styles
from utils import render_formula, format_number, show_dataset_context_note
from stats_functions import calculate_correlation

apply_styles()

st.title("Correlation and Relationship Analysis")
show_dataset_context_note()

df, error = load_data()
if error:
    st.error(error)
    st.stop()

st.header("Pearson Correlation Coefficient ($r$)")
st.markdown("Measures the linear relationship between two numerical variables. The value ranges from -1 to +1.")

render_formula(
    r"r = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{\sum (x_i - \bar{x})^2 \sum (y_i - \bar{y})^2}}",
    {
        "r": "Correlation coefficient",
        r"\bar{x}, \bar{y}": "Means of variable X and Y",
        r"x_i, y_i": "Individual paired observations"
    }
)

st.markdown("""
**Interpretation Guide (Rule of Thumb):**
- $r > 0$: Positive correlation (as X goes up, Y goes up)
- $r < 0$: Negative correlation (as X goes up, Y goes down)
- $r \approx 0$: No linear correlation
- Strength: 0.0 to 0.3 (Weak), 0.3 to 0.7 (Moderate), 0.7 to 1.0 (Strong)
""")

st.warning("⚠️ **Crucial Rule**: Correlation does not establish causation. Just because two stations have correlated ridership does not mean one causes the other; they may both be driven by a third factor (like rush hour).")

st.subheader("Calculate Correlation")
st.markdown("We will pivot the data to match Date+Hour pairs, comparing the ridership of two selected stations.")

stations = sorted(df['Station'].unique())

with st.form("corr_form"):
    col1, col2 = st.columns(2)
    with col1:
        station_x = st.selectbox("Station X", stations, index=0)
    with col2:
        station_y = st.selectbox("Station Y", stations, index=1 if len(stations)>1 else 0)
        
    submit = st.form_submit_button("Calculate Correlation")

if submit:
    if station_x == station_y:
        st.error("Please select two different stations for a meaningful correlation.")
    else:
        # Prepare paired data
        df_x = df[df['Station'] == station_x][['Date', 'Hour', 'Ridership']].rename(columns={'Ridership': 'X'})
        df_y = df[df['Station'] == station_y][['Date', 'Hour', 'Ridership']].rename(columns={'Ridership': 'Y'})
        
        merged = pd.merge(df_x, df_y, on=['Date', 'Hour'], how='inner')
        
        corr, n = calculate_correlation(merged, 'X', 'Y')
        
        if corr is None or pd.isna(corr):
            st.warning(f"Could not calculate correlation. Paired observations: {n}. Values might be constant.")
        else:
            st.success(f"**Pearson $r$**: {format_number(corr)}")
            st.markdown(f"**Based on**: {n} paired (Date+Hour) observations.")
            
            # Interpretation text
            direction = "positive" if corr > 0 else "negative"
            if abs(corr) < 0.1:
                direction = "near-zero"
                
            if abs(corr) < 0.3:
                strength = "weak"
            elif abs(corr) < 0.7:
                strength = "moderate"
            else:
                strength = "strong"
                
            st.markdown(f"**Interpretation**: There is a **{strength} {direction}** linear relationship between the ridership at {station_x} and {station_y}.")
