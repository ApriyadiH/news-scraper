# ui/widgets/loading_window/log_widget.py

from PySide6.QtWidgets import (
    QGroupBox,
    QPlainTextEdit,
    QVBoxLayout,
)


class LogWidget(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("Log", parent)

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.log = QPlainTextEdit()
        self.log.setReadOnly(True)

        layout.addWidget(self.log)

        self.setLayout(layout)

    def add_log(self, message):
        self.log.appendPlainText(message)

    def clear_log(self):
        self.log.clear()
