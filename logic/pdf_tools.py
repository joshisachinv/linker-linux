from PIL import Image, ImageDraw
import streamlit as st

from PIL import Image, ImageDraw
import streamlit as st

def draw_pdf_highlights(img, screen_rect, saved_links=None, show_saved=True, zoom=1.0):
    """Draws both the active selection and previously saved links."""
    draw = ImageDraw.Draw(img, "RGBA")
    
    # 1. Draw the "Active" (unsaved) highlight in Red/Yellow
    if screen_rect:
        draw.rectangle(screen_rect, fill=(255, 255, 0, 100), outline="red", width=2)
    
    # 2. Draw "Saved" highlights in Green if the toggle is ON
    if show_saved and saved_links:
        for addr, link in saved_links.items():
            # Only draw if the link is on the currently displayed page
            if link.page_index == st.session_state.get('current_page'):
                # Scale PDF coordinates back to screen pixels based on current zoom
                pdf_rect = link.rect # (x0, y0, x1, y1)
                screen_box = [
                    pdf_rect[0] * zoom, 
                    pdf_rect[1] * zoom, 
                    pdf_rect[2] * zoom, 
                    pdf_rect[3] * zoom
                ]
                draw.rectangle(screen_box, fill=(0, 255, 0, 60), outline="green", width=1)
    return img

def handle_vertex_selection(coords, zoom):
    """
    Reusable logic to capture two points and return a normalized rectangle.
    Returns: True if a selection was updated/completed, False otherwise.
    """
    if not coords:
        return False
        
    x, y = coords['x'], coords['y']

    # Step 1: Handle First Click
    if 'first_click' not in st.session_state:
        st.session_state['first_click'] = (x, y)
        st.toast("First corner set! Click the opposite corner.")
        return True
    
    # Step 2: Handle Second Click
    else:
        x0, y0 = st.session_state['first_click']
        
        # Normalize coordinates so selection works in any direction
        left, right = min(x0, x), max(x0, x)
        top, bottom = min(y0, y), max(y0, y)
        
        # Store Screen Coords for drawing the visual highlight
        st.session_state['active_rect_screen'] = [left, top, right, bottom]
        
        # Store PDF-scale Coords for the actual data link
        st.session_state['active_rect'] = (
            left / zoom, 
            top / zoom, 
            right / zoom, 
            bottom / zoom
        )
        
        # Reset first_click to allow for a new selection immediately
        del st.session_state['first_click']
        return True