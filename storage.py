import sqlite3

DB_NAME = "pause.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS sessions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        duration INTEGER,
        status TEXT
    )
    """)

    conn.commit()
    conn.close()

def save_session(date, duration, status):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    INSERT INTO sessions
    (date, duration, status)
    VALUES (?, ?, ?)
    """, (date, duration, status))

    conn.commit()
    conn.close()

def get_sessions():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    SELECT date, duration, status
    FROM sessions
    ORDER BY id DESC
    """)

    rows = cursor.fetchall()

    conn.close()

    return rows
