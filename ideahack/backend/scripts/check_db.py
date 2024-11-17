import sqlite3
from ideahack.backend.backend.settings import BASE_DIR

# Connect to the SQLite database (replace the path with your actual db path)
conn = sqlite3.connect(BASE_DIR / "db.sqlite3")
cursor = conn.cursor()

# Query to get the list of tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")

# Fetch all results
tables = cursor.fetchall()

# Print the table names
for table in tables:
    print(table[0])

# Close the connection
conn.close()
