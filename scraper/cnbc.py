# scraper\cnbc.py
import requests
import time
from bs4 import BeautifulSoup
from config import HEADERS
from utils import get_cutoff_date, cnbc_date

def scrape_cnbc(max_page=2000, days=2):
    old_article_threshold = days * 2
    cutoff_date = get_cutoff_date(days=days)
    results = []
    page = 1
    old_article_count = 0

    while page <= max_page:
        url = f"https://www.cnbcindonesia.com/indeks?page={page}"
        resp = requests.get(url, headers=HEADERS, timeout=15)
        soup = BeautifulSoup(resp.text, "html.parser")

        articles = soup.find_all("article")

        if not articles:
            print(f"article not found on page {page}")
            break

        stop_scraping = False

        for article in articles:
            link_tag = article.find("a")
            if not link_tag:
                continue
            title_tag = article.find("h2")
            if not title_tag:
                continue

            title_scraped = title_tag.get_text(strip=True)
            link_scraped = link_tag.get("href")

            date_formatted = cnbc_date(link_scraped)

            if date_formatted is None:
                continue

            if date_formatted < cutoff_date:
                old_article_count += 1
                if old_article_count >= old_article_threshold:
                    print(f"Hit {old_article_threshold} old articles in a row, stopping.")
                    stop_scraping = True
                    break
                continue

            category = link_scraped.split("https://www.cnbcindonesia.com/")[1].split("/")[0].title()

            results.append({
                "date": date_formatted,
                "url": link_scraped,
                "source": "cnbcindonesia.com",
                "category": category,
                "title": title_scraped,
                "content": None,
            })

        print(f"CNBC Indonesia.com, Page {page}: collected {len(results)} total so far")

        if stop_scraping:
            break

        page += 1
        time.sleep(1) 

    return results
