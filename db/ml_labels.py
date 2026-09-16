# db/ml_labels.py

from db.connection import get_connection

def save_ml_labels(ml_labels):
    conn = get_connection()
    cursor = conn.cursor()

    for raw_id, label, score in ml_labels:
        cursor.execute(
            """
            INSERT INTO ml_label (raw_id, label, score)
            VALUES (?, ?, ?)
            """,
            (raw_id, label, score)
        )

    conn.commit()
    conn.close()


def get_ml_labels(raw_ids):
    if not raw_ids:
        return {}

    conn = get_connection()
    cursor = conn.cursor()

    placeholders = ",".join("?" * len(raw_ids))

    cursor.execute(
        f"""
        SELECT raw_id, label, score
        FROM ml_label
        WHERE raw_id IN ({placeholders})
        """,
        raw_ids
    )

    rows = cursor.fetchall()
    conn.close()

    result = {}

    for raw_id, label, score in rows:
        result.setdefault(raw_id, []).append((label, score))

    return result


def clear_ml_labels():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("DELETE FROM ml_label")

    conn.commit()
    conn.close()