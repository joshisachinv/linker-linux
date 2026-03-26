import streamlit as st
import pandas as pd
from logic.links_store import try_load_embedded_links

def display_excel_column(uploaded_file):
    from components.styles import render_column_label
    render_column_label("Excel Viewer")
    
    if uploaded_file is None:
        return None, None

    # 1. Load Data
    excel_data = pd.read_excel(uploaded_file, sheet_name=None, header=None)
    display_sheets = [s for s in excel_data.keys() if s != "__PDF_LINKS__"]
    selected_sheet = st.selectbox("Select Sheet", display_sheets)
    
    if selected_sheet:
        df = excel_data[selected_sheet].fillna("")
        
        # FIX: Replaced width="stretch" with use_container_width=True
        # and ensured height is an integer to satisfy Python 3.14
        event = st.data_editor(
            df,
            key="excel_editor", 
            use_container_width=True, # Modern way to stretch width
            height=800,               # Integer height
            selection_mode="single-cell",
            disabled=True,
            hide_index=False
        )
        
        return selected_sheet, event
        
    return None, None