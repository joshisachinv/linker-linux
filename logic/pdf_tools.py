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