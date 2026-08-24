# ui/widgets/main_window/source_selector.py

from PySide6.QtCore import Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QGroupBox,
    QHBoxLayout,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from config import BISNIS_CATEGORIES, CNBC_CATEGORIES


class SourceSelector(QGroupBox):
    state_changed = Signal()

    def __init__(self, parent=None):
        super().__init__("Sources", parent)

        self._updating = False
        self.cnbc_categories = []
        self.bisnis_categories = []

        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout()
        columns_layout = QHBoxLayout()

        cnbc_widget = self.create_source_column(
            "CNBC Indonesia",
            CNBC_CATEGORIES,
            default_categories=["Market", "News"],
            source="cnbc",
        )

        bisnis_widget = self.create_source_column(
            "Bisnis.com",
            BISNIS_CATEGORIES,
            default_categories=["Market", "Finansial", "Ekonomi"],
            source="bisnis",
        )

        columns_layout.addWidget(cnbc_widget)
        columns_layout.addWidget(bisnis_widget)

        main_layout.addLayout(columns_layout)

        self.no_scrape_checkbox = QCheckBox("Don't scrape — export existing data only")
        self.no_scrape_checkbox.toggled.connect(self.toggle_no_scrape)

        main_layout.addWidget(self.no_scrape_checkbox)

        self.setLayout(main_layout)

    def create_source_column(
        self,
        source_name,
        categories,
        default_categories,
        source,
    ):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        source_checkbox = QCheckBox(source_name)
        source_checkbox.setChecked(True)
        layout.addWidget(source_checkbox)

        category_container = QWidget()
        category_layout = QVBoxLayout(category_container)

        category_checkboxes = []

        for category in categories:
            checkbox = QCheckBox(category["name"])
            checkbox.setChecked(category["name"] in default_categories)

            checkbox.stateChanged.connect(
                lambda state, source=source: self.category_changed(source)
            )

            category_layout.addWidget(checkbox)
            category_checkboxes.append((category, checkbox))

        if source == "cnbc":
            self.cnbc_checkbox = source_checkbox
            self.cnbc_categories = category_checkboxes
        else:
            self.bisnis_checkbox = source_checkbox
            self.bisnis_categories = category_checkboxes

        source_checkbox.stateChanged.connect(
            lambda state, source=source: self.source_changed(source)
        )

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setWidget(category_container)

        layout.addWidget(scroll)

        return widget

    def source_changed(self, source):
        if self._updating:
            return

        self._updating = True

        if source == "cnbc":
            source_checkbox = self.cnbc_checkbox
            categories = self.cnbc_categories
        else:
            source_checkbox = self.bisnis_checkbox
            categories = self.bisnis_categories

        checked = source_checkbox.isChecked()

        for _, checkbox in categories:
            checkbox.setChecked(checked)

        self._updating = False
        self.state_changed.emit()

    def category_changed(self, source):
        if self._updating:
            return

        if source == "cnbc":
            source_checkbox = self.cnbc_checkbox
            categories = self.cnbc_categories
        else:
            source_checkbox = self.bisnis_checkbox
            categories = self.bisnis_categories

        any_checked = any(checkbox.isChecked() for _, checkbox in categories)

        self._updating = True
        source_checkbox.setChecked(any_checked)
        self._updating = False

        self.state_changed.emit()

    def get_selected_sources(self):
        selected = {
            "cnbc": [],
            "bisnis": [],
        }

        if self.cnbc_checkbox.isChecked():
            selected["cnbc"] = [
                category
                for category, checkbox in self.cnbc_categories
                if checkbox.isChecked()
            ]

        if self.bisnis_checkbox.isChecked():
            selected["bisnis"] = [
                category
                for category, checkbox in self.bisnis_categories
                if checkbox.isChecked()
            ]

        return selected

    def should_scrape(self):
        return not self.no_scrape_checkbox.isChecked()

    def toggle_no_scrape(self, no_scrape):
        if self._updating:
            return

        self._updating = True

        if no_scrape:
            self.cnbc_checkbox.setChecked(False)
            self.bisnis_checkbox.setChecked(False)

            for _, checkbox in self.cnbc_categories:
                checkbox.setChecked(False)

            for _, checkbox in self.bisnis_categories:
                checkbox.setChecked(False)

        self._updating = False
        self.state_changed.emit()
