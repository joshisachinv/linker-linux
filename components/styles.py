import streamlit as st

def apply_custom_css():
    """
    Applies expanded CSS styling to the Streamlit app.
    Centralizes visual tweaks and fixes independent scrolling.
    """
    st.markdown("""
        <style>
            /* 1. Global Page Reset */
            .block-container {
                padding-top: 3rem;
                padding-bottom: 0rem;
            }

            /* 2. Fixed Top Header Layout */
            .custom-header {
                position: fixed;
                top: 0;
                left: 0;
                width: 100%;
                height: 40px;
                background-color: #f8f9fa;
                border-bottom: 1px solid #e0e0e0;
                display: flex;
                align-items: center;
                padding-left: 60px; 
                z-index: 99;
                font-size: 12px;
                font-weight: 600;
                color:rgb(12, 12, 12);
            }

            /* 3. Sidebar Toggle Protection */
            button[kind="headerNoContext"] {
                z-index: 1000 !important;
                background-color: transparent !important;
            }
            
            [data-testid="stHeader"] {
                background-color: rgba(0,0,0,0);
                border-bottom: none;
                z-index: 1000;
            }

            /* 4. Column Header Styling */
            .column-header {
                font-size: 12px !important;
                font-weight: bold;
                color: #007bff;
                text-transform: uppercase;
                margin-bottom: 3px;
                border-left: 3px solid #007bff;
                padding-left: 8px;
            }

        /* Make the PDF control row compact */
            [data-testid="column"] [data-testid="stVerticalBlock"] > div {
                gap: 0rem !important;
            }

            /* Style the mini-labels above the widgets */
            .viewer-label {
                font-size: 10px !important;
                color: #888;
                margin-bottom: -5px !important;
                font-weight: bold;
            }

            /* Shrink the height of the number input and slider */
            [data-testid="stNumberInput"], [data-testid="stSlider"] {
                padding-top: 0px !important;
                padding-bottom: 0px !important;
            }

            /* Force the slider and number input to be smaller */
            .stNumberInput input {
                height: 20px !important;
                font-size: 10px !important;
            }
            
            /* Remove the huge gap at the bottom of widgets */
            .element-container {
                margin-bottom: 0px !important;
            }    

            /* Ensure sidebar buttons fill the width */
            [data-testid="stSidebar"] button {
            width: 100% !important;
            }            
        </style>
    """, unsafe_allow_html=True)

def render_header(title):
    st.markdown(f'<div class="custom-header">{title}</div>', unsafe_allow_html=True)

def render_column_label(label):
    st.markdown(f'<p class="column-header">{label}</p>', unsafe_allow_html=True)