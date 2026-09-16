# ui\training_window.py

from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QMessageBox, QApplication

from db.schema import create_tables
from db.human_labels import get_raw_with_all_labels
from db.raws import reset_labels
from ui.widgets.training_window.header import TrainingHeader
from ui.widgets.training_window.table import TrainingTable
from ui.labeling_window import LabelingWindow
from ui.ml_loading_window import MLLoadingWindow

class TrainingWindow(QMainWindow):
    def __init__(self, main_window=None):
        create_tables()
        super().__init__()
        self.main_window = main_window

        self.ml_thread = None
        self.ml_worker = None

        self.setWindowTitle("Training Data")
        self.showMaximized()

        central_widget = QWidget()
        layout = QVBoxLayout()

        self.header = TrainingHeader()
        self.table_widget = TrainingTable()

        layout.addWidget(self.header)
        layout.addWidget(self.table_widget)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)


        self.header.back_clicked.connect(self.go_back)
        self.header.label_clicked.connect(self.open_labeling_window)
        self.header.train_clicked.connect(self.train_ml)
        self.header.filter_changed.connect(self.table_widget.apply_filter)
        self.header.page_size_changed.connect(self.table_widget.set_page_size)
        self.table_widget.clear_requested.connect(self.on_clear_requested)

        self.load_data()

    def load_data(self):
        rows = get_raw_with_all_labels()
        self.table_widget.set_rows(rows)

    def on_clear_requested(self, raw_id):
        confirm = QMessageBox.question(
            self, "Confirm",
            "Clear all labels (exact match, ML, human) for this article?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
        )
        if confirm == QMessageBox.StandardButton.Yes:
            reset_labels(raw_id)
            self.load_data()

    def open_labeling_window(self):
        self.labeling_window = LabelingWindow(main_window=self)
        self.labeling_window.show()
        self.hide()

    def go_back(self):
        self.hide()
        if self.main_window:
            self.main_window.show()
            self.close()

    def closeEvent(self, event):
        QApplication.quit()
        event.accept()

    def train_ml(self):
        self.ml_loading_window = MLLoadingWindow(main_window=self)

        self.ml_loading_window.finished.connect(self.on_ml_finished)
        self.ml_loading_window.error.connect(self.on_ml_error)

        self.ml_loading_window.show()
        self.hide()

        self.ml_loading_window.start_training()

    def on_ml_finished(self):
        self.load_data()

    def on_ml_error(self, message):
        QMessageBox.critical(self, "ML Training Error", message)
        self.header.train_button.setEnabled(True)