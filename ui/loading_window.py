# ui/loading_window.py

from PySide6.QtCore import QThread
from PySide6.QtWidgets import QWidget, QVBoxLayout
from ui.widgets.loading_window.log_widget import LogWidget
from ui.widgets.loading_window.progress_bar import ProgressBar
from ui.workers.pipeline_worker import PipelineWorker
from ui.completion_window import CompletionWindow


class LoadingWindow(QWidget):
    def __init__(
        self,
        sources=None,
        scrape_days=None,
        export_dates=None,
        export_path=None,
        main_window=None,
        parent=None,
    ):
        super().__init__(parent)

        self.setWindowTitle("News Scraper")
        self.resize(500, 650)

        self.main_window = main_window

        self.sources = sources
        self.scrape_days = scrape_days
        self.export_dates = export_dates
        self.export_path = export_path

        self.thread = None
        self.worker = None

        self.setup_ui()

    def setup_ui(self):
        layout = QVBoxLayout()

        self.log_widget = LogWidget()
        self.progress_bar = ProgressBar()

        layout.addWidget(self.log_widget)
        layout.addWidget(self.progress_bar)

        self.setLayout(layout)

    def start_pipeline(self):
        self.reset()
        self.thread = QThread()

        self.worker = PipelineWorker(
            sources=self.sources,
            scrape_days=self.scrape_days,
            export_dates=self.export_dates,
            export_path=self.export_path,
        )

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)

        self.worker.log.connect(self.add_log)
        self.worker.progress.connect(self.set_progress)
        self.worker.finished.connect(self.show_completion)
        self.worker.error.connect(self.pipeline_error)

        self.worker.finished.connect(self.thread.quit)
        self.worker.error.connect(self.thread.quit)

        self.thread.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.pipeline_thread_finished)

        self.thread.start()

    def pipeline_error(self, message):
        self.add_log(f"ERROR: {message}")

    def pipeline_thread_finished(self):
        self.thread = None
        self.worker = None

    def add_log(self, message):
        self.log_widget.add_log(message)

    def set_progress(self, value):
        self.progress_bar.set_progress(value)

    def reset(self):
        self.log_widget.clear_log()
        self.progress_bar.reset()

    def get_settings(self):
        return {
            "sources": self.sources,
            "scrape_days": self.scrape_days,
            "export_dates": self.export_dates,
            "export_path": self.export_path,
        }

    def show_completion(self, final_path):
        self.completion_window = CompletionWindow(
            report_path=final_path, main_window=self.main_window
        )

        self.completion_window.show()
        self.close()
