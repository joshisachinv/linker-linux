import streamlit as st
from components.styles import apply_custom_css, render_header, render_column_header
from components.sidebar import display_sidebar
from components.excel_view import display_excel_column
from components.pdf_view import display_pdf_column
from logic.initialization import initialize_session_state, update_expander_state
from logic.file_sync import sync_files_to_state

# 1. Config & Styles
st.set_page_config(page_title="Excel ↔ PDF Linker", page_icon="🔗", layout="wide")
apply_custom_css()
render_header("Excel ↔ PDF Linker")

# 2. State & Sync
initialize_session_state()
uploaded_excel, uploaded_pdf = display_sidebar()
sync_files_to_state(uploaded_excel, uploaded_pdf)
update_expander_state()

# 3. Toolbar & Layout
toolbar_left, toolbar_right = st.columns([3, 2])
with toolbar_right:
    st.session_state.pane_ratio = st.slider(
        "Pane split", 30, 70, st.session_state.pane_ratio, 5, key="pane_ratio_slider"
    )

left_ratio = st.session_state.pane_ratio
col1, col2 = st.columns([left_ratio, 100 - left_ratio], gap="small")

# 4. Viewers
with col1:
    render_column_header("Excel Workbench")
    if st.session_state.excel_file:
        sheet_name, cell_event = display_excel_column(st.session_state.excel_file)
        st.session_state["excel_editor"] = cell_event
    else:
        st.info("Upload an Excel file in the sidebar.")

with col2:
    render_column_header("PDF Evidence")
    if st.session_state.pdf_file:
        current_page, _ = display_pdf_column(st.session_state.pdf_file)
        st.session_state["current_page"] = current_page
    else:
        st.info("Upload a PDF file in the sidebar.")

# 5. Status Footer
if st.session_state.excel_file and st.session_state.pdf_file:
    display_page = (st.session_state.current_page + 1)
    st.caption(f"Ready to link: **Page {display_page}**")