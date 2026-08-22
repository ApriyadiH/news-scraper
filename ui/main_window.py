# ui/main_window.py
from PySide6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLabel,
    QSpinBox, QPushButton, QTextEdit
)
from PySide6.QtCore import QThread, Signal


class PipelineWorker(QThread):
    progress = Signal(str)
    finished = Signal(str)

    def __init__(self, scrape_days, export_days):
        super().__init__()
        self.scrape_days = scrape_days
        self.export_days = export_days

    def run(self):
        from main import run_pipeline  # deferred import, only happens when Run is clicked
        result_path = run_pipeline(self.scrape_days, self.export_days)
        self.finished.emit(result_path or "Done")


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("News Scraper")
        self.resize(500, 400)

        self.loading_label = QLabel("Loading, please wait...")
        layout = QVBoxLayout()
        layout.addWidget(self.loading_label)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        # build the real UI shortly after the window is already visible
        from PySide6.QtCore import QTimer
        QTimer.singleShot(0, self.build_real_ui)

    def build_real_ui(self):
        layout = QVBoxLayout()

        layout.addWidget(QLabel("Days to scrape:"))
        self.scrape_days_input = QSpinBox()
        self.scrape_days_input.setMinimum(1)
        self.scrape_days_input.setValue(2)
        layout.addWidget(self.scrape_days_input)

        layout.addWidget(QLabel("Days to export:"))
        self.export_days_input = QSpinBox()
        self.export_days_input.setMinimum(1)
        self.export_days_input.setValue(2)
        layout.addWidget(self.export_days_input)

        self.run_button = QPushButton("Run")
        self.run_button.clicked.connect(self.start_pipeline)
        layout.addWidget(self.run_button)

        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        layout.addWidget(self.log_output)

        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

    def start_pipeline(self):
        self.run_button.setEnabled(False)
        self.log_output.append("Starting pipeline...")

        scrape_days = self.scrape_days_input.value()
        export_days = self.export_days_input.value()

        self.worker = PipelineWorker(scrape_days, export_days)
        self.worker.finished.connect(self.on_finished)
        self.worker.start()

    def on_finished(self, result_path):
        self.log_output.append(f"Done! Report: {result_path}")
        self.run_button.setEnabled(True)