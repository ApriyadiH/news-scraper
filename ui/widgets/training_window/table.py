# ui\widgets\training_window\table.py

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QTableWidget, QTableWidgetItem, QMenu

class ScrollableTable(QTableWidget):
    def wheelEvent(self, event):
        if event.modifiers() & Qt.KeyboardModifier.ShiftModifier:
            delta = event.angleDelta().y()
            self.horizontalScrollBar().setValue(
                self.horizontalScrollBar().value() - delta
            )
            event.accept()
            return

        super().wheelEvent(event)

class TrainingTable(QWidget):
    PAGE_SIZE = 50

    clear_requested = Signal(int) 

    def __init__(self):
        super().__init__()

        self.all_rows = []
        self.filtered_rows = []
        self.current_page = 0

        layout = QVBoxLayout()

        self.table = ScrollableTable()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(
            ["Title", "Exact Match Label", "ML Label", "ML Score", "Human Label"]
        )
        self.table.setSortingEnabled(True)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.table.customContextMenuRequested.connect(self.show_context_menu)
        layout.addWidget(self.table)

        pagination_layout = QHBoxLayout()
        self.previous_button = QPushButton("PREVIOUS")
        self.page_label = QPushButton("Page 1")
        self.page_label.setEnabled(False)
        self.next_button = QPushButton("NEXT")
        pagination_layout.addWidget(self.previous_button)
        pagination_layout.addWidget(self.page_label)
        pagination_layout.addWidget(self.next_button)
        layout.addLayout(pagination_layout)

        self.setLayout(layout)

        self.previous_button.clicked.connect(self.previous_page)
        self.next_button.clicked.connect(self.next_page)

    def set_rows(self, rows):
        self.all_rows = rows
        self.filtered_rows = rows.copy()
        self.current_page = 0
        self.display_page()

    def apply_filter(self, text):
        text = text.lower().strip()
        if not text:
            self.filtered_rows = self.all_rows.copy()
        else:
            self.filtered_rows = [
                row for row in self.all_rows
                if text in f"{row[1]} {row[2] or ''} {row[3] or ''}".lower()
            ]
        self.current_page = 0
        self.display_page()

    def display_page(self):
        self.table.setSortingEnabled(False)

        start = self.current_page * self.PAGE_SIZE
        end = start + self.PAGE_SIZE
        page_rows = self.filtered_rows[start:end]

        self.table.clearContents()
        self.table.setRowCount(len(page_rows))

        for row_index, (raw_id, title, exact_labels, ml_labels, human_labels) in enumerate(page_rows):
            title_item = QTableWidgetItem(title)
            title_item.setData(Qt.ItemDataRole.UserRole, raw_id)
            self.table.setItem(row_index, 0, title_item)
            self.table.setItem(row_index, 1, QTableWidgetItem(exact_labels or ""))

            ml_label_text = ""
            ml_score_text = ""

            if ml_labels:
                predictions = ml_labels.split(",")

                label_list = []
                score_list = []

                for prediction in predictions:
                    label, score = prediction.rsplit(":", 1)

                    label_list.append(label)
                    score_list.append(f"{float(score):.3f}")

                ml_label_text = ", ".join(label_list)
                ml_score_text = ", ".join(score_list)

            self.table.setItem(
                row_index,
                2,
                QTableWidgetItem(ml_label_text)
            )

            self.table.setItem(
                row_index,
                3,
                QTableWidgetItem(ml_score_text)
            )

            self.table.setItem(
                row_index,
                4,
                QTableWidgetItem(human_labels or "")
            )

        self.table.setColumnWidth(0, 500)
        self.table.setColumnWidth(1, 250)
        self.table.setColumnWidth(2, 250)
        self.table.setColumnWidth(3, 100)
        self.table.setColumnWidth(4, 350)

        self.table.setSortingEnabled(True)
        self.update_pagination()

    def show_context_menu(self, position):
        item = self.table.itemAt(position)
        if not item:
            return
        row = item.row()
        title_item = self.table.item(row, 0)
        raw_id = title_item.data(Qt.ItemDataRole.UserRole)

        menu = QMenu(self)
        clear_action = menu.addAction("Empty Label")
        action = menu.exec(self.table.viewport().mapToGlobal(position))

        if action == clear_action:
            self.clear_requested.emit(raw_id)

    def update_pagination(self):
        total_rows = len(self.filtered_rows)
        total_pages = max(1, (total_rows + self.PAGE_SIZE - 1) // self.PAGE_SIZE)
        self.page_label.setText(f"Page {self.current_page + 1} / {total_pages}")
        self.previous_button.setEnabled(self.current_page > 0)
        self.next_button.setEnabled(self.current_page < total_pages - 1)

    def previous_page(self):
        if self.current_page > 0:
            self.current_page -= 1
            self.display_page()

    def next_page(self):
        total_pages = max(1, (len(self.filtered_rows) + self.PAGE_SIZE - 1) // self.PAGE_SIZE)
        if self.current_page < total_pages - 1:
            self.current_page += 1
            self.display_page()

    def set_page_size(self, size):
        self.PAGE_SIZE = size
        self.current_page = 0
        self.display_page()