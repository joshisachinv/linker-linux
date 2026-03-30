import streamlit as st

def apply_custom_css():
    st.markdown("""
    <style>
        /* 1. Global Layout Enhancements */
        :root {
            --primary: #3b82f6;
            --sidebar-bg: #F8FAFC;
            --panel-radius: 12px;
            --header-height: 45px;
        }

        .stAppViewContainer .main .block-container {
            padding-top: 4rem;
            padding-bottom: 1rem;
        }

        /* 2. Modern Sidebar Header & Navigation */
        [data-testid="stSidebarNav"] {
            padding-top: 2rem;
        }
        
        .sidebar-header {
            font-size: 1.6rem;
            font-weight: 800;
            background: linear-gradient(45deg, var(--primary), #60a5fa);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 1.5rem;
            letter-spacing: -0.02em;
        }

        /* 3. Status Cards for Sidebar */
        .status-card {
            background: white;
            border-radius: 10px;
            padding: 12px;
            border: 1px solid rgba(0, 0, 0, 0.05);
            margin-bottom: 8px;
            box-shadow: 0 1px 3px rgba(0,0,0,0.05);
        }

        .status-label {
            font-size: 0.65rem;
            font-weight: 700;
            color: #64748b;
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }

        .status-value {
            font-size: 0.85rem;
            font-weight: 600;
            color: #1e293b;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        /* 4. Panel & Column Headers */
        .panel-header {
            text-transform: uppercase;
            letter-spacing: 0.1em;
            color: var(--primary);
            font-size: 0.8rem;
            font-weight: 800;
            margin-bottom: 12px;
            border-left: 4px solid var(--primary);
            padding-left: 10px;
        }
    </style>
    """, unsafe_allow_html=True)

def render_sidebar_header(title: str):
    st.sidebar.markdown(f'<div class="sidebar-header">{title}</div>', unsafe_allow_html=True)

def render_status_card(label: str, value: str, is_ready: bool):
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
    st.markdown(f'<div class="panel-header">{title}</div>', unsafe_allow_html=True)