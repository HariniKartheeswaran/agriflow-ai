import sqlite3, json, os

db_path = "memory.db"

def init_db():
    with sqlite3.connect(db_path) as conn:
        conn.execute('''
            CREATE TABLE IF NOT EXISTS history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                data TEXT NOT NULL
            )
        ''')

def save_memory(data):
    init_db()
    with sqlite3.connect(db_path, timeout=10) as conn:
        conn.execute("INSERT INTO history (data) VALUES (?)", (json.dumps(data),))
        conn.execute('''
            DELETE FROM history 
            WHERE id NOT IN (
                SELECT id FROM history ORDER BY id DESC LIMIT 20
            )
        ''')