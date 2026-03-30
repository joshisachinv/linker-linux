import io
import fitz
import streamlit as st
from PIL import Image
from streamlit_image_coordinates import streamlit_image_coordinates
from logic.pdf_tools import draw_saved_highlights, handle_image_selection

@st.cache_data(show_spinner=False)
def render_pdf_page(file_bytes, page_index, zoom):
    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        page = doc.load_page(page_index)
        pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
        return pix.tobytes("png")

def display_pdf_column(uploaded_file, current_page, zoom):
    try:
        file_bytes = uploaded_file.getvalue()
        
        # Auto-clear stale selections on navigation
        if (st.session_state.get("prev_pg") != current_page or 
            st.session_state.get("prev_zm") != zoom):
            st.session_state.pop("active_rect", None)
            st.session_state.pop("active_rect_screen", None)
            st.session_state.prev_pg = current_page
            st.session_state.prev_zm = zoom

        # Render page with external zoom
        page_png = render_pdf_page(file_bytes, current_page, zoom)
        bg_img = Image.open(io.BytesIO(page_png)).convert("RGB")

        # Draw highlights
        bg_img = draw_saved_highlights(
            bg_img,
            st.session_state.get("links", {}),
            zoom,
            st.session_state.get("show_highlights_toggle", True),
        )

        # Interactive coordinate capture
        selection = streamlit_image_coordinates(
            bg_img,
            key=f"pdf_coords_{current_page}_{zoom}",
            width=bg_img.width,
            click_and_drag=True,
            cursor="crosshair",
        )
        handle_image_selection(selection, zoom)

    except Exception as exc:
        st.error(f"PDF Load Error: {exc}")