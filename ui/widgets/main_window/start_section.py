# ui\widgets\main_window\start_section.py

from PySide6.QtWidgets import (
    QGroupBox,
    QVBoxLayout,
    QPushButton,
)


class StartSection(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("Start", parent)

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.start_button = QPushButton("START SCRAPING")

        self.start_button.setMinimumHeight(65)

        self.start_button.setStyleSheet("""
            QPushButton {
                font-size: 26px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #dddddd;
            }

            QPushButton:pressed {
                background-color: #bbbbbb;
            }
        """)

        layout.addWidget(self.start_button)

        self.setLayout(layout)