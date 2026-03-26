import io

import fitz
import streamlit as st
from PIL import Image
from streamlit_drawable_canvas import st_canvas

from logic.pdf_tools import draw_saved_highlights, handle_canvas_selection


@st.cache_data(show_spinner=False)
def get_pdf_page_count(file_bytes: bytes) -> int:
    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        return len(doc)


@st.cache_data(show_spinner=False)
def render_pdf_page(file_bytes: bytes, page_index: int, zoom: float) -> bytes:
    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        page = doc.load_page(page_index)
        pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))
        return pix.tobytes("png")


def display_pdf_column(uploaded_file):
    from components.styles import render_column_label

    render_column_label("PDF Real-Time Linker")

    if uploaded_file is None:
        st.info("Upload PDF to begin.")
        return None, None

    try:
        file_bytes = uploaded_file.getvalue()
        total_pages = get_pdf_page_count(file_bytes)

        # Navigation and zoom
        nav_col, zoom_col = st.columns([1, 2])

        page_num = nav_col.number_input(
            "Page",
            min_value=1,
            max_value=total_pages,
            value=min(st.session_state.get("current_page", 0) + 1, total_pages),
            step=1,
            key="pdf_page_number",
        )

        zoom = zoom_col.slider(
            "Zoom",
            min_value=1.0,
            max_value=4.0,
            value=st.session_state.get("pdf_zoom", 2.0),
            step=0.1,
            key="pdf_zoom",
        )

        current_page = page_num - 1
        st.session_state["current_page"] = current_page

        # Render page image
        page_png = render_pdf_page(file_bytes, current_page, zoom)
        bg_img = Image.open(io.BytesIO(page_png)).convert("RGB")

        # Overlay saved highlights
        bg_img = draw_saved_highlights(
            bg_img,
            st.session_state.get("links", {}),
            zoom,
            st.session_state.get("show_highlights_toggle", True),
        )

        st.caption("🖱️ Drag to draw a rectangle over the target area")

        canvas_result = st_canvas(
            fill_color="rgba(255, 255, 0, 0.30)",
            stroke_width=2,
            stroke_color="#ff0000",
            background_image=bg_img,
            update_streamlit=True,
            height=bg_img.height,
            width=bg_img.width,
            drawing_mode="rect",
            key=f"pdf_canvas_page_{current_page}_zoom_{zoom}",
            display_toolbar=True,
        )

        # Save selection side effects in your existing logic
        handle_canvas_selection(canvas_result, zoom)

        # Keep return signature compatible with your app.py
        return current_page, None

    except Exception as exc:
        st.error(f"Failed to load PDF: {exc}")
        return None, None