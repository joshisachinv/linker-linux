import streamlit as st
import fitz
from PIL import Image, ImageDraw # Added ImageDraw for highlights
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
    # This shows the user what they have just clicked
    if 'active_rect_screen' in st.session_state:
        draw = ImageDraw.Draw(img, "RGBA")
        # Draw a semi-transparent yellow box
        # Coordinates: [x0, y0, x1, y1]
        draw.rectangle(
            st.session_state['active_rect_screen'], 
            fill=(255, 255, 0, 100), 
            outline="red", 
            width=3
        )

    st.caption("🎯 Click to highlight an area and link it to the Excel cell")
    
    # 4. CAPTURE CLICK
    coords = streamlit_image_coordinates(img, key="pdf_selector")
    
    if coords:
        # Save screen coords for drawing the highlight box next rerun
        x, y = coords['x'], coords['y']
        st.session_state['active_rect_screen'] = [x, y, x + 60, y + 25]
        
        # Save PDF-scale coords for the actual link (ignores zoom)
        pdf_x, pdf_y = x / zoom, y / zoom
        st.session_state['active_rect'] = (pdf_x, pdf_y, pdf_x + 50, pdf_y + 20)
        
        # Force rerun to show the highlight immediately
        st.rerun()

    return page_num - 1, doc