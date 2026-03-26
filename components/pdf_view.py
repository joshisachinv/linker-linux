import streamlit as st
import fitz
from PIL import Image
from streamlit_drawable_canvas import st_canvas
from logic.pdf_tools import draw_saved_highlights, handle_canvas_selection

@st.cache_resource
def load_pdf(file_bytes):
    return fitz.open(stream=file_bytes, filetype="pdf")

def display_pdf_column(uploaded_file):
    from components.styles import render_column_label
    render_column_label("PDF Real-Time Linker")

    if not uploaded_file:
        st.info("Upload PDF to begin.")
        return None, None

    doc = load_pdf(uploaded_file.getvalue())
    
    # Navigation & Zoom
    c1, c2, c3 = st.columns([1, 2, 1])
    page_num = c1.number_input("Page", 1, len(doc), 1)
    zoom = c2.slider("Zoom", 1.0, 4.0, 2.0, 0.1)
    st.session_state['current_page'] = page_num - 1

    # Render Background Page
    page = doc.load_page(page_num - 1)
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
    bg_img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    
    # Add persistent highlights to the background image
    bg_img = draw_saved_highlights(
        bg_img, 
        st.session_state.get('links', {}), 
        zoom, 
        st.session_state.get('show_highlights_toggle', True)
    )

    # REAL-TIME CANVAS
    st.caption("🖱️ Drag to draw a rectangle over the target area")
    canvas_result = st_canvas(
        fill_color="rgba(255, 255, 0, 0.3)", # Semi-transparent yellow
        stroke_width=2,
        stroke_color="#ff0000",
        background_image=bg_img,
        update_streamlit=True,
        height=bg_img.height,
        width=bg_img.width,
        drawing_mode="rect",
        key=f"canvas_p{page_num}_z{zoom}",
        display_toolbar=True # Shows Undo/Trash icons
    )

    # Process Drag Result
    if handle_canvas_selection(canvas_result, zoom):
        # Coordinates are now in st.session_state['active_rect']
        pass

    return page_num - 1, doc