import streamlit as st

def apply_custom_css():
    st.markdown("""
    <style>
        /* 1. Remove Vertical Dead Space */
        .block-container { padding-top: 1.5rem !important; }
        [data-testid="stVerticalBlock"] { gap: 0.1rem !important; }
        
        /* 2. Compact Sidebar and Status Cards */
        .status-card {
            background: white;
            border-radius: 8px;
            padding: 8px 12px;
            border: 1px solid rgba(0, 0, 0, 0.05);
            margin-bottom: 5px;
        }

        /* 3. Panel Header Styling */
        .panel-header {
            font-size: 0.7rem !important;
            font-weight: 800;
            color: #3b82f6;
            text-transform: uppercase;
            border-left: 3px solid #3b82f6;
            padding-left: 8px;
            margin-top: -10px;
            margin-bottom: 5px !important;
        }

        /* 4. Shrink Widgets */
        .stNumberInput, .stSlider, .stSelectbox { margin-top: -15px !important; }
        
        .sidebar-header {
            font-size: 1.4rem;
            font-weight: 800;
            background: linear-gradient(45deg, #3b82f6, #60a5fa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }
    </style>
    """, unsafe_allow_html=True)

def render_sidebar_header(title):
    st.sidebar.markdown(f'<div class="sidebar-header">{title}</div>', unsafe_allow_html=True)

def render_status_card(label, value, is_ready):
    icon = "✅" if is_ready else "⚪"
    st.sidebar.markdown(f"""
        <div class="status-card">
            <div style="font-size:0.6rem; font-weight:700; color:grey;">{label}</div>
            <div style="font-size:0.8rem; font-weight:600;">{value} {icon}</div>
        </div>
    """, unsafe_allow_html=True)

def render_column_header(title):
    st.markdown(f'<div class="panel-header">{title}</div>', unsafe_allow_html=True)

def render_header(title):
    st.markdown(f'<div style="font-weight:700; font-size:0.9rem; color:#1e293b;">{title}</div>', unsafe_allow_html=True)