# db\keywords.py

import csv
from db.connection import get_connection
from utils.path_utils import resource_path


def load_keywords_from_csv(filepath=None):
    if filepath is None:
        filepath = resource_path("data/keyword_map.csv")

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM keyword")

    with open(filepath, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f, delimiter=";")
        rows = [(row["keyword"], row["label"]) for row in reader]

    cursor.executemany("INSERT INTO keyword (keyword, label) VALUES (?, ?)", rows)

    conn.commit()
    conn.close()
    print(f"Loaded {len(rows)} keyword-label pairs from {filepath}")


def get_all_keywords():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT keyword, label FROM keyword")
    rows = cursor.fetchall()
    conn.close()
    return rows
