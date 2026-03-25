import streamlit as st
from models.pdf_link import PdfLink
from logic.cell_addr import cell_address

def capture_link(excel_selection, current_page, pdf_file):
    # Modern Streamlit selection logic
    selection = excel_selection.get("selection", {})
    cells = selection.get("cells", [])

    if not cells:
        st.sidebar.error("❌ Please click a cell in the table first!")
        return False

    # Grab [row, col] directly from the selection
    row_idx, col_idx = cells[0]
    
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