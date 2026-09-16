# db/labels.py
from db.connection import get_connection


def insert_label(raw_id, label):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO label (raw_id, label) VALUES (?, ?)", (raw_id, label)
    )
    conn.commit()
    conn.close()


def get_raw_with_labels():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT raw.id, raw.title, GROUP_CONCAT(label.label, ', ') AS labels
        FROM raw
        LEFT JOIN label ON raw.id = label.raw_id
        GROUP BY raw.id
        ORDER BY raw.id DESC
    """)
    rows = cursor.fetchall()
    conn.close()
    return rows