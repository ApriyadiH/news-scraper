# debug_ui.py

import sys
from PySide6.QtWidgets import QApplication
from ui.main_window import MainWindow


def main():
    app = QApplication(sys.argv)

    window = MainWindow(debug=True)
    window.show()
    window.showMaximized()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
