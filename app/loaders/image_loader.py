from PyQt6.QtGui import QPixmap


def load_image(path: str) -> tuple[QPixmap, str] | None:
    """Load a raster image file. Returns (pixmap, path) or None on failure."""
    px = QPixmap(path)
    if px.isNull():
        return None
    return px, path
