# ui/widgets/main_window/source_selector.py

from PySide6.QtCore import Qt, Signal
from PySide6.QtWidgets import (
    QCheckBox,
    QGroupBox,
    QHBoxLayout,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from config import BISNIS_CATEGORIES, CNBC_CATEGORIES, IDXCHANNEL_CATEGORIES


class SourceSelector(QGroupBox):
    state_changed = Signal()

    def __init__(self, parent=None):
        super().__init__("Sources", parent)

        self._updating = False
        self.cnbc_categories = []
        self.bisnis_categories = []
        self.idxchannel_categories = []

        self.setup_ui()

    def setup_ui(self):
        main_layout = QVBoxLayout()

        horizontal_scroll = QScrollArea() 
        horizontal_scroll.setWidgetResizable(True) 
        horizontal_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded) 
        horizontal_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)

        sources_container = QWidget() 
        sources_layout = QHBoxLayout(sources_container)

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

        idnfinancials_widget = self.create_no_category_source_column(
            "idnfinancials.com",
            source="idnfinancials",
        )

        idxchannel_widget = self.create_source_column(
            "Idxchannel.com",
            IDXCHANNEL_CATEGORIES,
            default_categories=["Market news", "Economics"],
            source="idxchannel",
        )

        sources_layout.addWidget(cnbc_widget)
        sources_layout.addWidget(bisnis_widget)
        sources_layout.addWidget(
            idnfinancials_widget, 
            alignment=Qt.AlignmentFlag.AlignTop,
        )
        sources_layout.addWidget(idxchannel_widget)

        sources_layout.addStretch() 
        horizontal_scroll.setWidget(sources_container) 
        main_layout.addWidget(horizontal_scroll)
        
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
        elif source == "bisnis":
            self.bisnis_checkbox = source_checkbox
            self.bisnis_categories = category_checkboxes
        else:
            self.idxchannel_checkbox = source_checkbox
            self.idxchannel_categories = category_checkboxes

        source_checkbox.stateChanged.connect(
            lambda state, source=source: self.source_changed(source)
        )

        vertical_scroll = QScrollArea()
        vertical_scroll.setWidgetResizable(True)
        vertical_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff) 
        vertical_scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAsNeeded) 
        vertical_scroll.setWidget(category_container) 
        layout.addWidget(vertical_scroll)

        return widget

    def create_no_category_source_column(
        self,
        source_name,
        source,
    ):
        widget = QWidget()
        layout = QVBoxLayout(widget)

        source_checkbox = QCheckBox(source_name)
        source_checkbox.setChecked(True)
        layout.addWidget(source_checkbox)

        if source == "idnfinancials":
            self.idnfinancials_checkbox = source_checkbox

        source_checkbox.stateChanged.connect(
            lambda state, source=source: self.source_changed(source)
        )

        widget.setMinimumWidth(160)

        return widget

    def source_changed(self, source):
        if self._updating:
            return

        self._updating = True

        if source == "cnbc":
            source_checkbox = self.cnbc_checkbox
            categories = self.cnbc_categories
        elif source == "bisnis":
            source_checkbox = self.bisnis_checkbox
            categories = self.bisnis_categories
        elif source == "idnfinancials":
            self._updating = False
            if self.idnfinancials_checkbox.isChecked(): 
                self.no_scrape_checkbox.setChecked(False)
            self.state_changed.emit()
            return
        elif source == "idxchannel":
            source_checkbox = self.idxchannel_checkbox
            categories = self.idxchannel_categories

        checked = source_checkbox.isChecked()

        if checked:
            self.no_scrape_checkbox.setChecked(False)

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
        elif source == "bisnis":
            source_checkbox = self.bisnis_checkbox
            categories = self.bisnis_categories
        elif source == "idxchannel":
            source_checkbox = self.idxchannel_checkbox
            categories = self.idxchannel_categories
        else:
            return

        any_checked = any(checkbox.isChecked() for _, checkbox in categories)

        self._updating = True
        source_checkbox.setChecked(any_checked)

        if any_checked: 
            self.no_scrape_checkbox.setChecked(False)

        self._updating = False

        self.state_changed.emit()

    def get_selected_sources(self):
        selected = {
            "cnbc": [],
            "bisnis": [],
            "idnfinancials": False,
            "idxchannel": [],
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

        if self.idnfinancials_checkbox.isChecked():
            selected["idnfinancials"] = True

        if self.idxchannel_checkbox.isChecked():
            selected["idxchannel"] = [
                category
                for category, checkbox in self.idxchannel_categories
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
            self.idnfinancials_checkbox.setChecked(False)
            self.idxchannel_checkbox.setChecked(False)

            for _, checkbox in self.cnbc_categories:
                checkbox.setChecked(False)

            for _, checkbox in self.bisnis_categories:
                checkbox.setChecked(False)

            for _, checkbox in self.idxchannel_categories:
                checkbox.setChecked(False)

        self._updating = False
        self.state_changed.emit()
