from PyQt6.QtWidgets import QListWidget, QListWidgetItem, QListView
from PyQt6.QtCore import Qt, QSize, pyqtSignal
from PyQt6.QtGui import QPixmap, QIcon, QPainter, QColor

from ..loaders.pdf_loader import parse_label

_THUMB = QSize(148, 94)
_GRID  = QSize(164, 122)
_BG    = "#161618"


class Sidebar(QListWidget):
    """Vertical filmstrip of image thumbnails. Emits image_selected(int)."""

    image_selected = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.setFixedWidth(176)
        self.setViewMode(QListView.ViewMode.IconMode)
        self.setFlow(QListView.Flow.TopToBottom)
        self.setWrapping(False)
        self.setIconSize(_THUMB)
        self.setGridSize(_GRID)
        self.setSpacing(0)
        self.setUniformItemSizes(True)
        self.setResizeMode(QListView.ResizeMode.Adjust)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.currentRowChanged.connect(self._on_row_changed)

    # ── Public API ─────────────────────────────────────────────────────────────

    def populate(self, pixmaps: list[QPixmap], paths: list[str]) -> None:
        """Rebuild the thumbnail list from scratch."""
        self.blockSignals(True)
        self.clear()
        for px, path in zip(pixmaps, paths):
            self.addItem(self._make_item(px, path))
        self.blockSignals(False)

    def select(self, idx: int) -> None:
        """Programmatically highlight a row without emitting image_selected."""
        self.blockSignals(True)
        self.setCurrentRow(idx)
        item = self.item(idx)
        if item:
            self.scrollToItem(item, QListWidget.ScrollHint.EnsureVisible)
        self.blockSignals(False)

    # ── Internals ──────────────────────────────────────────────────────────────

    def _make_item(self, px: QPixmap, path: str) -> QListWidgetItem:
        scaled = px.scaled(_THUMB, Qt.AspectRatioMode.KeepAspectRatio,
                           Qt.TransformationMode.SmoothTransformation)
        canvas = QPixmap(_THUMB)
        canvas.fill(QColor(_BG))
        p = QPainter(canvas)
        x = (_THUMB.width()  - scaled.width())  // 2
        y = (_THUMB.height() - scaled.height()) // 2
        p.drawPixmap(x, y, scaled)
        p.end()

        base, tag = parse_label(path)
        item = QListWidgetItem(QIcon(canvas), base + tag)
        item.setTextAlignment(Qt.AlignmentFlag.AlignHCenter | Qt.AlignmentFlag.AlignBottom)
        return item

    def _on_row_changed(self, row: int) -> None:
        if row >= 0:
            self.image_selected.emit(row)
