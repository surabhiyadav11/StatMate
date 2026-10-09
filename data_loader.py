import streamlit as st
import pandas as pd
import os

@st.cache_data
def load_data():
    """Loads and validates the station hourly dataset."""
    file_path = os.path.join(os.path.dirname(__file__), "data", "station-hourly.csv")
    if not os.path.exists(file_path):
        return None, "Dataset not found. Please ensure 'data/station-hourly.csv' exists."
    
    try:
        df = pd.read_csv(file_path, sep=";")
        
        # Validate columns
        required_cols = {"Date", "Hour", "Station", "Ridership"}
        if not required_cols.issubset(df.columns):
            return None, f"Missing required columns. Found: {list(df.columns)}"
            
        # Parse Dates
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        
        # Convert numeric types
        df['Hour'] = pd.to_numeric(df['Hour'], errors='coerce')
        df['Ridership'] = pd.to_numeric(df['Ridership'], errors='coerce')
        
        # Drop rows where Date, Hour, Station or Ridership is completely null
        df = df.dropna(subset=['Date', 'Hour', 'Station', 'Ridership'])
        
        # Ensure Ridership is >= 0
        df = df[df['Ridership'] >= 0]
        
        return df, None
        
    except Exception as e:
        return None, f"Error loading data: {str(e)}"
