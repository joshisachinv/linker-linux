import streamlit as st
from PIL import Image, ImageDraw

def handle_canvas_selection(canvas_result, zoom):
    """Parses real-time drag data from the canvas."""
    if not canvas_result or not canvas_result.json_data:
        return False
        
    objects = canvas_result.json_data.get("objects")
    if not objects:
        return False

    # Get the latest rectangle drawn by the user
    rect = objects[-1] 
    if rect.get("type") == "rect":
        # Canvas coordinates (left, top, width, height)
        l, t = rect["left"], rect["top"]
        w, h = rect["width"] * rect["scaleX"], rect["height"] * rect["scaleY"]
        
        # Store for the link (Scaled down by zoom to be resolution-independent)
        st.session_state['active_rect'] = (l/zoom, t/zoom, (l+w)/zoom, (t+h)/zoom)
        st.session_state['active_rect_screen'] = [l, t, l+w, t+h]
        return True
    return False

def draw_saved_highlights(img, saved_links, zoom, show_saved):
    """Draws persistent green boxes for existing links on the background image."""
    if not show_saved or not saved_links:
        return img
        
    draw = ImageDraw.Draw(img, "RGBA")
    curr_page = st.session_state.get('current_page', 0)
    
    for addr, link in saved_links.items():
        if link.page_index == curr_page:
            # Scale PDF points to current screen zoom
            box = [v * zoom for v in link.rect]
            draw.rectangle(box, fill=(0, 255, 0, 40), outline=(0, 150, 0, 150), width=1)
    return img