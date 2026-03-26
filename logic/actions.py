import streamlit as st
from models.pdf_link import PdfLink
from logic.cell_addr import cell_address


def capture_link(excel_selection, current_page, pdf_file):
    """
    Capture a link between the currently selected Excel cell
    and the currently selected PDF rectangle.
    """

    if not excel_selection:
        st.sidebar.error("❌ Select an Excel cell first.")
        return False

    if current_page is None:
        st.sidebar.error("❌ No PDF page is currently selected.")
        return False

    row_idx = excel_selection.get("row_index")
    col_idx = excel_selection.get("column_index")
    sheet_name = excel_selection.get("sheet_name")
    cell_ref = excel_selection.get("cell_ref")

    if row_idx is None or col_idx is None:
        st.sidebar.error("❌ Invalid Excel selection.")
        return False

    if not cell_ref:
        cell_ref = cell_address(row_idx, col_idx)

    if pdf_file is None:
        st.sidebar.error("❌ Upload a PDF first.")
        return False

    rect = st.session_state.get("active_rect")
    if rect is None:
        st.sidebar.error("❌ Draw or select an area on the PDF first.")
        return False

    try:
        x0, y0, x1, y1 = rect
        rect = (
            min(float(x0), float(x1)),
            min(float(y0), float(y1)),
            max(float(x0), float(x1)),
            max(float(y0), float(y1)),
        )
    except Exception:
        st.sidebar.error("❌ Invalid PDF selection area.")
        return False

    if "active_rect_screen" in st.session_state:
        del st.session_state["active_rect_screen"]

    new_link = PdfLink(
        pdf_path=pdf_file.name,
        page_index=current_page,
        rect=rect,
        sheet_name=sheet_name,
        cell_ref=cell_ref,
    )

    if "links" not in st.session_state:
        st.session_state.links = {}

    link_key = f"{sheet_name}!{cell_ref}" if sheet_name else cell_ref
    st.session_state.links[link_key] = new_link

    st.sidebar.success(f"✅ Linked {link_key} to area on page {current_page + 1}")
    return True