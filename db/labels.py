# db\labels.py
from db.connection import get_connection

def insert_label(raw_id, label):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "INSERT OR IGNORE INTO label (raw_id, label) VALUES (?, ?)",
        (raw_id, label)
    )
    conn.commit()
    conn.close()

def get_labels_for_article(raw_id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT label FROM label WHERE raw_id = ?", (raw_id,))
    rows = cursor.fetchall()
    conn.close()
    return [row[0] for row in rows]

def clear_all_labels():
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM label")
    conn.commit()
    conn.close()
    print("Cleared all rows from label table.")