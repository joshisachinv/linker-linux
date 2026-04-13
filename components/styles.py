import streamlit as st


def apply_custom_css():
    """
    Refined Professional Theme — 'Blueprint'
    Clean workstation aesthetic with precise grid lines, strong typographic hierarchy,
    and purposeful color usage. Built for long sessions and data-dense workflows.
    """
    st.markdown("""
    <style>
        /* ─── FONTS ─────────────────────────────────────────────────────────────── */
        @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Mono:wght@400;600&family=IBM+Plex+Sans:wght@300;400;500;600;700&display=swap');

        * {
            font-family: 'IBM Plex Sans', sans-serif !important;
        }

        code, .mono {
            font-family: 'IBM Plex Mono', monospace !important;
        }

        /* ─── CSS VARIABLES ──────────────────────────────────────────────────────── */
        :root {
            --blue-900: #0f2d6e;
            --blue-700: #1a4fad;
            --blue-500: #2563eb;
            --blue-300: #93c5fd;
            --blue-100: #dbeafe;
            --blue-50:  #eff6ff;

            --ink-900: #0c1120;
            --ink-700: #1e293b;
            --ink-500: #475569;
            --ink-300: #94a3b8;
            --ink-100: #e2e8f0;
            --ink-50:  #f8fafc;

            --green-500: #16a34a;
            --green-100: #dcfce7;
            --red-500:   #dc2626;
            --red-100:   #fee2e2;
            --amber-500: #d97706;
            --amber-100: #fef3c7;

            --surface:        #ffffff;
            --surface-raised: #f8fafc;
            --border:         #e2e8f0;
            --border-strong:  #cbd5e1;

            --shadow-sm: 0 1px 3px rgba(15,45,110,0.08), 0 1px 2px rgba(15,45,110,0.04);
            --shadow-md: 0 4px 12px rgba(15,45,110,0.10), 0 2px 4px rgba(15,45,110,0.06);
            --shadow-lg: 0 8px 24px rgba(15,45,110,0.12), 0 4px 8px rgba(15,45,110,0.08);

            --radius-sm: 4px;
            --radius-md: 8px;
            --radius-lg: 12px;
        }

        /* ─── PAGE & LAYOUT ──────────────────────────────────────────────────────── */
        .stApp {
            background-color: #f0f4f8 !important;
            background-image:
                linear-gradient(rgba(37,99,235,0.03) 1px, transparent 1px),
                linear-gradient(90deg, rgba(37,99,235,0.03) 1px, transparent 1px);
            background-size: 24px 24px;
        }

        .block-container {
            padding: 1rem 1.25rem 0.5rem !important;
            max-width: 100% !important;
        }

        [data-testid="stVerticalBlock"] {
            gap: 0.15rem !important;
        }

        .element-container {
            margin-top: 0.15rem !important;
            margin-bottom: 0.15rem !important;
        }

        [data-testid="stHeader"] {
            display: none !important;
        }

        /* ─── TOOLBAR STRIP ───────────────────────────────────────────────────────── */
        div[data-testid="stHorizontalBlock"]:has(button) {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            padding: 6px 14px !important;
            margin-bottom: 10px !important;
            box-shadow: var(--shadow-sm);
            align-items: center;
            gap: 8px;
        }

        /* Hide widget labels inside toolbar only */
        div[data-testid="stHorizontalBlock"]:has(button) label {
            display: none !important;
        }

        /* ─── BUTTONS ─────────────────────────────────────────────────────────────── */
        button {
            height: 30px !important;
            min-height: 30px !important;
            padding: 0 14px !important;
            line-height: 30px !important;
            font-size: 0.78rem !important;
            font-weight: 600 !important;
            letter-spacing: 0.02em !important;
            border-radius: var(--radius-sm) !important;
            transition: all 0.15s ease !important;
        }

        button[kind="primary"] {
            background: linear-gradient(135deg, var(--blue-700), var(--blue-500)) !important;
            border: none !important;
            box-shadow: 0 2px 6px rgba(37,99,235,0.35) !important;
        }

        button[kind="primary"]:hover {
            background: linear-gradient(135deg, var(--blue-900), var(--blue-700)) !important;
            box-shadow: 0 4px 12px rgba(37,99,235,0.4) !important;
            transform: translateY(-1px) !important;
        }

        button[kind="secondary"] {
            background: var(--surface) !important;
            border: 1px solid var(--border-strong) !important;
            color: var(--ink-700) !important;
        }

        button[kind="secondary"]:hover {
            background: var(--blue-50) !important;
            border-color: var(--blue-300) !important;
            color: var(--blue-700) !important;
        }

        /* ─── INPUTS & SELECTS ────────────────────────────────────────────────────── */
        .stNumberInput input,
        .stSelectbox div[data-baseweb="select"] > div,
        .stTextInput input {
            height: 30px !important;
            font-size: 0.8rem !important;
            border-color: var(--border-strong) !important;
            border-radius: var(--radius-sm) !important;
            background: var(--surface) !important;
            color: var(--ink-700) !important;
        }

        .stNumberInput input:focus,
        .stTextInput input:focus {
            border-color: var(--blue-500) !important;
            box-shadow: 0 0 0 3px rgba(37,99,235,0.12) !important;
        }

        /* Slider */
        [data-testid="stSlider"] [data-baseweb="slider"] [role="slider"] {
            background-color: var(--blue-500) !important;
            border: 2px solid white !important;
            box-shadow: 0 1px 4px rgba(37,99,235,0.4) !important;
        }

        [data-testid="stSlider"] [data-baseweb="slider"] div[data-testid="stThumbValue"] {
            color: var(--blue-700) !important;
            font-size: 0.7rem !important;
            font-weight: 600 !important;
        }

        /* ─── SIDEBAR ─────────────────────────────────────────────────────────────── */
        [data-testid="stSidebar"] {
            background: var(--surface) !important;
            border-right: 1px solid var(--border) !important;
            box-shadow: var(--shadow-md) !important;
        }

        [data-testid="stSidebar"] > div {
            padding: 0.75rem 0.85rem !important;
        }

        /* Sidebar section titles */
        [data-testid="stSidebar"] h3 {
            font-size: 0.65rem !important;
            font-weight: 700 !important;
            letter-spacing: 0.1em !important;
            text-transform: uppercase !important;
            color: var(--ink-300) !important;
            margin: 0.6rem 0 0.3rem !important;
        }

        /* Sidebar dividers */
        [data-testid="stSidebar"] hr {
            border-color: var(--border) !important;
            margin: 0.5rem 0 !important;
        }

        /* Expander */
        [data-testid="stExpander"] {
            border: 1px solid var(--border) !important;
            border-radius: var(--radius-md) !important;
            background: var(--surface-raised) !important;
            margin-bottom: 4px !important;
        }

        [data-testid="stExpander"] summary {
            font-size: 0.78rem !important;
            font-weight: 600 !important;
            color: var(--ink-700) !important;
            padding: 6px 10px !important;
        }

        [data-testid="stExpander"] summary:hover {
            background: var(--blue-50) !important;
            color: var(--blue-700) !important;
        }

        /* File Uploader */
        [data-testid="stFileUploader"] {
            background: var(--surface-raised) !important;
            border: 1.5px dashed var(--border-strong) !important;
            border-radius: var(--radius-md) !important;
            transition: border-color 0.2s ease !important;
        }

        [data-testid="stFileUploader"]:hover {
            border-color: var(--blue-300) !important;
            background: var(--blue-50) !important;
        }

        [data-testid="stFileUploader"] section {
            padding: 8px 10px !important;
        }

        [data-testid="stFileUploader"] label {
            font-size: 0.72rem !important;
            color: var(--ink-500) !important;
        }

        /* Toggle */
        [data-testid="stToggle"] label {
            font-size: 0.78rem !important;
            color: var(--ink-700) !important;
        }

        /* Checkbox */
        [data-testid="stCheckbox"] label {
            font-size: 0.78rem !important;
            color: var(--ink-700) !important;
        }

        /* ─── ALERT / STATUS MESSAGES ─────────────────────────────────────────────── */
        div.stAlert {
            border-radius: var(--radius-md) !important;
            border: 1px solid transparent !important;
            padding: 0.4rem 0.85rem !important;
            font-size: 0.78rem !important;
            font-weight: 500 !important;
        }

        div.stAlert[data-baseweb="notification"][kind="info"] {
            background: var(--blue-50) !important;
            border-color: var(--blue-100) !important;
            color: var(--blue-700) !important;
        }

        div.stAlert[data-baseweb="notification"][kind="success"] {
            background: var(--green-100) !important;
            border-color: #bbf7d0 !important;
            color: var(--green-500) !important;
        }

        div.stAlert[data-baseweb="notification"][kind="error"] {
            background: var(--red-100) !important;
            border-color: #fecaca !important;
            color: var(--red-500) !important;
        }

        div.stAlert[data-baseweb="notification"][kind="warning"] {
            background: var(--amber-100) !important;
            border-color: #fde68a !important;
            color: var(--amber-500) !important;
        }

        /* ─── AGGRID (EXCEL GRID) ─────────────────────────────────────────────────── */
        .ag-theme-alpine {
            --ag-font-family: 'IBM Plex Sans', sans-serif !important;
            --ag-font-size: 12px !important;
            --ag-grid-size: 3px !important;
            --ag-row-height: 26px !important;
            --ag-header-height: 30px !important;
            --ag-header-background-color: #f1f5f9 !important;
            --ag-header-foreground-color: #475569 !important;
            --ag-border-color: #e2e8f0 !important;
            --ag-row-hover-color: #eff6ff !important;
            --ag-selected-row-background-color: #dbeafe !important;
            --ag-odd-row-background-color: #fafbfc !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius-md) !important;
            box-shadow: var(--shadow-sm) !important;
        }

        .ag-header-cell {
            border-right: 1px solid var(--border) !important;
        }

        .ag-header-cell-label {
            justify-content: center !important;
            font-weight: 600 !important;
            font-size: 0.72rem !important;
            letter-spacing: 0.03em !important;
        }

        .ag-cell {
            border-right: 1px solid var(--border) !important;
            font-size: 0.77rem !important;
        }

        /* ─── COLUMN PANELS ───────────────────────────────────────────────────────── */
        .panel-wrapper {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            padding: 10px 12px;
            box-shadow: var(--shadow-sm);
            height: 100%;
        }

        /* ─── SCROLLBAR ───────────────────────────────────────────────────────────── */
        ::-webkit-scrollbar {
            width: 5px;
            height: 5px;
        }

        ::-webkit-scrollbar-track {
            background: var(--ink-50);
        }

        ::-webkit-scrollbar-thumb {
            background: var(--ink-100);
            border-radius: 10px;
        }

        ::-webkit-scrollbar-thumb:hover {
            background: var(--blue-300);
        }

    </style>
    """, unsafe_allow_html=True)


def render_sidebar_header(title: str):
    st.sidebar.markdown(f"""
        <div style="
            padding: 10px 2px 6px;
            margin-bottom: 4px;
        ">
            <div style="
                font-family: 'IBM Plex Mono', monospace;
                font-size: 1.1rem;
                font-weight: 600;
                color: #0f2d6e;
                letter-spacing: -0.02em;
                display: flex;
                align-items: center;
                gap: 8px;
            ">
                <span style="
                    display: inline-flex;
                    align-items: center;
                    justify-content: center;
                    width: 26px;
                    height: 26px;
                    background: linear-gradient(135deg, #1a4fad, #2563eb);
                    border-radius: 6px;
                    color: white;
                    font-size: 0.8rem;
                ">🔗</span>
                {title}
            </div>
            <div style="
                font-size: 0.62rem;
                color: #94a3b8;
                font-weight: 500;
                letter-spacing: 0.06em;
                text-transform: uppercase;
                margin-top: 3px;
                padding-left: 34px;
            ">Evidence Linking System</div>
        </div>
    """, unsafe_allow_html=True)


def render_status_card(label: str, value: str, is_ready: bool):
    dot_color = "#16a34a" if is_ready else "#94a3b8"
    bg_color  = "#f0fdf4" if is_ready else "#f8fafc"
    border    = "#bbf7d0" if is_ready else "#e2e8f0"
    text      = "#166534" if is_ready else "#64748b"

    st.sidebar.markdown(f"""
        <div style="
            background: {bg_color};
            border: 1px solid {border};
            border-radius: 6px;
            padding: 6px 10px;
            margin-bottom: 5px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 8px;
        ">
            <div>
                <div style="font-size:0.58rem; font-weight:700; color:#94a3b8;
                            text-transform:uppercase; letter-spacing:0.07em;">
                    {label}
                </div>
                <div style="font-size:0.73rem; font-weight:600; color:{text};
                            margin-top:1px; white-space:nowrap; overflow:hidden;
                            text-overflow:ellipsis; max-width:160px;">
                    {value}
                </div>
            </div>
            <div style="
                width: 8px; height: 8px; border-radius: 50%;
                background: {dot_color};
                flex-shrink: 0;
                box-shadow: 0 0 0 3px {border};
            "></div>
        </div>
    """, unsafe_allow_html=True)


def render_column_header(title: str, subtitle: str = ""):
    st.markdown(f"""
        <div style="
            display: flex;
            align-items: center;
            gap: 8px;
            padding: 6px 2px 8px;
            border-bottom: 2px solid #dbeafe;
            margin-bottom: 8px;
        ">
            <div style="
                font-size: 0.72rem;
                font-weight: 700;
                color: #1a4fad;
                text-transform: uppercase;
                letter-spacing: 0.08em;
            ">{title}</div>
            {"<div style='font-size:0.65rem;color:#94a3b8;margin-left:auto;'>" + subtitle + "</div>" if subtitle else ""}
        </div>
    """, unsafe_allow_html=True)


def render_header(title: str):
    st.markdown(f"""
        <div style="
            display: flex;
            align-items: center;
            gap: 10px;
            padding: 4px 0 2px;
        ">
            <div style="
                font-family: 'IBM Plex Mono', monospace;
                font-size: 0.78rem;
                font-weight: 600;
                color: #475569;
                letter-spacing: 0.04em;
            ">{title}</div>
            <div style="
                height: 1px;
                flex: 1;
                background: linear-gradient(90deg, #e2e8f0, transparent);
            "></div>
        </div>
    """, unsafe_allow_html=True)


def apply_excel_ui_style():
    st.markdown("""
        <style>
        .ag-theme-alpine {
            border: 1px solid #e2e8f0 !important;
            border-radius: 8px !important;
            overflow: hidden !important;
        }

        .ag-header {
            background: linear-gradient(180deg, #f8fafc, #f1f5f9) !important;
            border-bottom: 2px solid #e2e8f0 !important;
        }

        .ag-header-cell-label {
            justify-content: center !important;
            font-weight: 700 !important;
            font-size: 0.7rem !important;
            color: #475569 !important;
            letter-spacing: 0.04em !important;
            text-transform: uppercase !important;
        }

        .ag-row-even { background-color: #ffffff !important; }
        .ag-row-odd  { background-color: #fafbfc !important; }

        .ag-row-selected {
            background-color: #dbeafe !important;
            border-left: 3px solid #2563eb !important;
        }

        .ag-cell-focus {
            border: 1px solid #93c5fd !important;
            box-shadow: inset 0 0 0 1px #93c5fd !important;
        }
        </style>
    """, unsafe_allow_html=True)