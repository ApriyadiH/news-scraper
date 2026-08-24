# db\labels.py

from db.connection import get_connection


def insert_label(raw_id, label):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO label (raw_id, label) VALUES (?, ?)", (raw_id, label)
    )
    conn.commit()
    conn.close()
