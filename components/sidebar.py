import streamlit as st
from logic.actions import capture_link
from logic.links_store import save_links_into_excel
import io

def display_sidebar():
    with st.sidebar:
        st.title("Settings & Uploads")
        
        excel_file = st.file_uploader("Upload Excel", type=["xlsx", "xlsm"])
        pdf_file = st.file_uploader("Upload PDF", type="pdf")
        
        st.divider()
        
        # 1. Capture Action
        if st.button("🔗 Capture & Link Selection", use_container_width=True):
            editor_event = st.session_state.get('editor_event')
            if editor_event is not None:
                capture_link(editor_event, st.session_state.get('current_page', 0), pdf_file)
            else:
                st.sidebar.warning("Select an Excel cell first.")

        # 2. Save Action
        if 'links' in st.session_state and st.session_state.links:
            st.divider()
            if st.button("💾 Save Links to Excel", use_container_width=True):
                output = io.BytesIO()
                # Create temporary file to handle openpyxl saving
                with open("temp_linked.xlsx", "wb") as f:
                    f.write(excel_file.getbuffer())
                
                save_links_into_excel("temp_linked.xlsx", st.session_state.links)
                
                with open("temp_linked.xlsx", "rb") as f:
                    st.download_button(
                        label="📥 Download Linked Excel",
                        data=f.read(),
                        file_name=f"linked_{excel_file.name}",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )
                st.success("Links embedded! Click download above.")

        st.divider()
        with st.expander("🔍 Developer Debug"):
            st.write("Current Page:", st.session_state.get('current_page'))
            editor_state = st.session_state.get("excel_editor", "Not found")
            st.write("Excel Editor State:", editor_state)
        
        if 'links' in st.session_state and st.session_state.links:
            with st.expander("📝 Current Session Links"):
                for cell, link in st.session_state.links.items():
                    st.write(f"**{cell}** → Page {link.page_index + 1}")

        if st.button("🗑️ Clear Cache", use_container_width=True):
            st.cache_data.clear()
            st.success("Cache cleared!")

    return excel_file, pdf_file