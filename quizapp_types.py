import sqlite3
import uuid

import random
from datetime import datetime
from datetime import date

# to generate random Unique IDs
import re

created_at = date.today()
updated_at = date.today()

# Connect to the database
conn = sqlite3.connect('vwquiz.db')
cursor = conn.cursor()

# Create the quizapp_types table if it doesn't exist
cursor.execute('''
    CREATE TABLE IF NOT EXISTS quizapp_types (
        id INTEGER PRIMARY KEY,
        gfg_name TEXT
    )
''')

# Insert some data into the quizapp_types table
categories = ['Artificial Intelligence', 'Psychology', 'Python', 'Language R', 'Statistics']
for category in categories:
    type_uid = uuid.uuid4()
    type_uid = str(type_uid).replace('-', '')
    cursor.execute('INSERT INTO quizapp_types (uid, created_at, updated_at, gfg_name) VALUES (?, ?, ?, ?)', (type_uid, created_at, updated_at, category,))

conn.commit()
# Retrieve the list of categories from the quizapp_types table
cursor.execute('SELECT gfg_name FROM quizapp_types')
categories = [row[0] for row in cursor.fetchall()]


def select_category(categories):

# Display the list of categories and ask the user to select one
    print("Select a category:")
    for i, category in enumerate(categories):
        print(f"{i+1}. {category}")

# Get the user's selection
    while True:
        try:
            user_input = int(input("Enter the serial number of your selection: "))
            if 1 <= user_input <= len(categories):
                break
            else:
                print("Invalid selection. Please enter a number between 1 and", len(categories))
        except ValueError:
            print("Invalid input. Please enter a number.")

# Execute the query
    cursor.execute("SELECT * FROM quizapp_types WHERE gfg_name = ?", (categories[user_input-1],))
    rows = cursor.fetchall()

# Process the results (e.g., print or use them)
    for row in rows:
        print(row)

# Display the user's selection
    print(f"You selected: {categories[user_input-1]}")

select_category(categories)
# Close the connection to the database
conn.close()

