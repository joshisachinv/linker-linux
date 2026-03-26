import streamlit as st
from models.pdf_link import PdfLink
from logic.cell_addr import cell_address

def capture_link(excel_selection, current_page, pdf_file):
    # 1. Get Excel Address from Editor state
    state = st.session_state.get("excel_editor", {})
    selection = state.get("selection", {})
    cells = selection.get("cells", [])
    
    row_idx, col_idx = None, None

    if cells:
        row_idx, col_idx = cells[0]
    elif state.get("edited_rows"):
        row_str = list(state["edited_rows"].keys())[-1]
        row_idx = int(row_str)
        row_data = state["edited_rows"][row_str]
        col_idx = int(list(row_data.keys())[-1]) if row_data else 0

    if row_idx is None:
        st.sidebar.error("❌ Select an Excel cell first!")
        return False

    if 'active_rect_screen' in st.session_state:
    del st.session_state['active_rect_screen']

    # 2. Get the Rect from the PDF Click
    # Default to top of page if no area was clicked
    rect = st.session_state.get('active_rect', (0, 0, 100, 20))

    addr = cell_address(row_idx, col_idx)
    pdf_name = pdf_file.name if pdf_file else "Unknown.pdf"

    new_link = PdfLink(
        pdf_path=pdf_name,
        page_index=current_page,
        rect=rect # Use the captured rectangle
    )

    if 'links' not in st.session_state:
        st.session_state.links = {}
    
    st.session_state.links[addr] = new_link
    st.sidebar.success(f"✅ Linked {addr} to Area on Page {current_page + 1}")
    return True