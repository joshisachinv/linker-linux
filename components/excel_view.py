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
    from components.styles import render_column_label

    render_column_label("Excel Viewer")

    if uploaded_file is None:
        return None, None

    try:
        # Read workbook
        excel_data = pd.read_excel(uploaded_file, sheet_name=None, header=None)

        # Optional: load saved links metadata if your helper uses it
        try:
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

        df_raw = excel_data[selected_sheet].fillna("")

        # Create Excel-like headers: A, B, C...
        df = df_raw.copy()
        df.columns = [excel_col_name(i) for i in range(len(df.columns))]

        # Add a visible row number column
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
            width=90,
            editable=False,
        )

        # Enable single-cell selection with JS
        gb.configure_grid_options(
            suppressRowClickSelection=False,
            rowSelection="single",
            enableRangeSelection=True,
        )

        # Highlight selected cell
        cellstyle_jscode = JsCode(
            """
            function(params) {
                const selected = params.api.getCellRanges();
                if (!selected || selected.length === 0) {
                    return {};
                }

                const range = selected[0];
                const startRow = Math.min(range.startRow.rowIndex, range.endRow.rowIndex);
                const endRow = Math.max(range.startRow.rowIndex, range.endRow.rowIndex);

                let cols = range.columns.map(col => col.getColId());

                if (
                    params.rowIndex >= startRow &&
                    params.rowIndex <= endRow &&
                    cols.includes(params.colDef.field)
                ) {
                    return {
                        backgroundColor: "#DCEBFF",
                        border: "2px solid #4A90E2"
                    };
                }

                return {};
            }
            """
        )

        for col in df_display.columns:
            gb.configure_column(col, cellStyle=cellstyle_jscode)

        grid_options = gb.build()

        st.caption("Click a cell to select it for linking.")

        grid_response = AgGrid(
            df_display,
            gridOptions=grid_options,
            key=f"excel_grid_{selected_sheet}",
            height=800,
            width="100%",
            fit_columns_on_grid_load=False,
            allow_unsafe_jscode=True,
            enable_enterprise_modules=False,
            update_mode=GridUpdateMode.SELECTION_CHANGED,
            reload_data=False,
            theme="streamlit",
        )

        selected_rows = grid_response.get("selected_rows", [])

        # Try to get selected cell using range selection info from AgGrid response
        selected_cell = None
        selected_ranges = grid_response.get("grid_state", {}).get("cellSelection", [])

        if selected_ranges:
            first_range = selected_ranges[0]
            row_index = first_range.get("startRow", 0)

            columns = first_range.get("columns", [])
            if columns:
                column_name = columns[0]

                if column_name != "__row__":
                    column_index = list(df.columns).index(column_name)
                    cell_value = df.iloc[row_index, column_index]
                    cell_ref = f"{column_name}{row_index + 1}"

                    selected_cell = {
                        "sheet_name": selected_sheet,
                        "row_index": int(row_index),
                        "column_index": int(column_index),
                        "column_name": column_name,
                        "cell_value": cell_value,
                        "cell_ref": cell_ref,
                    }

        # Fallback: if range selection is unavailable, use selected row only
        if selected_cell is None and len(selected_rows) > 0:
            st.info("Row selected. Click directly inside a cell to capture an exact cell.")
        elif selected_cell:
            st.success(
                f"Selected cell: {selected_cell['cell_ref']} "
                f"(value: {selected_cell['cell_value']})"
            )

        return selected_sheet, selected_cell

    except Exception as exc:
        st.error(f"Failed to read Excel file: {exc}")
        return None, None