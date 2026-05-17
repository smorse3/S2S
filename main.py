import sys

from PySide6.QtWidgets import QApplication

from gui.main_window import MainWindow
from gui.styles import apply_win95_style


def main():
    app = QApplication(sys.argv)

    apply_win95_style(app)

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()