import streamlit as st

def get_file_signature(uploaded_file):
    """Generates a signature to detect if the uploaded file has changed."""
    if uploaded_file is None:
        return None
    return (uploaded_file.name, uploaded_file.size)

def sync_files_to_state(uploaded_excel, uploaded_pdf):
    """Updates session state and triggers a rerun if new files are detected."""
    new_excel_sig = get_file_signature(uploaded_excel)
    new_pdf_sig = get_file_signature(uploaded_pdf)

    # Detect changes
    if (new_excel_sig != st.session_state.excel_sig or 
        new_pdf_sig != st.session_state.pdf_sig):
        
        st.session_state.excel_file = uploaded_excel
        st.session_state.pdf_file = uploaded_pdf
        st.session_state.excel_sig = new_excel_sig
        st.session_state.pdf_sig = new_pdf_sig
        st.rerun()