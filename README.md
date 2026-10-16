# StatMate: Probability & Statistics Analyzer

## Overview
StatMate is a Probability and Statistics learning application that uses real hourly station-entry data from the Bengaluru Namma Metro dataset. The goal is to provide a clean, academic interface to teach statistical concepts by applying them to real data.

## Running the Application
1. Install dependencies:
   ```bash
   python -m pip install -r requirements.txt
   ```
2. Run the application:
   ```bash
   python -m streamlit run app.py
   ```

## Design Principles
- **Minimal, Academic Look**: White background, muted indigo accents, clear typography.
- **Learning First**: Every concept includes definitions, formulas, symbol explanations, and calculations.
- **Form-Based Interactivity**: Inputs do not recalculate until submitted.

## Datasett
The dataset `station-hourly.csv` tracks hourly passenger entries at Namma Metro stations. It does not measure train crowding.
