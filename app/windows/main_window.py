import os

from PyQt6.QtWidgets import (
    QMainWindow, QToolBar, QFileDialog, QLabel,
    QWidget, QSizePolicy, QSplitter,
)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QAction, QKeySequence, QPixmap

from ..style import QSS
from ..loaders.image_loader import load_image
from ..loaders.pdf_loader import load_pdf, parse_label
from ..widgets.image_view import ImageView
from ..widgets.sidebar import Sidebar


class ImageViewer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Image Viewer")
        self.resize(1280, 840)

        self._pixmaps: list[QPixmap] = []
        self._paths:   list[str]     = []
        self._idx = 0

        self._build_ui()
        self.setStyleSheet(QSS)

    # ── Layout ─────────────────────────────────────────────────────────────────

    def _build_ui(self) -> None:
        self._view    = ImageView()
        self._sidebar = Sidebar()

        self._view.zoom_changed.connect(self._on_zoom_changed)
        self._sidebar.image_selected.connect(self._on_sidebar_select)

        splitter = QSplitter(Qt.Orientation.Horizontal)
        splitter.addWidget(self._sidebar)
        splitter.addWidget(self._view)
        splitter.setSizes([176, 1104])
        splitter.setStretchFactor(0, 0)
        splitter.setStretchFactor(1, 1)
        splitter.setHandleWidth(1)
        self.setCentralWidget(splitter)

        self.addToolBar(self._build_toolbar())

        sb = self.statusBar()
        self._lbl_file = QLabel("  Open images to get started")
        self._lbl_nav  = QLabel()
        self._lbl_nav.setAlignment(Qt.AlignmentFlag.AlignRight)
        sb.addWidget(self._lbl_file, 1)
        sb.addPermanentWidget(self._lbl_nav)

    def _build_toolbar(self) -> QToolBar:
        tb = QToolBar("Main", self)
        tb.setMovable(False)
        tb.setIconSize(QSize(0, 0))

        open_act = QAction("  Open…  ", self)
        open_act.triggered.connect(self.load_images)
        open_act.setShortcut(QKeySequence.StandardKey.Open)
        tb.addAction(open_act)
        tb.widgetForAction(open_act).setObjectName("accent")

        tb.addSeparator()

        prev_act = QAction("▲  Prev", self)
        prev_act.triggered.connect(self.prev_image)
        tb.addAction(prev_act)

        next_act = QAction("▼  Next", self)
        next_act.triggered.connect(self.next_image)
        tb.addAction(next_act)

        tb.addSeparator()

        zoom_out_act = QAction("  −  ", self)
        zoom_out_act.triggered.connect(self.zoom_out)
        tb.addAction(zoom_out_act)

        self._zoom_label = QLabel("  100%  ")
        self._zoom_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self._zoom_label.setMinimumWidth(56)
        self._zoom_label.setStyleSheet("color: #636366; font-size: 12px;")
        tb.addWidget(self._zoom_label)

        zoom_in_act = QAction("  +  ", self)
        zoom_in_act.triggered.connect(self.zoom_in)
        tb.addAction(zoom_in_act)

        tb.addSeparator()

        fit_act = QAction("  Fit  ", self)
        fit_act.triggered.connect(self._view.fit)
        fit_act.setShortcut(QKeySequence(Qt.Key.Key_F))
        tb.addAction(fit_act)

        one_act = QAction("  1:1  ", self)
        one_act.triggered.connect(self.reset_zoom)
        one_act.setShortcut(QKeySequence(Qt.Key.Key_1))
        tb.addAction(one_act)

        spacer = QWidget()
        spacer.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Preferred)
        tb.addWidget(spacer)

        hint = QLabel("↑ ↓ navigate  ·  scroll zoom  ·  drag pan  ")
        hint.setStyleSheet("color: #3a3a3c; font-size: 11px;")
        tb.addWidget(hint)

        return tb

    # ── Loading ────────────────────────────────────────────────────────────────

    def load_images(self) -> None:
        paths, _ = QFileDialog.getOpenFileNames(
            self, "Open Images / PDFs", "",
            "Supported files (*.png *.jpg *.jpeg *.bmp *.gif "
            "*.tiff *.tif *.webp *.pdf);;All files (*.*)",
        )
        if not paths:
            return

        self._pixmaps.clear()
        self._paths.clear()

        for p in sorted(paths):
            if p.lower().endswith(".pdf"):
                for px, label in load_pdf(p):
                    self._pixmaps.append(px)
                    self._paths.append(label)
            else:
                result = load_image(p)
                if result:
                    self._pixmaps.append(result[0])
                    self._paths.append(result[1])

        if not self._pixmaps:
            return

        self._idx = 0
        self._view.set_zoom(1.0)
        self._sidebar.populate(self._pixmaps, self._paths)
        self._show()

    # ── Navigation ─────────────────────────────────────────────────────────────

    def next_image(self) -> None:
        if self._pixmaps and self._idx < len(self._pixmaps) - 1:
            self._idx += 1
            self._show()

    def prev_image(self) -> None:
        if self._pixmaps and self._idx > 0:
            self._idx -= 1
            self._show()

    def _on_sidebar_select(self, row: int) -> None:
        if 0 <= row < len(self._pixmaps) and row != self._idx:
            self._idx = row
            self._show(sync_sidebar=False)

    # ── Zoom ───────────────────────────────────────────────────────────────────

    def zoom_in(self)    -> None: self._view.set_zoom(self._view.zoom * 1.25)
    def zoom_out(self)   -> None: self._view.set_zoom(self._view.zoom / 1.25)
    def reset_zoom(self) -> None: self._view.set_zoom(1.0)

    def _on_zoom_changed(self, zoom: float) -> None:
        self._zoom_label.setText(f"  {int(zoom * 100)}%  ")

    # ── Display ────────────────────────────────────────────────────────────────

    def _show(self, sync_sidebar: bool = True) -> None:
        self._view.show_pixmap(self._pixmaps[self._idx])

        base, tag = parse_label(self._paths[self._idx])
        self._lbl_file.setText(f"   {base}{tag}")
        self._lbl_nav.setText(f"{self._idx + 1} / {len(self._pixmaps)}   ")

        if sync_sidebar:
            self._sidebar.select(self._idx)

    # ── Keyboard ───────────────────────────────────────────────────────────────

    def keyPressEvent(self, event) -> None:
        k = event.key()
        if   k == Qt.Key.Key_Up:                          self.prev_image()
        elif k == Qt.Key.Key_Down:                        self.next_image()
        elif k in (Qt.Key.Key_Plus, Qt.Key.Key_Equal):    self.zoom_in()
        elif k == Qt.Key.Key_Minus:                       self.zoom_out()
        else:                                             super().keyPressEvent(event)
