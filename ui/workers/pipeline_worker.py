# ui/workers/pipeline_worker.py

from PySide6.QtCore import QObject, Signal, Slot

from db.schema import create_tables
from db.keywords import load_keywords_from_csv
from db.articles import insert_articles

from labeling.keyword_labeler import run_labeling

from export.report_builder import build_all_sheets_by_date
from export.excel_export import export_sheets_to_excel

from notifications import notify_done

from scraper.cnbc import scrape_cnbc
from scraper.bisnis import scrape_bisnis


class PipelineWorker(QObject):

    log = Signal(str)
    progress = Signal(int)
    finished = Signal(str)
    error = Signal(str)

    def __init__(
        self,
        sources,
        scrape_days,
        export_dates,
        export_path,
    ):
        super().__init__()

        self.sources = sources
        self.scrape_days = scrape_days
        self.export_dates = export_dates
        self.export_path = export_path

    @Slot()
    def run(self):
        try:
            self.run_pipeline()

        except Exception as e:
            self.error.emit(str(e))

    def run_pipeline(self):

        self.log.emit("")
        self.log.emit("--- Preparing database ---")

        create_tables()
        self.progress.emit(5)

        self.log.emit("")
        self.log.emit("--- Loading keywords ---")
        load_keywords_from_csv()

        self.progress.emit(10)

        all_scrapers = [
            ("cnbc", scrape_cnbc),
            ("bisnis", scrape_bisnis),
        ]

        self.log.emit("")
        self.log.emit("--- Scraping ---")

        for source_name, scrape_function in all_scrapers:

            categories = self.sources.get(
                source_name,
                []
            )

            if not categories:
                self.log.emit("")
                self.log.emit(f"{source_name}: skipped")
                continue

            self.log.emit("")
            self.log.emit(f"--- Scraping {source_name} ---")
            self.log.emit("Categories:")

            for category in categories:
                self.log.emit(f"  - {category['name']}")

            try:
                data = scrape_function(
                    days=self.scrape_days,
                    category_list=categories,
                )
                self.log.emit(f"{source_name}: {len(data)} articles scraped")

                insert_articles(data)
                self.log.emit(f"{source_name}: articles inserted")

            except Exception as e:
                self.log.emit(f"{source_name} scraper failed: {e}")
                continue

        self.progress.emit(50)

        self.log.emit("")
        self.log.emit("--- Running labeling ---")

        run_labeling()
        self.log.emit("Labeling complete.")

        self.progress.emit(70)

        self.log.emit("")
        self.log.emit("--- Exporting to Excel ---")

        if self.export_dates["mode"] == "all":
            self.log.emit("Export range: all available data")

            sheets = build_all_sheets_by_date(all_date=True)
        else:
            start_date = self.export_dates["start"]
            end_date = self.export_dates["end"]

            self.log.emit(f"Export start: {start_date}")
            self.log.emit(f"Export end: {end_date}")

            sheets = build_all_sheets_by_date(
                start_date=start_date,
                end_date=end_date,
            )

        self.progress.emit(85)

        self.log.emit("Report data prepared.")

        final_path = export_sheets_to_excel(
            sheets,
            filepath=self.export_path,
        )

        self.log.emit(f"Report saved to: {final_path}")
        self.progress.emit(95)

        notify_done(message=f"Report saved to {final_path}")

        self.log.emit("Notification sent.")
        self.progress.emit(100)

        self.log.emit("")
        self.log.emit("=== PIPELINE COMPLETE ===")

        self.finished.emit(str(final_path))