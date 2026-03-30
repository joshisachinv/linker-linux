import streamlit as st
from components.styles import apply_custom_css, render_header, render_column_header, render_status_card
from components.sidebar import display_sidebar
from components.excel_view import display_excel_column
from components.pdf_view import display_pdf_column

st.set_page_config(
    page_title="Excel ↔ PDF Linker",
    page_icon="🔗",
    layout="wide",
)

apply_custom_css()
render_header("Excel ↔ PDF Linker")

# Session state
defaults = {
    "excel_file": None,
    "pdf_file": None,
    "excel_sig": None,
    "pdf_sig": None,
    "current_page": 0,
    "editor_event": None,
    "links": {},
    "pane_ratio": 45,  # Excel width %
    "sources_expanded": True,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# Logic to collapse if both files are present
if st.session_state.excel_file and st.session_state.pdf_file:
    st.session_state.sources_expanded = False
else:
    st.session_state.sources_expanded = True

def file_sig(uploaded):
    if uploaded is None:
        return None
    return (uploaded.name, uploaded.size)

uploaded_excel, uploaded_pdf = display_sidebar()

new_excel_sig = file_sig(uploaded_excel)
new_pdf_sig = file_sig(uploaded_pdf)

if new_excel_sig != st.session_state.excel_sig or new_pdf_sig != st.session_state.pdf_sig:
    st.session_state.excel_file = uploaded_excel
    st.session_state.pdf_file = uploaded_pdf
    st.session_state.excel_sig = new_excel_sig
    st.session_state.pdf_sig = new_pdf_sig
    st.rerun()

# Top toolbar
toolbar_left, toolbar_right = st.columns([3, 2])

st.markdown(
    """
    <style>
    div[data-testid="stHorizontalBlock"] {
        margin-top: -10px;
        margin-bottom: -10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

with toolbar_left:
    st.caption("Link spreadsheet cells to PDF regions.")

with toolbar_right:
    st.session_state.pane_ratio = st.slider(
        "Pane split",
        min_value=30,
        max_value=70,
        value=st.session_state.pane_ratio,
        step=5,
        key="pane_ratio_slider",
    )

left_ratio = st.session_state.pane_ratio
right_ratio = 100 - left_ratio

col1, col2 = st.columns([left_ratio, right_ratio], gap="small")

sheet_name = None
cell_event = None
current_page = st.session_state.current_page

with col1:
    render_column_header("Excel Workbench")
    if st.session_state.excel_file:
        sheet_name, cell_event = display_excel_column(st.session_state.excel_file)
        st.session_state["excel_editor"] = cell_event
    else:
        st.info("Upload an Excel file in the sidebar.")

with col2:
    render_column_header("PDF Evidence")
    render_status_card("PDF File", pdf_file.name if pdf_file else "Not Loaded", pdf_file is not None)
    if st.session_state.pdf_file:
        current_page, _ = display_pdf_column(st.session_state.pdf_file)
        st.session_state["current_page"] = current_page
    else:
        st.info("Upload a PDF file in the sidebar.")

# Initialize expander state if not present
if "sources_expanded" not in st.session_state:
    st.session_state.sources_expanded = True


if st.session_state.excel_file and st.session_state.pdf_file:
    display_page = (current_page + 1) if current_page is not None else 1
    display_sheet = sheet_name if sheet_name else "Unknown Sheet"
    st.caption(f"Ready to link: **{display_sheet}** ↔ **Page {display_page}**")
    