import streamlit as st
from models.pdf_link import PdfLink
from logic.cell_addr import cell_address

def capture_link(excel_selection, current_page, pdf_file):
    # This key MUST match the 'key' argument in st.data_editor exactly
    state = st.session_state.get("excel_editor", {})
    
    row_idx = None
    col_idx = 0 

    # --- THE LEGACY HUNT ---
    # Look for 'edited_rows' as confirmed in your previous debug logs
    edited_rows = state.get("edited_rows", {})
    if edited_rows:
        # Get the most recently edited row
        row_str = list(edited_rows.keys())[-1]
        row_idx = int(row_str)
        
        # Get the column index from the nested dictionary
        row_data = edited_rows[row_str]
        if row_data:
            col_str = list(row_data.keys())[-1]
            col_idx = int(col_str)
    
    # Fallback for newer Streamlit versions if the environment updates
    elif state.get("selection") and state["selection"].get("cells"):
        cells = state["selection"]["cells"]
        row_idx = cells[0][0]
        col_idx = cells[0][1]

    # --- VALIDATION ---
    if row_idx is None:
        st.sidebar.error("❌ Link Failed: No row detected.")
        st.sidebar.info("Tip: Double-click a cell and press Enter to 'select' it.")
        return False

    # 2. Proceed with linking
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