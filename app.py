import streamlit as st
from components.styles import apply_custom_css, render_header, render_column_header
from components.sidebar import display_sidebar
from components.excel_view import display_excel_column
from components.pdf_view import display_pdf_column
from logic.initialization import initialize_session_state, update_expander_state
from logic.file_sync import sync_files_to_state

# 1. Config & Styles
st.set_page_config(page_title="Linker Pro", page_icon="🔗", layout="wide")
apply_custom_css()

# 2. Initialize State
initialize_session_state()
uploaded_excel, uploaded_pdf = display_sidebar()
sync_files_to_state(uploaded_excel, uploaded_pdf)
update_expander_state()

# 3. GLOBAL TOOLBAR (High Density)
if not st.session_state.get("full_screen_mode", False):
    render_header("Excel ↔ PDF Linker")
    
    # Single row for all primary actions
    t_col1, t_col2, t_col3 = st.columns([2, 5, 2])
    
    with t_col1:
        if st.button("🔗 Finalize Link", type="primary", use_container_width=True):
            from logic.actions import capture_link
            capture_link(st.session_state.excel_editor, st.session_state.current_page, uploaded_pdf)

    with t_col2:
        # Integrated PDF Controls (Page, Zoom) and Pane Split
        c1, c2, c3 = st.columns([1, 2, 2])
        with c1:
            page_input = st.number_input("PG", 1, 1000, st.session_state.current_page + 1, step=1, label_visibility="collapsed")
            st.session_state.current_page = page_input - 1
        with c2:
            st.session_state.pdf_zoom = st.slider("ZOOM", 1.0, 4.0, st.session_state.get("pdf_zoom", 2.0), 0.1, label_visibility="collapsed")
        with c3:
            st.session_state.pane_ratio = st.slider("SPLIT", 30, 70, st.session_state.pane_ratio, 5, label_visibility="collapsed")

    with t_col3:
        st.markdown(f"<div style='text-align:right; padding-top:5px; font-size:0.8rem; color:#3b82f6;'><b>Links: {len(st.session_state.links)}</b></div>", unsafe_allow_html=True)

# 4. MAIN VIEWPORT
col1, col2 = st.columns([st.session_state.pane_ratio, 100 - st.session_state.pane_ratio], gap="small")

with col1:
    render_column_header("Excel Workbench")
    if st.session_state.excel_file:
        sheet_name, cell_event = display_excel_column(st.session_state.excel_file)
        st.session_state["excel_editor"] = cell_event
    else:
        st.info("Upload Excel in sidebar.")

with col2:
    render_column_header("PDF Evidence")
    if st.session_state.pdf_file:
        display_pdf_column(st.session_state.pdf_file, st.session_state.current_page, st.session_state.get("pdf_zoom", 2.0))
    else:
        st.info("Upload PDF in sidebar.")