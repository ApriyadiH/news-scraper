# ui/completion_window.py

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

from ui.widgets.completion_window.exit_button import ExitButton
from ui.widgets.completion_window.main_menu_button import MainMenuButton
from ui.widgets.completion_window.open_report_button import OpenReportButton


class CompletionWindow(QWidget):
    def __init__(self, report_path=None, main_window=None, parent=None):
        super().__init__(parent)

        self.setWindowTitle("News Scraper - Complete")
        self.resize(500, 650)

        self.setup_ui(report_path, main_window)

    def setup_ui(self, report_path, main_window):
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.title = QLabel("Scraping Complete!")
        self.title.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.path_label = QLabel(f"Report saved to:\n{report_path or 'Unknown'}")
        self.path_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.path_label.setWordWrap(True)

        self.open_button = OpenReportButton(report_path)

        self.menu_button = MainMenuButton(
            main_window=main_window,
            completion_window=self,
        )

        self.exit_button = ExitButton()

        layout.addWidget(self.title)
        layout.addSpacing(20)
        layout.addWidget(self.path_label)
        layout.addSpacing(30)
        layout.addWidget(self.open_button)
        layout.addWidget(self.menu_button)
        layout.addWidget(self.exit_button)

        self.setLayout(layout)
