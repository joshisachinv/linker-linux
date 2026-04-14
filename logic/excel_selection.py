import streamlit as st
from logic.excel_helpers import ROW_COL_NAME


def build_selected_cell_from_click(df, sheet_name: str, cell_clicked):
    if not cell_clicked:
        return None

    row_index = cell_clicked.get("rowIndex")
    column_name = cell_clicked.get("columnId")

    if not column_name or row_index is None:
        return None

    if column_name == ROW_COL_NAME:
        return None

    try:
        cols = list(df.columns)
        if column_name not in cols:
            st.warning(f"Column '{column_name}' not found. Available: {', '.join(cols)}")
            return None
        column_index = cols.index(column_name)
        cell_value = df.iloc[row_index, column_index]
    except Exception:
        return None

    cell_ref = f"{column_name}{row_index + 1}"
    st.success(f"**Selected Cell:** {cell_ref} | **Value:** {cell_value}")

    return {
        "sheet_name": sheet_name,
        "row_index": int(row_index),
        "column_index": int(column_index),
        "column_name": column_name,
        "cell_value": cell_value,
        "cell_ref": cell_ref,
    }