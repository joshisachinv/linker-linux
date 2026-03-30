import os
import tempfile
import streamlit as st
from components.styles import render_sidebar_header, render_status_card
from logic.actions import capture_link
from logic.links_store import save_links_into_excel

def display_sidebar():
    with st.sidebar:
        render_sidebar_header("Linker Pro")
        st.caption("Precision Evidence Linking System")

        st.divider()

        # 1. View Mode
        st.subheader("🖥️ View Mode")
        st.toggle("Full Screen Focus", key="full_screen_mode")
        st.caption("Collapses toolbar and headers for inspection.")

        st.divider()

        # 2. Data Sources (Auto-collapse logic)
        with st.expander(
            "📁 Data Sources", 
            expanded=st.session_state.get("sources_expanded", True),
            key="sources_expander_widget"
        ):
            excel_file = st.file_uploader("Workbook", type=["xlsx", "xlsm"], key="excel_upload")
            pdf_file = st.file_uploader("Document", type=["pdf"], key="pdf_upload")

        # 3. System Status Cards
        render_status_card("Excel File", excel_file.name if excel_file else "Not Loaded", excel_file is not None)
        render_status_card("PDF File", pdf_file.name if pdf_file else "Not Loaded", pdf_file is not None)

        st.divider()

        # 4. Display Toggles
        st.subheader("👁️ Display")
        st.checkbox("Show Saved Highlights", value=True, key="show_highlights_toggle")

        st.divider()

        # 5. Export Actions
        st.subheader("💾 Export")
        link_count = len(st.session_state.get("links", {}))
        
        if st.button("Save Links to Excel", use_container_width=True, disabled=(link_count == 0)):
            if excel_file:
                try:
                    with tempfile.NamedTemporaryFile(delete=False, suffix=".xlsx") as tmp:
                        tmp.write(excel_file.getbuffer())
                        temp_path = tmp.name
                    
                    save_links_into_excel(temp_path, st.session_state.links)
                    
                    with open(temp_path, "rb") as f:
                        st.session_state["linked_excel_bytes"] = f.read()
                    st.session_state["linked_excel_name"] = f"linked_{excel_file.name}"
                    st.success("Workbook ready.")
                except Exception as e:
                    st.error(f"Save error: {e}")
                finally:
                    if "temp_path" in locals() and os.path.exists(temp_path):
                        os.remove(temp_path)

        if "linked_excel_bytes" in st.session_state:
            st.download_button(
                "Download Linked Excel",
                data=st.session_state["linked_excel_bytes"],
                file_name=st.session_state["linked_excel_name"],
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

        st.divider()

        # 6. Maintenance
        if st.button("Clear Session Cache", use_container_width=True):
            st.cache_data.clear()
            st.session_state.links = {}
            st.rerun()

    return excel_file, pdf_file