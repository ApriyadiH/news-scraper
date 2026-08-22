# main.py
from db.schema import create_tables
from db.keywords import load_keywords_from_csv
from db.articles import insert_articles
from labeling.keyword_labeler import run_labeling
from export.report_builder import build_all_sheets
from export.excel_export import export_sheets_to_excel
from notifications import notify_done

from scraper.cnbc import scrape_cnbc
from scraper.bisnis import scrape_bisnis

def ask_days(prompt_text, default=2):
    while True:
        raw_input_value = input(f"{prompt_text} (default {default}): ").strip()
        if raw_input_value == "":
            return default
        if raw_input_value.isdigit() and int(raw_input_value) > 0:
            return int(raw_input_value)
        print("Please enter a positive whole number.")


def run_pipeline(scrape_days, export_days):
    create_tables()
    load_keywords_from_csv()

    all_scrapers = [
        ("cnbc", scrape_cnbc),
        ("bisnis", scrape_bisnis),
    ]

    for source_name, scrape_function in all_scrapers:
        print(f"\n--- Scraping {source_name} ---")

        try:
            data = scrape_function(days=scrape_days)
            print(f"{source_name}: {len(data)} articles scraped")
            insert_articles(data)

        except Exception as e:
            print(f"{source_name} scraper failed: {e}")
            continue

    print("\n--- Running labeling ---")
    run_labeling()

    print("\n--- Exporting to Excel ---")
    sheets = build_all_sheets(days=export_days)
    final_path = export_sheets_to_excel(sheets)
    print(f"\nDone! Check {final_path} for your report.")

    notify_done(message=f"Report saved to {final_path}")

if __name__ == "__main__":
    print("=== News Scraper ===\n")
    print("\nWARNING: Please close report.xlsx before you start!")
    scrape_days = ask_days("How many days back should I scrape?")
    export_days = ask_days("How many days back should the export cover?")

    run_pipeline(scrape_days, export_days)
    input("\nPress Enter to exit...")
