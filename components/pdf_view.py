import streamlit as st
import fitz  # PyMuPDF
from PIL import Image

@st.cache_resource
def load_pdf(file_bytes):
    """Caches the PDF document so it doesn't reload on every zoom change."""
    return fitz.open(stream=file_bytes, filetype="pdf")

def display_pdf_column(uploaded_file):
    from components.styles import render_column_label
    render_column_label("PDF Viewer")

    if uploaded_file:
        # Use bytes to allow caching
        file_bytes = uploaded_file.getvalue()
        doc = load_pdf(file_bytes)
        
        # Add zoom and page selection in a neat row
        with st.container():
            # Use 3 columns to give the page input a smaller width
            c1, c2, c3 = st.columns([1, 2, 1]) 
    
            with c1:
                st.markdown('<p class="viewer-label">PAGE</p>', unsafe_allow_html=True)
                page_num = st.number_input(
                    "Page", 1, len(doc), 1, 
                    label_visibility="collapsed",
                    key="pdf_page_input"
                )
    
            with c2:
                st.markdown('<p class="viewer-label">ZOOM</p>', unsafe_allow_html=True)
                zoom = st.slider(
                    "Zoom", 1.0, 4.0, 2.0, 0.1,
                    label_visibility="collapsed",
                    key="pdf_zoom_slider"
                )
    
            with c3:
            # Show a small status of total pages
                st.markdown(f'<p class="viewer-label">OF {len(doc)}</p>', unsafe_allow_html=True)

        # RENDER THE IMAGE
        page = doc.load_page(page_num - 1)
        mat = fitz.Matrix(zoom*4, zoom*4)
        pix = page.get_pixmap(matrix=mat)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        # Displaying inside the scroll container
        with st.container():
            st.image(img)
        
        return page_num - 1, doc
    else:
        st.info("Upload a PDF in the sidebar to begin.")
    return None, None