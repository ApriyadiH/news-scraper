# scraper\kontan.py
import requests
import time
from datetime import timedelta
from bs4 import BeautifulSoup
from config import HEADERS
from utils import get_today, get_cutoff_date, convert_date

def scrape_kontan(max_article=1000, days=2):
    cutoff_date = get_cutoff_date(days=days)
    current_date = get_today()
    results = []

    while current_date >= cutoff_date:
        day = f"{current_date.day:02d}"
        month = f"{current_date.month:02d}"
        year = current_date.year

        article_count = 0

        while article_count <= max_article:
            url = f"https://www.kontan.co.id/search/indeks?kanal=&tanggal={day}&bulan={month}&tahun={year}&pos=indeks&per_page={article_count}"
            resp = requests.get(url, headers=HEADERS, timeout=10)
            soup = BeautifulSoup(resp.text, "html.parser")

            article_list = soup.find("div", class_="list-berita")
            if article_list is None:
                break

            articles = article_list.find_all("li")

            if not articles:
                break

            for article in articles:
                link_tag = article.find("a")
                if not link_tag:
                    continue
                title_tag = article.find("h1")
                if not title_tag:
                    continue
                date_tag = article.find_all("span")[1]
                if not date_tag:
                    continue

                title_scraped = title_tag.get_text(strip=True)
                link_scraped = link_tag.get("href")
                date_scraped = date_tag.get_text(strip=True).split("| ")[1]
                date_formatted = convert_date(date_scraped)

                category = link_scraped.split("https://")[1].split(".kontan.co.id/")[0].title()

                results.append({
                    "date": date_formatted,
                    "url": link_scraped,
                    "source": "kontan.co.id",
                    "category": category,
                    "title": title_scraped,
                    "content": None,
                })
            print(f"kontan.co.id, {year}-{month}-{day}, article {article_count + 1} to {article_count + 20}: {len(results)} total so far")    
            article_count += 20
            time.sleep(1) 

        current_date -= timedelta(days=1)

    return results
