import streamlit as st
import pandas as pd
from logic.links_store import try_load_embedded_links

def display_excel_column(uploaded_file):
    # ... (header loading logic) ...
    if selected_sheet:
        df = excel_data[selected_sheet].fillna("")
        
        event = st.data_editor(
            df,
            key="excel_editor",
            selection_mode="single-cell", # THE FIX: One-click selection
            disabled=True,                # User can't edit, but CAN select
            hide_index=False,
        )
        return selected_sheet, event