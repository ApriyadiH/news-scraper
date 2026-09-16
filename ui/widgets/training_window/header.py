# ui\widgets\training_window\header.py

from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QComboBox
from PySide6.QtCore import Signal

class TrainingHeader(QWidget):
    back_clicked = Signal()
    label_clicked = Signal()
    train_clicked = Signal()
    filter_changed = Signal(str)
    page_size_changed = Signal(int)

    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()

        button_layout = QHBoxLayout()

        self.back_button = QPushButton("BACK")
        self.label_button = QPushButton("LABEL")
        self.train_button = QPushButton("TRAIN ML")

        self.back_button.setMinimumHeight(40)
        self.label_button.setMinimumHeight(40)
        self.train_button.setMinimumHeight(40)

        button_layout.addWidget(self.back_button)
        button_layout.addWidget(self.label_button)
        button_layout.addWidget(self.train_button)
        
        self.page_size_combo = QComboBox()
        self.page_size_combo.addItems(["25", "50", "100", "200"])
        self.page_size_combo.setCurrentText("50")
        self.page_size_combo.setMinimumHeight(40)

        button_layout.addWidget(self.page_size_combo)

        layout.addLayout(button_layout)

        self.filter_input = QLineEdit()
        self.filter_input.setPlaceholderText("Filter table...")
        layout.addWidget(self.filter_input)

        self.setLayout(layout)

        self.back_button.clicked.connect(self.back_clicked.emit)
        self.label_button.clicked.connect(self.label_clicked.emit)
        self.train_button.clicked.connect(self.train_clicked.emit)
        self.filter_input.textChanged.connect(self.filter_changed.emit)

        self.page_size_combo.currentTextChanged.connect(
            lambda value: self.page_size_changed.emit(int(value))
        )