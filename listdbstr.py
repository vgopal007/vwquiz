import sqlite3

def list_tables_and_structure(db_path):
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    # List all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print("Tables:")
    for table in tables:
        print(table[0])

        # Get table structure
        cursor.execute(f"PRAGMA table_info({table[0]});")
        columns = cursor.fetchall()
        print("Structure:")
        for column in columns:
            print(column)

        # List primary keys
        primary_keys = [col[1] for col in columns if col[5] > 0]
        print("  Primary Keys:")
        for pk in primary_keys:
            print(f"    {pk}")

        # List foreign keys
        cursor.execute(f"PRAGMA foreign_key_list({table});")
        foreign_keys = cursor.fetchall()
        print("  Foreign Keys:")
        for fk in foreign_keys:
            print(f"    {fk[3]} references {fk[2]}({fk[4]})")

        # List indexes
        cursor.execute(f"PRAGMA index_list({table});")
        indexes = cursor.fetchall()
        print("  Indexes:")
        for index in indexes:
            index_name = index[1]
            cursor.execute(f"PRAGMA index_info({index_name});")
            index_info = cursor.fetchall()
            columns_in_index = [info[2] for info in index_info]
            print(f"    {index_name} on columns {columns_in_index}")


    conn.close()

# Example usage
dbname="db.sqlite3"
dbname=input("Database Name? ").strip()
list_tables_and_structure('dbname')
