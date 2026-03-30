import streamlit as st

def apply_custom_css():
    """
    Applies a professional, high-density CSS theme to the application.
    Optimized for document inspection and precision linking.
    """
    st.markdown("""
    <style>
        * ============================================================
           1. CORE OVERLAP FIX
           Forces Streamlit's top header to be transparent and 
           behind our custom toolbar.
           ============================================================ */
        
        [data-testid="stHeader"] {
            background-color: rgba(0,0,0,0) !important;
            border-bottom: none !important;
            z-index: 0 !important; /* Move system bar behind everything */
        }
        
        /* ============================================================
           1. GLOBAL LAYOUT & SPACING
           Reclaims vertical space and reduces default gaps.
           ============================================================ */
        
        /* Reduce main container padding to move content higher up */
        .block-container { 
            padding-top: 2.5rem !important; 
            padding-bottom: 0rem !important; 
            max-width: 98% !important;
        }
        
        /* ============================================================
           2. TOP TOOLBAR (GLOBAL CONTROLS)
           Styles the horizontal row containing Link, Sheet, Page, and Zoom.
           ============================================================ */
        
        /* Create a subtle 'docked' look for the toolbar */
        div[data-testid="stHorizontalBlock"]:has(button) {
            background-color: #f8faff;
            border: 1px solid #e2e8f0;
            border-radius: 6px;
            padding: 8px 12px !important;
            margin-bottom: 20px !important;
            box-shadow: 0 2px 4px rgba(0,0,0,0.02);
            z-index: 1001 !important;
            position: relative;
            align-items: center;
        }

        /* Hide labels for toolbar widgets to save height (tooltips handle info) */
        [data-testid="stHorizontalBlock"] label {
            display: none !important;
        }

        /* Reduce the height of inputs in the toolbar */
        .stNumberInput input, .stSelectbox div[data-baseweb="select"] {
            height: 30px !important;
            font-size: 0.85rem !important;
        }

        /* ============================================================
           3. PANEL HEADERS (EXCEL & PDF LABELS)
           Provides clear visual anchors for the two main work areas.
           ============================================================ */
        
        .panel-header {
            font-size: 0.7rem !important;
            font-weight: 800;
            color: #2563eb; /* Primary Blue */
            text-transform: uppercase;
            letter-spacing: 0.08em;
            border-left: 3px solid #2563eb;
            padding-left: 8px;
            margin-top: 5px;
            margin-bottom: 8px !important;
        }

        /* ============================================================
           4. SIDEBAR & STATUS CARDS
           Professional styling for the 'Setup' and 'Export' area.
           ============================================================ */
        
        /* Sidebar Title Gradient */
        .sidebar-header {
            font-size: 1.4rem;
            font-weight: 800;
            background: linear-gradient(45deg, #1e40af, #3b82f6);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }

        /* Glassmorphism-style Status Cards */
        .status-card {
            background: #ffffff;
            border-radius: 8px;
            padding: 10px 14px;
            border: 1px solid #f1f5f9;
            box-shadow: 0 1px 2px rgba(0,0,0,0.03);
            margin-bottom: 6px;
        }

        .status-label {
            font-size: 0.6rem;
            font-weight: 700;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.03em;
        }

        .status-value {
            font-size: 0.8rem;
            font-weight: 600;
            color: #0f172a;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        /* Target the specific emotion cache class for dividers */
        .st-emotion-cache-1h1td79 {
            margin-top: 0.5rem !important;
            margin-bottom: 0.5rem !important;
            padding-top: 0px !important;
            padding-bottom: 0px !important;
        }

        /* Alternative: Target all dividers globally for consistency */
        hr {
            margin-top: 0.5rem !important;
            margin-bottom: 0.5rem !important;
        }

        /* ============================================================
           5. WIDGET OVERRIDES
           Fine-tuning specific Streamlit components for density.
           ============================================================ */
        
        /* Make sliders more compact */
        .stSlider {
            margin-top: -10px !important;
        }

        /* Ensure Sidebar Buttons are full width */
        [data-testid="stSidebar"] button {
            width: 100% !important;
            border-radius: 6px !important;
        }

        /* Style Captions (Instructions) */
        .stCaption {
            font-size: 0.72rem !important;
            color: #64748b !important;
            line-height: 1.2 !important;
        }
    </style>
    """, unsafe_allow_html=True)

def render_sidebar_header(title: str):
    """Renders the main logo/title in the sidebar."""
    st.sidebar.markdown(f'<div class="sidebar-header">{title}</div>', unsafe_allow_html=True)

def render_status_card(label: str, value: str, is_ready: bool):
    """Renders a high-density status indicator."""
    icon = "✅" if is_ready else "⚪"
    st.sidebar.markdown(f"""
        <div class="status-card">
            <div class="status-label">{label}</div>
            <div class="status-value">
                <span>{value}</span>
                <span>{icon}</span>
            </div>
        </div>
    """, unsafe_allow_html=True)

def render_column_header(title: str):
    """Renders the header for the Excel and PDF columns."""
    st.markdown(f'<div class="panel-header">{title}</div>', unsafe_allow_html=True)

def render_header(title: str):
    """Renders a small breadcrumb-style header above the toolbar."""
    st.markdown(f'<div style="font-weight:700; font-size:0.85rem; color:#475569; margin-bottom:8px;">{title}</div>', unsafe_allow_html=True)