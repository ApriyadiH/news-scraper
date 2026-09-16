# ui/widgets/main_window/start_section.py

from PySide6.QtWidgets import QGroupBox, QHBoxLayout, QPushButton

class ActionSection(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("Actions", parent)
        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout()

        self.training_button = QPushButton("GO TO TRAINING WINDOW")
        self.training_button.setMinimumHeight(65)

        self.start_button = QPushButton("START SCRAPING")
        self.start_button.setMinimumHeight(65)

        self.training_button.setStyleSheet("""
            QPushButton {
                font-size: 18px;
                font-weight: bold;
            }

            QPushButton:hover {
                background-color: #dddddd;
            }

            QPushButton:pressed {
                background-color: #bbbbbb;
            }
        """)

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

        layout.addWidget(self.training_button)
        layout.addWidget(self.start_button)

        self.setLayout(layout)