import streamlit as st

def format_number(num):
    """Formats a number for display, removing trailing zeros if integer."""
    if isinstance(num, (int, float)):
        if num == int(num):
            return f"{int(num)}"
        return f"{num:.4f}".rstrip('0').rstrip('.')
    return str(num)

def render_formula(formula, meanings):
    """Renders a latex formula and the meanings of its symbols."""
    st.latex(formula)
    with st.expander("Symbol Meanings"):
        for symbol, meaning in meanings.items():
            st.markdown(f"- **{symbol}**: {meaning}")

def show_dataset_context_note():
    st.info("ℹ️ **Note**: This dataset records the number of passengers entering the station per hour. It does not measure the number of people inside the trains.")
