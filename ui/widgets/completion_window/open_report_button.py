# ui/widgets/completion_window/open_report_button.py

import os
import subprocess

from PySide6.QtWidgets import QPushButton


class OpenReportButton(QPushButton):
    def __init__(self, report_path=None, parent=None):
        super().__init__("Open Report", parent)

        self.report_path = report_path
        self.clicked.connect(self.open_report_location)

    def set_report_path(self, report_path):
        self.report_path = report_path

    def open_report_location(self):
        if self.report_path and os.path.exists(self.report_path):
            subprocess.Popen(
                [
                    "explorer",
                    "/select,",
                    os.path.normpath(self.report_path),
                ]
            )
