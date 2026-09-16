# ui/widgets/labeling_window/label_editor.py

import webbrowser
from PySide6.QtCore import Signal, Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QComboBox, QPushButton

UNLABELED = "UNLABELED"

class LabelEditor(QWidget):
    labels_changed = Signal(int, list)

    def __init__(self):
        super().__init__()

        self.available_labels = []
        self.rows = []

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)

        self._build_header()

    def _build_header(self):
        layout = QHBoxLayout()
        layout.setContentsMargins(0, 0, 0, 0)

        for text, width in [
            ("Title", 300),
            ("Exact Label", 120),
            ("ML Label", 120),
            ("ML Score", 80),
            ("", 60),
            ("", 100),
        ]:
            label = QLabel(text)
            label.setFixedWidth(width)
            layout.addWidget(label)

            if text:
                label.setStyleSheet("font-weight: bold;")

        labels_label = QLabel("Labels")
        labels_label.setStyleSheet("font-weight: bold;")
        layout.addWidget(labels_label)

        layout.addStretch()

        self.layout.addLayout(layout)

    def load_rows(self, rows, available_labels):
        self.available_labels = available_labels

        for row in self.rows:
            row.deleteLater()

        self.rows.clear()

        for raw_id, title, url, exact_label in rows:
            row = self._create_row(
                raw_id,
                title,
                url,
                exact_label,
                "",
                "",
            )

            self.rows.append(row)
            self.layout.addWidget(row)

    def _create_row(
        self,
        raw_id,
        title,
        url,
        exact_label,
        ml_label,
        ml_score,
    ):
        row = QWidget()

        row.raw_id = raw_id
        row.url = url
        row.labels = []
        row.is_unlabeled = False

        layout = QHBoxLayout(row)
        layout.setContentsMargins(0, 0, 0, 0)

        title_label = QLabel(title)
        title_label.setFixedWidth(300)
        title_label.setWordWrap(True)
        layout.addWidget(title_label)

        exact_label_widget = QLabel(exact_label or "")
        exact_label_widget.setFixedWidth(120)
        layout.addWidget(exact_label_widget)

        ml_label_widget = QLabel(ml_label or "")
        ml_label_widget.setFixedWidth(120)
        layout.addWidget(ml_label_widget)

        ml_score_widget = QLabel(
            str(ml_score) if ml_score not in (None, "") else ""
        )
        ml_score_widget.setFixedWidth(80)
        layout.addWidget(ml_score_widget)

        open_button = QPushButton("Open")
        open_button.setFixedWidth(60)
        open_button.clicked.connect(
            lambda: self._open_url(row)
        )
        layout.addWidget(open_button)

        unlabeled_button = QPushButton(UNLABELED)
        unlabeled_button.setCheckable(True)
        unlabeled_button.setFixedWidth(100)
        unlabeled_button.clicked.connect(
            lambda: self._toggle_unlabeled(row, unlabeled_button)
        )
        layout.addWidget(unlabeled_button)

        combo_layout = QHBoxLayout()
        combo_layout.setContentsMargins(0, 0, 0, 0)
        layout.addLayout(combo_layout)

        row.combo_layout = combo_layout
        row.unlabeled_button = unlabeled_button

        layout.addStretch()

        self._rebuild(row)

        return row

    def _open_url(self, row):
        if row.url:
            webbrowser.open(row.url)

    def _toggle_unlabeled(self, row, button):
        row.is_unlabeled = button.isChecked()

        if row.is_unlabeled:
            row.labels = []
            self.labels_changed.emit(row.raw_id, [UNLABELED])
        else:
            self._notify(row)

        self._rebuild(row)

    def _rebuild(self, row):
        while row.combo_layout.count():
            item = row.combo_layout.takeAt(0)
            widget = item.widget()

            if widget:
                widget.deleteLater()

        if row.is_unlabeled:
            return

        if not row.labels or row.labels[-1] != "":
            row.labels.append("")

        for index, label in enumerate(row.labels):
            combo = self._create_combo(row, index, label)
            row.combo_layout.addWidget(combo)

            remove_button = QPushButton("−")
            remove_button.setFixedWidth(30)
            remove_button.clicked.connect(
                lambda checked=False, i=index:
                    self._remove(row, i)
            )
            row.combo_layout.addWidget(remove_button)

    def _create_combo(self, row, index, current_label):
        combo = QComboBox()
        combo.addItem("")

        selected_labels = {
            label for i, label in enumerate(row.labels)
            if label and i != index
        }

        for label in self.available_labels:
            if label not in selected_labels:
                combo.addItem(label)

        if current_label:
            combo_index = combo.findText(current_label)
            if combo_index >= 0:
                combo.setCurrentIndex(combo_index)

        combo.currentTextChanged.connect(
            lambda value: self._combo_changed(row, index, value)
        )

        combo.setFixedWidth(130)

        return combo

    def _combo_changed(self, row, index, value):
        if index >= len(row.labels):
            return

        if value:
            row.labels[index] = value

            if index == len(row.labels) - 1:
                row.labels.append("")
        else:
            row.labels.pop(index)

        self._notify(row)
        self._rebuild(row)

    def _remove(self, row, index):
        if index < len(row.labels):
            row.labels.pop(index)

        self._notify(row)
        self._rebuild(row)

    def _notify(self, row):
        clean_labels = [
            label for label in row.labels if label
        ]

        self.labels_changed.emit(
            row.raw_id,
            clean_labels,
        )