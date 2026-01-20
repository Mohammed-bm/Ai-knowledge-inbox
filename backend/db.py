import sqlite3

conn = sqlite3.connect("items.db", check_same_thread=False)
cursor = conn.cursor()

# Enable foreign key enforcement
cursor.execute("PRAGMA foreign_keys = ON;")

# Items table
cursor.execute("""
CREATE TABLE IF NOT EXISTS items (
    id TEXT PRIMARY KEY,
    type TEXT NOT NULL CHECK(type IN ('note', 'url')),
    source TEXT,
    raw_text TEXT NOT NULL,
    created_at TEXT DEFAULT (datetime('now'))
)
""")

# Chunks table
cursor.execute("""
CREATE TABLE IF NOT EXISTS chunks (
    chunk_id TEXT PRIMARY KEY,
    item_id TEXT NOT NULL,
    chunk_text TEXT NOT NULL,
    embedding TEXT NOT NULL,
    FOREIGN KEY(item_id) REFERENCES items(id) ON DELETE CASCADE
)
""")

conn.commit()