from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PySide6.QtCore import Qt

class MLCompletionWindow(QWidget):
    def __init__(self, main_window=None):
        super().__init__()

        self.main_window = main_window

        self.setWindowTitle("ML Training Complete")
        self.resize(500, 300)

        layout = QVBoxLayout()

        self.title_label = QLabel("ML TRAINING COMPLETE")
        self.title_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.message_label = QLabel("The model has been trained and all ML labels have been updated.")
        self.message_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.message_label.setWordWrap(True)

        self.back_button = QPushButton("BACK TO TRAINING")
        self.back_button.setMinimumHeight(50)

        layout.addWidget(self.title_label)
        layout.addWidget(self.message_label)
        layout.addWidget(self.back_button)

        self.setLayout(layout)

        self.back_button.clicked.connect(self.go_back)

    def go_back(self):
        if self.main_window:
            self.main_window.load_data()
            self.main_window.show()

        self.close()

    def closeEvent(self, event):
        if self.main_window:
            self.main_window.load_data()
            self.main_window.show()

        event.accept()