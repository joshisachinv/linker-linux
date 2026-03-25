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
                # We need to save to a buffer so the user can download it
                output = io.BytesIO()
                # Create a temporary copy of the file to save into
                with open("temp_linked.xlsx", "wb") as f:
                    f.write(excel_file.getbuffer())
                
                # Use your links_store logic to embed data
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
        # ... (rest of your debug and clear cache code)
    return excel_file, pdf_file