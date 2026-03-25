import streamlit as st
from components.styles import apply_custom_css, render_header
from components.sidebar import display_sidebar
from components.excel_view import display_excel_column
from components.pdf_view import display_pdf_column

# 1. SETUP
st.set_page_config(layout="wide", page_title="Excel ↔ PDF Linker")
apply_custom_css()
render_header("Excel ↔ PDF Linker")

# 2. INITIALIZE SESSION STATE
if 'excel_file' not in st.session_state:
    st.session_state.excel_file = None
if 'pdf_file' not in st.session_state:
    st.session_state.pdf_file = None

# 3. SIDEBAR (Run this BEFORE the layout to capture uploads immediately)
uploaded_excel, uploaded_pdf = display_sidebar()

# Change detection: If files are new, update state and rerun
if uploaded_excel != st.session_state.excel_file or uploaded_pdf != st.session_state.pdf_file:
    st.session_state.excel_file = uploaded_excel
    st.session_state.pdf_file = uploaded_pdf
    st.rerun()

# 4. MAIN SCREEN LAYOUT
col1, col2 = st.columns(2) 
sheet_name, editor_event = None, None
current_page, pdf_doc = 0, None

with col1:
    if st.session_state.excel_file:
        sheet_name, editor_event = display_excel_column(st.session_state.excel_file)
        st.session_state['editor_event'] = editor_event
    else:
        st.info("Please upload an Excel file in the sidebar.")

with col2:
    if st.session_state.pdf_file:
        current_page, pdf_doc = display_pdf_column(st.session_state.pdf_file)
        st.session_state['current_page'] = current_page
    else:
        st.info("Please upload a PDF file in the sidebar.")

# 5. FOOTER / STATUS
if st.session_state.excel_file and st.session_state.pdf_file:
    st.divider()
    display_page = (current_page + 1) if current_page is not None else 1
    display_sheet = sheet_name if sheet_name else "Unknown Sheet"
    st.info(f"Ready to link: {display_sheet} <--> Page {display_page}")