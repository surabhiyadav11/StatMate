import streamlit as st
import pandas as pd
from data_loader import load_data
from styles import apply_styles
from utils import show_dataset_context_note
import charts

apply_styles()

st.title("Data Visualization")
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
    st.warning("Dataset is empty. Cannot visualize data.")
    st.stop()

st.markdown("Use the selections below to generate standard statistical visualizations. Note that selections here do not filter the dataset used on other pages.")

chart_type = st.selectbox("Select Chart Type", ["Histogram", "Box Plot", "Line Chart (Hourly Pattern)", "Bar Chart (Station Comparison)"])

with st.form("viz_form"):
    st.write("Configure Chart")
    
    if chart_type == "Histogram":
        col = st.selectbox("Column to distribute", ["Ridership"])
        bins = st.number_input("Number of bins (approximate)", min_value=5, max_value=100, value=20)
    elif chart_type == "Box Plot":
        y_col = st.selectbox("Numerical Column", ["Ridership"])
        x_col = st.selectbox("Group By", ["None", "Station", "Hour"])
    elif chart_type == "Line Chart (Hourly Pattern)":
        st.write("Aggregates average ridership by Hour.")
        group_station = st.checkbox("Group by Station (may be cluttered if many stations selected)")
    elif chart_type == "Bar Chart (Station Comparison)":
        st.write("Aggregates total ridership by Station.")
        
    submit = st.form_submit_button("Generate Chart")

if submit:
    if chart_type == "Histogram":
        fig = charts.plot_histogram(f_df, col, f"Distribution of {col}", col)
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("**Explanation**: A histogram shows the frequency of data points falling within specific ranges (bins). It helps identify the shape and spread of the data.")
        
    elif chart_type == "Box Plot":
        x = None if x_col == "None" else x_col
        fig = charts.plot_boxplot(f_df, x, y_col, f"Box Plot of {y_col}" + (f" by {x}" if x else ""))
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("**Explanation**: A box plot visualizes the five-number summary (minimum, Q1, median, Q3, maximum) and highlights potential outliers.")
        
    elif chart_type == "Line Chart (Hourly Pattern)":
        if group_station:
            agg_df = f_df.groupby(['Hour', 'Station'])['Ridership'].mean().reset_index()
            fig = charts.plot_line_chart(agg_df, 'Hour', 'Ridership', "Average Hourly Ridership by Station", group_col='Station')
        else:
            agg_df = f_df.groupby('Hour')['Ridership'].mean().reset_index()
            fig = charts.plot_line_chart(agg_df, 'Hour', 'Ridership', "Average Hourly Ridership (All Selected Stations)")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("**Explanation**: A line chart is ideal for showing trends over time or sequential intervals, such as ridership patterns throughout the day.")
        
    elif chart_type == "Bar Chart (Station Comparison)":
        agg_df = f_df.groupby('Station')['Ridership'].sum().reset_index()
        # Sort for better presentation
        agg_df = agg_df.sort_values('Ridership', ascending=False)
        fig = charts.plot_bar_chart(agg_df, 'Station', 'Ridership', "Total Ridership per Station")
        st.plotly_chart(fig, use_container_width=True)
        st.markdown("**Explanation**: A bar chart compares categorical data (stations) based on a quantitative metric (total ridership).")
