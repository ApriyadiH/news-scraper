# db\connection.py
import sqlite3
import os
from utils import get_app_data_dir

DB_PATH = os.path.join(get_app_data_dir(), "news.db")

def get_connection():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("PRAGMA foreign_keys = ON")
    return conn