import streamlit as st
from models.pdf_link import PdfLink
from logic.cell_addr import cell_address

def capture_link(excel_selection, current_page, pdf_file):
    # 1. Access the modern selection dictionary directly from the event
    selection = excel_selection.get("selection", {})
    cells = selection.get("cells", [])

    # 2. Check if a cell was actually clicked
    if not cells:
        st.sidebar.error("❌ Please click a cell in the Excel table first!")
        return False

    # 3. Extract indices: cells[0] is exactly [row_index, col_index]
    row_idx, col_idx = cells[0]
    
    # 4. Convert to Excel Address
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