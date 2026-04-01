import sys
from PyQt6.QtWidgets import QApplication
from app.style import dark_palette
from app.windows.main_window import ImageViewer

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    app.setPalette(dark_palette())

    win = ImageViewer()
    win.show()
    sys.exit(app.exec())
