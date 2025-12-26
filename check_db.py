import sqlite3
import os
from src.config import DB_FILE

print(f"DB_FILE: {DB_FILE}")

if os.path.exists(DB_FILE):
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("SELECT count(*) FROM messages")
    count = cursor.fetchone()[0]
    print(f"Total messages: {count}")
    
    cursor.execute("SELECT character_name, count(*) FROM messages GROUP BY character_name")
    rows = cursor.fetchall()
    for row in rows:
        print(f"Character: {row[0]}, Messages: {row[1]}")
    
    conn.close()
else:
    print("DB File does not exist.")
