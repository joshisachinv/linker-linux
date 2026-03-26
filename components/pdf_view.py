import streamlit as st
import fitz
from PIL import Image, ImageDraw # Added ImageDraw for highlights
from streamlit_image_coordinates import streamlit_image_coordinates
from logic.pdf_tools import draw_pdf_highlights, update_selection_state

@st.cache_resource
def load_pdf(file_bytes):
    return fitz.open(stream=file_bytes, filetype="pdf")

def display_pdf_column(uploaded_file):
    from components.styles import render_column_label
    render_column_label("PDF Viewer")

    if not uploaded_file:
        st.info("Upload a PDF in the sidebar to begin.")
        return None, None

    doc = load_pdf(uploaded_file.getvalue())
    
    # 1. Navigation Controls
    with st.container():
        c1, c2, c3 = st.columns([1, 2, 1]) 
        with c1:
            page_num = st.number_input("Page", 1, len(doc), 1, key="pdf_page_input")
        with c2:
            zoom = st.slider("Zoom", 1.0, 4.0, 2.0, 0.1, key="pdf_zoom_slider")
        with c3:
            st.markdown(f"<br>OF {len(doc)}", unsafe_allow_html=True)

    # 2. Render Base Page
    page = doc.load_page(page_num - 1)
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    
    # 3. DRAW THE HIGHLIGHT IF AN AREA IS SELECTED
    img = draw_pdf_highlights(img, st.session_state.get('active_rect_screen'))
    
    # 4. CAPTURE CLICK
    st.caption("🎯 Click to highlight an area")
    coords = streamlit_image_coordinates(img, key="pdf_selector")
    
    # 5. Handle Selection (Modularized)
    if update_selection_state(coords, zoom):
        st.rerun()

    return page_num - 1, doc