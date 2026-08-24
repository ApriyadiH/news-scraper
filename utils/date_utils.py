# utils\date_utils.py

from datetime import datetime, timedelta
from zoneinfo import ZoneInfo


def get_today():
    return datetime.now(ZoneInfo("Asia/Jakarta")).date()


def get_cutoff_date(days=2):
    date_output = get_today() - timedelta(days=days - 1)
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


def parse_iso_datetime(date_str):
    return datetime.fromisoformat(date_str)
