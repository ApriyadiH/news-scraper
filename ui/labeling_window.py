# ui\labeling_window.py

from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QScrollArea, QMessageBox, QApplication
from PySide6.QtCore import Qt
from ui.widgets.horizontal_scroll_area import HorizontalScrollArea
from db.keywords import get_distinct_labels
from db.human_labels import get_raw_missing_human_label, save_human_labels
from ui.widgets.labeling_window.label_editor import LabelEditor


class LabelingWindow(QMainWindow):
    ROW_LIMIT = 15

    def __init__(self, main_window=None):
        super().__init__()
        self.main_window = main_window
        self.pending_labels = {}
        self.has_changes = False

        self.setWindowTitle("Assign Human Label")
        self.showMaximized()

        central_widget = QWidget()
        main_layout = QVBoxLayout()

        title_label = QLabel("Assign Human Label")
        title_label.setStyleSheet("font-size: 22px; font-weight: bold; padding: 10px;")
        main_layout.addWidget(title_label)

        button_layout = QHBoxLayout()
        self.back_button = QPushButton("BACK")
        self.save_button = QPushButton("SAVE")
        self.back_button.setMinimumHeight(40)
        self.save_button.setMinimumHeight(40)
        button_layout.addWidget(self.back_button)
        button_layout.addWidget(self.save_button)
        main_layout.addLayout(button_layout)

        self.content_scroll = HorizontalScrollArea()
        self.content_scroll.setWidgetResizable(True)
        self.content_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)
        self.content_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded)

        self.label_editor = LabelEditor()
        self.content_scroll.setWidget(self.label_editor)

        main_layout.addWidget(self.content_scroll)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        self.back_button.clicked.connect(self.go_back)
        self.save_button.clicked.connect(self.save_data)

        self.load_data()

    def load_data(self):
        available_labels = get_distinct_labels()
        rows = get_raw_missing_human_label(limit=self.ROW_LIMIT)
        self.label_editor.load_rows(rows, available_labels)

    def on_labels_changed(self, raw_id, labels):
        self.pending_labels[raw_id] = labels
        self.has_changes = True

    def save_data(self):
        to_save = {raw_id: labels for raw_id, labels in self.pending_labels.items() if labels}
        save_human_labels(to_save)
        print(f"Saved {len(to_save)} rows.")
        self.has_changes = False
        self.go_back()

    def go_back(self):
        if self.has_changes:
            confirm = QMessageBox.question(
                self, "Unsaved changes",
                "You have unsaved changes. Go back without saving?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if confirm != QMessageBox.StandardButton.Yes:
                return
        self.hide()
        if self.main_window:
            self.main_window.load_data()
            self.main_window.show()

    def closeEvent(self, event):
        if self.has_changes:
            confirm = QMessageBox.question(
                self, "Unsaved changes",
                "You have unsaved changes. Close without saving?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            if confirm != QMessageBox.StandardButton.Yes:
                event.ignore()
                return
            
        QApplication.quit()
        event.accept()