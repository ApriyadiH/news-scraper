# scraper\idxchannel.py

import time
from bs4 import BeautifulSoup
from config import HEADERS, IDXCHANNEL_CATEGORIES
from utils.date_utils import get_cutoff_date, parse_iso_datetime
from utils.http_utils import fetch_page

def scrape_idxchannel(days=2, category_list=IDXCHANNEL_CATEGORIES):
    cutoff_date = get_cutoff_date(days=days)
    results = []

    for category in category_list:
        url = f"https://www.idxchannel.com/{category['id']}/sitemap.xml"
        resp = fetch_page(url, headers=HEADERS, retries=3, timeout=15)

        if resp is None:
            print("Failed to fetch IDX Channel sitemap")
            continue

        soup = BeautifulSoup(resp.text, "xml")

        articles = soup.find_all("url")

        if not articles:
            print(f"article not found on {category['name']}")
            continue

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

            results.append(
                {
                    "date": date_formatted,
                    "url": link_scraped,
                    "source": "idxchannel.com",
                    "category": category["name"],
                    "title": title_scraped,
                    "content": None,
                }
            )

        print(
            f"IDX Channel, category {category['name']} collected {len(results)} total so far"
        )
        time.sleep(1)
    return results
