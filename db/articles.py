# db/articles.py

import sqlite3

from db.connection import get_connection


def insert_articles(data):
    conn = get_connection()
    cursor = conn.cursor()

    inserted = 0
    skipped = 0

    for item in data:
        date_value = item.get("date")

        if hasattr(date_value, "isoformat"):
            date_value = date_value.isoformat()

        try:
            cursor.execute(
                """
                INSERT INTO raw (
                    date,
                    url,
                    source,
                    category,
                    title,
                    content,
                    is_labeled
                )
                VALUES (?, ?, ?, ?, ?, ?, 0)
                """,
                (
                    date_value,
                    item.get("url"),
                    item.get("source"),
                    item.get("category"),
                    item.get("title"),
                    item.get("content"),
                ),
            )
            inserted += 1

        except sqlite3.IntegrityError:
            skipped += 1

    conn.commit()
    conn.close()

    print(f"Inserted {inserted} new articles, skipped {skipped} duplicates.")


def get_unlabeled_articles(limit=None):
    conn = get_connection()
    cursor = conn.cursor()

    if limit:
        cursor.execute(
            "SELECT id, title FROM raw WHERE is_labeled = 0 LIMIT ?",
            (limit,),
        )
    else:
        cursor.execute("SELECT id, title FROM raw WHERE is_labeled = 0")

    rows = cursor.fetchall()
    conn.close()

    return rows


def mark_as_labeled(raw_id):
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute(
        "UPDATE raw SET is_labeled = 1 WHERE id = ?",
        (raw_id,),
    )

    conn.commit()
    conn.close()
