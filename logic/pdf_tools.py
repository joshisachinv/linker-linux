from PIL import Image, ImageDraw
import streamlit as st

def draw_pdf_highlights(img, screen_rect):
    """Draws a semi-transparent highlight on a PIL image."""
    if screen_rect:
        draw = ImageDraw.Draw(img, "RGBA")
        # Standard yellow highlight with 40% transparency (100/255)
        draw.rectangle(
            screen_rect, 
            fill=(255, 255, 0, 100), 
            outline="red", 
            width=2
        )
    return img

def update_selection_state(coords, zoom):
    """Calculates and stores screen and PDF-scale coordinates."""
    if coords:
        x, y = coords['x'], coords['y']
        
        # Define the size of the box (e.g., 60x25 pixels)
        box_w, box_h = 60, 25
        
        # Store screen coordinates for visual drawing
        st.session_state['active_rect_screen'] = [x, y, x + box_w, y + box_h]
        
        # Store PDF-scale coordinates for the actual link (ignores zoom)
        st.session_state['active_rect'] = (
            x / zoom, 
            y / zoom, 
            (x + box_w) / zoom, 
            (y + box_h) / zoom
        )
        return True
    return False

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