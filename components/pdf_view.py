import streamlit as st
import fitz
from PIL import Image
from streamlit_drawable_canvas import st_canvas
from logic.pdf_tools import draw_pdf_highlights, handle_canvas_selection

@st.cache_resource
def load_pdf(file_bytes):
    return fitz.open(stream=file_bytes, filetype="pdf")

def display_pdf_column(uploaded_file):
    from components.styles import render_column_label
    render_column_label("PDF Viewer")

    if not uploaded_file:
        st.info("Upload a PDF in the sidebar.")
        return None, None

    doc = load_pdf(uploaded_file.getvalue())
    
    # 1. Navigation & Zoom
    with st.container():
        c1, c2, c3 = st.columns([1, 2, 1]) 
        with c1:
            page_num = st.number_input("Page", 1, len(doc), 1, key="pdf_page_input")
        with c2:
            zoom = st.slider("Zoom", 1.0, 4.0, 2.0, 0.1, key="pdf_zoom_slider")
        with c3:
            st.markdown(f"<br>OF {len(doc)}", unsafe_allow_html=True)

    # 2. Render Page Background
    page = doc.load_page(page_num - 1)
    pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
    bg_img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    
    # 3. Draw ONLY Saved Highlights onto the background image
    # The Canvas will handle the current "active" drag box
    bg_img = draw_pdf_highlights(
        bg_img, 
        None, # No active rect here
        saved_links=st.session_state.get('links', {}),
        show_saved=st.session_state.get('show_highlights_toggle', True),
        zoom=zoom
    )

    # 4. The Drawable Canvas
    st.caption("🖱️ Drag your mouse to select an area")
    canvas_result = st_canvas(
        fill_color="rgba(255, 255, 0, 0.3)",  # Yellow highlight
        stroke_width=2,
        stroke_color="#ff0000",
        background_image=bg_img,
        update_streamlit=True,
        height=bg_img.height,
        width=bg_img.width,
        drawing_mode="rect",
        key=f"canvas_{page_num}_{zoom}",
    )

    # 5. Process Selection
    if handle_canvas_selection(canvas_result, zoom):
        # We don't always need st.rerun() here as the canvas updates 
        # but it helps sync st.session_state['active_rect'] immediately
        pass

    return page_num - 1, doc