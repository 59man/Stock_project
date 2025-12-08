
'''script for creating databeses '''


import sqlite3
from pathlib import Path

conn = sqlite3.connect('backend/Data.db')
c = conn.cursor()
sql_dir = Path("backend/sql_tables")

for sql_file in sql_dir.glob("*.sql"):
    with open(sql_file, "r", encoding="utf-8") as f:
        sql_script = f.read()
        print(f"Executing: {sql_file.name}")
        c.executescript(sql_script)

conn.commit()
conn.close()

