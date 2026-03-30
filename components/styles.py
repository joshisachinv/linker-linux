import streamlit as st

def apply_custom_css():
    """
    Consolidated High-Density CSS Theme.
    Optimized to reclaim vertical space and unify workstation aesthetics.
    """
    st.markdown("""
    <style>
        /* 1. GLOBAL LAYOUT & SPACING */
        .block-container { 
            padding-top: 1.5rem !important; 
            padding-bottom: 0rem !important; 
            max-width: 98% !important;
        }

        /* Forces all vertical stacks (main & sidebar) to be ultra-tight */
        [data-testid="stVerticalBlock"] { 
            gap: 0rem !important; 
        }

        /* Targets every widget container to 'crush' default margins */
        .element-container {
            margin-top: 0.1rem !important;
            margin-bottom: 0.1rem !important;
        }

        /* Move Streamlit header behind content to prevent overlap */
        [data-testid="stHeader"] {
            background-color: rgba(0,0,0,0) !important;
            border-bottom: none !important;
            z-index: 0 !important;
        }

        /* 2. DOCKED TOP TOOLBAR */
        div[data-testid="stHorizontalBlock"]:has(button) {
            background-color: #f8faff;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            padding: 4px 10px !important;
            margin-bottom: 12px !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.02);
            z-index: 1001 !important;
            position: relative;
            align-items: center;
        }

        /* Collapse all labels in the toolbar and sidebar for density */
        [data-testid="stHorizontalBlock"] label, [data-testid="stSidebar"] label {
            display: none !important;
        }

        /* 3. BUTTONS & INPUTS */
        button {
            height: 26px !important;
            min-height: 26px !important;
            padding: 0px 12px !important;
            line-height: 26px !important;
            font-size: 0.8rem !important;
            font-weight: 600 !important;
            border-radius: 4px !important;
        }

        button[kind="primary"] {
            background-color: #2563eb !important;
            border: none !important;
        }

        .stNumberInput input, .stSelectbox div[data-baseweb="select"] {
            height: 26px !important;
            font-size: 0.8rem !important;
        }

        /* 4. SIDEBAR COMPONENTS */
        [data-testid="stSidebar"] {
            background-color: #f8faff !important;
        }

        /* Tighten Expanders (Data Sources) */
        [data-testid="stExpander"] {
            margin-bottom: 0px !important;
        }
        
        [data-testid="stExpander"] summary {
            padding: 2px 8px !important;
        }

        /* Tighten File Uploaders (Workbook/Document) */
        [data-testid="stFileUploader"] section {
            padding: 4px 8px !important;
        }

        /* Status Cards Glassmorphism */
        .status-card {
            background: #ffffff;
            border-radius: 6px;
            padding: 6px 10px;
            border: 1px solid #f1f5f9;
            margin-bottom: 4px;
        }

        /* 5. TITLES & HEADERS */
        .panel-header {
            font-size: 0.7rem !important;
            font-weight: 800;
            color: #2563eb;
            text-transform: uppercase;
            border-left: 3px solid #2563eb;
            padding-left: 8px;
            margin-bottom: 6px !important;
        }

        .sidebar-header {
            font-size: 1.3rem;
            font-weight: 800;
            background: linear-gradient(45deg, #1e40af, #3b82f6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
        }

        hr {
            margin-top: 0.4rem !important;
            margin-bottom: 0.4rem !important;
        }
    </style>
    """, unsafe_allow_html=True)

def render_sidebar_header(title: str):
    st.sidebar.markdown(f'<div class="sidebar-header">{title}</div>', unsafe_allow_html=True)

def render_status_card(label: str, value: str, is_ready: bool):
    icon = "✅" if is_ready else "⚪"
    st.sidebar.markdown(f"""
        <div class="status-card">
            <div style="font-size: 0.55rem; font-weight: 700; color: #64748b; text-transform: uppercase;">{label}</div>
            <div style="font-size: 0.75rem; font-weight: 600; color: #0f172a; display: flex; justify-content: space-between;">
                <span>{value}</span>
                <span>{icon}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_column_header(title: str):
    st.markdown(f'<div class="panel-header">{title}</div>', unsafe_allow_html=True)

def render_header(title: str):
    st.markdown(f'<div style="font-weight:700; font-size:0.8rem; color:#475569; margin-bottom:4px;">{title}</div>', unsafe_allow_html=True)