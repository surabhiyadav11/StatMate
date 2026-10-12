import streamlit as st

def apply_styles():
    """Injects custom CSS to enforce the white, minimal, academic look."""
    st.markdown(
        """
        <style>
        /* Base academic styling */
        body {
            color: #111827;
            background-color: #FFFFFF;
        }
        
        /* Sidebar styling */
        [data-testid="stSidebar"] {
            background-color: #F3F4F6;
            border-right: 1px solid #E5E7EB;
        }
        
        /* Header styling */
        h1, h2, h3, h4, h5, h6 {
            color: #111827;
            font-family: "sans serif";
            font-weight: 600;
        }
        
        /* Metric styling */
        [data-testid="stMetricValue"] {
            color: #4F46E5;
        }
        
        /* DataFrame styling */
        [data-testid="stDataFrame"] {
            border: 1px solid #E5E7EB;
            border-radius: 4px;
        }
        
        /* Buttons */
        .stButton>button {
            background-color: #4F46E5;
            color: white;
            border: none;
            border-radius: 4px;
        }
        
        .stButton>button:hover {
            background-color: #4338CA;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
