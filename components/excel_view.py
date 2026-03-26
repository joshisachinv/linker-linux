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
        
        # 2. Modern Selection Mode (Requires Streamlit 1.35+)
        event = st.data_editor(
            df,
            key="excel_editor", 
            width="stretch",
            height=800,
            disabled=True,
            hide_index=False
        )
        
        # 3. Check for existing links
        try:
            links = try_load_embedded_links(uploaded_file)
            if links:
                st.success(f"Found {len(links)} embedded links.")
        except:
            pass
            
        return selected_sheet, event
        
    return None, None