import streamlit as st
import fitz  # PyMuPDF
from PIL import Image

@st.cache_resource
def load_pdf(file_bytes):
    return fitz.open(stream=file_bytes, filetype="pdf")

def display_pdf_column(uploaded_file):
    from components.styles import render_column_label
    render_column_label("PDF Viewer")

    if uploaded_file:
        file_bytes = uploaded_file.getvalue()
        doc = load_pdf(file_bytes)
        
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

        page = doc.load_page(page_num - 1)
        mat = fitz.Matrix(zoom*4, zoom*4)
        pix = page.get_pixmap(matrix=mat)
        img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
        
        with st.container():
            st.image(img)
        
        return page_num - 1, doc
    return None, None