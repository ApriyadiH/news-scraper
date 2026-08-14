# utils.py
from datetime import datetime, timedelta
from datetime import date as date_class
from zoneinfo import ZoneInfo
import sys
import os

def get_app_data_dir():
    if getattr(sys, 'frozen', False):
        base_dir = os.path.join(os.environ["LOCALAPPDATA"], "NewsScraperApp")
    else:
        base_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")

    os.makedirs(base_dir, exist_ok=True)
    return base_dir

def get_app_dir():
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))

def resource_path(relative_path):
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)

def get_today():
    date_output = datetime.now(ZoneInfo("Asia/Jakarta")).date() 
    return date_output

def get_cutoff_date(days=2):
    date_output = get_today() - timedelta(days=days-1) 
    return date_output

def convert_date(date_str):
    month_map = {
        "Jan": "01", 
        "Januari": "01",
        "January": "01",
        "Feb": "02", 
        "Februari": "02",
        "February": "02",
        "Mar": "03", 
        "Maret": "03", 
        "March": "03",
        "Apr": "04", 
        "April": "04",
        "May": "05",
        "Mei": "05", 
        "Jun": "06", 
        "Juni": "06",
        "June": "06", 
        "Jul": "07", 
        "Juli": "07", 
        "July": "07", 
        "Agu": "08",
        "Agt": "08",
        "Aug": "08",
        "Agustus": "08",
        "August": "08",
        "Sep": "09", 
        "September": "09", 
        "Okt": "10", 
        "Oct": "10",
        "Oktober": "10", 
        "Nov": "11", 
        "November": "11", 
        "Des": "12",
        "Dec": "12",
        "Desember": "12",
    }
    day, month_name, year = date_str.strip().split(" ")
    month_number = month_map[month_name]
    day = day.zfill(2)
    date_string = f"{day}-{month_number}-{year}"
    date_output = datetime.strptime(date_string, "%d-%m-%Y").date()
    return date_output

def convert_relative_date(date_str):
    date_str = date_str.strip().lower()

    if "hari yang lalu" in date_str:
        match = date_str.split(" hari yang lalu")[0]
        days = int(match) if match else 0
        return get_today() - timedelta(days=days)

    if "jam yang lalu" in date_str or "menit yang lalu" in date_str or "detik yang lalu" in date_str:
        return get_today()

    raise ValueError(f"Unrecognized relative date format: {date_str}")

from datetime import date as date_class

def cnbc_date(url):
    try:
        hasil = url.split("https://www.cnbcindonesia.com/")[1]
        hasil = hasil.split("/")[1]
        tahun = hasil[:4]
        bulan = hasil[4:6]
        tanggal = hasil[6:8]
        return date_class(int(tahun), int(bulan), int(tanggal))
    except (IndexError, ValueError):
        return None
    
if __name__ == "__main__":
    print("App data dir:", get_app_data_dir())