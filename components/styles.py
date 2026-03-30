import streamlit as st

def apply_custom_css():
    st.markdown("""
    <style>
        /* 1. Reset Page Padding - Reclaim vertical space */
        .block-container { 
            padding-top: 1rem !important; 
            padding-bottom: 0rem !important; 
        }
        
        /* 2. Remove the huge gap between vertical elements */
        [data-testid="stVerticalBlock"] { gap: 0.15rem !important; }

        /* 3. High-Density Headers */
        .panel-header {
            font-size: 0.75rem !important;
            font-weight: 800;
            color: #3b82f6;
            text-transform: uppercase;
            border-left: 3px solid #3b82f6;
            padding-left: 8px;
            margin-top: -10px;
            margin-bottom: 5px !important;
        }

        /* 4. Shrink Widgets for density */
        .stNumberInput, .stSlider, .stSelectbox { 
            margin-top: -15px !important; 
        }
        
        .stNumberInput input {
            height: 28px !important;
            font-size: 0.8rem !important;
        }

        /* 5. Sticky Toolbar Styling (Non-fixed to avoid hiding) */
        .custom-toolbar {
            background-color: #f8f9fa;
            border-radius: 8px;
            padding: 8px;
            border: 1px solid #e0e0e0;
            margin-bottom: 10px;
        }

        /* 1. Ultra-dense toolbar container */
        [data-testid="stHorizontalBlock"] {
            background: #f8faff;
            border-radius: 4px;
            padding: 4px 8px !important;
            margin-bottom: 8px !important;
        }

        /* 2. Remove the space reserved for hidden labels */
            .stSelectbox label, .stNumberInput label, .stSlider label {
            display: none !important;
        }

    </style>
    """, unsafe_allow_html=True)

def render_sidebar_header(title):
    st.sidebar.markdown(f'<div style="font-size:1.4rem; font-weight:800; background:linear-gradient(45deg, #3b82f6, #60a5fa); -webkit-background-clip:text; -webkit-text-fill-color:transparent;">{title}</div>', unsafe_allow_html=True)

def render_status_card(label, value, is_ready):
    icon = "✅" if is_ready else "⚪"
    st.sidebar.markdown(f"""
        <div style="background:white; border-radius:8px; padding:8px 12px; border:1px solid rgba(0,0,0,0.05); margin-bottom:5px;">
            <div style="font-size:0.6rem; font-weight:700; color:grey; text-transform:uppercase;">{label}</div>
            <div style="font-size:0.8rem; font-weight:600;">{value} {icon}</div>
        </div>
    """, unsafe_allow_html=True)

def render_column_header(title):
    st.markdown(f'<div class="panel-header">{title}</div>', unsafe_allow_html=True)

def render_header(title):
    st.markdown(f'<div style="font-weight:700; font-size:0.9rem; color:#1e293b; margin-bottom:10px;">{title}</div>', unsafe_allow_html=True)