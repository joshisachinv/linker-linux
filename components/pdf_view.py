import io

import fitz
import streamlit as st
from PIL import Image
from streamlit_image_coordinates import streamlit_image_coordinates
from logic.pdf_tools import draw_saved_highlights, handle_image_selection


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
    if uploaded_file is None:
        st.info("Upload PDF to begin.")
        return None, None

    try:
        file_bytes = uploaded_file.getvalue()
        total_pages = get_pdf_page_count(file_bytes)

        nav_col, zoom_col = st.columns([1, 2])
        
        raw_current_page = st.session_state.get("current_page")
        safe_current_page = raw_current_page if raw_current_page is not None else 0
        
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

        previous_page = st.session_state.get("current_page")
        previous_zoom = st.session_state.get("pdf_zoom_last")

        # Clear stale selection if page or zoom changed
        if previous_page != current_page or previous_zoom != zoom:
            st.session_state.pop("active_rect", None)
            st.session_state.pop("active_rect_screen", None)

        st.session_state["current_page"] = current_page
        st.session_state["pdf_zoom_last"] = zoom

        # Render page
        page_png = render_pdf_page(file_bytes, current_page, zoom)
        bg_img = Image.open(io.BytesIO(page_png)).convert("RGB")

        # Draw saved highlights on top
        bg_img = draw_saved_highlights(
            bg_img,
            st.session_state.get("links", {}),
            zoom,
            st.session_state.get("show_highlights_toggle", True),
        )

        st.caption("Drag on the PDF image to select a region.")

        # This component supports click-and-drag selection
        selection = streamlit_image_coordinates(
            bg_img,
            key=f"pdf_image_coords_{current_page}_{zoom}",
            width=bg_img.width,
            click_and_drag=True,
            use_column_width="never",
            cursor="crosshair",
        )

        handle_image_selection(selection, zoom)

        # Optional live status
        rect = st.session_state.get("active_rect_screen")
        if rect:
            x0, y0, x1, y1 = rect
            st.caption(
                f"Selected area: ({int(x0)}, {int(y0)}) → ({int(x1)}, {int(y1)})"
            )

        return current_page, None

    except Exception as exc:
        st.error(f"Failed to load PDF: {exc}")
        return None, None