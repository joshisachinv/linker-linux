import pandas as pd
import streamlit as st
from logic.excel_helpers import add_row_numbers, ROW_COL_NAME


def render_excel_grid(df, selected_sheet: str):
    """Render the Excel data as a clickable Streamlit dataframe."""
    df_display = add_row_numbers(df)

    st.dataframe(
        df_display,
        use_container_width=True,
        height=420,
        hide_index=True,
    )

    # Let user type the cell reference manually
    col1, col2 = st.columns([1, 2])
    with col1:
        st.markdown(
            "<div style='font-size:0.75rem;color:#475569;"
            "padding-top:6px;'>Select cell:</div>",
            unsafe_allow_html=True,
        )
    with col2:
        cell_input = st.text_input(
            "cell_ref_input",
            placeholder="e.g. B3",
            label_visibility="collapsed",
            key=f"cell_input_{selected_sheet}",
        )

    if cell_input:
        cell_input = cell_input.strip().upper()
        # Parse column letters and row number
        col_str = "".join(c for c in cell_input if c.isalpha())
        row_str = "".join(c for c in cell_input if c.isdigit())
        if col_str and row_str:
            return {"columnId": col_str, "rowIndex": int(row_str) - 1}

    return None