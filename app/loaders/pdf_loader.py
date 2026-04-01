import os
from PyQt6.QtGui import QPixmap, QImage
import fitz  # pymupdf

_PAGE_TAG = "[p.{n}]"


def load_pdf(path: str) -> list[tuple[QPixmap, str]]:
    """Render every page of a PDF at 150 DPI. Returns list of (pixmap, label)."""
    results = []
    doc = fitz.open(path)
    for i, page in enumerate(doc):
        pix  = page.get_pixmap(dpi=150)
        qimg = QImage(pix.samples, pix.width, pix.height,
                      pix.stride, QImage.Format.Format_RGB888)
        label = f"{path} {_PAGE_TAG.format(n=i + 1)}"
        results.append((QPixmap.fromImage(qimg), label))
    doc.close()
    return results


def parse_label(path: str) -> tuple[str, str]:
    """Split a path label into (basename, page_tag).

    For regular images  → ("photo.jpg", "")
    For PDF pages       → ("report.pdf", " [p.3]")
    """
    if " [p." in path:
        file_part, tag_part = path.split(" [p.", 1)
        return os.path.basename(file_part), f" [p.{tag_part}"
    return os.path.basename(path), ""
