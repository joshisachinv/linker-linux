from dataclasses import dataclass, asdict
from typing import Tuple

@dataclass
class PdfLink:
    pdf_path: str
    page_index: int
    rect: Tuple[float, float, float, float]  # (x0, y0, x1, y1) in page coords

    def to_json(self) -> dict:
        """Converts the link object into a dictionary for JSON storage."""
        d = asdict(self)
        d["rect"] = list(self.rect)
        return d

    @staticmethod
    def from_json(d: dict) -> "PdfLink":
        """Creates a link object from a JSON dictionary."""
        return PdfLink(
            pdf_path=d["pdf_path"], 
            page_index=int(d["page_index"]), 
            rect=tuple(d["rect"])
        )