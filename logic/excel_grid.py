import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

from logic.excel_helpers import add_row_numbers, ROW_COL_NAME


GRID_HEIGHT = 420


def _build_grid_options(df_display):
    gb = GridOptionsBuilder.from_dataframe(df_display)

    gb.configure_default_column(
        editable=False,
        resizable=True,
        sortable=True,
        filter=True,
        wrapText=False,
        width=100, 
        minWidth=50,
    )

    gb.configure_column(
        ROW_COL_NAME,
        header_name="",
        pinned="left",
        width=50,
        editable=False,
        cellStyle={'backgroundColor': '#f8f9fa', 'fontWeight': 'bold'}
    )

    gb.configure_grid_options(
        suppressRowClickSelection=False,
        rowSelection="single",
        domLayout='normal',
    )

    return gb.build()


def _normalize_selected_row(selected_rows):
    if selected_rows is None:
        return None

    if isinstance(selected_rows, pd.DataFrame):
        if selected_rows.empty:
            return None
        return selected_rows.iloc[0].to_dict()

    if isinstance(selected_rows, pd.Series):
        return selected_rows.to_dict()

    if isinstance(selected_rows, list):
        if len(selected_rows) == 0:
            return None
        first = selected_rows[0]
        if isinstance(first, pd.Series):
            return first.to_dict()
        return first

    if isinstance(selected_rows, dict):
        return selected_rows

    return None


def render_excel_grid(df, selected_sheet: str):
    df_display = add_row_numbers(df)

    grid_response = AgGrid(
        df_display,
        gridOptions=_build_grid_options(df_display),
        key=f"excel_grid_{selected_sheet}",
        height=GRID_HEIGHT,
        width="100%",
        fit_columns_on_grid_load=False,
        allow_unsafe_jscode=False,
        enable_enterprise_modules=False,
        update_mode=GridUpdateMode.VALUE_CHANGED | GridUpdateMode.SELECTION_CHANGED, 
        reload_data=False,
        theme="alpine",
    )

    cell_clicked = grid_response.get("cell_clicked")
    
    if not cell_clicked:
        st.info("Click any cell in the grid to select it.")
        return None

    return cell_clicked 