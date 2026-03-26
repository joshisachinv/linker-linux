import json
import openpyxl
from typing import Dict
from models.pdf_link import PdfLink

def save_links_into_excel(xlsx_path: str, links: Dict[str, PdfLink]) -> None:
    data = {k: v.to_json() for k, v in links.items()}
    json_text = json.dumps(data)
    wb = openpyxl.load_workbook(xlsx_path)
    ws = wb["__PDF_LINKS__"] if "__PDF_LINKS__" in wb.sheetnames else wb.create_sheet("__PDF_LINKS__")
    ws.delete_rows(1, ws.max_row)
    chunk = 30000
    for i in range(0, len(json_text), chunk):
        ws.cell(row=1 + i // chunk, column=1, value=json_text[i:i+chunk])
    ws.sheet_state = "hidden"
    wb.save(xlsx_path)

def try_load_embedded_links(xlsx_path: str) -> Dict[str, PdfLink]:
    wb = openpyxl.load_workbook(xlsx_path, read_only=True, data_only=True)
    if "__PDF_LINKS__" not in wb.sheetnames: return {}
    ws = wb["__PDF_LINKS__"]
    parts = [str(row[0]) for row in ws.iter_rows(values_only=True) if row[0]]
    if not parts: return {}
    data = json.loads("".join(parts))
    return {k: PdfLink.from_json(v) for k, v in data.items()}