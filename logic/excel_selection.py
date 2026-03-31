import pandas as pd
import streamlit as st
from logic.excel_helpers import ROW_COL_NAME

def build_selected_cell_from_row_and_column(df, sheet_name: str, selected_row):
    if selected_row is None:
        return None

    # Normalizing selected_row
    if isinstance(selected_row, pd.DataFrame):
        if selected_row.empty:
            return None
        selected_row = selected_row.iloc[0].to_dict()

    if isinstance(selected_row, pd.Series):
        selected_row = selected_row.to_dict()

    if not isinstance(selected_row, dict):
        st.warning(f"Unexpected row selection type: {type(selected_row).__name__}")
        return None

    # Resolve row index
    row_number_1_based = selected_row.get(ROW_COL_NAME, 1)
    try:
        row_index = max(0, int(row_number_1_based) - 1)
    except Exception:
        st.warning(f"Could not parse selected row: {row_number_1_based}")
        return None

    # --- Persistent State Logic ---
    column_state_key = f"persistent_col_{sheet_name}"
    all_columns = list(df.columns)

    # 1. Initialize session state if it's the first run
    if column_state_key not in st.session_state:
        st.session_state[column_state_key] = all_columns[0]

    # 2. Determine the correct index to show in the dropdown
    # This prevents it from defaulting to 0 (Column A) on every refresh
    try:
        current_selection_index = all_columns.index(st.session_state[column_state_key])
    except ValueError:
        current_selection_index = 0

    left, right = st.columns([1, 2])
    
    with left:
        selected_column = st.selectbox(
            "Column",
            options=all_columns,
            index=current_selection_index, # Critical: Force dropdown to the saved column
            key=f"selected_column_widget_{sheet_name}",
        )

    # 3. Update the persistent state immediately after user interaction
    st.session_state[column_state_key] = selected_column

    # Resolve cell coordinates
    try:
        column_index = all_columns.index(selected_column)
        cell_value = df.iloc[row_index, column_index]
    except Exception as exc:
        st.warning(f"Could not resolve selected cell: {type(exc).__name__}: {exc}")
        return None

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