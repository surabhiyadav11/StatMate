import streamlit as st
import pandas as pd
from data_loader import load_data
from styles import apply_styles
from utils import render_formula, format_number, show_dataset_context_note
from probability_functions import empirical_probability, classification_probabilities, conditional_probability

apply_styles()

st.title("Probability")
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
    st.warning("Dataset is empty. Cannot calculate probability.")
    st.stop()

st.header("1. Empirical Probability")
st.markdown("The ratio of the number of outcomes in which a specified event occurs to the total number of trials, based on historical data.")
render_formula(
    r"P(A) = \frac{\text{Number of times event A occurred}}{\text{Total number of observations}}",
    {"A": "The event of interest"}
)

st.markdown("Define Event A (Ridership threshold):")
with st.form("empirical_prob_form"):
    threshold = st.number_input("Ridership greater than or equal to:", min_value=0, value=1000)
    submit_emp = st.form_submit_button("Calculate Probability")

if submit_emp:
    cond_series = f_df['Ridership'] >= threshold
    prob, satisfying, total = empirical_probability(f_df, cond_series)
    st.success(f"**Result**: {format_number(prob)} ({satisfying} / {total})")
    st.markdown(f"**Interpretation**: Based on this dataset, there is a {format_number(prob*100)}% chance that hourly ridership at a randomly selected observation is $\ge$ {threshold}.")

st.divider()

st.header("2. Passenger Activity Classification")
st.markdown("We can categorize ridership into mutually exclusive and exhaustive events. The sum of their probabilities must equal 1.")
st.info("Note: These are user-defined analytical categories, NOT official crowd-density classifications.")

with st.form("classification_form"):
    col1, col2 = st.columns(2)
    with col1:
        low_med = st.number_input("Low to Medium Threshold:", min_value=1, value=500)
    with col2:
        med_high = st.number_input("Medium to High Threshold:", min_value=2, value=1500)
    
    submit_class = st.form_submit_button("Calculate Classification")

if submit_class:
    if low_med >= med_high:
        st.error("Low/Medium threshold must be less than Medium/High threshold.")
    else:
        probs = classification_probabilities(f_df, 'Ridership', low_med, med_high)
        
        st.markdown(f"- **P(Low)** (Ridership < {low_med}): {format_number(probs['P_Low'])}")
        st.markdown(f"- **P(Medium)** ({low_med} $\le$ Ridership < {med_high}): {format_number(probs['P_Med'])}")
        st.markdown(f"- **P(High)** (Ridership $\ge$ {med_high}): {format_number(probs['P_High'])}")
        
        total_p = probs['P_Low'] + probs['P_Med'] + probs['P_High']
        st.success(f"**Sum of Probabilities**: {format_number(total_p)}")

st.divider()

st.header("3. Conditional Probability")
st.markdown("The probability of event A occurring given that event B has already occurred.")
render_formula(
    r"P(A|B) = \frac{P(A \cap B)}{P(B)} = \frac{\text{Count}(A \text{ and } B)}{\text{Count}(B)}",
    {"A": "Target Event", "B": "Condition/Given Event"}
)

with st.form("conditional_form"):
    st.markdown("Define Event A (Target):")
    target_thresh = st.number_input("Event A: Ridership greater than or equal to", min_value=0, value=1000, key="cond_A")
    
    st.markdown("Define Event B (Given):")
    stations = sorted(df['Station'].unique())
    b_station = st.selectbox("Event B: Station equals", ["All"] + stations)
    
    submit_cond = st.form_submit_button("Calculate Conditional Probability")

if submit_cond:
    mask_A = f_df['Ridership'] >= target_thresh
    mask_B = pd.Series([True]*len(f_df), index=f_df.index) if b_station == "All" else f_df['Station'] == b_station
    
    prob, count_ab, count_b = conditional_probability(f_df, mask_A, mask_B)
    
    if count_b == 0:
        st.warning("Event B has 0 occurrences in the dataset. Conditional probability is undefined.")
    else:
        st.success(f"**P(A|B)**: {format_number(prob)} ({count_ab} / {count_b})")
        st.markdown(f"**Interpretation**: Given that the station is {b_station}, there is a {format_number(prob*100)}% chance that hourly ridership is $\ge$ {target_thresh}.")
