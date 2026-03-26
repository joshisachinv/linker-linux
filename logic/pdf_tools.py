import streamlit as st

def handle_canvas_selection(canvas_result, zoom):
    """
    Parses the JSON from streamlit-drawable-canvas to find the latest rectangle.
    Returns: True if a new box was found, False otherwise.
    """
    if canvas_result is None or canvas_result.json_data is None:
        return False
        
    objects = canvas_result.json_data.get("objects")
    if not objects:
        return False

    # Get the most recently drawn object (the last one in the list)
    latest_obj = objects[-1]
    
    if latest_obj.get("type") == "rect":
        # Extract coordinates
        left = latest_obj["left"]
        top = latest_obj["top"]
        width = latest_obj["width"] * latest_obj["scaleX"]
        height = latest_obj["height"] * latest_obj["scaleY"]
        
        # Store for the link (scaled by zoom)
        st.session_state['active_rect'] = (
            left / zoom,
            top / zoom,
            (left + width) / zoom,
            (top + height) / zoom
        )
        # Store for visual persistence if needed
        st.session_state['active_rect_screen'] = [left, top, left + width, top + height]
        return True
        
    return False