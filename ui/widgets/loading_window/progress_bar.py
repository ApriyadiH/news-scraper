from PySide6.QtWidgets import (
    QGroupBox,
    QProgressBar,
    QVBoxLayout,
)


class ProgressBar(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("Progress", parent)

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.progress = QProgressBar()
        self.progress.setRange(0, 100)
        self.progress.setValue(0)

        layout.addWidget(self.progress)

        self.setLayout(layout)

    def set_progress(self, value):
        self.progress.setValue(value)

    def reset(self):
        self.progress.setValue(0)