import streamlit as st


def apply_custom_css():
    st.markdown("""
    <style>
        :root {
            --app-header-h: 48px;
            --panel-radius: 16px;
            --panel-border: 1px solid rgba(49, 51, 63, 0.18);
            --panel-bg: rgba(255, 255, 255, 0.72);
            --panel-shadow: 0 2px 10px rgba(0, 0, 0, 0.04);
        }

        .stAppViewContainer .main .block-container {
            padding-top: calc(var(--app-header-h) + 1rem);
            padding-bottom: 1rem;
            max-width: 100%;
        }

        .app-header {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: var(--app-header-h);
            display: flex;
            align-items: center;
            padding: 0 1rem;
            background: rgba(255, 255, 255, 0.88);
            backdrop-filter: blur(10px);
            border-bottom: 1px solid rgba(49, 51, 63, 0.12);
            z-index: 9999;
            font-size: 0.95rem;
            font-weight: 700;
            letter-spacing: 0.01em;
        }

        section[data-testid="stSidebar"] {
            border-right: 1px solid rgba(49, 51, 63, 0.10);
        }

        section[data-testid="stSidebar"] > div {
            padding-top: calc(var(--app-header-h) + 0.5rem);
        }

        .panel {
            background: var(--panel-bg);
            border: var(--panel-border);
            border-radius: var(--panel-radius);
            box-shadow: var(--panel-shadow);
            padding: 0.75rem 0.9rem 0.9rem 0.9rem;
            min-height: 70vh;
        }

        .panel-title {
            font-size: 0.76rem;
            font-weight: 700;
            letter-spacing: 0.08em;
            text-transform: uppercase;
            color: #3b82f6;
            margin-bottom: 0.5rem;
        }

        .toolbar-caption {
            color: rgba(49, 51, 63, 0.75);
            font-size: 0.9rem;
        }

        /* Make dataframe / grid area feel denser */
        .stDataFrame, .stTable {
            border-radius: 12px;
            overflow: hidden;
        }
    </style>
    """, unsafe_allow_html=True)


def render_header(title: str):
    st.markdown(f'<div class="app-header">{title}</div>', unsafe_allow_html=True)


def render_panel_start(title: str):
    st.markdown(f'<div class="panel"><div class="panel-title">{title}</div>', unsafe_allow_html=True)


def render_panel_end():
    st.markdown('</div>', unsafe_allow_html=True)

def render_sidebar_section(title):
    st.markdown(
        f"""
        <div style="
            font-size: 0.78rem;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.04em;
            margin-top: 0.25rem;
            margin-bottom: 0.35rem;
            color: #3b82f6;
        ">{title}</div>
        """,
        unsafe_allow_html=True,
    )