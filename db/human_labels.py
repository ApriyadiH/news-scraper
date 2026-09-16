# db\human_labels.py

from db.connection import get_connection

def save_human_labels(human_labels_dict):
    conn = get_connection()
    cursor = conn.cursor()

    for raw_id, labels in human_labels_dict.items():
        cursor.execute("DELETE FROM human_label WHERE raw_id = ?", (raw_id,))
        for label in labels:
            cursor.execute(
                "INSERT INTO human_label (raw_id, label) VALUES (?, ?)",
                (raw_id, label)
            )

    conn.commit()
    conn.close()


def get_human_labels(raw_ids):
    if not raw_ids:
        return {}

    conn = get_connection()
    cursor = conn.cursor()
    placeholders = ",".join("?" * len(raw_ids))
    cursor.execute(
        f"SELECT raw_id, label FROM human_label WHERE raw_id IN ({placeholders})",
        raw_ids
    )
    rows = cursor.fetchall()
    conn.close()

    result = {}
    for raw_id, label in rows:
        result.setdefault(raw_id, []).append(label)
    return result

def get_raw_missing_human_label(limit=15):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT 
            raw.id, 
            raw.title, 
            raw.url,
            GROUP_CONCAT(DISTINCT label.label) AS exact_labels
        FROM raw
        LEFT JOIN label ON raw.id = label.raw_id
        LEFT JOIN human_label ON raw.id = human_label.raw_id
        WHERE human_label.id IS NULL
        GROUP BY raw.id
        ORDER BY raw.id DESC
        LIMIT ?
    """, (limit,))
    rows = cursor.fetchall()
    conn.close()
    return rows


def get_raw_with_all_labels():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            raw.id,
            raw.title,

            (
                SELECT GROUP_CONCAT(DISTINCT label.label)
                FROM label
                WHERE label.raw_id = raw.id
            ) AS exact_labels,

            (
                SELECT GROUP_CONCAT(
                    ml_label.label || ':' || ml_label.score
                )
                FROM ml_label
                WHERE ml_label.raw_id = raw.id
            ) AS ml_labels,

            (
                SELECT GROUP_CONCAT(DISTINCT human_label.label)
                FROM human_label
                WHERE human_label.raw_id = raw.id
            ) AS human_labels

        FROM raw
        ORDER BY raw.id DESC
    """)

    rows = cursor.fetchall()
    conn.close()

    return rows

def get_training_data():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT
            raw.id,
            raw.title,
            GROUP_CONCAT(DISTINCT human_label.label)
        FROM raw
        JOIN human_label ON raw.id = human_label.raw_id
        GROUP BY raw.id
        ORDER BY raw.id
    """)

    rows = cursor.fetchall()
    conn.close()

    return rows