import streamlit as st

def initialize_session_state():
    """Initializes all default session state variables."""
    defaults = {
        "excel_file": None,
        "pdf_file": None,
        "excel_sig": None,
        "pdf_sig": None,
        "current_page": 0,
        "editor_event": None,
        "links": {},
        "pane_ratio": 45,
        "sources_expanded": True,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def update_expander_state():
    """Collapses the data source expander if both files are present."""
    if st.session_state.excel_file and st.session_state.pdf_file:
        st.session_state.sources_expanded = False
    else:
        st.session_state.sources_expanded = True