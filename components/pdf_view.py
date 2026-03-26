import streamlit as st
import fitz
from PIL import Image
from streamlit_image_coordinates import streamlit_image_coordinates
from logic.pdf_tools import handle_vertex_selection, draw_pdf_highlights

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
    
    # 1. Navigation & Scaling Controls
    with st.container():
        c1, c2, c3 = st.columns([1, 2, 1]) 
        with c1:
            page_num = st.number_input("Page", 1, len(doc), 1, key="pdf_page_input")
        with c2:
            zoom = st.slider("Zoom", 1.0, 4.0, 2.0, 0.1, key="pdf_zoom_slider")
        with c3:
            st.markdown(f"<br>OF {len(doc)}", unsafe_allow_html=True)

    # 2. State & Data Prep
    show_highlights = st.session_state.get('show_highlights_toggle', True)
    saved_links = st.session_state.get('links', {})
    st.session_state['current_page'] = page_num - 1 # Ensure sync for highlight drawing
     
    # 3. Render PDF Page to Image
    page = doc.load_page(page_num - 1)
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    
    # 4. Draw Highlights (Both Active Selection and Persistent Links)
    img = draw_pdf_highlights(
            img, 
            st.session_state.get('active_rect_screen'),
            saved_links=saved_links,
            show_saved=show_highlights,
            zoom=zoom
    )
    
    # 5. Single Interactive Component
    # We use a static key or one tied to zoom to prevent unnecessary resets
    st.caption("🎯 Click twice to define a custom area (Top-Left then Bottom-Right)")
    coords = streamlit_image_coordinates(img, key=f"pdf_selector_p{page_num}_z{zoom}")
    
    # 6. Logic Handling
    if handle_vertex_selection(coords, zoom):
        st.rerun()

    return page_num - 1, doc