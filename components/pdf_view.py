import io

import fitz
import streamlit as st
from PIL import Image
from streamlit_image_coordinates import streamlit_image_coordinates

from logic.pdf_tools import draw_saved_highlights, handle_image_selection


def _normalize_zoom(zoom: float) -> float:
    """Normalize zoom for stable caching and widget keys."""
    return round(float(zoom), 2)


@st.cache_data(show_spinner=False)
def get_pdf_page_count(file_bytes: bytes) -> int:
    """Return the number of pages in the PDF."""
    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        return len(doc)


@st.cache_data(show_spinner=False)
def render_pdf_page(file_bytes: bytes, page_index: int, zoom: float) -> tuple[bytes, int]:
    """
    Render a PDF page to PNG bytes.

    Returns:
        (png_bytes, safe_page_index)
    """
    zoom = _normalize_zoom(zoom)

    with fitz.open(stream=file_bytes, filetype="pdf") as doc:
        page_count = len(doc)
        if page_count == 0:
            raise ValueError("The PDF contains no pages.")

        safe_page_index = max(0, min(int(page_index), page_count - 1))
        page = doc.load_page(safe_page_index)
        pix = page.get_pixmap(matrix=fitz.Matrix(zoom, zoom))

        return pix.tobytes("png"), safe_page_index


def clear_pdf_selection_if_view_changed(current_page: int, zoom: float) -> None:
    """Clear stale rectangle selections when page or zoom changes."""
    zoom = _normalize_zoom(zoom)

    if (
        st.session_state.get("prev_pg") != current_page
        or st.session_state.get("prev_zm") != zoom
    ):
        st.session_state.pop("active_rect", None)
        st.session_state.pop("active_rect_screen", None)
        st.session_state["prev_pg"] = current_page
        st.session_state["prev_zm"] = zoom


def _render_pdf_image(file_bytes: bytes, current_page: int, zoom: float) -> tuple[Image.Image, int, int]:
    """
    Render the PDF page and return:
        (background_image, safe_page_index, page_count)
    """
    page_count = get_pdf_page_count(file_bytes)
    page_png, safe_page_index = render_pdf_page(file_bytes, current_page, zoom)
    bg_img = Image.open(io.BytesIO(page_png)).convert("RGB")
    return bg_img, safe_page_index, page_count


def display_pdf_column(uploaded_file, current_page: int = 0, zoom: float = 2.0) -> tuple[int | None, int | None]:
    """
    Render the PDF viewer and process user selections.

    Returns:
        (safe_page_index, page_count)
    """
    if uploaded_file is None:
        st.info("Upload a PDF in the sidebar.")
        return None, None

    file_bytes = uploaded_file.getvalue()
    zoom = _normalize_zoom(zoom)
    clear_pdf_selection_if_view_changed(current_page, zoom)

    try:
        bg_img, safe_page_index, page_count = _render_pdf_image(file_bytes, current_page, zoom)
        st.session_state["current_page"] = safe_page_index
        st.session_state["pdf_page_count"] = page_count
    except Exception as exc:
        st.error(f"Failed to render PDF page: {exc}")
        return None, None

    try:
        bg_img = draw_saved_highlights(
            bg_img,
            st.session_state.get("links", {}),
            zoom,
            st.session_state.get("show_highlights_toggle", True),
        )

        zoom_key = f"{zoom:.2f}"
        selection = streamlit_image_coordinates(
            bg_img,
            key=f"pdf_coords_{safe_page_index}_{zoom_key}",
            width=bg_img.width,
            click_and_drag=True,
            cursor="crosshair",
        )

        if selection:
            handle_image_selection(selection, zoom)

    except Exception as exc:
        st.error(f"Failed during PDF interaction: {exc}")
        return safe_page_index, page_count

    return safe_page_index, page_count