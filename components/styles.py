import streamlit as st

def apply_custom_css():
    st.markdown("""
        <style>
            .block-container { padding-top: 3rem; padding-bottom: 0rem; }
            .custom-header {
                position: fixed; top: 0; left: 0; width: 100%; height: 40px;
                background-color: #f8f9fa; border-bottom: 1px solid #e0e0e0;
                display: flex; align-items: center; padding-left: 60px; 
                z-index: 99; font-size: 12px; font-weight: 600; color:rgb(12, 12, 12);
            }
            .column-header {
                font-size: 12px !important; font-weight: bold; color: #007bff;
                text-transform: uppercase; margin-bottom: 3px;
                border-left: 3px solid #007bff; padding-left: 8px;
            }
            .viewer-label { font-size: 10px !important; color: #888; margin-bottom: -5px !important; font-weight: bold; }
        </style>
    """, unsafe_allow_html=True)

def render_header(title):
    st.markdown(f'<div class="custom-header">{title}</div>', unsafe_allow_html=True)

def render_column_label(label):
    st.markdown(f'<p class="column-header">{label}</p>', unsafe_allow_html=True)