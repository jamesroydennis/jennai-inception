import sqlite3
from pathlib import Path
import sys
import os

# Ensure config is importable
sys.path.append(str(Path(__file__).resolve().parents[4]))

from config.config import SCHEMA_PATH, DB_PATH

def initialize_database():
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema_sql = f.read()

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.executescript(schema_sql)
    conn.commit()
    conn.close()

    print(f"✅ Database created at: {DB_PATH}")

if __name__ == "__main__":
    initialize_database()
    if not DB_PATH.exists():
        print(f"Database file does not exist at {DB_PATH}. Initializing...")
        initialize_database()
    else:
        print(f"Database already exists at {DB_PATH}. No action taken.")