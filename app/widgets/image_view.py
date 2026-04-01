from PyQt6.QtWidgets import QGraphicsView, QGraphicsScene, QGraphicsPixmapItem
from PyQt6.QtCore import Qt, QRectF, pyqtSignal
from PyQt6.QtGui import QPainter, QColor, QPixmap, QWheelEvent


class ImageView(QGraphicsView):
    zoom_changed = pyqtSignal(float)

    def __init__(self):
        super().__init__()
        self._scene = QGraphicsScene(self)
        self._item: QGraphicsPixmapItem | None = None
        self._zoom = 1.0

        self.setScene(self._scene)
        self.setRenderHints(
            QPainter.RenderHint.Antialiasing |
            QPainter.RenderHint.SmoothPixmapTransform,
        )
        self.setTransformationAnchor(QGraphicsView.ViewportAnchor.AnchorUnderMouse)
        self.setResizeAnchor(QGraphicsView.ViewportAnchor.AnchorViewCenter)
        self.setDragMode(QGraphicsView.DragMode.ScrollHandDrag)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.setBackgroundBrush(QColor("#111111"))

    # ── Public API ─────────────────────────────────────────────────────────────

    @property
    def zoom(self) -> float:
        return self._zoom

    def show_pixmap(self, px: QPixmap) -> None:
        """Replace the displayed pixmap, preserving the current zoom."""
        if self._item is None:
            self._item = QGraphicsPixmapItem(px)
            self._item.setTransformationMode(Qt.TransformationMode.SmoothTransformation)
            self._scene.addItem(self._item)
        else:
            self._item.setPixmap(px)
        self._scene.setSceneRect(QRectF(px.rect()))

    def set_zoom(self, zoom: float) -> None:
        zoom = max(0.02, min(32.0, zoom))
        self.resetTransform()
        self.scale(zoom, zoom)
        self._zoom = zoom
        self.zoom_changed.emit(zoom)

    def fit(self) -> None:
        if self._item is None:
            return
        self.fitInView(self._item, Qt.AspectRatioMode.KeepAspectRatio)
        self._zoom = self.transform().m11()
        self.zoom_changed.emit(self._zoom)

    # ── Events ─────────────────────────────────────────────────────────────────

    def wheelEvent(self, event: QWheelEvent) -> None:
        factor = 1.25 if event.angleDelta().y() > 0 else 0.8
        new = self._zoom * factor
        if 0.02 <= new <= 32.0:
            self._zoom = new
            self.scale(factor, factor)
            self.zoom_changed.emit(self._zoom)

    def keyPressEvent(self, event) -> None:
        event.ignore()  # let QMainWindow handle navigation/zoom keys
