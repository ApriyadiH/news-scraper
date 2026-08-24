# ui\main_window.py

from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout
from ui.widgets.main_window.source_selector import SourceSelector
from ui.widgets.main_window.date_selector import DateSelector
from ui.widgets.main_window.export_selector import ExportSelector
from ui.widgets.main_window.start_section import StartSection
from ui.loading_window import LoadingWindow


class MainWindow(QMainWindow):
    def __init__(self, debug=False):
        super().__init__()
        self.debug = debug
        self.resize(500, 650)
        self.setup_ui()
        self.setup_debug()

    def setup_ui(self):
        central_widget = QWidget()
        layout = QVBoxLayout()

        self.source_selector = SourceSelector()
        self.date_selector = DateSelector()
        self.export_selector = ExportSelector()
        self.start_section = StartSection()
        self.start_section.start_button.clicked.connect(self.start_scraping)

        layout.addWidget(self.source_selector)
        layout.addWidget(self.date_selector)
        layout.addWidget(self.export_selector)
        layout.addWidget(self.start_section)

        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

    def setup_debug(self):
        if not self.debug:
            return

        print("=== DEBUG MODE ENABLED ===")

        # Source selector
        self.source_selector.state_changed.connect(self.debug_source_selector)

        # Date selector
        self.date_selector.scrape_days.valueChanged.connect(self.debug_date_selector)

        self.date_selector.export_all.toggled.connect(self.debug_date_selector)

        self.date_selector.start_date.dateChanged.connect(self.debug_date_selector)

        self.date_selector.end_date.dateChanged.connect(self.debug_date_selector)

        # Export selector
        self.export_selector.path_input.textChanged.connect(self.debug_export_selector)

    def debug_source_selector(self):
        print("\n=== SOURCE SELECTOR ===")

        selected = self.source_selector.get_selected_sources()

        print("CNBC:")
        for category in selected["cnbc"]:
            print(f"  - {category['name']}")

        print("Bisnis:")
        for category in selected["bisnis"]:
            print(f"  - {category['name']}")

        print("Don't scrape:", not self.source_selector.should_scrape())

        print("========================")

    def debug_date_selector(self):
        print("\n=== DATE SELECTOR ===")

        scrape_days = self.date_selector.get_scrape_days()
        export_dates = self.date_selector.get_export_dates()

        print("Scrape days:")
        print(f"  - {scrape_days} days")

        print("Export:")

        if export_dates["mode"] == "all":
            print("  - All available data")

        else:
            print(f"  - Start: {export_dates['start']}")
            print(f"  - End:   {export_dates['end']}")

        print("====================")

    def debug_export_selector(self):
        print("\n=== EXPORT SELECTOR ===")

        path = self.export_selector.get_export_path()

        if path:
            print(f"Export path: {path}")
        else:
            print("Export path: NOT SELECTED")

        print("========================")

    def start_scraping(self):
        sources = self.source_selector.get_selected_sources()
        scrape_days = self.date_selector.get_scrape_days()
        export_dates = self.date_selector.get_export_dates()
        export_path = self.export_selector.get_export_path()

        self.loading_window = LoadingWindow(
            sources=sources,
            scrape_days=scrape_days,
            export_dates=export_dates,
            export_path=export_path,
            main_window=self,
        )

        if self.debug:
            print("\n=== START SCRAPING ===")
            print(self.loading_window.get_settings())

        self.loading_window.show()
        self.hide()
        self.loading_window.start_pipeline()
