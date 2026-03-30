import streamlit as st

def initialize_session_state():
    defaults = {
        "excel_file": None,
        "pdf_file": None,
        "excel_sig": None,
        "pdf_sig": None,
        "current_page": 0,
        "pdf_zoom": 2.0,
        "full_screen_mode": False,
        "editor_event": None,
        "links": {},
        "pane_ratio": 45,
        "sources_expanded": True,
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v

def update_expander_state():
    if st.session_state.excel_file and st.session_state.pdf_file:
        st.session_state.sources_expanded = False
    else:
        st.session_state.sources_expanded = True