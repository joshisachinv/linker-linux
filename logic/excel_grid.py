import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode

from logic.excel_helpers import add_row_numbers, ROW_COL_NAME


GRID_HEIGHT = 420


def _build_grid_options(df_display):
    gb = GridOptionsBuilder.from_dataframe(df_display)

    gb.configure_default_column(
        editable=False,
        resizable=True,
        sortable=False,
        filter=False,
        wrapText=False,
    )

    gb.configure_column(
        ROW_COL_NAME,
        header_name="",
        pinned="left",
        width=42,
        editable=False,
    )

    gb.configure_grid_options(
        suppressRowClickSelection=False,
        rowSelection="single",
    )

    return gb.build()


def render_excel_grid(df, selected_sheet: str):
    """
    Render the Excel-like grid and return the selected row object, if any.
    """
    df_display = add_row_numbers(df)

    st.caption("Select a row, then choose a column below.")

    grid_response = AgGrid(
        df_display,
        gridOptions=_build_grid_options(df_display),
        key=f"excel_grid_{selected_sheet}",
        height=GRID_HEIGHT,
        width="100%",
        fit_columns_on_grid_load=False,
        allow_unsafe_jscode=False,
        enable_enterprise_modules=False,
        update_mode=GridUpdateMode.SELECTION_CHANGED,
        reload_data=False,
        theme="streamlit",
    )

    selected_rows = grid_response.get("selected_rows", []) if grid_response else []

    if len(selected_rows) == 0:
        st.info("Select a row in the grid to choose a cell.")
        return None

    return selected_rows[0]