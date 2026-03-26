import pandas as pd
import streamlit as st
from st_aggrid import AgGrid, GridOptionsBuilder, GridUpdateMode, JsCode
from logic.links_store import try_load_embedded_links


def excel_col_name(col_idx: int) -> str:
    """Convert zero-based column index to Excel-style column letters."""
    result = ""
    col_idx += 1
    while col_idx > 0:
        col_idx, remainder = divmod(col_idx - 1, 26)
        result = chr(65 + remainder) + result
    return result


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
            embedded_links = try_load_embedded_links(uploaded_file)
            st.session_state["embedded_links"] = embedded_links
        except Exception:
            st.session_state["embedded_links"] = {}

        display_sheets = [sheet for sheet in excel_data.keys() if sheet != "__PDF_LINKS__"]

        if not display_sheets:
            st.warning("No visible sheets found in this workbook.")
            return None, None

        selected_sheet = st.selectbox(
            "Select Sheet",
            options=display_sheets,
            key="selected_excel_sheet",
        )

        df_raw = excel_data[selected_sheet]
        df_raw = df_raw.where(df_raw.notna(), "")
        df = df_raw.astype(str)

        df.columns = [excel_col_name(i) for i in range(len(df.columns))]

        df_display = df.copy()
        df_display.insert(0, "__row__", range(1, len(df_display) + 1))

        gb = GridOptionsBuilder.from_dataframe(df_display)

        gb.configure_default_column(
            editable=False,
            resizable=True,
            sortable=False,
            filter=False,
            wrapText=False,
        )

        gb.configure_column(
            "__row__",
            header_name="Row",
            pinned="left",
            width=70,
            editable=False,
        )

        gb.configure_grid_options(
            suppressRowClickSelection=False,
            rowSelection="single",
        )

        grid_options = gb.build()

        st.caption("Select a row, then choose the target column below.")

        grid_response = AgGrid(
            df_display,
            gridOptions=grid_options,
            key=f"excel_grid_{selected_sheet}",
            height=420,
            width="100%",
            fit_columns_on_grid_load=False,
            allow_unsafe_jscode=True,
            enable_enterprise_modules=False,
            update_mode=GridUpdateMode.SELECTION_CHANGED,
            reload_data=False,
            theme="streamlit",
        )

        selected_rows = grid_response.get("selected_rows", []) if grid_response else []
        selected_cell = None

        if len(selected_rows) > 0:
            selected_row = selected_rows[0]

            # Row number may come back as "__row__"
            row_number_1_based = selected_row.get("__row__", 1)
            row_index = int(row_number_1_based) - 1

            col_pick_left, col_pick_right = st.columns([1, 2])

            with col_pick_left:
                selected_column = st.selectbox(
                    "Column",
                    options=list(df.columns),
                    key=f"selected_column_{selected_sheet}",
                )

            with col_pick_right:
                cell_value = df.iloc[row_index, list(df.columns).index(selected_column)]
                st.text_input(
                    "Cell value",
                    value=str(cell_value),
                    disabled=True,
                    key=f"selected_cell_value_{selected_sheet}",
                )

            column_index = list(df.columns).index(selected_column)
            cell_ref = f"{selected_column}{row_index + 1}"

            selected_cell = {
                "sheet_name": selected_sheet,
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
        else:
            st.info("Select a row in the grid to choose a cell.")

        return selected_sheet, selected_cell

    except Exception as exc:
        st.error(f"Failed to read Excel file: {exc}")
        return None, None