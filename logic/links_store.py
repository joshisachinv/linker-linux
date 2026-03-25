import json
import openpyxl
from typing import Dict, List
from models.pdf_link import PdfLink

def save_links_into_excel(xlsx_path: str, links: Dict[str, PdfLink]) -> None:
    """Saves link data into a hidden sheet called '__PDF_LINKS__'."""
    data = {k: v.to_json() for k, v in links.items()}
    json_text = json.dumps(data, separators=(",", ":"))
    
    wb = openpyxl.load_workbook(xlsx_path)
    sheet_name = "__PDF_LINKS__"
    
    if sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
        ws.delete_rows(1, ws.max_row)
    else:
        ws = wb.create_sheet(title=sheet_name)
    
    # Excel has a character limit per cell; we split long data into 'chunks'
    chunk = 30000
    for i in range(0, len(json_text), chunk):
        ws.cell(row=1 + i // chunk, column=1, value=json_text[i:i+chunk])
    
    ws.sheet_state = "hidden" # Keeps the data out of view for normal users
    wb.save(xlsx_path)

def try_load_embedded_links(xlsx_path: str) -> Dict[str, PdfLink]:
    """Checks the Excel file for the hidden sheet and loads any existing links."""
    wb = openpyxl.load_workbook(xlsx_path, read_only=True, data_only=True)
    if "__PDF_LINKS__" not in wb.sheetnames:
        return {}
        
    ws = wb["__PDF_LINKS__"]
    parts = [str(row[0]) for row in ws.iter_rows(values_only=True) if row[0]]
    
    if not parts:
        return {}
        
    data = json.loads("".join(parts))
    return {k: PdfLink.from_json(v) for k, v in data.items()}