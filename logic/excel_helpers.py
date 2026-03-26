import pandas as pd


HIDDEN_METADATA_SHEET = "__PDF_LINKS__"
ROW_COL_NAME = "__row__"


def excel_col_name(col_idx: int) -> str:
    """Convert zero-based column index to Excel-style column letters."""
    result = ""
    col_idx += 1
    while col_idx > 0:
        col_idx, remainder = divmod(col_idx - 1, 26)
        result = chr(65 + remainder) + result
    return result


def get_visible_sheets(excel_data: dict) -> list[str]:
    return [sheet for sheet in excel_data.keys() if sheet != HIDDEN_METADATA_SHEET]


def prepare_display_dataframe(df_raw: pd.DataFrame) -> pd.DataFrame:
    """
    Make the dataframe safe for Streamlit/AgGrid display and assign Excel-style headers.
    """
    df = df_raw.where(df_raw.notna(), "").astype(str).copy()
    df.columns = [excel_col_name(i) for i in range(len(df.columns))]
    return df


def add_row_numbers(df: pd.DataFrame) -> pd.DataFrame:
    df_display = df.copy()
    df_display.insert(0, ROW_COL_NAME, range(1, len(df_display) + 1))
    return df_display