# ui/widgets/main_window/export_selector.py

from PySide6.QtWidgets import (
    QFileDialog,
    QGroupBox,
    QHBoxLayout,
    QLineEdit,
    QPushButton,
)

from utils.path_utils import get_desktop_dir


class ExportSelector(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("Export Location", parent)

        self.setup_ui()

    def setup_ui(self):
        layout = QHBoxLayout()

        self.path_input = QLineEdit()

        desktop_path = get_desktop_dir()
        self.path_input.setPlaceholderText(desktop_path)

        browse_button = QPushButton("Browse")
        browse_button.clicked.connect(self.browse)

        layout.addWidget(self.path_input)
        layout.addWidget(browse_button)

        self.setLayout(layout)

    def browse(self):
        folder = QFileDialog.getExistingDirectory(
            self,
            "Choose Export Folder",
        )

        if folder:
            self.path_input.setText(folder)

    def get_export_path(self):
        path = self.path_input.text().strip()

        if not path:
            return get_desktop_dir()

        return path
