# scraper\bisnis.py

import time
from bs4 import BeautifulSoup
from config import HEADERS, BISNIS_CATEGORIES
from utils.date_utils import get_today, get_cutoff_date, convert_date
from utils.http_utils import fetch_page

def scrape_bisnis(max_page=17, days=2, category_list=BISNIS_CATEGORIES):
    cutoff_date = get_cutoff_date(days=days)
    results = []

    for category in category_list:
        page = 1
        while page <= max_page:
            url = f"https://www.bisnis.com/index?categoryId={category['id']}&type=indeks&page={page}"
            resp = fetch_page(
                url, 
                headers = HEADERS, 
                retries=3,
                timeout=15
            )
            
            soup = BeautifulSoup(resp.text, "html.parser")

            articles = soup.find_all("div", class_="art--row")

            if not articles:
                print(f"article not found on page {page}")
                break

            stop_scraping = False

            for article in articles:
                link_tag = article.find("a", class_="artLink")
                if not link_tag:
                    continue
                title_tag = article.find("h4")
                if not title_tag:
                    continue
                date_tag = article.find("div", class_="artDate")
                if not date_tag:
                    continue

                title_scraped = title_tag.get_text(strip=True)
                link_scraped = link_tag.get("href")
                date_scraped = date_tag.get_text(strip=True)
                is_today = "jam yang lalu" in date_scraped or "menit yang lalu" in date_scraped or "detik yang lalu" in date_scraped

                if is_today:
                    date_formatted = get_today()
                else:
                    date_formatted = convert_date(date_scraped.split(" | ")[0])

                if  not is_today and date_formatted < cutoff_date:
                    stop_scraping = True
                    break

                results.append({
                    "date": date_formatted,
                    "url": link_scraped,
                    "source": "bisnis.com",
                    "category": category['name'],
                    "title": title_scraped,
                    "content": None,
                })

            print(f"Bisnis.com, Category {category['name']}, Page {page}: collected {len(results)} total so far")
            
            if stop_scraping:
                break
            
            page += 1
            time.sleep(1) 

    return results