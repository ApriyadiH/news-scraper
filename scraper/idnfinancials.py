# scraper/idnfinancial.py

import time
from bs4 import BeautifulSoup
from config import HEADERS
from utils.date_utils import get_cutoff_date, parse_iso_datetime
from utils.http_utils import fetch_page


def scrape_idnfinancials(days=2):
    cutoff_date = get_cutoff_date(days=days)
    results = []

    url = "https://www.idnfinancials.com/sitemap-news-id.xml"

    resp = fetch_page(
        url,
        headers=HEADERS,
        retries=3,
        timeout=15,
    )

    if resp is None:
        print("Failed to fetch IDN Financial sitemap")
        return results

    soup = BeautifulSoup(resp.text, "xml")
    articles = soup.find_all("url")

    if not articles:
        print("Articles not found in IDN Financial sitemap")
        return results

    for article in articles:
        link_tag = article.find("loc")
        if not link_tag:
            continue

        title_tag = article.find("news:title")
        if not title_tag:
            continue

        date_tag = article.find("news:publication_date")
        if not date_tag:
            continue

        link_scraped = link_tag.get_text(strip=True)
        title_scraped = title_tag.get_text(strip=True)

        date_scraped = date_tag.get_text(strip=True)
        date_formatted = parse_iso_datetime(date_scraped).date()

        if date_formatted < cutoff_date:
            continue

        category = (
            link_scraped
            .split("https://www.idnfinancials.com/id/")[1]
            .split("/")[0]
        )

        results.append(
            {
                "date": date_formatted,
                "url": link_scraped,
                "source": "idnfinancial.com",
                "category": category,
                "title": title_scraped,
                "content": None,
            }
        )

        if len(results) % 10 == 0:
            print(
                f"IDNFinancials, collected {len(results)} total so far"
            )

    return results