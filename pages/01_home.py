import streamlit as st
import pandas as pd
from data_loader import load_data
from styles import apply_styles
from utils import show_dataset_context_note

apply_styles()

st.title("Home: Overview & Dataset Explorer")
st.markdown("Welcome to **StatMate**, a clean, academic tool for learning Probability and Statistics using real dataset from the Bengaluru Namma Metro.")

show_dataset_context_note()

# Load data
df, error = load_data()

if error:
    st.error(error)
else:
    st.header("Dataset Explorer")
    st.markdown("Use this section to filter and preview the dataset before analyzing it on other pages.")
    
    with st.form("filter_form"):
        col1, col2 = st.columns(2)
        with col1:
            all_stations = sorted(df['Station'].unique())
            selected_station = st.selectbox("Select Station (Optional)", ["All"] + all_stations)
        with col2:
            all_dates = sorted(df['Date'].dt.date.unique())
            selected_date = st.selectbox("Select Date (Optional)", ["All"] + [str(d) for d in all_dates])
            
        submit = st.form_submit_button("Apply Filters")
        
    if "filtered_df" not in st.session_state:
        st.session_state.filtered_df = df
        
    if submit:
        temp_df = df.copy()
        if selected_station != "All":
            temp_df = temp_df[temp_df['Station'] == selected_station]
        if selected_date != "All":
            temp_df = temp_df[temp_df['Date'].dt.date.astype(str) == selected_date]
        st.session_state.filtered_df = temp_df
        
    f_df = st.session_state.filtered_df
    
    st.subheader("Dataset Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Total Observations", len(f_df))
    col2.metric("Unique Stations", f_df['Station'].nunique())
    avg_ridership = f_df['Ridership'].mean()
    col3.metric("Avg Hourly Entries", f"{avg_ridership:.2f}" if not pd.isna(avg_ridership) else "0")
    
    st.markdown("### Data Preview")
    if not f_df.empty:
        st.dataframe(f_df.head(10), use_container_width=True)
        st.markdown(f"*(Showing top {min(10, len(f_df))} rows)*")
        
        csv = f_df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download Filtered Data as CSV",
            data=csv,
            file_name='statmate_filtered_data.csv',
            mime='text/csv',
        )
    else:
        st.warning("No data matches the selected filters.")
        
    with st.expander("Detailed Dataset Information"):
        st.write("**Missing Values:**", f_df.isnull().sum().to_dict())
        st.write("**Data Types:**", f_df.dtypes.astype(str).to_dict())
        st.write("**Duplicate Rows:**", f_df.duplicated().sum())
