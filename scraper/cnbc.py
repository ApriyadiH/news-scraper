# scraper\cnbc.py

import time
from bs4 import BeautifulSoup
from config import HEADERS, CNBC_CATEGORIES
from utils.date_utils import get_cutoff_date, parse_iso_datetime
from utils.http_utils import fetch_page


def scrape_cnbc(days=2, category_list=CNBC_CATEGORIES):
    old_article_threshold = days * 2
    cutoff_date = get_cutoff_date(days=days)
    results = []

    for category in category_list:
        url = f"https://www.cnbcindonesia.com/{category['id']}/sitemap_news.xml"
        resp = fetch_page(url, headers=HEADERS, retries=3, timeout=15)

        if resp is None:
            print("Failed to fetch CNBC sitemap")
            continue

        soup = BeautifulSoup(resp.text, "xml")

        old_article_count = 0
        articles = soup.find_all("url")

        if not articles:
            print(f"article not found on {category['name']}")
            break

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
                old_article_count += 1
                if old_article_count >= old_article_threshold:
                    print(
                        f"Hit {old_article_threshold} old articles in a row, stopping."
                    )
                    break
                continue

            results.append(
                {
                    "date": date_formatted,
                    "url": link_scraped,
                    "source": "cnbcindonesia.com",
                    "category": category["name"],
                    "title": title_scraped,
                    "content": None,
                }
            )

        print(
            f"CNBC Indonesia.com, category {category['name']} collected {len(results)} total so far"
        )
        time.sleep(1)
    return results
