from PySide6.QtCore import QObject, Signal, Slot

from labeling.ml_trainer import train_model


class MLWorker(QObject):
    log = Signal(str)
    progress = Signal(int)
    finished = Signal()
    error = Signal(str)

    @Slot()
    def run(self):
        try:
            self.log.emit("--- Starting ML training ---")
            self.progress.emit(5)

            self.log.emit("Training model...")
            train_model(progress_callback=self.update_progress, log_callback=self.log_message)

            self.progress.emit(100)
            self.log.emit("")
            self.log.emit("=== ML TRAINING COMPLETE ===")

            self.finished.emit()

        except Exception as e:
            self.error.emit(str(e))

    def update_progress(self, value):
        self.progress.emit(value)

    def log_message(self, message):
        self.log.emit(message)