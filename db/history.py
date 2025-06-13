import sqlite3
from typing import List, Tuple

DB_PATH = "data/chat_history.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("""
    CREATE TABLE IF NOT EXISTS chat_history (
        session_ID TEXT,
        role TEXT,
        content TEXT
    )          
    """)
    conn.commit()
    conn.close()

def add_message(session_id: str, role: str, content: str):
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("INSERT INTO chat_history (session_id, role, content) VALUES (?, ?, ?)," \
    (session_id, role, content))
    conn.commit()
    conn.close()

def get_history(session_id: str) -> List[Tuple[str, str]]:
    conn = sqlite3.connect(DB_PATH)
    c = conn.cursor()
    c.execute("SELECT role, content from chat_history" \
    "WHERE session_id = ?", (session_id))
    rows = c.fetchall()
    conn.commit()
    conn.close()
    return rows