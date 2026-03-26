import streamlit as st
from PIL import Image, ImageDraw

def draw_pdf_highlights(img, screen_rect, saved_links=None, show_saved=True, zoom=1.0):
    """
    Draws persistent green highlights for saved links.
    (The canvas handles the 'active' yellow box, so we don't draw it here).
    """
    draw = ImageDraw.Draw(img, "RGBA")
    
    # Draw "Saved" highlights in Green if the toggle is ON
    if show_saved and saved_links:
        current_page = st.session_state.get('current_page', 0)
        for addr, link in saved_links.items():
            # Only draw if the link is on the currently displayed page
            if link.page_index == current_page:
                # Scale PDF coordinates back to screen pixels based on current zoom
                pdf_rect = link.rect # (x0, y0, x1, y1)
                screen_box = [
                    pdf_rect[0] * zoom, 
                    pdf_rect[1] * zoom, 
                    pdf_rect[2] * zoom, 
                    pdf_rect[3] * zoom
                ]
                # Light green fill with a darker green border
                draw.rectangle(screen_box, fill=(0, 255, 0, 40), outline=(0, 150, 0, 150), width=1)
    return img

def handle_canvas_selection(canvas_result, zoom):
    """
    Parses the JSON from streamlit-drawable-canvas to find the latest rectangle.
    """
    if canvas_result is None or canvas_result.json_data is None:
        return False
        
    objects = canvas_result.json_data.get("objects")
    if not objects:
        return False

    # Get the most recently drawn object (the last one in the list)
    latest_obj = objects[-1]
    
    if latest_obj.get("type") == "rect":
        # Extract coordinates from the canvas JSON format
        left = latest_obj["left"]
        top = latest_obj["top"]
        width = latest_obj["width"] * latest_obj["scaleX"]
        height = latest_obj["height"] * latest_obj["scaleY"]
        
        # Store for the actual PDF link (scaled down by zoom to be resolution-independent)
        st.session_state['active_rect'] = (
            left / zoom,
            top / zoom,
            (left + width) / zoom,
            (top + height) / zoom
        )
        return True
        
    return False