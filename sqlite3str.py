import sqlite3
dbname="db.sqlite3"
dbname=input("Database Name? ").strip()

def get_table_schema(table_name):
    conn = sqlite3.connect(dbname)
    cursor = conn.cursor()
    
    # Using PRAGMA table_info
    cursor.execute(f'PRAGMA table_info({table_name});')
    columns = cursor.fetchall()
    
    # Using sqlite_master
    cursor.execute(f"SELECT sql FROM sqlite_master WHERE type='table' AND name='{table_name}';")
    table_sql = cursor.fetchone()
    
    conn.close()
    
    return columns, table_sql

# Example usage
columns, table_sql = get_table_schema('users')
print("Columns:", columns)
print("Table SQL:", table_sql)
