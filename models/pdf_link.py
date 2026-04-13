from dataclasses import dataclass, asdict
from typing import Tuple, Optional


@dataclass
class PdfLink:
    pdf_path: str
    page_index: int
    rect: Tuple[float, float, float, float]
    sheet_name: Optional[str] = None
    cell_ref: Optional[str] = None

    def to_json(self) -> dict:
        d = asdict(self)

        # Ensure rect is JSON-safe
        d["rect"] = list(self.rect)
        return d

    @staticmethod
    def from_json(d: dict) -> "PdfLink":
        try:
            rect = d.get("rect", (0, 0, 0, 0))

            # Ensure valid rectangle
            if not isinstance(rect, (list, tuple)) or len(rect) != 4:
                raise ValueError("Invalid rect format")

            x0, y0, x1, y1 = [float(v) for v in rect]

            # Normalize
            rect_tuple = (
                min(x0, x1),
                min(y0, y1),
                max(x0, x1),
                max(y0, y1),
            )

            return PdfLink(
                pdf_path=d.get("pdf_path", "Unknown.pdf"),
                page_index=int(d.get("page_index", 0)),
                rect=rect_tuple,
                sheet_name=d.get("sheet_name"),
                cell_ref=d.get("cell_ref"),
            )

        except Exception as e:
            import streamlit as st
            st.warning(f"⚠️ Could not load a saved link — it may be corrupted: {e}")
            return PdfLink(
                pdf_path="Unknown.pdf",
                page_index=0,
                rect=(0, 0, 0, 0),
                sheet_name=None,
            )