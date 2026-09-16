from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout

from ui.widgets.loading_window.log_widget import LogWidget
from ui.widgets.loading_window.progress_bar import ProgressBar
from ui.workers.ml_worker import MLWorker
from ui.ml_completion_window import MLCompletionWindow


class MLLoadingWindow(QWidget):
    finished = Signal()
    error = Signal(str)

    def __init__(self, main_window=None):
        super().__init__()

        self.main_window = main_window

        self.setWindowTitle("ML Training")
        self.resize(500, 650)

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

    def start_training(self):
        self.reset()

        self.thread = QThread()
        self.worker = MLWorker()

        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)

        self.worker.log.connect(self.add_log)
        self.worker.progress.connect(self.set_progress)
        self.worker.finished.connect(self.training_finished)
        self.worker.error.connect(self.training_error)

        self.worker.finished.connect(self.thread.quit)
        self.worker.error.connect(self.thread.quit)

        self.thread.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.thread.finished.connect(self.thread_finished)

        self.thread.start()

    def add_log(self, message):
        self.log_widget.add_log(message)

    def set_progress(self, value):
        self.progress_bar.set_progress(value)

    def training_finished(self):
        self.add_log("")
        self.add_log("=== ML TRAINING COMPLETE ===")
        self.progress_bar.set_progress(100)

        self.finished.emit()

        self.completion_window = MLCompletionWindow(
            main_window=self.main_window
        )
        self.completion_window.show()
        self.close()

    def training_error(self, message):
        self.add_log(f"ERROR: {message}")
        self.error.emit(message)

    def thread_finished(self):
        self.thread = None
        self.worker = None

    def reset(self):
        self.log_widget.clear_log()
        self.progress_bar.reset()