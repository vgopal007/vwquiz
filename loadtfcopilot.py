# this will read True or False questions sourced from MS CoPilot and insert into vwquiz.db
# Assumes this prefix on the first and every other odd number line
# question_type can be RB (Radio Button),CB(Check Box), IN(User Input)
import sqlite3
import json
import uuid
import random
#import vwquizfunclib
from  vwquizfunclib import select_category
import re

from datetime import datetime
from datetime import date

prefix1 = "True or False: "
# Assumes this prefix on the second and every other even number line
prefix21 = "True."
prefix22 = "False."

# Open the text file
filename = input ("Enter the filename of the True/False Question Set from MS COPilot :")

try:
 with open(filename, 'r' ,encoding='utf-8') as file:
  lines = file.readlines()
except UnicodeDecodeError as e:
  print(f"Error decoding file: {e}")



# Connect to the SQLite database (or create it if it doesn't exist)
conn = sqlite3.connect('vwquiz.db')
cursor = conn.cursor()
# Enable foreign key constraints, not ON by default!
cursor.execute("PRAGMA foreign_keys = ON;")

# Retrieve the list of categories from the quizapp_types table 
cursor.execute('SELECT gfg_name FROM quizapp_types')
categories = [row[0] for row in cursor.fetchall()]

cat = select_category(categories) # ask user to select a category
cursor.execute("SELECT uid, gfg_name FROM quizapp_types where gfg_name=?", (cat,))

rows = cursor.fetchall()
for row in rows:
    print(f"ID: {row[0]}, Category: {row[1]}")
    gfg_id= row[0]

gfg_id = str(gfg_id).replace('-', '')


created_at = date.today()
updated_at = date.today()

# Process the lines and insert into the database
for i in range(0, len(lines), 2):
    line1 = lines[i].strip()
    line2 = lines[i+1].strip()
    if line1.startswith(prefix1):
       question = line1[len(prefix1):].strip()
    else:
       print(line1, " does not match pattern ", prefix1)
       continue

    if line2.startswith(prefix21):
       answer = prefix21.split(".")[0]
       answer_explanation = line2[len(prefix21):].strip()
    elif line2.startswith(prefix22):
       answer = prefix22.split(".")[0]
       answer_explanation = line2[len(prefix22):].strip()
    else:
       print(line2, " does not match pattern ", prefix2)
       continue

    question_id = uuid.uuid4()
    question_id = str(question_id).replace('-', '')
    cursor.execute('INSERT INTO quizapp_question (uid, created_at, updated_at, question_type, question, topic, marks,answer_explanation, gfg_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)', (question_id, created_at, updated_at,"RB", question,cat, 1, answer_explanation, gfg_id))   
    print("Question : ", prefix1, question)
    print(question_id, created_at, updated_at,"RB", question,cat, 1, answer_explanation, gfg_id)
    

    print("Answer : ", answer, answer_explanation)
    answer_id = uuid.uuid4()
    answer_id = str(answer_id).replace('-', '')

    cursor.execute('INSERT INTO quizapp_answer (uid, created_at, updated_at,answer, is_correct,question_id) VALUES (?, ?, ?, ?, ?, ?)', (answer_id, created_at, updated_at,"True",answer=="True",question_id))

    print (answer_id, created_at, updated_at,"True",answer=="True",question_id)
    answer_id = uuid.uuid4()
    answer_id = str(answer_id).replace('-', '')

    cursor.execute('INSERT INTO quizapp_answer (uid, created_at, updated_at,answer, is_correct,question_id) VALUES (?, ?, ?, ?, ?, ?)', (answer_id, created_at, updated_at,"False",answer=="False",question_id))
    print (answer_id, created_at, updated_at,"False",answer=="False",question_id)
    conn.commit()



