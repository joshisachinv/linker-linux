from dataclasses import dataclass, asdict
from typing import Tuple

@dataclass
class PdfLink:
    pdf_path: str
    page_index: int
    rect: Tuple[float, float, float, float]

    def to_json(self) -> dict:
        d = asdict(self)
        d["rect"] = list(self.rect)
        return d

    @staticmethod
    def from_json(d: dict) -> "PdfLink":
        return PdfLink(pdf_path=d["pdf_path"], page_index=int(d["page_index"]), rect=tuple(d["rect"]))