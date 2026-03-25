import streamlit as st
from logic.actions import capture_link

def display_sidebar():
    with st.sidebar:
        st.title("Settings & Uploads")
        
        excel_file = st.file_uploader("Upload Excel", type=["xlsx", "xlsm"])
        pdf_file = st.file_uploader("Upload PDF", type="pdf")
        
        st.divider()
        
        # FIX: Use use_container_width=True for modern Streamlit
        if st.button("🔗 Capture & Link Selection", use_container_width=True):
            editor_event = st.session_state.get('editor_event')
    
            if editor_event is not None:
                capture_link(editor_event, st.session_state.get('current_page', 0), pdf_file)
            else:
                st.sidebar.warning("Select an Excel cell first.")
        
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