import random
import sqlite3

def get_db_connection():
    conn = sqlite3.connect("waste_bins.db")
    conn.row_factory = sqlite3.Row
    return conn


def create_table():
    conn = get_db_connection()

    # Store registered bins
    conn.execute("""
        CREATE TABLE IF NOT EXISTS bins (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bin_id TEXT UNIQUE NOT NULL,
            location TEXT NOT NULL,
            fill_level INTEGER DEFAULT 0,
            status TEXT DEFAULT 'Normal',
            fill_rate INTEGER DEFAULT 1
        )
    """)

    # Add fill_rate column to existing databases if needed
    columns = [
        row["name"]
        for row in conn.execute("PRAGMA table_info(bins)").fetchall()
    ]

    if "fill_rate" not in columns:
        conn.execute(
            "ALTER TABLE bins ADD COLUMN fill_rate INTEGER DEFAULT 1"
        )

        existing_bins = conn.execute(
            "SELECT id FROM bins"
        ).fetchall()

        for bin in existing_bins:
            conn.execute(
                "UPDATE bins SET fill_rate = ? WHERE id = ?",
                (random.randint(1, 5), bin["id"])
            )

    # Store completed waste collections
    conn.execute("""
        CREATE TABLE IF NOT EXISTS collection_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            bin_id TEXT NOT NULL,
            location TEXT NOT NULL,
            collected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)

    conn.commit()
    conn.close()
