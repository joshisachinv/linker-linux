import pandas as pd
import streamlit as st
from logic.excel_helpers import ROW_COL_NAME

def build_selected_cell_from_click(df, sheet_name: str, cell_clicked):
    if not cell_clicked:
        return None

    # AgGrid click events provide 0-based indices and the column ID
    row_index = cell_clicked.get("rowIndex")
    column_name = cell_clicked.get("columnId")

    if column_name == ROW_COL_NAME or row_index is None:
        return None

    try:
        cell_value = df.iloc[row_index, list(df.columns).index(column_name)]
        column_index = list(df.columns).index(column_name)
    except Exception:
        return None

    cell_ref = f"{column_name}{row_index + 1}"

    # Displaying the result as a clean, high-density success bar
    st.success(f"**Selected Cell:** {cell_ref} | **Value:** {cell_value}")

    return {
        "sheet_name": sheet_name,
        "row_index": int(row_index),
        "column_index": int(column_index),
        "column_name": column_name,
        "cell_value": cell_value,
        "cell_ref": cell_ref,
    }