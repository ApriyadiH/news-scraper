# db\schema.py
from db.connection import get_connection

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS raw (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date DATE,
            url TEXT NOT NULL UNIQUE,
            source TEXT,
            category TEXT,
            title TEXT NOT NULL,
            content TEXT,
            is_labeled BOOLEAN NOT NULL DEFAULT 0
        )
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_raw_is_labeled ON raw(is_labeled)
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS keyword (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            keyword TEXT NOT NULL,
            label TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS label (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            raw_id INTEGER NOT NULL,
            label TEXT NOT NULL,
            UNIQUE(raw_id, label),
            FOREIGN KEY (raw_id) REFERENCES raw(id)
        )
    """)

    cursor.execute("""
        CREATE INDEX IF NOT EXISTS idx_label_raw_id ON label(raw_id)
    """)

    conn.commit()
    conn.close()
    print("Tables created (or already exist).")

if __name__ == "__main__":
    create_tables()