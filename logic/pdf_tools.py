import streamlit as st
from PIL import ImageDraw


def handle_canvas_selection(canvas_result, zoom, min_size_px=8):
    """
    Parse the latest rectangle from the canvas and store it in session state.

    Stores:
    - active_rect: PDF-space coordinates (x0, y0, x1, y1)
    - active_rect_screen: screen-space coordinates for current zoom
    """
    if not canvas_result or not getattr(canvas_result, "json_data", None):
        st.session_state.pop("active_rect", None)
        st.session_state.pop("active_rect_screen", None)
        return False

    objects = canvas_result.json_data.get("objects", [])
    rects = [obj for obj in objects if obj.get("type") == "rect"]

    if not rects:
        st.session_state.pop("active_rect", None)
        st.session_state.pop("active_rect_screen", None)
        return False

    rect = rects[-1]

    try:
        left = float(rect.get("left", 0))
        top = float(rect.get("top", 0))
        width = float(rect.get("width", 0)) * float(rect.get("scaleX", 1))
        height = float(rect.get("height", 0)) * float(rect.get("scaleY", 1))
    except (TypeError, ValueError):
        st.session_state.pop("active_rect", None)
        st.session_state.pop("active_rect_screen", None)
        return False

    if width < min_size_px or height < min_size_px:
        return False

    x0_screen = left
    y0_screen = top
    x1_screen = left + width
    y1_screen = top + height

    # Normalize screen coordinates
    x0_screen, x1_screen = sorted([x0_screen, x1_screen])
    y0_screen, y1_screen = sorted([y0_screen, y1_screen])

    # Convert to PDF-space coordinates
    x0_pdf = x0_screen / zoom
    y0_pdf = y0_screen / zoom
    x1_pdf = x1_screen / zoom
    y1_pdf = y1_screen / zoom

    st.session_state["active_rect"] = (x0_pdf, y0_pdf, x1_pdf, y1_pdf)
    st.session_state["active_rect_screen"] = [x0_screen, y0_screen, x1_screen, y1_screen]
    return True


def draw_saved_highlights(img, saved_links, zoom, show_saved):
    """
    Draw persistent green boxes for saved links on the current PDF page.
    """
    if not show_saved or not saved_links:
        return img

    draw = ImageDraw.Draw(img, "RGBA")
    curr_page = st.session_state.get("current_page", 0)

    for addr, link in saved_links.items():
        if getattr(link, "page_index", None) != curr_page:
            continue

        rect = getattr(link, "rect", None)
        if not rect or len(rect) != 4:
            continue

        try:
            x0, y0, x1, y1 = [float(v) for v in rect]
        except (TypeError, ValueError):
            continue

        x0, x1 = sorted([x0, x1])
        y0, y1 = sorted([y0, y1])

        box = [x0 * zoom, y0 * zoom, x1 * zoom, y1 * zoom]
        draw.rectangle(
            box,
            fill=(0, 255, 0, 40),
            outline=(0, 150, 0, 150),
            width=2
        )

    return img