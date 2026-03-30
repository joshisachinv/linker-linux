import streamlit as st
from components.styles import render_sidebar_header, render_status_card
from logic.actions import capture_link
from logic.links_store import save_links_into_excel

def display_sidebar():
    with st.sidebar:
        # Styled Header
        render_sidebar_header("Linker Pro")
        st.caption("Precision Evidence Linking System")

        st.divider()

        # Files Section
        st.subheader("📁 Data Sources")
        excel_file = st.file_uploader("Workbook", type=["xlsx", "xlsm"], key="ex_up")
        pdf_file = st.file_uploader("Document", type=["pdf"], key="pdf_up")

        # System Status Cards
        render_status_card("Excel File", excel_file.name if excel_file else "Not Loaded", excel_file is not None)
        render_status_card("PDF File", pdf_file.name if pdf_file else "Not Loaded", pdf_file is not None)

        st.divider()

        # Linking Actions
        st.subheader("🔗 Actions")
        excel_ready = st.session_state.get("excel_editor") is not None
        pdf_ready = st.session_state.get("active_rect") is not None
        
        render_status_card("Cell Selected", "Ready" if excel_ready else "Waiting", excel_ready)
        render_status_card("Area Selected", "Ready" if pdf_ready else "Waiting", pdf_ready)

        if st.button("Finalize Link", use_container_width=True, type="primary"):
            if excel_ready and pdf_ready:
                capture_link(st.session_state.excel_editor, st.session_state.current_page, pdf_file)
            else:
                st.warning("Complete selections before linking.")

    return excel_file, pdf_file