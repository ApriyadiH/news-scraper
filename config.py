# config.py

import os
from dotenv import load_dotenv

load_dotenv()

CONTACT_EMAIL = os.getenv("SCRAPER_CONTACT_EMAIL")

HEADERS = {
    "User-Agent": f"MarketNewsScraper/1.0 (contact: {CONTACT_EMAIL})",
}

BISNIS_CATEGORIES = [
    {"id": "1", "name": "Rekomendasi"},
    {"id": "655", "name": "Premium"},
    {"id": "194", "name": "Market"},
    {"id": "5", "name": "Finansial"},
    {"id": "43", "name": "Ekonomi"},
    {"id": "277", "name": "Tekno"},
    {"id": "197", "name": "Style"},
    {"id": "186", "name": "Kabar"},
    {"id": "650", "name": "Hijau"},
    {"id": "392", "name": "Bola"},
    {"id": "547", "name": "Infografik"},
    {"id": "272", "name": "Otomotif"},
    {"id": "258", "name": "Entrepreneur"},
    {"id": "222", "name": "Travel"},
    {"id": "382", "name": "Jakarta"},
    {"id": "548", "name": "Bandung"},
    {"id": "420", "name": "Banten"},
    {"id": "528", "name": "Semarang"},
    {"id": "526", "name": "Surabaya"},
    {"id": "529", "name": "Bali"},
    {"id": "527", "name": "Sumatera"},
    {"id": "406", "name": "Kalimantan"},
    {"id": "530", "name": "Sulawesi"},
    {"id": "413", "name": "Papua"},
    {"id": "242", "name": "Koran"},
    {"id": "638", "name": "Viral"},
    {"id": "390", "name": "Ramadan"},
    {"id": "551", "name": "Video"},
]

CNBC_CATEGORIES = [
    {"id": "market", "name": "Market"},
    {"id": "news", "name": "News"},
    {"id": "entrepreneur", "name": "Entrepreneur"},
    {"id": "syariah", "name": "Syariah"},
    {"id": "tech", "name": "Tech"},
    {"id": "lifestyle", "name": "Lifestyle"},
    {"id": "opini", "name": "Opini"},
    {"id": "mymoney", "name": "My money"},
    {"id": "cuap-cuap-cuan", "name": "Cuap cuap cuan"},
    {"id": "research", "name": "Research"},
]
