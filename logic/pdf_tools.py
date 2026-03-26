import streamlit as st
from PIL import ImageDraw


def handle_image_selection(selection, zoom, min_size_px=8):
    """
    Parse click/drag output from streamlit-image-coordinates and store:
    - active_rect: PDF-space coordinates
    - active_rect_screen: current displayed-image coordinates
    """
    if not selection:
        return False

    try:
        # Expected drag payload shape from the component:
        # {"x1": ..., "y1": ..., "x2": ..., "y2": ...}
        if all(k in selection for k in ("x1", "y1", "x2", "y2")):
            x0_screen = float(selection["x1"])
            y0_screen = float(selection["y1"])
            x1_screen = float(selection["x2"])
            y1_screen = float(selection["y2"])
        elif "x" in selection and "y" in selection:
            # Plain click fallback: make a tiny rectangle
            x0_screen = float(selection["x"])
            y0_screen = float(selection["y"])
            x1_screen = x0_screen + 20
            y1_screen = y0_screen + 20
        else:
            return False
    except (TypeError, ValueError):
        return False

    x0_screen, x1_screen = sorted([x0_screen, x1_screen])
    y0_screen, y1_screen = sorted([y0_screen, y1_screen])

    if (x1_screen - x0_screen) < min_size_px or (y1_screen - y0_screen) < min_size_px:
        return False

    st.session_state["active_rect_screen"] = [x0_screen, y0_screen, x1_screen, y1_screen]
    st.session_state["active_rect"] = (
        x0_screen / zoom,
        y0_screen / zoom,
        x1_screen / zoom,
        y1_screen / zoom,
    )
    return True


def draw_saved_highlights(img, saved_links, zoom, show_saved):
    if not show_saved or not saved_links:
        return img

    draw = ImageDraw.Draw(img, "RGBA")
    curr_page = st.session_state.get("current_page", 0)

    for _, link in saved_links.items():
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
            outline=(0, 150, 0, 180),
            width=2,
        )

    # Draw current unsaved selection too
    active = st.session_state.get("active_rect_screen")
    if active:
        draw.rectangle(
            active,
            fill=(255, 255, 0, 35),
            outline=(255, 0, 0, 200),
            width=2,
        )

    return img