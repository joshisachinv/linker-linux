import pandas as pd
from logic.cell_addr import num_to_col_letters

HIDDEN_METADATA_SHEET = "__PDF_LINKS__"
ROW_COL_NAME = "__row__"


def get_visible_sheets(excel_data: dict) -> list[str]:
    return [sheet for sheet in excel_data.keys() if sheet != HIDDEN_METADATA_SHEET]


def prepare_display_dataframe(df_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Make the dataframe safe for Streamlit/AgGrid display and assign Excel-style headers.
    """
    df = df_raw.where(df_raw.notna(), "").astype(str).copy()
    df.columns = [num_to_col_letters(i) for i in range(len(df.columns))]
    return df


def add_row_numbers(df: pd.DataFrame) -> pd.DataFrame:
    df_display = df.copy()
    df_display.insert(0, ROW_COL_NAME, range(1, len(df_display) + 1))
    return df_display