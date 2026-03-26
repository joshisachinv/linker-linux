import pandas as pd
import streamlit as st

from logic.links_store import try_load_embedded_links
from logic.excel_helpers import get_visible_sheets, prepare_display_dataframe
from logic.excel_grid import render_excel_grid
from logic.excel_selection import build_selected_cell_from_row_and_column


def display_excel_column(uploaded_file):
    if uploaded_file is None:
        return None, None

    try:
        if hasattr(uploaded_file, "seek"):
            uploaded_file.seek(0)
        excel_data = pd.read_excel(uploaded_file, sheet_name=None, header=None)

        try:
            if hasattr(uploaded_file, "seek"):
                uploaded_file.seek(0)
            st.session_state["embedded_links"] = try_load_embedded_links(uploaded_file)
        except Exception:
            st.session_state["embedded_links"] = {}

        display_sheets = get_visible_sheets(excel_data)

        if not display_sheets:
            st.warning("No visible sheets found in this workbook.")
            return None, None

        selected_sheet = st.selectbox(
            "Select Sheet",
            options=display_sheets,
            key="selected_excel_sheet",
        )

        df = prepare_display_dataframe(excel_data[selected_sheet])
        selected_row = render_excel_grid(df, selected_sheet)
        selected_cell = build_selected_cell_from_row_and_column(df, selected_sheet, selected_row)

        return selected_sheet, selected_cell

    except Exception as exc:
        st.error(f"Failed to read Excel file: {exc}")
        return None, None