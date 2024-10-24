import sqlite3
dbname="db.sqlite3"
dbname=input("Database Name? ").strip()

# Connect to the database
conn = sqlite3.connect(dbname)
cursor = conn.cursor()

# Get the list of tables
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()
print("Tables:", tables)

# Iterate through tables and print their contents
for table_name in tables:
    table_name = table_name[0]
    print(f"\nContents of table {table_name}:")
    cursor.execute(f"SELECT * FROM {table_name}")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

    cursor.execute(f"PRAGMA table_info({table_name})")
    columns = cursor.fetchall()

# Print column information
    for column in columns:
        print(column)


conn.close()
