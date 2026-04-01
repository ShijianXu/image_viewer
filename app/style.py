from PyQt6.QtGui import QPalette, QColor

QSS = """
QMainWindow, QWidget#root {
    background: #111;
}

/* ── Toolbar ── */
QToolBar {
    background: #1c1c1e;
    border: none;
    border-bottom: 1px solid #2c2c2e;
    padding: 5px 10px;
    spacing: 2px;
}
QToolBar::separator {
    background: #3a3a3c;
    width: 1px;
    margin: 5px 8px;
}
QToolButton {
    color: #ebebf5cc;
    background: transparent;
    border: none;
    border-radius: 6px;
    padding: 5px 13px;
    font-size: 13px;
}
QToolButton:hover   { background: #2c2c2e; }
QToolButton:pressed { background: #48484a; }

QToolButton#accent {
    background: #0a84ff;
    color: #fff;
    font-weight: 600;
    border-radius: 6px;
    padding: 5px 14px;
}
QToolButton#accent:hover   { background: #409cff; }
QToolButton#accent:pressed { background: #0060df; }

/* ── Canvas ── */
QGraphicsView {
    background: #111;
    border: none;
}

/* ── Sidebar ── */
QSplitter::handle {
    background: #2c2c2e;
    width: 1px;
}
QListWidget {
    background: #161618;
    border: none;
    border-right: 1px solid #2c2c2e;
    outline: none;
    padding: 6px 4px;
}
QListWidget::item {
    background: transparent;
    border-radius: 6px;
    color: #636366;
    font-size: 10px;
    padding: 3px 2px;
    margin: 2px 4px;
}
QListWidget::item:hover:!selected {
    background: #2c2c2e;
    color: #aeaeb2;
}
QListWidget::item:selected {
    background: #1c3a5e;
    color: #ebebf5;
    border: 1px solid #0a84ff;
}

/* ── Status bar ── */
QStatusBar {
    background: #1c1c1e;
    color: #636366;
    border-top: 1px solid #2c2c2e;
    font-size: 12px;
    padding: 2px 6px;
}
QStatusBar QLabel { color: #636366; font-size: 12px; padding: 0 4px; }

/* ── Slim scrollbars ── */
QScrollBar:vertical {
    background: transparent; width: 6px; margin: 0;
}
QScrollBar::handle:vertical {
    background: #48484a; border-radius: 3px; min-height: 24px;
}
QScrollBar::handle:vertical:hover { background: #636366; }
QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical { height: 0; }
QScrollBar::add-page:vertical, QScrollBar::sub-page:vertical { background: none; }

QScrollBar:horizontal {
    background: transparent; height: 6px; margin: 0;
}
QScrollBar::handle:horizontal {
    background: #48484a; border-radius: 3px; min-width: 24px;
}
QScrollBar::handle:horizontal:hover { background: #636366; }
QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal { width: 0; }
QScrollBar::add-page:horizontal, QScrollBar::sub-page:horizontal { background: none; }
"""


def dark_palette() -> QPalette:
    p = QPalette()
    p.setColor(QPalette.ColorRole.Window,          QColor("#1c1c1e"))
    p.setColor(QPalette.ColorRole.WindowText,      QColor("#ebebf5"))
    p.setColor(QPalette.ColorRole.Base,            QColor("#2c2c2e"))
    p.setColor(QPalette.ColorRole.AlternateBase,   QColor("#1c1c1e"))
    p.setColor(QPalette.ColorRole.Text,            QColor("#ebebf5"))
    p.setColor(QPalette.ColorRole.Button,          QColor("#2c2c2e"))
    p.setColor(QPalette.ColorRole.ButtonText,      QColor("#ebebf5"))
    p.setColor(QPalette.ColorRole.Highlight,       QColor("#0a84ff"))
    p.setColor(QPalette.ColorRole.HighlightedText, QColor("#ffffff"))
    p.setColor(QPalette.ColorRole.ToolTipBase,     QColor("#2c2c2e"))
    p.setColor(QPalette.ColorRole.ToolTipText,     QColor("#ebebf5"))
    p.setColor(QPalette.ColorRole.PlaceholderText, QColor("#636366"))
    return p
