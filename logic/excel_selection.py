import pandas as pd
import streamlit as st

from logic.excel_helpers import ROW_COL_NAME


def build_selected_cell_from_row_and_column(df, sheet_name: str, selected_row):
    """
    Excel-like fallback selector:
    - user selects a row in the grid
    - user chooses a column below
    - returns an exact cell payload
    """
    if selected_row is None:
        return None

    # AgGrid can sometimes return a one-row DataFrame instead of a dict
    if isinstance(selected_row, pd.DataFrame):
        if selected_row.empty:
            return None
        selected_row = selected_row.iloc[0].to_dict()

    if isinstance(selected_row, pd.Series):
        selected_row = selected_row.to_dict()

    if not isinstance(selected_row, dict):
        return None

    row_number_1_based = selected_row.get(ROW_COL_NAME, 1)
    row_index = max(0, int(row_number_1_based) - 1)

    left, right = st.columns([1, 2])

    with left:
        selected_column = st.selectbox(
            "Column",
            options=list(df.columns),
            key=f"selected_column_{sheet_name}",
        )

    column_index = list(df.columns).index(selected_column)
    cell_value = df.iloc[row_index, column_index]
    cell_ref = f"{selected_column}{row_index + 1}"

    with right:
        st.text_input(
            "Cell value",
            value=str(cell_value),
            disabled=True,
            key=f"selected_cell_value_{sheet_name}",
        )

    selected_cell = {
        "sheet_name": sheet_name,
        "row_index": int(row_index),
        "column_index": int(column_index),
        "column_name": selected_column,
        "cell_value": cell_value,
        "cell_ref": cell_ref,
    }

    st.success(
        f"Selected cell: {selected_cell['cell_ref']} "
        f"(value: {selected_cell['cell_value']})"
    )

    return selected_cell