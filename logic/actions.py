import streamlit as st
from models.pdf_link import PdfLink
from logic.cell_addr import cell_address

def capture_link(excel_selection, current_page, pdf_file):
    # Access the editor state from session_state
    state = st.session_state.get("excel_editor", {})
    
    row_idx = None
    col_idx = 0 

    # Try Modern Selection first
    if state.get("selection") and state["selection"].get("cells"):
        row_idx, col_idx = state["selection"]["cells"][0]
    
    # Fallback to Edited Rows (Requires user to double-click and hit Enter)
    elif state.get("edited_rows"):
        row_str = list(state["edited_rows"].keys())[-1]
        row_idx = int(row_str)
        row_data = state["edited_rows"][row_str]
        if row_data:
            col_idx = int(list(row_data.keys())[-1])

    if row_idx is None:
        st.sidebar.error("❌ No cell detected. Double-click + Enter to select.")
        return False

    addr = cell_address(row_idx, col_idx)
    pdf_name = pdf_file.name if pdf_file else "Unknown.pdf"

    new_link = PdfLink(
        pdf_path=pdf_name,
        page_index=current_page,
        rect=(0, 0, 100, 100) 
    )

    if 'links' not in st.session_state:
        st.session_state.links = {}
    
    st.session_state.links[addr] = new_link
    st.sidebar.success(f"✅ Linked {addr} to Page {current_page + 1}")
    return True