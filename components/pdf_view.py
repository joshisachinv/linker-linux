import streamlit as st
import fitz  # PyMuPDF
from PIL import Image
from streamlit_image_coordinates import streamlit_image_coordinates

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
        
    # Navigation controls
    with st.container():
        c1, c2, c3 = st.columns([1, 2, 1]) 
        with c1:
            st.markdown('<p class="viewer-label">PAGE</p>', unsafe_allow_html=True)
            page_num = st.number_input("Page", 1, len(doc), 1, label_visibility="collapsed", key="pdf_page_input")
        with c2:
            st.markdown('<p class="viewer-label">ZOOM</p>', unsafe_allow_html=True)
            zoom = st.slider("Zoom", 1.0, 4.0, 2.0, 0.1, label_visibility="collapsed", key="pdf_zoom_slider")
        with c3:
            st.markdown(f'<p class="viewer-label">OF {len(doc)}</p>', unsafe_allow_html=True)

    # Render Page
    page = doc.load_page(page_num - 1)
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    
    st.caption("🎯 Click on the PDF area to link it to the selected Excel cell")
    
    # CAPTURE CLICK COORDINATES
    coords = streamlit_image_coordinates(img, key="pdf_selector")
    
    # Store the latest click in session state for the capture button
    if coords:
        # Convert click to PDF points (scale back from zoom)
        pdf_x = coords['x'] / zoom
        pdf_y = coords['y'] / zoom
        # Create a small 50x20 box around the click
        st.session_state['active_rect'] = (pdf_x, pdf_y, pdf_x + 50, pdf_y + 20)
        st.toast(f"Area Selected at {coords['x']}, {coords['y']}")

    return page_num - 1, doc
  