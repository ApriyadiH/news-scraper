# ui/widgets/main_window/date_selector.py

from datetime import date, timedelta

from PySide6.QtCore import QDate
from PySide6.QtWidgets import (
    QCheckBox,
    QDateEdit,
    QGridLayout,
    QGroupBox,
    QLabel,
    QSpinBox,
)


class DateSelector(QGroupBox):
    def __init__(self, parent=None):
        super().__init__("Date", parent)

        self.setup_ui()

    def setup_ui(self):
        layout = QGridLayout()

        layout.addWidget(QLabel("Scraping period"), 0, 0)
        layout.addWidget(QLabel("Export"), 0, 1)

        scrape_row = QGridLayout()

        scrape_label = QLabel("Number of days:")

        self.scrape_days = QSpinBox()
        self.scrape_days.setMinimum(1)
        self.scrape_days.setMaximum(30)
        self.scrape_days.setValue(2)

        scrape_days_label = QLabel("days")

        scrape_row.addWidget(scrape_label, 0, 0)
        scrape_row.addWidget(self.scrape_days, 0, 1)
        scrape_row.addWidget(scrape_days_label, 0, 2)

        layout.addLayout(scrape_row, 1, 0)

        self.export_all = QCheckBox("All available data")
        self.export_all.setChecked(True)

        layout.addWidget(self.export_all, 1, 1)

        self.scrape_start_label = QLabel()
        layout.addWidget(self.scrape_start_label, 2, 0)

        start_row = QGridLayout()
        start_row.addWidget(QLabel("Start:"), 0, 0)

        self.start_date = QDateEdit()
        self.start_date.setCalendarPopup(True)
        self.start_date.setDate(QDate.currentDate().addDays(-1))

        start_row.addWidget(self.start_date, 0, 1)
        layout.addLayout(start_row, 2, 1)

        self.scrape_end_label = QLabel()
        layout.addWidget(self.scrape_end_label, 3, 0)

        end_row = QGridLayout()
        end_row.addWidget(QLabel("End:"), 0, 0)

        self.end_date = QDateEdit()
        self.end_date.setCalendarPopup(True)
        self.end_date.setDate(QDate.currentDate())

        end_row.addWidget(self.end_date, 0, 1)
        layout.addLayout(end_row, 3, 1)

        self.start_date.setEnabled(False)
        self.end_date.setEnabled(False)

        self.export_all.toggled.connect(self.toggle_export_dates)
        self.scrape_days.valueChanged.connect(self.update_scrape_preview)

        self.setLayout(layout)

        self.update_scrape_preview()

    def update_scrape_preview(self):
        days = self.scrape_days.value()
        today = date.today()

        start_date = today
        end_date = today - timedelta(days=days - 1)

        self.scrape_start_label.setText(
            f"Start date: {start_date.strftime('%d %B %Y')}"
        )

        self.scrape_end_label.setText(f"End date: {end_date.strftime('%d %B %Y')}")

    def toggle_export_dates(self, all_data):
        self.start_date.setEnabled(not all_data)
        self.end_date.setEnabled(not all_data)

    def get_scrape_days(self):
        return self.scrape_days.value()

    def get_export_dates(self):
        if self.export_all.isChecked():
            return {"mode": "all"}

        start = self.start_date.date().toPython()
        end = self.end_date.date().toPython()

        return {
            "mode": "date",
            "start": start,
            "end": end,
        }
