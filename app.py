import pandas as pd
import streamlit as st
from io import BytesIO

from components.excel_view import display_excel_column
from components.pdf_view import display_pdf_column
from components.sidebar import display_sidebar
from components.styles import apply_custom_css, render_column_header, render_header
from logic.actions import capture_link
from logic.excel_helpers import get_visible_sheets
from logic.file_sync import sync_files_to_state
from logic.initialization import initialize_session_state, update_expander_state


@st.cache_data
def load_visible_sheets(file_bytes: bytes):
    xl = pd.read_excel(BytesIO(file_bytes), sheet_name=None, header=None)
    return get_visible_sheets(xl)


def configure_app():
    st.set_page_config(page_title="Linker Pro", page_icon="🔗", layout="wide")
    apply_custom_css()


def render_toolbar():
    if st.session_state.get("full_screen_mode", False):
        return

    render_header("Excel ↔ PDF Linker")

    toolbar_cols = st.columns([2, 2.5, 1.6, 1.6, 1.5], gap="small")

    # ── Finalize Link Button ──────────────────────────────────────────────────
    with toolbar_cols[0]:
        if st.button("🔗 Finalize Link", type="primary", use_container_width=True):
            excel_editor = st.session_state.get("excel_editor")
            pdf_file     = st.session_state.get("pdf_file")
            current_page = st.session_state.get("current_page", 0)

            if excel_editor is None:
                st.warning("Select a cell before finalizing the link.")
            elif pdf_file is None:
                st.warning("Upload a PDF before finalizing the link.")
            else:
                try:
                    capture_link(excel_editor, current_page, pdf_file)
                    st.success("Link finalized successfully.")
                except Exception as e:
                    st.error(f"Failed to finalize link: {e}")

    # ── Sheet Selector ────────────────────────────────────────────────────────
    with toolbar_cols[1]:
        excel_file = st.session_state.get("excel_file")
        if excel_file is not None:
            try:
                display_sheets = load_visible_sheets(excel_file.getvalue())
                if display_sheets:
                    current_sheet = st.session_state.get("selected_sheet")
                    default_index = (
                        display_sheets.index(current_sheet)
                        if current_sheet in display_sheets
                        else 0
                    )
                    st.session_state.selected_sheet = st.selectbox(
                        "Sheet",
                        options=display_sheets,
                        index=default_index,
                        label_visibility="collapsed",
                        key="toolbar_sheet_selector",
                    )
                else:
                    st.warning("No visible sheets found.")
            except Exception as e:
                st.error(f"Failed to read sheets: {e}")
        else:
            st.markdown(
                "<div style='font-size:0.72rem;color:#94a3b8;"
                "padding:6px 0;'>No workbook loaded</div>",
                unsafe_allow_html=True,
            )

    # ── Page Number ───────────────────────────────────────────────────────────
    with toolbar_cols[2]:
        max_page     = max(1, st.session_state.get("pdf_page_count", 1))
        current_page = min(st.session_state.get("current_page", 0), max_page - 1)
        page_input   = st.number_input(
            "Page",
            min_value=1,
            max_value=max_page,
            value=current_page + 1,
            step=1,
            label_visibility="collapsed",
            help=f"PDF page (1 of {max_page})",
        )
        st.session_state.current_page = page_input - 1

    # ── Zoom Slider ───────────────────────────────────────────────────────────
    with toolbar_cols[3]:
        st.session_state.pdf_zoom = st.slider(
            "Zoom",
            min_value=1.0,
            max_value=4.0,
            value=float(st.session_state.get("pdf_zoom", 2.0)),
            step=0.25,
            label_visibility="collapsed",
            help="PDF zoom level",
        )

    # ── Split Slider ──────────────────────────────────────────────────────────
    with toolbar_cols[4]:
        st.session_state.pane_ratio = st.slider(
            "Split",
            min_value=30,
            max_value=70,
            value=int(st.session_state.get("pane_ratio", 50)),
            step=5,
            label_visibility="collapsed",
            help="Adjust the Excel / PDF panel split",
        )


def _render_toolbar_hints():
    """Render small contextual hints below the toolbar."""
    excel_editor = st.session_state.get("excel_editor")
    active_rect  = st.session_state.get("active_rect")

    cell_status = (
        f"<span style='color:#16a34a;'>✔ Cell selected</span>"
        if excel_editor
        else "<span style='color:#94a3b8;'>○ No cell selected</span>"
    )
    rect_status = (
        f"<span style='color:#16a34a;'>✔ Area drawn</span>"
        if active_rect
        else "<span style='color:#94a3b8;'>○ No area drawn</span>"
    )
    link_count = len(st.session_state.get("links", {}))
    link_badge = (
        f"<span style='background:#2563eb;color:white;padding:1px 7px;"
        f"border-radius:10px;font-size:0.65rem;font-weight:700;'>{link_count} link{'s' if link_count != 1 else ''}</span>"
        if link_count > 0
        else "<span style='color:#cbd5e1;font-size:0.68rem;'>0 links</span>"
    )

    st.markdown(f"""
        <div style="
            display: flex;
            gap: 20px;
            align-items: center;
            padding: 3px 4px 8px;
            font-size: 0.68rem;
            font-weight: 500;
            color: #64748b;
        ">
            {cell_status} &nbsp;·&nbsp; {rect_status} &nbsp;·&nbsp; {link_badge}
        </div>
    """, unsafe_allow_html=True)


def render_main_view():
    excel_ratio = st.session_state.get("pane_ratio", 50)
    pdf_ratio   = 100 - excel_ratio

    left_col, right_col = st.columns([excel_ratio, pdf_ratio], gap="small")

    # ── Excel Panel ───────────────────────────────────────────────────────────
    with left_col:
        excel_file = st.session_state.get("excel_file")

        render_column_header(
            "📊 Excel",
            subtitle=excel_file.name if excel_file else "",
        )

        if excel_file is not None:
            try:
                sheet_name, cell_event = display_excel_column(excel_file)
                if sheet_name:
                    st.session_state.selected_sheet = sheet_name
                st.session_state.excel_editor = cell_event
            except Exception as e:
                st.error(f"Failed to load Excel view: {e}")
                import traceback
                st.text(traceback.format_exc())
        else:
            st.info("Upload an Excel file in the sidebar to begin.")

    # ── PDF Panel ─────────────────────────────────────────────────────────────
    with right_col:
        pdf_file     = st.session_state.get("pdf_file")
        current_page = st.session_state.get("current_page", 0)
        page_count   = st.session_state.get("pdf_page_count", 1)

        render_column_header(
            "📄 PDF",
            subtitle=f"Page {current_page + 1} of {page_count}" if pdf_file else "",
        )

        if pdf_file is not None:
            try:
                current_page = st.session_state.get("current_page", 0)
                pdf_zoom = st.session_state.get("pdf_zoom", 2.0)
                display_pdf_column(pdf_file, current_page, pdf_zoom)
            except Exception as e:
                st.error(f"Failed to load PDF view: {e}")
                import traceback
                st.text(traceback.format_exc())
        else:
            st.info("Upload a PDF file in the sidebar to begin.")


def main():
    configure_app()
    initialize_session_state()

    uploaded_excel, uploaded_pdf = display_sidebar()
    sync_files_to_state(uploaded_excel, uploaded_pdf)
    update_expander_state()

    render_toolbar()
    _render_toolbar_hints()
    render_main_view()


if __name__ == "__main__":
    main()